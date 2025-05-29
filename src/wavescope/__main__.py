import http.server
import socketserver
import os
import sys
from pathlib import Path

def run_server(directory: Path, port=8000):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on port {port} (http://localhost:{port}/) from directory: {directory}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Start a simple HTTP server to serve the public directory.")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    args = parser.parse_args()

    # Compute path to 'wavescope/src/wavescope/public' relative to this file
    public_dir = Path(__file__).resolve().parent / "public/fft"
    run_server(public_dir, args.port)

if __name__ == "__main__":
    main()
