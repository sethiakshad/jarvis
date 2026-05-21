import express from 'express';
import { getQuestions, checkAnswer, generateQuestionsManual, refreshLevelQuestions } from '../controllers/questionController.js';

const router = express.Router();

router.get('/:jobId', getQuestions);
router.post('/check-answer', checkAnswer);
router.post('/generate-questions', generateQuestionsManual);
router.post('/refresh-level', refreshLevelQuestions);

router.post('/log-current', (req, res) => {
    const { question, answer } = req.body;
    console.log(`\n[CURRENT NODE DISPLAYED]`);
    console.log(`QUESTION: ${question}`);
    console.log(`ANSWER  : ${answer}\n`);
    res.json({ success: true });
});

export default router;
