import os
import requests
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from speech_recognition import Recognizer, Microphone
import tempfile
from pygame import mixer
import time
import datetime
import re

# Initialize ElevenLabs (free tier)
ELEVENLABS_API_KEY = "sk_9d42f39f62b02282c1604dcd2b23bd07fd0351bb8fbb0c7b"  # Replace with your valid key
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default free voice

# Initialize pygame mixer
mixer.init()

def text_to_speech(text):
    """Convert text to speech using ElevenLabs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False, mode='wb') as temp_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            mixer.music.load(temp_file_path)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
            mixer.music.stop()
            mixer.music.unload()
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Error during playback: {e}")
            try:
                mixer.music.stop()
                mixer.music.unload()
                os.remove(temp_file_path)
            except:
                pass
    else:
        print("Error in TTS:", response.text)

def speech_to_text():
    """Convert speech to text using Google's Web Speech API"""
    r = Recognizer()
    with Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        print("Error:", e)
        return ""

def handle_conversation():
    """Main conversation loop"""
    appointment = {
        'date': None,
        'time': None,
        'confirmed': False
    }

    ai_response = "Hello! I'm your booking assistant. What day would you like to schedule your appointment?"
    print("AI:", ai_response)
    text_to_speech(ai_response)

    while True:
        user_input = speech_to_text()
        if not user_input:
            continue

        print("User:", user_input)
        user_input = user_input.lower()

        # Exit commands
        if any(word in user_input for word in ["cancel", "stop", "exit", "quit", "bye"]):
            ai_response = "Thank you for using our service. Goodbye!"
            print("AI:", ai_response)
            text_to_speech(ai_response)
            break

        # Handle date input
        if appointment['date'] is None:
            if any(word in user_input for word in [
                "today", "tomorrow", "next", "monday", "tuesday", "wednesday",
                "thursday", "friday", "saturday", "sunday"
            ]):
                appointment['date'] = user_input
                ai_response = f"I see you'd like to book for {user_input}. What time would work best for you?"
            else:
                ai_response = "I didn't catch the day. Could you please specify which day you'd like to book? For example, 'Monday' or 'next week'?"

        # Handle time input
        elif appointment['time'] is None:
            if any(word in user_input for word in ["morning", "afternoon", "evening"]) or \
               ":" in user_input or any(str(hour) in user_input for hour in range(1, 13)):
                appointment['time'] = user_input
                ai_response = f"Great! Just to confirm - you'd like an appointment for {appointment['date']} at {appointment['time']}. Is this correct?"
            else:
                ai_response = "What time would you prefer? You can say morning, afternoon, or a specific time."

        # Handle confirmation
        elif not appointment['confirmed']:
            if any(word in user_input for word in ["yes", "correct", "right", "sure", "okay", "confirm"]):
                appointment['confirmed'] = True
                ai_response = "Perfect! I've scheduled your appointment. Would you like me to send you an email confirmation?"
            elif any(word in user_input for word in ["no", "wrong", "incorrect", "change"]):
                appointment['date'] = None
                appointment['time'] = None
                ai_response = "Let's try again. What day would you like to schedule your appointment?"
            else:
                ai_response = "I didn't catch that. Please say 'yes' to confirm or 'no' to reschedule."

        # Handle email confirmation
        else:
            if any(word in user_input for word in ["yes", "sure", "okay", "please"]):
                ai_response = "I'll send you an email confirmation right away. Thank you for booking with us. Have a great day!"
                print("AI:", ai_response)
                text_to_speech(ai_response)
                break
            elif any(word in user_input for word in ["no", "don't", "skip"]):
                ai_response = "No problem. Your appointment is confirmed. Thank you for booking with us. Have a great day!"
                print("AI:", ai_response)
                text_to_speech(ai_response)
                break
            else:
                ai_response = "Would you like me to send you an email confirmation? Please say yes or no."

        print("AI:", ai_response)
        text_to_speech(ai_response)


if __name__ == "__main__":
    handle_conversation()
