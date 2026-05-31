import mongoose from 'mongoose';

const learningProjectSchema = new mongoose.Schema(
    {
        jobId: {
            type: String,
            required: true,
            unique: true,
            index: true,
        },
        studentId: {
            type: String,
            required: true,
            index: true,
        },
        title: {
            type: String,
            default: 'Untitled Project',
        },
        focusTopic: {
            type: String,
            default: '',
        },
        audioLanguage: {
            type: String,
            default: 'english',
        },
        videoUrl: {
            type: String,
            default: '',
        },
        scenesTotal: {
            type: Number,
            default: 0,
        },
        scenesRendered: {
            type: Number,
            default: 0,
        },

        // ── Learning Progress ──────────────────────────────────────────
        watchedDuration: {
            type: Number,
            default: 0, // seconds watched
        },
        videoDuration: {
            type: Number,
            default: 0, // total video duration in seconds
        },
        completionPercentage: {
            type: Number,
            default: 0, // 0–100
        },
        lastWatched: {
            type: Date,
            default: null,
        },
        unlockedQuizLevel: {
            type: Number,
            default: 1, // 1, 2, or 3
        },
        quizAttempts: {
            type: Number,
            default: 0,
        },
        masteryScore: {
            type: Number,
            default: 0, // 0–100, computed from quiz attempts
        },
        weakConcepts: {
            type: [String],
            default: [],
        },

        // ── Library Features ───────────────────────────────────────────
        bookmarked: {
            type: Boolean,
            default: false,
        },
        revisionReady: {
            type: Boolean,
            default: false, // true once RevisionSummary is generated
        },

        // ── Pipeline Status ────────────────────────────────────────────
        pipelineStatus: {
            type: String,
            default: 'processing', // 'processing' | 'done' | 'error'
        },
    },
    {
        timestamps: true, // adds createdAt + updatedAt automatically
    }
);

const LearningProject = mongoose.model('LearningProject', learningProjectSchema);
export default LearningProject;
