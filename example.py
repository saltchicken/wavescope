import asyncio
import wavescope
import numpy as np

async def my_task(publisher):
    while True:
        freqs = np.linspace(0, 24000, 1024, dtype=np.float32)
        mags = np.abs(np.random.randn(1024)).astype(np.float32)

        # Concatenate freq and mag arrays into single bytes object
        data = np.concatenate((freqs, mags)).tobytes()

        publisher.send(data)
        await asyncio.sleep(0.01)

async def run():
    # ws = wavescope.WaveScope()
    publisher = wavescope.Publisher()
    task = asyncio.create_task(my_task(publisher.publisher))
    await asyncio.gather(task, publisher.server_task)


def main():
    asyncio.run(run())
