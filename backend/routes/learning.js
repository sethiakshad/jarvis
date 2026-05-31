import express from 'express';
import jwt from 'jsonwebtoken';
import { 
    getProjects, getProject, updateProgress, toggleBookmark, deleteProject,
    getRevisionSummary, triggerRevisionGeneration, generatePracticeQuestions, saveQuizAttempt
} from '../controllers/learningController.js';

const router = express.Router();

// Middleware to verify Student JWT
const verifyStudent = (req, res, next) => {
    const token = req.headers.authorization?.split(" ")[1];
    if (!token) return res.status(401).json({ success: false, message: "No token provided." });

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        // We only require that they have a student_id
        if (!decoded.student_id) {
            return res.status(403).json({ success: false, message: "Access denied. Valid student token required." });
        }
        req.user = decoded; // { id, student_id, email, name, ... }
        next();
    } catch (error) {
        return res.status(401).json({ success: false, message: "Invalid or expired token." });
    }
};

// All routes require auth
router.use(verifyStudent);

router.get('/projects', getProjects);
router.get('/projects/:jobId', getProject);
router.patch('/projects/:jobId/progress', updateProgress);
router.patch('/projects/:jobId/bookmark', toggleBookmark);
router.delete('/projects/:jobId', deleteProject);

router.get('/projects/:jobId/revision', getRevisionSummary);
router.post('/projects/:jobId/revision/generate', triggerRevisionGeneration);

router.post('/projects/:jobId/practice', generatePracticeQuestions);
router.post('/projects/:jobId/attempt', saveQuizAttempt);

export default router;
