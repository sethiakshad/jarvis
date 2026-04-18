import ffmpeg from 'fluent-ffmpeg';
import ffmpegInstaller from '@ffmpeg-installer/ffmpeg';
import fs from 'fs';
import path from 'path';

// Configure fluent-ffmpeg to use the static binary
ffmpeg.setFfmpegPath(ffmpegInstaller.path);

/**
 * Merges a list of video files sequentially.
 * @param {string[]} videoFiles - Array of paths to video files to merge
 * @param {string} outputPath - Path pointing to the final final.mp4
 * @returns {Promise<void>}
 */
export async function mergeVideos(videoFiles, outputPath) {
    return new Promise((resolve, reject) => {
        if (!videoFiles || videoFiles.length === 0) {
            return reject(new Error('No videos to merge.'));
        }

        // Sort files numerically by extracting the number from scene{number}.mp4
        const sortedFiles = [...videoFiles].sort((a, b) => {
            const numA = parseInt(path.basename(a).replace(/[^0-9]/g, '')) || 0;
            const numB = parseInt(path.basename(b).replace(/[^0-9]/g, '')) || 0;
            return numA - numB;
        });

        // Create a temporary list.txt for ffmpeg concat demuxer
        const workDir = path.dirname(outputPath);
        const listPath = path.join(workDir, 'list.txt');
        
        const listContent = sortedFiles.map(file => {
            // ffmpeg concat requires format: file 'path/to/file'
            // Need absolute or relative correctly formatted. 
            // Better to make it relative to the list.txt location or absolute correctly escaped.
            return `file '${file.replace(/\\/g, '/')}'`; 
        }).join('\n');
        
        fs.writeFileSync(listPath, listContent);

        // Run FFmpeg
        ffmpeg()
            .input(listPath)
            .inputOptions(['-f', 'concat', '-safe', '0'])
            .outputOptions(['-c', 'copy'])
            .output(outputPath)
            .on('end', () => {
                // Return success
                resolve();
            })
            .on('error', (err) => {
                reject(new Error(`FFmpeg merge error: ${err.message}`));
            })
            .run();
    });
}
