'''
+-------------------+        +-----------------------+        +------------------+        +------------------------+
|   Step 1: Install |        |  Step 2: Real-Time    |        |  Step 3: Pass    |        |  Step 4: Live Audio    |
|   Python Libraries|        |  Transcription with   |        |  Real-Time       |        |  Stream from Murf.ai  |
+-------------------+        |       AssemblyAI      |        |  Transcript to   |        |                        |
|                   |        +-----------------------+        |      Gemini      |        +------------------------+
| - assemblyai      |                    |                    +------------------+                    |
| - google.generativeai |                |                             |                              |
| - requests        |                    v                             v                              v
| - mpv             |        +-----------------------+        +------------------+        +------------------------+
| - portaudio       |        |                       |        |                  |        |                        |
+-------------------+        |  AssemblyAI performs  |-------->  Gemini generates|-------->  Murf.ai streams       |
                             |  real-time speech-to- |        |  response based  |        |  response as live      |
                             |  text transcription   |        |  on transcription|        |  audio to the user     |
                             |                       |        |                  |        |                        |
                             +-----------------------+        +------------------+        +------------------------+
'''

import assemblyai as aai
import google.generativeai as genai
import requests
import json
from pydub import AudioSegment
from pydub.playback import play
import io
import os

class AI_Assistant:
    def __init__(self):
        # API Keys
        aai.settings.api_key = "4627285ff75e4798b3aa6128eb68195c"
        genai.configure(api_key="AIzaSyBZFki_hs-ZyX4ZY9zRqd6bPPMqWS_BfYE")
        self.murf_api_key = "ap2_ea5d5b87-4494-41ee-ba0e-be04ac3b166d"
        
        # Initialize Gemini model
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Transcription setup
        self.transcriber = None
        
        # Conversation history
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

    ###### Step 2: Real-Time Transcription with AssemblyAI ######
        
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)
    
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occurred:", error)
        return

    def on_close(self):
        return

    ###### Step 3: Pass real-time transcript to Gemini ######
    
    def generate_ai_response(self, transcript):
        self.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\nPatient: {transcript.text}", end="\r\n")

        # Format conversation history for Gemini
        conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.full_transcript])
        
        # Get response from Gemini
        response = self.gemini_model.generate_content(
            f"Continue this conversation as the dental receptionist:\n{conversation}"
        )
        
        ai_response = response.text
        self.generate_audio(ai_response)

        self.start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")

    ###### Step 4: Generate audio with Murf.ai ######
        
    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        # Murf.ai API call
        headers = {
            "Authorization": f"Bearer {self.murf_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "voiceId": "en-US-Nancy",  # Change to your preferred voice
            "speed": 1.0,
            "pitch": 1.0,
            "sampleRate": 24000,
            "format": "mp3"
        }
        
        response = requests.post(
            "https://api.murf.ai/v1/speech/synthesize",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            # Save and play the audio
            audio_data = response.content
            audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
            play(audio)
        else:
            print(f"Error generating audio: {response.text}")

# Initialize and run the assistant
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()