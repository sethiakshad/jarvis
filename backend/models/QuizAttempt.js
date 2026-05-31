import mongoose from 'mongoose';

const quizAttemptSchema = new mongoose.Schema(
    {
        studentId: {
            type: String,
            required: true,
            index: true,
        },
        jobId: {
            type: String,
            required: true,
            index: true,
        },
        mode: {
            type: String,
            enum: ['standard', 'quick_mcq', 'challenge', 'viva', 'short_answers'],
            default: 'standard',
        },
        score: {
            type: Number,
            default: 0,
        },
        totalQuestions: {
            type: Number,
            default: 0,
        },
        correctAnswers: {
            type: Number,
            default: 0,
        },
        weakTopics: {
            type: [String],
            default: [],
        },
        attemptedAt: {
            type: Date,
            default: Date.now,
        },
    },
    { timestamps: false }
);

const QuizAttempt = mongoose.model('QuizAttempt', quizAttemptSchema);
export default QuizAttempt;
