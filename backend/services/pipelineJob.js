import fs from 'fs';
import path from 'path';
import { extractText } from '../utils/pdfExtractor.js';
import { checkRelevance, generateScenes, generateManimCode } from './gemini.js';
import { runManimCodeWithRetry } from './manimRunner.js';
import { mergeVideos } from '../utils/videoMerger.js';

// Global Job Store
export const jobsStore = {};

// Concurrency limit variables
const MAX_CONCURRENT_JOBS = 2;
let activeJobs = 0;
const jobQueue = [];

/**
 * Initiates the background pipeline for a given job.
 * Enforces concurrency limits.
 */
export async function startPipelineJob(jobId, buffer) {
    if (activeJobs >= MAX_CONCURRENT_JOBS) {
        jobsStore[jobId].status = "queued";
        jobQueue.push({ jobId, buffer });
        return;
    }

    try {
        activeJobs++;
        jobsStore[jobId].status = "processing";
        await runPipeline(jobId, buffer);
    } catch (error) {
        console.error(`[Job ${jobId}] Pipeline failed:`, error);
        jobsStore[jobId] = {
            status: "error",
            error: error.message
        };
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

/**
 * The core orchestration logic
 */
async function runPipeline(jobId, buffer) {
    const jobDir = path.resolve(`./temp/videos/${jobId}`);
    if (!fs.existsSync(jobDir)) {
        fs.mkdirSync(jobDir, { recursive: true });
    }

    // 1. Extraction (limit strictly ~8000)
    console.log(`[Job ${jobId}] Extracting text...`);
    const text = await extractText(buffer, 8000);

    // 2. Relevance Check
    console.log(`[Job ${jobId}] Checking relevance...`);
    const isValid = await checkRelevance(text);
    if (!isValid) {
        throw new Error('INVALID: Uploaded file does not contain educational content. Please upload a valid academic PDF/PPT.');
    }

    // 3. Scene Generation (Max 4 scenes handled by Gemini strict constraint)
    console.log(`[Job ${jobId}] Generating scenes JSON...`);
    let scenes = [];
    try {
        scenes = await generateScenes(text);
    } catch (e) {
        throw new Error('Failed to parse Gemini scene representation as valid JSON. Raw API response may have strayed.');
    }

    if (!Array.isArray(scenes) || scenes.length === 0) {
        throw new Error('Scene logic generation produced empty or invalid array format.');
    }
    
    // Safety crop in case Gemini outputs 5+
    scenes = scenes.slice(0, 4);

    // 4. Manim Generation per Scene
    let generatedVideoPaths = [];
    
    for (const scene of scenes) {
        console.log(`[Job ${jobId}] Processing Scene ${scene.scene_id}: ${scene.title}`);
        
        // Generate Manim code
        const code = await generateManimCode(scene);
        
        // Run and potentially auto-fix
        await runManimCodeWithRetry(code, scene, jobId);
        
        // The runner logic enforces that output goes to `temp/videos/{jobId}/scene{scene_id}.mp4`
        const expectedVideoOutput = path.join(jobDir, `scene${scene.scene_id}.mp4`);
        if (fs.existsSync(expectedVideoOutput)) {
            generatedVideoPaths.push(expectedVideoOutput);
        } else {
            throw new Error(`Video file scene${scene.scene_id}.mp4 inexplicably missing after supposed success.`);
        }
    }

    // 5. Build final output 
    console.log(`[Job ${jobId}] Merging ${generatedVideoPaths.length} videos...`);
    const finalOutputPath = path.join(jobDir, `final.mp4`);
    await mergeVideos(generatedVideoPaths, finalOutputPath);

    // 6. Complete
    jobsStore[jobId] = {
        status: "done",
        videoUrl: `/videos/${jobId}/final.mp4`
    };
    console.log(`[Job ${jobId}] Pipeline complete. Accessible at /videos/${jobId}/final.mp4`);
}
