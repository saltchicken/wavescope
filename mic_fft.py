# fft_server.py
import asyncio
import numpy as np
import pyaudio
import websockets

# Audio config
CHUNK = 1024           # Number of samples per FFT
RATE = 48000           # Sampling rate
FORMAT = pyaudio.paFloat32
CHANNELS = 1

# FFT frequency bins
freqs = np.fft.rfftfreq(CHUNK, d=1/RATE).astype(np.float32)

# Start PyAudio stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

async def handler(ws):
    try:
        while True:
            # Read raw audio
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.float32)

            # Compute FFT magnitude
            fft = np.fft.rfft(samples)
            mags = np.abs(fft).astype(np.float32)

            # Optional: normalize magnitude (log scale or linear)
            mags /= np.max(mags) + 1e-8  # avoid division by 0
            mags *= 100  # scale for visualization

            # Combine freqs + mags and send
            payload = np.concatenate((freqs, mags)).tobytes()
            await ws.send(payload)

            await asyncio.sleep(1/60)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
