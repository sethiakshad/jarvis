import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the API using API key from .env (trimmed for safety)
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY_MANIM_CODE?.trim());

// Model configs
const jsonModel = genAI.getGenerativeModel({ 
    model: 'gemini-2.5-flash',
    generationConfig: { responseMimeType: 'application/json' }
});

const codeModel = genAI.getGenerativeModel({ 
    model: 'gemini-2.5-flash' 
});

/**
 * Helper to call Gemini with retry logic for 429 rate limits.
 */
async function withRetry(fn, taskName = "Gemini Call", maxRetries = 5) {
    let lastError;
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            lastError = error;
            const isRateLimit = error.status === 429 || 
                               error.message?.includes('429') || 
                               error.message?.includes('ResourceExhausted') ||
                               error.message?.includes('Quota');

            if (isRateLimit) {
                // Determine delay: use provided retryDelay or fallback to exponential backoff
                let delayMs = 10000 * Math.pow(2, i); // Start with 10s, then 20s, 40s...
                
                try {
                    // Search for google.rpc.RetryInfo in the error details/links
                    // The error object from @google/generative-ai can be deep
                    const errorDetails = error.response?.error?.details || error.details || [];
                    const retryInfo = errorDetails.find(d => d['@type']?.includes('RetryInfo') || d.description?.includes('RetryInfo'));
                    
                    if (retryInfo?.retryDelay) {
                        // "48s" -> 48
                        const seconds = parseInt(retryInfo.retryDelay);
                        if (!isNaN(seconds)) {
                            delayMs = (seconds * 1000) + 2000; // Add 2s safety buffer
                        }
                    } else if (error.links) {
                        const linkRetry = error.links.find(l => l.description?.includes('RetryInfo'));
                        if (linkRetry?.retryDelay) {
                            const seconds = parseInt(linkRetry.retryDelay);
                            if (!isNaN(seconds)) {
                                delayMs = (seconds * 1000) + 2000;
                            }
                        }
                    }
                } catch (parseError) {
                    console.error("[Gemini] Error parsing retry info:", parseError.message);
                }

                // Add jitter (±10%)
                const jitter = delayMs * 0.1 * (Math.random() - 0.5);
                const finalDelay = Math.max(1000, delayMs + jitter);

                console.warn(`[${taskName}] Rate limited (429). Retrying in ${(finalDelay / 1000).toFixed(1)}s... (Attempt ${i + 1}/${maxRetries})`);
                await new Promise(resolve => setTimeout(resolve, finalDelay));
            } else {
                // If not a rate limit error, throw immediately
                throw error;
            }
        }
    }
    throw lastError;
}

/**
 * Checks if the content is valid educational/STEM material.
 */
export async function checkRelevance(text) {
    return await withRetry(async () => {
        const prompt = `Task: Determine if EDUCATIONAL/STEM. Output: {"valid": true} or {"valid": false}. Content: ${text}`;
        const result = await jsonModel.generateContent(prompt);
        const response = await result.response;
        const json = JSON.parse(response.text());
        return json.valid === true;
    }, "Relevance Check");
}

/**
 * Generates max 4 scenes for Manim animation.
 */
export async function generateScenes(text) {
    return await withRetry(async () => {
        const prompt = `Task: Convert to JSON array of max 4 scenes. 
        Rules: 
        - scene_id MUST be an integer (1, 2, 3, 4).
        - Keys: scene_id, title, concept, explanation, visual_plan. 
        Text: ${text}`;
        const result = await jsonModel.generateContent(prompt);
        const response = await result.response;
        return JSON.parse(response.text());
    }, "Scene Generation");
}

/**
 * Generates Manim executable code for one scene.
 */
export async function generateManimCode(scene) {
    return await withRetry(async () => {
        const prompt = `Task: Generate ManimCE codebase for Scene${scene.scene_id}. 
        STRICT RULES:
        - Use ONLY standard Manim Community Edition library.
        - FORBIDDEN: Do not use 'Grid', 'SVGMobject', or any external assets/files.
        - FORBIDDEN: Do not use 'self.mobjects' or '*self.mobjects' in animations.
        - Use basic mobjects: Text, MathTex, Circle, Square, Arrow, Line, NumberPlane.
        - Use 'VGroup()' for standard collections of mobjects (Text, MathTex, Circle, Square, Arrow, Line, NumberPlane) as they are VMobjects and required for animations like 'Create' and 'Write'.
        - LAYOUT: Never overlap text. If placing items inside a box, ensure the box label (e.g., 'AGENT') is placed ABOVE or BELOW the internal components, or fades out before they appear.
        - SPACING: Use 'arrange(DOWN, buff=0.4)' or similar to provide breathable spacing.
        - AESTHETICS: Use a distinct, vibrant color palette (e.g., BLUE, GREEN, TEAL, GOLD). Ensure font sizes are readable (default 36-48 for titles, 24-30 for labels).
        - COMPATIBILITY: Use 'fill_opacity=' instead of 'opacity=' for mobjects like Dot, Circle, and Square.
        - class Scene${scene.scene_id}(Scene): ...
        - Output ONLY Python code. No markdown.
        Scene Info: ${JSON.stringify(scene)}`;
        const result = await codeModel.generateContent(prompt);
        const response = await result.response;
        let code = response.text().trim();
        return code.replace(/```python|```/g, "").trim();
    }, `Code Gen Scene ${scene.scene_id}`);
}

/**
 * Fixes broken Manim code iteratively.
 */
export async function fixManimCode(error, code) {
    return await withRetry(async () => {
        const prompt = `Task: Fix this ManimCE error. 
        Current Error: ${error}
        STRICT RULES:
        - If 'TypeError: Create only works for VMobjects', replace 'Group' with 'VGroup' and ensure all members are standard vector shapes/text.
        - If 'TypeError: ... got an unexpected keyword argument \'opacity\'', replace 'opacity=' with 'fill_opacity=' or 'stroke_opacity=' (use fill_opacity for Dot, Circle, Square).
        - If 'TypeError: ... got an unexpected keyword argument \'font_size\'', ensure it is only used with Text/MathTex.
        - If NameError for 'Grid', use 'NumberPlane' instead.
        - If FileNotFoundError, remove the asset-loading line entirely.
        - Output ONLY corrected code. No explanations.
        Broken Code:
        ${code}`;
        const result = await codeModel.generateContent(prompt);
        const response = await result.response;
        let fixedCode = response.text().trim();
        return fixedCode.replace(/```python|```/g, "").trim();
    }, "Code Fix");
}
