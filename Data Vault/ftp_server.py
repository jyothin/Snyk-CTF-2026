from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pathlib import Path


HOST = "0.0.0.0"
PORT = 2121
FTP_DIR = str(Path(__file__).parent)


def main():
    # Create authorizer
    authorizer = DummyAuthorizer()
    
    # Add anonymous user with read permissions
    authorizer.add_anonymous(FTP_DIR, perm="elr")
    
    # Create handler and assign authorizer
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Set banner message
    handler.banner = "FTP Server Ready"
    
    # Create FTP server
    server = FTPServer((HOST, PORT), handler)
    
    print(f"FTP Server running on {HOST}:{PORT}")
    print(f"Serving directory: {FTP_DIR}")
    print("Anonymous login enabled (read-only)")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down FTP server...")
        server.close_all()
        print("FTP Server stopped.")


if __name__ == "__main__":
    main()
