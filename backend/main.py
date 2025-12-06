"""
MCP Server Entrypoint

This module serves as the main entrypoint for starting the Invoice Reader MCP server.
It uses uvicorn to run the FastAPI application with development-friendly settings.

Usage:
    # Start the MCP server
    python main.py
    
    # Or use uvicorn directly
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload
    
The server will be available at:
    - Main MCP endpoint: http://0.0.0.0:8001/mcp
    - Server info: http://0.0.0.0:8001/
    - Health check: http://0.0.0.0:8001/health

Configuration:
    - Host: 0.0.0.0 (accessible from all network interfaces)
    - Port: 8001
    - Reload: Enabled in development mode (auto-restart on code changes)
"""

import uvicorn
from mcp_server import app


if __name__ == "__main__":
    # Run the FastAPI MCP server with uvicorn
    uvicorn.run(
        "mcp_server:app",  # App module path
        host="0.0.0.0",    # Listen on all network interfaces
        port=8001,         # Server port
        reload=True,       # Enable auto-reload for development
        log_level="info"   # Logging level
    )

