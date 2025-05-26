import zmq
import numpy as np
import time

def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5655")  # Bind to all interfaces on port 5555

    while True:
        # Example FFT data (1024 bins)
        freqs = np.linspace(0, 24000, 1024, dtype=np.float32)
        mags = np.abs(np.random.randn(1024)).astype(np.float32)

        # Concatenate freq and mag arrays into single bytes object
        data = np.concatenate((freqs, mags)).tobytes()

        # Send raw bytes via ZMQ publisher
        publisher.send(data)

        print("Sent FFT data")
        time.sleep(1 / 60)  # ~60 Hz publishing rate

if __name__ == "__main__":
    main()
