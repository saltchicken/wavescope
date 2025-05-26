import asyncio
import zmq
import numpy as np
import time

from . import bridge

class Publisher:
    def __init__(self, port=5655):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        # TODO: Test with localhost
        self.publisher.bind(f"tcp://*:{port}")
        self.bridge_task = asyncio.create_task(bridge.start_server())
