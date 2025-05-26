import numpy as np
import asyncio
import websockets

async def handler(ws):
    while True:
        # Simulate FFT data (1024 bins)
        freqs = np.linspace(0, 24000, 1024, dtype=np.float32)
        mags = np.abs(np.random.randn(1024)).astype(np.float32)

        # Concatenate freqs and mags into a single binary payload
        data = np.concatenate((freqs, mags)).tobytes()

        await ws.send(data)

        await asyncio.sleep(1 / 60)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
