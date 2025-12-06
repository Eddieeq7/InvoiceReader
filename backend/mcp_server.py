"""
MCP Server for Invoice Reader

This module implements a fully functional MCP (Model Context Protocol) server
using FastAPI. It exposes the InvoiceReaderTool as an MCP tool via JSON-RPC,
allowing clients to extract structured invoice data from PDF files.

Architecture:
- FastAPI handles HTTP requests at the `/mcp` endpoint
- JSON-RPC 2.0 protocol for tool invocation
- InvoiceReaderTool performs the actual invoice extraction

Usage:
    # Run the server
    uvicorn mcp_server:app --host 0.0.0.0 --port 8000
    
    # Send a JSON-RPC request
    POST /mcp
    {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "extract_invoice",
            "arguments": {
                "file_url": "path/to/invoice.pdf"
            }
        },
        "id": 1
    }
"""

from typing import Any, Dict, List
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import os
import uuid

from mcp_tools.invoice_reader import InvoiceReaderTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Upload directory for invoice files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Initialize FastAPI app
app = FastAPI(
    title="Invoice Reader MCP Server",
    description="MCP server for extracting structured data from invoice PDFs",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the invoice reader tool
invoice_tool = InvoiceReaderTool()


# MCP Tool Handler
async def extract_invoice(file_url: str) -> Dict[str, Any]:
    """
    Extract structured invoice data from a PDF file.
    
    This MCP tool wraps the InvoiceReaderTool.extract() method and provides
    invoice data extraction capabilities via JSON-RPC.
    
    Args:
        file_url: URL or file path to the PDF invoice file
        
    Returns:
        Dictionary containing extracted invoice data including:
        - invoice_number: Invoice identifier
        - date: Invoice date
        - due_date: Payment due date
        - vendor: Vendor/supplier information
        - items: List of line items with descriptions and amounts
        - subtotal: Subtotal amount before tax
        - tax: Tax amount
        - total: Total amount including tax
        - metadata: Additional metadata about the invoice
        
    Raises:
        Exception: If the file cannot be processed or parsed
    """
    try:
        # Log the extraction request
        logger.info(f"Extracting invoice from: {file_url}")
        
        # Call the InvoiceReaderTool to extract invoice data
        result = invoice_tool.extract(file_url)
        
        logger.info(f"Successfully extracted invoice data")
        return result
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise Exception(f"File not found: {str(e)}")
    except ValueError as e:
        logger.error(f"Invalid file or parsing error: {str(e)}")
        raise Exception(f"Invalid file or parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Error extracting invoice: {str(e)}")
        raise Exception(f"Error extracting invoice: {str(e)}")


@app.post("/mcp")
async def handle_mcp_request(request: Request) -> JSONResponse:
    """
    Handle MCP JSON-RPC requests.
    
    This endpoint receives JSON-RPC 2.0 requests and routes them to the
    appropriate MCP tool handler. It supports the following JSON-RPC methods:
    - initialize: Initialize the MCP session
    - tools/list: List all available tools
    - tools/call: Call a specific tool with arguments
    
    Args:
        request: FastAPI request object containing JSON-RPC payload
        
    Returns:
        JSONResponse with JSON-RPC 2.0 response containing:
        - For initialize: Server capabilities and information
        - For tools/list: List of available tools with schemas
        - For tools/call: Result from the tool execution
        - For errors: JSON-RPC error response
        
    Example Request:
        {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "extract_invoice",
                "arguments": {
                    "file_url": "/path/to/invoice.pdf"
                }
            },
            "id": 1
        }
        
    Example Response:
        {
            "jsonrpc": "2.0",
            "result": {
                "invoice_number": "INV-001",
                "date": "2025-12-01",
                "total": 1250.00,
                ...
            },
            "id": 1
        }
    """
    try:
        # Parse JSON-RPC request
        body = await request.json()
        
        # Log the request method
        logger.info(f"Received JSON-RPC request: {body.get('method')}")
        
        # Validate JSON-RPC format
        if not isinstance(body, dict) or body.get("jsonrpc") != "2.0":
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request"
                    },
                    "id": body.get("id")
                },
                status_code=400
            )
        
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        
        # Handle initialize method (MCP protocol initialization)
        if method == "initialize":
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "invoice-reader-server",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    },
                    "id": request_id
                }
            )
        
        # Handle tools/list method
        elif method == "tools/list":
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": [
                            {
                                "name": "extract_invoice",
                                "description": "Extract structured invoice data from a PDF file",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_url": {
                                            "type": "string",
                                            "description": "URL or file path to the PDF invoice file"
                                        }
                                    },
                                    "required": ["file_url"]
                                }
                            }
                        ]
                    },
                    "id": request_id
                }
            )
        
        # Handle tools/call method
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name != "extract_invoice":
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {tool_name}"
                        },
                        "id": request_id
                    },
                    status_code=404
                )
            
            # Validate required arguments
            if "file_url" not in arguments:
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": "Invalid params: 'file_url' is required"
                        },
                        "id": request_id
                    },
                    status_code=400
                )
            
            # Execute the tool
            try:
                result = await extract_invoice(arguments["file_url"])
                
                # Return MCP-compliant response with content array
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2)
                                }
                            ],
                            "isError": False
                        },
                        "id": request_id
                    }
                )
            except Exception as e:
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32000,
                            "message": str(e)
                        },
                        "id": request_id
                    },
                    status_code=500
                )
        
        # Unsupported method
        else:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request_id
                },
                status_code=404
            )
    
    except json.JSONDecodeError:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                },
                "id": None
            },
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": body.get("id") if 'body' in locals() else None
            },
            status_code=500
        )


@app.get("/")
async def root():
    """
    Root endpoint providing server information.
    
    Returns basic information about the MCP server and available endpoints.
    """
    return {
        "name": "Invoice Reader MCP Server",
        "version": "1.0.0",
        "protocolVersion": "2024-11-05",
        "description": "MCP server for extracting structured data from invoice PDFs",
        "endpoints": {
            "/mcp": "POST - MCP JSON-RPC endpoint",
            "/": "GET - Server information",
            "/health": "GET - Health check"
        },
        "tools": ["extract_invoice"],
        "capabilities": {
            "tools": {}
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment.
    
    Returns the server status and health information.
    """
    return {
        "status": "healthy",
        "service": "invoice-reader-mcp-server",
        "version": "1.0.0"
    }


@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)) -> JSONResponse:
    """
    Upload an invoice PDF file to the server.
    
    This endpoint accepts a PDF file upload and saves it to the server's
    upload directory. It returns the server-side file path that can be
    used with the extract_invoice MCP tool.
    
    Args:
        file: The uploaded PDF file
        
    Returns:
        JSONResponse containing:
        - file_url: Server-side file path for the uploaded PDF
        - filename: Original filename
        - size: File size in bytes
        
    Example:
        POST /upload
        Content-Type: multipart/form-data
        
        Response:
        {
            "file_url": "/path/to/server/file.pdf",
            "filename": "invoice.pdf",
            "size": 12345
        }
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={"error": "Only PDF files are allowed"}
            )
        
        # Generate unique filename
        ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Uploaded file: {file.filename} ({len(content)} bytes) -> {file_path}")
        
        return JSONResponse(content={
            "file_url": file_path,
            "filename": file.filename,
            "size": len(content)
        })
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Upload failed: {str(e)}"}
        )
