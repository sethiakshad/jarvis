import LearningProject from '../models/LearningProject.js';
import RevisionSummary from '../models/RevisionSummary.js';
import QuizAttempt from '../models/QuizAttempt.js';
import Question from '../models/Question.js';
import { generateQuestionsFromText } from '../services/questionService.js';
import { generateRevisionSummary } from '../services/revisionService.js';

// Get all projects for student
export async function getProjects(req, res) {
    try {
        const projects = await LearningProject.find({ studentId: req.user.student_id }).sort({ createdAt: -1 });
        res.json({ success: true, projects });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Get single project
export async function getProject(req, res) {
    try {
        const project = await LearningProject.findOne({ jobId: req.params.jobId, studentId: req.user.student_id });
        if (!project) return res.status(404).json({ success: false, error: 'Project not found' });
        res.json({ success: true, project });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Update progress
export async function updateProgress(req, res) {
    try {
        const { watchedDuration, videoDuration, completionPercentage, unlockedQuizLevel } = req.body;
        
        const update = { lastWatched: new Date() };
        if (watchedDuration !== undefined) update.watchedDuration = watchedDuration;
        if (videoDuration !== undefined) update.videoDuration = videoDuration;
        if (completionPercentage !== undefined) update.completionPercentage = completionPercentage;
        if (unlockedQuizLevel !== undefined) update.unlockedQuizLevel = unlockedQuizLevel;

        const project = await LearningProject.findOneAndUpdate(
            { jobId: req.params.jobId, studentId: req.user.student_id },
            update,
            { new: true }
        );
        res.json({ success: true, project });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Toggle bookmark
export async function toggleBookmark(req, res) {
    try {
        const project = await LearningProject.findOne({ jobId: req.params.jobId, studentId: req.user.student_id });
        if (!project) return res.status(404).json({ success: false, error: 'Project not found' });
        
        project.bookmarked = !project.bookmarked;
        await project.save();
        res.json({ success: true, bookmarked: project.bookmarked });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Delete project
export async function deleteProject(req, res) {
    try {
        const deleted = await LearningProject.findOneAndDelete({ jobId: req.params.jobId, studentId: req.user.student_id });
        if (!deleted) return res.status(404).json({ success: false, error: 'Project not found' });
        
        // Also delete associated data (soft concepts)
        await RevisionSummary.findOneAndDelete({ jobId: req.params.jobId });
        await QuizAttempt.deleteMany({ jobId: req.params.jobId });
        
        res.json({ success: true, message: 'Project deleted' });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Get revision summary
export async function getRevisionSummary(req, res) {
    try {
        const summary = await RevisionSummary.findOne({ jobId: req.params.jobId });
        if (!summary) return res.status(404).json({ success: false, error: 'Summary not found' });
        res.json({ success: true, summary });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Generate revision summary
export async function triggerRevisionGeneration(req, res) {
    try {
        const { jobId } = req.params;
        const project = await LearningProject.findOne({ jobId, studentId: req.user.student_id });
        if (!project) return res.status(404).json({ success: false, error: 'Project not found' });
        
        if (project.revisionReady) {
            return res.json({ success: true, message: 'Revision already exists' });
        }
        
        const qDoc = await Question.findOne({ jobId }).lean();
        if (!qDoc || !qDoc.sourceText) {
            return res.status(400).json({ success: false, error: 'Source text missing' });
        }

        // Trigger async
        generateRevisionSummary(jobId, qDoc.sourceText).catch(console.error);
        res.status(202).json({ success: true, message: 'Generation started' });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Generate fresh practice questions
export async function generatePracticeQuestions(req, res) {
    try {
        const { jobId } = req.params;
        const { mode } = req.body;
        
        const qDoc = await Question.findOne({ jobId }).lean();
        if (!qDoc || !qDoc.sourceText) {
            return res.status(400).json({ success: false, error: 'Source text missing' });
        }

        let numMcqs = 0;
        let numShorts = 0;
        
        switch(mode) {
            case 'quick_mcq': numMcqs = 5; break;
            case 'viva': numShorts = 3; break;
            case 'challenge': numMcqs = 5; numShorts = 2; break;
            case 'short_answers': numShorts = 5; break;
            default: numMcqs = 3; numShorts = 2; break; // standard
        }

        const questions = await generateQuestionsFromText(qDoc.sourceText, numMcqs, numShorts);
        res.json({ success: true, questions });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Save quiz attempt
export async function saveQuizAttempt(req, res) {
    try {
        const { jobId } = req.params;
        const { mode, score, totalQuestions, correctAnswers, weakTopics } = req.body;
        
        await QuizAttempt.create({
            studentId: req.user.student_id,
            jobId,
            mode, score, totalQuestions, correctAnswers, weakTopics
        });

        // Update project mastery and weak concepts
        const project = await LearningProject.findOne({ jobId, studentId: req.user.student_id });
        if (project) {
            project.quizAttempts += 1;
            
            // Simple moving average for mastery
            if (project.masteryScore === 0) {
                project.masteryScore = score;
            } else {
                project.masteryScore = Math.round((project.masteryScore + score) / 2);
            }

            // Append unique weak topics
            if (weakTopics && weakTopics.length > 0) {
                const combined = [...new Set([...project.weakConcepts, ...weakTopics])];
                // keep last 5 to avoid bloating
                project.weakConcepts = combined.slice(-5);
            }
            
            await project.save();
        }

        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}
