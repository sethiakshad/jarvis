import mongoose from 'mongoose';

const revisionSummarySchema = new mongoose.Schema(
    {
        jobId: {
            type: String,
            required: true,
            unique: true,
            index: true,
        },
        keyConcepts: {
            type: [String],
            default: [],
        },
        formulas: {
            type: [String],
            default: [],
        },
        definitions: {
            type: [
                {
                    term: { type: String, required: true },
                    definition: { type: String, required: true },
                },
            ],
            default: [],
        },
        examPoints: {
            type: [String],
            default: [],
        },
        quickRecap: {
            type: String,
            default: '',
        },
        generatedAt: {
            type: Date,
            default: Date.now,
        },
    },
    { timestamps: false }
);

const RevisionSummary = mongoose.model('RevisionSummary', revisionSummarySchema);
export default RevisionSummary;
