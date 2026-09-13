from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
from typing import Optional
from video_processor import download_video, get_transcript, find_highlight, create_reel, analyze_with_ai

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store
jobs = {}

class VideoRequest(BaseModel):
    url: str
    tagline: Optional[str] = None

def update_job(job_id, progress, status, result=None, error=None):
    jobs[job_id] = {
        "progress": progress,
        "status": status,
        "result": result,
        "error": error
    }

def process_video_task(job_id: str, url: str, tagline: str):
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        update_job(job_id, 0, "Starting download...")
        
        # Callback for download progress
        def download_progress(progress, message):
            update_job(job_id, progress, message)

        # 1. Download
        print(f"Downloading {url}...")
        video_id, video_path = download_video(url, progress_callback=download_progress)
        
        # 2. Analyze
        update_job(job_id, 50, "Analyzing content...")
        print(f"Fetching transcript for {video_id}...")
        transcript = get_transcript(video_id)
        
        start_time = 0
        duration = 22 # Default
        final_tagline = tagline or "Watch This!"
        
        if openai_api_key and transcript:
            update_job(job_id, 55, "AI is finding the best moment...")
            print("Analyzing with AI...")
            ai_start, ai_duration, ai_tagline = analyze_with_ai(transcript, openai_api_key)
            if ai_start is not None:
                start_time = ai_start
                duration = ai_duration
                print(f"AI selected start time: {start_time}, duration: {duration}")
            if ai_tagline and not tagline:
                final_tagline = ai_tagline
                print(f"AI generated tagline: {final_tagline}")
        else:
            # Fallback to heuristic
            start_time = find_highlight(transcript)
            print(f"Heuristic start time: {start_time}")
        
        # 3. Create Reel
        update_job(job_id, 70, f"Creating {duration}s reel (scanning for faces)...")
        output_filename = f"downloads/reel_{video_id}_{uuid.uuid4().hex[:8]}.mp4"
        print(f"Creating reel: {output_filename}")
        success = create_reel(video_path, start_time, final_tagline, output_filename, duration)
        
        if not success:
            raise Exception("Failed to create reel")
            
        update_job(job_id, 100, "Completed", result={
            "filename": output_filename,
            "video_id": video_id,
            "start_time": start_time,
            "duration": duration,
            "tagline": final_tagline
        })
        
    except Exception as e:
        print(f"Error: {e}")
        update_job(job_id, 0, "Failed", error=str(e))

@app.post("/process")
async def process_video(request: VideoRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"progress": 0, "status": "Queued", "result": None, "error": None}
    background_tasks.add_task(process_video_task, job_id, request.url, request.tagline)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"downloads/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
