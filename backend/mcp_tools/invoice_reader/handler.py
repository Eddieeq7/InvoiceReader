"""
MCP Handler for Invoice Reader Tool

This module defines the InvoiceReaderTool class which implements the MCP-compliant
handler for invoice extraction. The handler coordinates the OCR and parsing steps
to extract structured invoice data from PDF files.

MCP Flow:
1. Receives JSON-RPC request with file_url parameter
2. Calls OCR module to extract text from PDF
3. Calls parser module to structure the extracted text
4. Returns structured invoice data as Python dict
"""

from typing import Dict, Any
from .ocr import extract_text
from .parser import parse_invoice


class InvoiceReaderTool:
    """
    MCP-compliant tool handler for invoice extraction.
    
    This class implements the extract method that will be called via JSON-RPC
    from the FastAPI MCP server. It orchestrates the OCR and parsing pipeline.
    """
    
    def extract(self, file_url: str) -> Dict[str, Any]:
        """
        Extract invoice data from a PDF file.
        
        This is the main entry point for the MCP tool. It processes the invoice
        through the OCR and parsing pipeline and returns structured data.
        
        Args:
            file_url: URL or file path to the PDF invoice file
            
        Returns:
            Dictionary containing extracted invoice data with the following structure:
            {
                "invoice_number": str,
                "date": str,
                "due_date": str,
                "vendor": str,
                "items": List[Dict],
                "subtotal": float,
                "tax": float,
                "total": float,
                "metadata": Dict
            }
            
        Raises:
            FileNotFoundError: If the file cannot be accessed
            ValueError: If the file is not a valid PDF or cannot be processed
        """
        # Step 1: Extract text from PDF using OCR
        # TODO: Implement OCR text extraction
        text = extract_text(file_url)
        
        # Step 2: Parse the extracted text into structured data
        # TODO: Implement invoice parsing logic
        invoice_data = parse_invoice(text)
        
        # Return structured invoice data
        return invoice_data

