import asyncio
import zmq
import numpy as np
import time

import .bridge

class Publisher:
    def __init__(self, port=5655):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        # TODO: Test with localhost
        self.publisher.bind(f"tcp://*:{port}")
        self.bridge_task = asyncio.create_task(bridge.start_server())

async def test(publisher):
    while True:
        freqs = np.linspace(0, 24000, 1024, dtype=np.float32)
        mags = np.abs(np.random.randn(1024)).astype(np.float32)

        # Concatenate freq and mag arrays into single bytes object
        data = np.concatenate((freqs, mags)).tobytes()

        publisher.send(data)
        await asyncio.sleep(1 / 60)  # ~60 Hz publishing rate

async def main():
    publisher = Publisher()
    test_task = asyncio.create_task(test(publisher.publisher))
    await asyncio.gather(publisher.bridge_task, test_task)

if __name__ == "__main__":
    asyncio.run(main())
