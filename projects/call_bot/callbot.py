import asyncio
import sounddevice as sd
import numpy as np
import websockets
import json
import base64
import os

# Your OpenAI API key
OPENAI_API_KEY = "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"  # replace with your key

# Audio configuration
SAMPLE_RATE = 16000  # Hz
BLOCK_SIZE = 1024
CHANNELS = 1

async def main():
    uri = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"

    # WebSocket headers for authentication
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1",
    }

    print("🔊 Connecting to GPT-4o Realtime API...")
    async with websockets.connect(uri, extra_headers=headers) as ws:
        print("✅ Connected! Start speaking... (Press Ctrl+C to stop)")

        # Start the audio input stream
        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_b64 = base64.b64encode(indata[:, 0].tobytes()).decode("utf-8")
            asyncio.run_coroutine_threadsafe(
                ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": audio_b64
                })),
                loop
            )

        loop = asyncio.get_running_loop()
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=BLOCK_SIZE, callback=callback):
            await ws.send(json.dumps({"type": "response.create"}))

            async for message in ws:
                data = json.loads(message)
                if data.get("type") == "response.audio.delta":
                    # Decode and play the audio
                    audio_data = base64.b64decode(data["delta"])
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    sd.play(audio_array, SAMPLE_RATE)
                elif data.get("type") == "response.completed":
                    print("\n🤖 Conversation round completed.\n")
                    await ws.send(json.dumps({"type": "response.create"}))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Conversation ended by user.")
