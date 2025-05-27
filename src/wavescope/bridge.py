import asyncio
import websockets
import zmq
import zmq.asyncio

class Publisher:
    def __init__(self, port=5655):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        # TODO: Test with localhost
        self.publisher.bind(f"tcp://*:{port}")
        self.server_task = asyncio.create_task(start_server())

async def handler(ws):
    ctx = zmq.asyncio.Context()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5655")  # Adjust to your ZMQ publisher address
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics


    async def receive_and_forward():
        while True:
            msg = await subscriber.recv()
            await ws.send(msg)

    async def handle_topic_selection():
        async for message in ws:
            print(f"Received topic selection: {message}")
            topic = message.decode()
            print(f"Subscribing to topic: {topic}")
            # subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
    try:
        await asyncio.gather(
            receive_and_forward(),
            handle_topic_selection()
        )

    finally:
        subscriber.close()
        ctx.term()

async def start_server(host="localhost", port=8765):
    async with websockets.serve(handler, host, port):
        print(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
