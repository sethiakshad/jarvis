import subprocess
import sys
import json
import os
import shutil

def run_manim(file_path, scene_name, job_id):
    # Dynamically locate FFmpeg in the backend node_modules
    backend_node_modules = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "node_modules"))
    ffmpeg_dir = os.path.join(backend_node_modules, "@ffmpeg-installer", "win32-x64")
    
    if os.path.exists(ffmpeg_dir):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

    # Determine absolute path to the generated videos
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "temp", "videos", job_id, scene_name))
    
    # Use sys.executable -m manim for robustness
    command = [sys.executable, "-m", "manim", "-pql", file_path, scene_name, "--media_dir", media_dir]
    
    try:
        # Run subprocess
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        
        # After execution, Manim produces outputs in complex directory structures.
        # usually media_dir/videos/file/480p15/SceneName.mp4
        # We need to find that file and move it to temp/videos/{job_id}/{scene_name.lower()}.mp4
        
        # For simplicity, search the media_dir for .mp4 files
        video_found = False
        if os.path.exists(media_dir):
            for root, dirs, files in os.walk(media_dir):
                for f in files:
                    if f == f"{scene_name}.mp4":
                        # Move it to the flat structure expected
                        target_path = os.path.join("..", "backend", "temp", "videos", job_id, f"{scene_name.lower()}.mp4")
                        source_path = os.path.join(root, f)
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        shutil.move(source_path, target_path)
                        video_found = True
                        break
        
        # We must output strictly JSON to stdout
        if video_found:
            print(json.dumps({"success": True}))
        else:
            print(json.dumps({"success": False, "error": f"Video file {scene_name}.mp4 not found after rendering."}))
            
    except subprocess.CalledProcessError as e:
        # Strict return on error
        print(json.dumps({"success": False, "error": e.stderr if e.stderr else e.stdout}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"success": False, "error": "Missing arguments. Usage: python runner.py <file.py> <SceneName> <jobId>"}))
        sys.exit(1)
        
    file_py = sys.argv[1]
    scene_name = sys.argv[2]
    job_id = sys.argv[3]
    
    run_manim(file_py, scene_name, job_id)
