#!/usr/bin/env python3
"""
DiscoveryOS Server Launcher - Uses SQLite by default
"""
import os
import sys
import socket
import time

# Ensure we use SQLite by default
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite:///./discoveryos.db"
    print("[INFO] Using SQLite database: discoveryos.db")

# Now import and run FastAPI
from main import app
import uvicorn

def find_available_port(preferred_port=8000):
    """Find an available port starting from preferred_port"""
    for port in range(preferred_port, preferred_port + 100):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', port))
            sock.close()
            time.sleep(0.1)  # Brief delay to ensure port is released
            return port
        except OSError:
            continue
    return preferred_port

if __name__ == "__main__":
    print("\n" + "="*70)
if __name__ == "__main__":
    print("\n" + "="*70)
    print("DiscoveryOS Backend - Starting Server")
    print("="*70)
    
    port = find_available_port(5000)  # Changed from 8000 to 5000
    print(f"API Documentation: http://localhost:{port}/docs")
    print("\nDatabase: SQLite (discoveryos.db)")
    print("Press Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

