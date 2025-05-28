import asyncio
import json
import websockets
import zmq
import zmq.asyncio

class Publisher:
    def __init__(self, port=5655):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.port = port
        self.queue = asyncio.Queue()
        self.server_task = asyncio.create_task(self.start_server())
        self.data = {"test": "testing"}

    async def handler(self, ws):
        async def receive_and_forward():
            while True:
                msg = await self.queue.get()
                await ws.send(msg)

        async def message_from_client():
            async for message in ws:
                message = json.loads(message)
                if message.get("type") == "init":
                    print(f"Received message: {message.get('data')}")
                    await ws.send(json.dumps({"type": "init", "data": self.data}))
                    # subscriber.setsockopt_string(zmq.SUBSCRIBE, message)

        try:
            await asyncio.gather(
                receive_and_forward(),
                message_from_client()
            )
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            subscriber.close()
            ctx.term()

    async def start_server(self, host="localhost", port=8765):
        async with websockets.serve(self.handler, host, port):
            print(f"WebSocket server running on ws://{host}:{port}")
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())
