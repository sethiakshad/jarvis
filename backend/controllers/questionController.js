import Question from '../models/Question.js';
import { generateQuestionsFromText, evaluateShortAnswer } from '../services/questionService.js';
import { extractText } from '../utils/pdfExtractor.js'; // Assuming we might need it if manually triggered
import fs from 'fs';
import path from 'path';

/**
 * Fetches questions for a specific job.
 */
export async function getQuestions(req, res) {
    const { jobId } = req.params;
    try {
        const questionData = await Question.findOne({ jobId });
        if (!questionData) {
            return res.status(404).json({ error: 'Questions not found for this job.' });
        }
        res.json(questionData);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
}

/**
 * Refreshes questions for a specific level (generates new ones).
 */
export async function refreshLevelQuestions(req, res) {
    const { jobId, level } = req.body;
    try {
        const questionDoc = await Question.findOne({ jobId });
        if (!questionDoc || !questionDoc.sourceText) {
            return res.status(404).json({ error: 'Source text not found. Cannot refresh questions.' });
        }

        // Generate a small batch for the specific level
        // We assume Level 1: 2 questions, Level 2: 2 questions, Level 3: 1 question
        const mcqCount = (level === 1 || level === 2) ? 2 : 0;
        const shortCount = (level === 2) ? 0 : (level === 3 ? 1 : 0);
        
        // Actually, let's just generate a mix and assign to level
        const newQuestions = await generateQuestionsFromText(questionDoc.sourceText, 2, 1);
        newQuestions.forEach(q => q.level = parseInt(level));

        // Filter out old questions of this level and append new ones
        questionDoc.questions = questionDoc.questions.filter(q => q.level !== parseInt(level));
        questionDoc.questions.push(...newQuestions);

        await questionDoc.save();
        res.json({ success: true, questions: questionDoc.questions });
    } catch (err) {
        console.error("Refresh failed:", err);
        res.status(500).json({ error: err.message });
    }
}

/**
 * Manually trigger question generation (if needed outside pipeline).
 */
export async function generateQuestionsManual(req, res) {
    const { jobId, count } = req.body;
    // In a real app, you'd fetch the text from DB or a stored file.
    // For now, we assume the pipeline already handled it, or we'd need the text.
    // Let's assume we can't easily do it without the text source.
    res.status(501).json({ error: 'Manual generation requires stored document text. Use the pipeline.' });
}

/**
 * Evaluates an answer.
 */
export async function checkAnswer(req, res) {
    const { type, userAnswer, correctAnswer } = req.body;

    // Log for user to check in terminal
    console.log(`\n[TAKTICAL CHECK] Type: ${type}`);
    console.log(`[USER ANSWER]: ${userAnswer}`);
    console.log(`[EXPECTED]: ${correctAnswer}\n`);

    if (type === 'mcq') {
        const isCorrect = userAnswer === correctAnswer;
        return res.json({
            correct: isCorrect,
            score: isCorrect ? 100 : 0,
            feedback: isCorrect ? 'Perfect!' : `Incorrect. The correct answer was: ${correctAnswer}`
        });
    }

    if (type === 'short') {
        try {
            const evaluation = await evaluateShortAnswer(userAnswer, correctAnswer);
            res.json(evaluation);
        } catch (err) {
            res.status(500).json({ error: 'Evaluation failed.' });
        }
        return;
    }

    res.status(400).json({ error: 'Invalid question type.' });
}
