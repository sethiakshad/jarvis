import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the API using API key from .env (trimmed for safety)
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY_MANIM_CODE?.trim());
const modelInstance = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

/**
 * Checks if the content is valid educational/STEM material.
 * @param {string} text - The extracted PDF text
 * @returns {Promise<boolean>} Object with success property
 */
export async function checkRelevance(text) {
    const prompt = `You are a strict classifier.

Task:
Determine whether the following content is EDUCATIONAL/STEM.

Rules:
- VALID → if content contains concepts, explanations, formulas, or academic material
- INVALID → if content is random text, memes, stories, ads, or non-educational

Output format (STRICT):
VALID
OR
INVALID

Content:
${text}`;

    const result = await modelInstance.generateContent(prompt);
    const response = await result.response;
    const responseText = response.text();
    
    return responseText.trim().toUpperCase() === 'VALID';
}

/**
 * Generates max 4 scenes for Manim animation.
 * @param {string} text - Educational text
 * @returns {Promise<Array>} Array of scene objects
 */
export async function generateScenes(text) {
    const prompt = `You are an expert educational content structuring AI.

Task:
Convert the given text into SMALL, VISUALIZABLE scenes for Manim animation.

Rules:
- Each scene must represent ONE clear concept
- Keep scenes SHORT (max 3-4 lines explanation)
- Must be visually representable
- No repetition
- Maintain logical flow
- Max 4 scenes ONLY

STRICT OUTPUT FORMAT (JSON ONLY, NO EXTRA TEXT):

[
  {
    "scene_id": 1,
    "title": "Short title",
    "concept": "Main concept",
    "explanation": "Short explanation",
    "visual_plan": "What animation should show"
  }
]

Text:
${text}`;

    const result = await modelInstance.generateContent(prompt);
    const response = await result.response;
    const rawText = response.text().trim();
    
    // Strict Markdown stripping
    const cleanText = rawText.replace(/```json|```/g, "");
    
    return JSON.parse(cleanText);
}

/**
 * Generates Manim executable code for one scene.
 * @param {Object} scene - The scene object
 * @returns {Promise<string>} The generated Python code
 */
export async function generateManimCode(scene) {
    const sceneId = scene.scene_id;
    const prompt = `You are a ManimCE expert.

Task:
Generate valid ManimCE Python code for the given scene.

STRICT RULES:
- Use Manim Community Edition syntax ONLY
- One class named Scene${sceneId}
- Must inherit from Scene
- No external libraries
- Use only standard Manim objects (Text, MathTex, Circle, Arrow, etc.)
- Code MUST run without modification
- Keep animation simple and clean

OUTPUT:
Return ONLY Python code. No explanations.

Scene:
${JSON.stringify(scene)}`;

    const result = await modelInstance.generateContent(prompt);
    const response = await result.response;
    let code = response.text().trim();
    
    // In case code is wrapped in markdown
    code = code.replace(/```python|```/g, "").trim();
    return code;
}

/**
 * Fixes broken Manim code iteratively.
 * @param {string} error - The execution error
 * @param {string} code - The broken code
 * @returns {Promise<string>} The fixed Python code
 */
export async function fixManimCode(error, code) {
    const prompt = `You are a debugging expert for ManimCE.

Task:
Fix the given code so it runs without errors.

Rules:
- Preserve original logic
- Fix syntax/import/runtime errors
- Ensure compatibility with ManimCE
- Do NOT add explanations

OUTPUT:
Return ONLY corrected Python code

Error:
${error}

Code:
${code}`;

    const result = await modelInstance.generateContent(prompt);
    const response = await result.response;
    let fixedCode = response.text().trim();
    
    fixedCode = fixedCode.replace(/```python|```/g, "").trim();
    return fixedCode;
}
