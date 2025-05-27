import asyncio
import websockets
import zmq
import zmq.asyncio

class Publisher:
    def __init__(self, port=5655):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.port = port
        # TODO: Test with localhost
        self.publisher.bind(f"tcp://*:{self.port}")
        self.server_task = asyncio.create_task(start_server())

async def handler(ws):
    ctx = zmq.asyncio.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(f"tcp://localhost:{self.port}")  # Adjust to your ZMQ publisher address
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics

    async def receive_and_forward():
        while True:
            msg = await subscriber.recv()
            await ws.send(msg)

    async def handle_topic_selection():
        async for message in ws:
            print(f"Received topic selection: {message}")
            # subscriber.setsockopt_string(zmq.SUBSCRIBE, message)

    try:
        await asyncio.gather(
            receive_and_forward(),
            handle_topic_selection()
        )
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        subscriber.close()
        ctx.term()

async def start_server(host="localhost", port=8765):
    async with websockets.serve(handler, host, port):
        print(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
