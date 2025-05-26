import asyncio
import websockets
import zmq
import zmq.asyncio

async def handler(ws):
    ctx = zmq.asyncio.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")  # Adjust to your ZMQ publisher address
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics

    try:
        while True:
            # # Simulate FFT data
            # freqs = np.linspace(0, 24000, 1024, dtype=np.float32)
            # mags = np.abs(np.random.randn(1024)).astype(np.float32)
            #
            # # Concatenate freqs and mags into a single binary payload
            # data = np.concatenate((freqs, mags)).tobytes()
            
            # Wait for FFT data message from ZMQ publisher
            msg = await subscriber.recv()
            
            # msg is raw bytes of FFT data, directly forward it to WebSocket clients
            await ws.send(msg)

            # If you want to control send rate, you can add sleep here or handle backpressure
            # await asyncio.sleep(1 / 60)
    finally:
        subscriber.close()
        ctx.term()

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())
