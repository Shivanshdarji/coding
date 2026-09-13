import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip
from moviepy.config import change_settings
import math
import PIL.Image
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Monkey patch for Pillow 10+ if needed
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url, progress_callback=None):
    def ydl_hook(d):
        if d['status'] == 'downloading':
            if progress_callback:
                try:
                    p = d.get('_percent_str', '0%').replace('%','')
                    progress = float(p) / 2
                    progress_callback(progress, f"Downloading: {p}%")
                except:
                    pass
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback(50, "Download complete. Processing...")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'progress_hooks': [ydl_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        filename = ydl.prepare_filename(info)
        return video_id, filename

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        try:
            print("Attempting list_transcripts...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en']).fetch()
            return transcript
        except Exception as e2:
            print(f"Fallback failed: {e2}")
        return None

def find_highlight(transcript, duration=22):
    if not transcript:
        return 0
    max_density = 0
    best_start = 0
    for i in range(len(transcript)):
        current_start = transcript[i]['start']
        current_end = current_start + duration
        char_count = 0
        for j in range(i, len(transcript)):
            item = transcript[j]
            if item['start'] >= current_end:
                break
            char_count += len(item['text'])
        if char_count > max_density:
            max_density = char_count
            best_start = current_start
    return best_start

def analyze_with_ai(transcript, api_key):
    if not transcript or not api_key:
        return None, None, None
        
    try:
        client = OpenAI(api_key=api_key)
        
        full_text = " ".join([f"[{t['start']:.1f}] {t['text']}" for t in transcript])
        if len(full_text) > 30000:
            full_text = full_text[:30000] + "..."
            
        prompt = """
        Analyze this YouTube transcript and identify the SINGLE most viral, engaging, and standalone segment suitable for an Instagram Reel.
        The segment can be between 15 and 60 seconds long. Choose the best duration for the content.
        Also write a short, punchy, 2-5 word tagline for it.
        
        Return ONLY a JSON object:
        {
            "start_time": <float seconds>,
            "duration": <float seconds>,
            "tagline": "<string>"
        }
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a viral content expert."},
                {"role": "user", "content": f"{prompt}\n\nTranscript:\n{full_text}"}
            ],
            response_format={ "type": "json_object" }
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('start_time'), result.get('duration', 22), result.get('tagline')
        
    except Exception as e:
        print(f"AI Analysis failed: {e}")
        return None, None, None

def get_stable_face_center(clip):
    try:
        # Sample frames more frequently (every 0.5s) for better accuracy
        duration = clip.duration
        timestamps = np.arange(0, duration, 0.5)
        
        centers_x = []
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        for t in timestamps:
            try:
                frame = clip.get_frame(t)
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                    x, y, w, h = largest_face
                    centers_x.append(x + w/2)
            except:
                continue
                
        if not centers_x:
            return None
            
        # Return median X to avoid jitter
        return np.median(centers_x)
            
    except Exception as e:
        print(f"Stable face detection failed: {e}")
    
    return None

def create_rich_text_clip(tagline, duration):
    try:
        img_w, img_h = 1080, 400
        img = Image.new('RGBA', (img_w, img_h), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("impact.ttf", 80)
        except:
            try:
                font = ImageFont.truetype("arialbd.ttf", 70)
            except:
                font = ImageFont.load_default()
            
        words = tagline.split()
        if not words: return None
        longest_word = max(words, key=len)
        
        total_width = 0
        word_widths = []
        space_width = draw.textlength(" ", font=font)
        
        for w_str in words:
            width = draw.textlength(w_str, font=font)
            word_widths.append(width)
            total_width += width
        
        total_width += (len(words) - 1) * space_width
        current_x = (img_w - total_width) / 2
        y = (img_h - 100) / 2
        
        for i, w_str in enumerate(words):
            color = 'red' if w_str == longest_word else 'white'
            draw.text((current_x+2, y+2), w_str, font=font, fill='black')
            draw.text((current_x, y), w_str, font=font, fill=color)
            current_x += word_widths[i] + space_width
            
        txt_clip = ImageClip(np.array(img)).set_duration(duration)
        txt_clip = txt_clip.set_position(("center", 200))
        return txt_clip
    except Exception as e:
        print(f"Rich text generation failed: {e}")
        return None

def create_reel(video_path, start_time, tagline, output_filename, duration=22):
    try:
        clip = VideoFileClip(video_path)
        if start_time + duration > clip.duration:
            start_time = max(0, clip.duration - duration)
        subclip = clip.subclip(start_time, start_time + duration)
        
        w, h = subclip.size
        target_w = 1080
        target_h = 1920
        
        face_x = get_stable_face_center(subclip)
        min_dim = min(w, h)
        
        if face_x:
            print(f"Stable face center found at X={face_x}")
            # Center the crop on the face
            x1 = face_x - min_dim/2
            
            # Clamp to video bounds
            if x1 < 0: x1 = 0
            if x1 + min_dim > w: x1 = w - min_dim
            
            square_clip = subclip.crop(x1=x1, width=min_dim, height=min_dim, y_center=h/2)
        else:
            print("No face found, using center crop")
            square_clip = subclip.crop(width=min_dim, height=min_dim, x_center=w/2, y_center=h/2)
            
        square_clip = square_clip.resize(width=1080)
        square_clip = square_clip.set_position(("center", "center"))
        
        bg_clip = ColorClip(size=(target_w, target_h), color=(0,0,0), duration=duration)
        
        txt_clip = create_rich_text_clip(tagline, duration)
        if txt_clip:
            final_clip = CompositeVideoClip([bg_clip, square_clip, txt_clip])
        else:
            final_clip = CompositeVideoClip([bg_clip, square_clip])

        final_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac')
        final_clip.close()
        clip.close()
        return True
    except Exception as e:
        print(f"Error creating reel: {e}")
        return False
