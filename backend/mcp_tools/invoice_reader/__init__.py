"""
Invoice Reader MCP Tool

This package provides an MCP-compliant tool for extracting and parsing
invoice data from PDF files. The tool can be called via JSON-RPC from
a FastAPI MCP server.

MCP Flow:
1. FastAPI receives JSON-RPC request
2. Routes to InvoiceReaderTool.extract()
3. Tool coordinates OCR and parsing
4. Returns structured invoice data

Usage:
    from mcp_tools.invoice_reader import InvoiceReaderTool
    
    tool = InvoiceReaderTool()
    result = tool.extract("path/to/invoice.pdf")
"""

from .handler import InvoiceReaderTool

__all__ = ["InvoiceReaderTool"]

