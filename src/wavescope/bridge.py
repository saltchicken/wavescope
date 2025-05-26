import asyncio
import websockets
import zmq
import zmq.asyncio

async def handler(ws):
    ctx = zmq.asyncio.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5655")  # Adjust to your ZMQ publisher address
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics

    try:
        while True:
            msg = await subscriber.recv()
            await ws.send(msg)
    finally:
        subscriber.close()
        ctx.term()

async def start_server(host="localhost", port=8765):
    async with websockets.serve(handler, host, port):
        print(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
