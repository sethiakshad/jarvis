import { spawn } from 'child_process';
import path from 'path';
import { fixManimCode } from './gemini.js';
import fs from 'fs';

/**
 * Runs the Manim python runner with a timeout limit.
 * @param {string} pyFilePath - Temp python file path
 * @param {string} sceneName - e.g. Scene1
 * @param {string} jobId - The job ID
 * @returns {Promise<Object>} The parsed JSON output from runner.py
 */
function execPythonRunner(pyFilePath, sceneName, jobId) {
    return new Promise((resolve) => {
        // e:\nexus\python-service\runner.py
        const runnerPath = path.resolve('../python-service/runner.py');
        const processArgs = [runnerPath, pyFilePath, sceneName, jobId];

        const child = spawn('python', processArgs, { cwd: path.resolve('../python-service') });
        
        let stdoutData = '';
        let stderrData = '';

        child.stdout.on('data', (data) => {
            stdoutData += data.toString();
        });

        child.stderr.on('data', (data) => {
            stderrData += data.toString();
        });

        // 300s (5 min) timeout requirement. Manim rendering can be CPU intensive.
        const timeout = setTimeout(() => {
            child.kill();
            resolve({ success: false, error: 'Execution timeout exceeded (300s). Rendering this scene is taking longer than expected.' });
        }, 300000);

        child.on('close', () => {
            clearTimeout(timeout);
            try {
                // Runner should print exactly one json line at the very end
                const lines = stdoutData.trim().split('\n');
                const lastLine = lines[lines.length - 1]; // Assume last line is the JSON output
                const result = JSON.parse(lastLine);
                resolve(result);
            } catch (e) {
                // If parsing fails, fall back to capturing whatever output happened
                resolve({ success: false, error: `JSON Parse error from Python runner. Stdout: ${stdoutData}. Stderr: ${stderrData}` });
            }
        });
    });
}

/**
 * Executes a scene using runner.py, attempting Gemini auto-fix up to 3 times on failure.
 * @param {string} code - The generated python manim code
 * @param {Object} scene - Scene object containing scene_id
 * @param {string} jobId - The unique job id
 * @returns {Promise<void>} Resolves if successful, rejects if execution failed entirely
 */
export async function runManimCodeWithRetry(code, scene, jobId) {
    const sceneName = `Scene${scene.scene_id}`;
    let currentCode = code;
    
    // Save currentCode to a temporary python file named scene{scene_id}.py
    const pyDir = path.resolve(`./temp/videos/${jobId}`);
    if (!fs.existsSync(pyDir)) {
        fs.mkdirSync(pyDir, { recursive: true });
    }
    
    const pyFilePath = path.join(pyDir, `scene${scene.scene_id}_code.py`);

    for (let i = 0; i < 3; i++) {
        fs.writeFileSync(pyFilePath, currentCode);

        console.log(`[Job ${jobId}] Running manim for ${sceneName} (Attempt ${i+1}/3)`);
        const result = await execPythonRunner(pyFilePath, sceneName, jobId);
        
        if (result.success) {
            console.log(`[Job ${jobId}] ${sceneName} rendered successfully.`);
            return;
        }

        console.error(`[Job ${jobId}] ${sceneName} failed:`, result.error);
        if (i < 2) {
            console.log(`[Job ${jobId}] Auto-fixing ${sceneName} error via Gemini...`);
            currentCode = await fixManimCode(result.error, currentCode);
        } else {
            throw new Error(`Failed to render ${sceneName} after 3 attempts. Last error: ${result.error}`);
        }
    }
}
