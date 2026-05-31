import { GoogleGenAI } from '@google/genai';
import RevisionSummary from '../models/RevisionSummary.js';
import LearningProject from '../models/LearningProject.js';

const apiKey = process.env.GEMINI_API_KEY_MANIM_CODE?.trim();
const genAI = new GoogleGenAI({ apiKey });
const modelName = process.env.GEMINI_MODEL || 'gemini-3-flash-preview';

/**
 * Generates a quick revision summary from source text and saves it to DB.
 * This is non-blocking and meant to run async after the pipeline finishes.
 */
export async function generateRevisionSummary(jobId, sourceText) {
    if (!sourceText || sourceText.length < 50) return;

    try {
        const prompt = `
Task: Generate a smart revision summary for an educational topic based on the provided text.
The output MUST be a strict JSON object with no markdown fences, formatted exactly as follows:
{
  "keyConcepts": ["Concept 1", "Concept 2"],
  "formulas": ["Formula 1", "Formula 2"],
  "definitions": [
    {"term": "Term 1", "definition": "Definition 1"}
  ],
  "examPoints": ["Important point 1 for exams"],
  "quickRecap": "A 2-3 sentence summary of the entire topic."
}

Text:
${sourceText.slice(0, 10000)}
`;
        
        console.log(`[revisionService] Generating summary for job ${jobId}...`);
        const response = await genAI.models.generateContent({
            model: modelName,
            contents: prompt,
            config: { responseMimeType: 'application/json' }
        });

        if (!response?.text) {
            throw new Error("Empty response from Gemini");
        }

        const raw = response.text.replace(/```json|```/g, '').trim();
        const parsed = JSON.parse(raw);

        // Save to DB
        await RevisionSummary.create({
            jobId,
            keyConcepts: parsed.keyConcepts || [],
            formulas: parsed.formulas || [],
            definitions: parsed.definitions || [],
            examPoints: parsed.examPoints || [],
            quickRecap: parsed.quickRecap || ''
        });

        // Update LearningProject
        await LearningProject.findOneAndUpdate(
            { jobId },
            { revisionReady: true },
            { new: true }
        );

        console.log(`[revisionService] Summary successfully generated for ${jobId}`);

    } catch (err) {
        console.error(`[revisionService] Error generating summary for ${jobId}:`, err.message);
    }
}
