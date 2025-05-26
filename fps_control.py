import asyncio
import numpy as np
import websockets
import json
import time

SAMPLE_RATE = 1024
N = 256
FREQ = 60
TARGET_DT = 1 / 60  # 60 Hz = 16.666... ms per frame

async def send_fft(websocket):
    t = 0.0
    while True:
        start = time.perf_counter()

        # === Signal + FFT ===
        x = np.arange(N) / SAMPLE_RATE
        signal = np.sin(2 * np.pi * (FREQ + t * 2) * x  + t) + 0.2 * np.random.randn(N)
        max_val = np.max(np.abs(signal))
        if max_val > 0:
            signal = signal / max_val
        fft_vals = np.fft.rfft(signal)
        fft_magnitude = np.abs(fft_vals)

        # === Send over WebSocket ===
        payload = {
            "freqs": np.fft.rfftfreq(N, 1/SAMPLE_RATE).tolist(),
            "mags": fft_magnitude.tolist()
        }
        await websocket.send(json.dumps(payload))

        # === Precise frame timing ===
        elapsed = time.perf_counter() - start
        sleep_time = max(0, TARGET_DT - elapsed)
        await asyncio.sleep(sleep_time)

        t += 0.05  # phase shift for continuous animation

async def main():
    print("WebSocket server running at ws://localhost:8765")
    async with websockets.serve(send_fft, "localhost", 8765):
        await asyncio.Future()  # Run forever

# Recommended for Python 3.7+
if __name__ == "__main__":
    asyncio.run(main())
