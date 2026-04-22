import fs from 'fs';
import path from 'path';
import { extractText } from '../utils/pdfExtractor.js';
import { checkRelevance, generateScenes, generateManimCode } from './gemini.js';
import { runManimCodeWithRetry } from './manimRunner.js';
import { mergeVideos } from '../utils/videoMerger.js';
import { generateFallbackVideo } from '../utils/fallbackVideoGenerator.js';

// Global Job Store
export const jobsStore = {};

// Concurrency limit
const MAX_CONCURRENT_JOBS = 2;
let activeJobs = 0;
const jobQueue = [];

function updateJob(jobId, patch) {
    jobsStore[jobId] = { ...jobsStore[jobId], ...patch };
}

export async function startPipelineJob(jobId, buffer) {
    if (activeJobs >= MAX_CONCURRENT_JOBS) {
        updateJob(jobId, { status: 'queued', statusMessage: 'Waiting in queue...' });
        jobQueue.push({ jobId, buffer });
        return;
    }

    try {
        activeJobs++;
        updateJob(jobId, { status: 'processing', statusMessage: 'Starting pipeline...' });
        await runPipeline(jobId, buffer);
    } catch (error) {
        console.error(`[Job ${jobId}] Pipeline failed:`, error);
        updateJob(jobId, {
            status: 'error',
            error: error.message,
            statusMessage: 'Pipeline failed.',
            timestamp: new Date().toISOString()
        });
    } finally {
        activeJobs--;
        processNextInQueue();
    }
}

function processNextInQueue() {
    if (jobQueue.length > 0 && activeJobs < MAX_CONCURRENT_JOBS) {
        const nextJob = jobQueue.shift();
        startPipelineJob(nextJob.jobId, nextJob.buffer);
    }
}

async function runPipeline(jobId, buffer) {
    const jobDir = path.resolve(`./temp/videos/${jobId}`);
    if (!fs.existsSync(jobDir)) {
        fs.mkdirSync(jobDir, { recursive: true });
    }

    // ── Step 1: Extract text ──────────────────────────────────────────────────
    updateJob(jobId, { statusMessage: 'Extracting document text...' });
    console.log(`[Job ${jobId}] Extracting text...`);
    const text = await extractText(buffer, 8000);

    // ── Step 2: Relevance check ───────────────────────────────────────────────
    updateJob(jobId, { statusMessage: 'Checking content relevance...' });
    console.log(`[Job ${jobId}] Checking relevance...`);
    const isValid = await checkRelevance(text);
    if (!isValid) {
        throw new Error('INVALID: Uploaded file does not appear to contain educational content.');
    }

    // ── Step 3: Generate scene plan ───────────────────────────────────────────
    updateJob(jobId, { statusMessage: 'Generating scene plan with AI...' });
    console.log(`[Job ${jobId}] Generating scenes JSON...`);
    let scenes = [];
    try {
        scenes = await generateScenes(text);
    } catch (e) {
        throw new Error(`Scene generation failed: ${e.message}`);
    }

    if (!Array.isArray(scenes) || scenes.length === 0) {
        throw new Error('AI returned empty or invalid scene list.');
    }
    scenes = scenes.slice(0, 4);

    // ── Step 4: Render each scene (skip failures — don't abort) ──────────────
    const generatedVideoPaths = [];
    const failedScenes = [];

    for (let idx = 0; idx < scenes.length; idx++) {
        const scene = scenes[idx];
        updateJob(jobId, {
            statusMessage: `Rendering scene ${idx + 1}/${scenes.length}: "${scene.title}"...`
        });
        console.log(`[Job ${jobId}] Generating Manim code for Scene${scene.scene_id}...`);

        let code;
        try {
            code = await generateManimCode(scene);
        } catch (e) {
            console.error(`[Job ${jobId}] Code generation failed for scene ${scene.scene_id}:`, e.message);
            failedScenes.push(scene.scene_id);
            continue;
        }

        const result = await runManimCodeWithRetry(code, scene, jobId);

        if (result.success) {
            const videoFile = path.join(jobDir, `scene${scene.scene_id}.mp4`);
            if (fs.existsSync(videoFile)) {
                generatedVideoPaths.push(videoFile);
            } else {
                console.warn(`[Job ${jobId}] Scene${scene.scene_id} reported success but no mp4 found.`);
                failedScenes.push(scene.scene_id);
            }
        } else {
            failedScenes.push(scene.scene_id);
        }

        // Brief pause between scenes to release OS file handles
        await new Promise(resolve => setTimeout(resolve, 800));
    }

    const finalOutputPath = path.join(jobDir, 'final.mp4');

    // ── Step 5: Merge or fallback ─────────────────────────────────────────────
    if (generatedVideoPaths.length > 0) {
        updateJob(jobId, {
            statusMessage: `Merging ${generatedVideoPaths.length} scene(s)...`
        });
        console.log(`[Job ${jobId}] Merging ${generatedVideoPaths.length} video(s)...`);

        if (generatedVideoPaths.length === 1) {
            // Only 1 scene — just copy, no need to concat
            fs.copyFileSync(generatedVideoPaths[0], finalOutputPath);
        } else {
            await mergeVideos(generatedVideoPaths, finalOutputPath);
        }
    } else {
        // Zero scenes rendered — use fallback generator
        console.warn(`[Job ${jobId}] All Manim scenes failed. Generating fallback video...`);
        updateJob(jobId, { statusMessage: 'All scenes failed — generating fallback video...' });
        await generateFallbackVideo(scenes, finalOutputPath);
    }

    if (!fs.existsSync(finalOutputPath)) {
        throw new Error('Final video was not created. Pipeline failed completely.');
    }

    // ── Step 6: Done ──────────────────────────────────────────────────────────
    const partial = failedScenes.length > 0 && generatedVideoPaths.length > 0;
    updateJob(jobId, {
        status: 'done',
        videoUrl: `/videos/${jobId}/final.mp4`,
        completedAt: new Date().toISOString(),
        statusMessage: partial
            ? `Done (${generatedVideoPaths.length}/${scenes.length} scenes rendered)`
            : generatedVideoPaths.length === 0
                ? 'Done (fallback video generated)'
                : 'Done — all scenes rendered!',
        scenesRendered: generatedVideoPaths.length,
        scenesTotal: scenes.length
    });

    console.log(`[Job ${jobId}] Complete → /videos/${jobId}/final.mp4`);
}
