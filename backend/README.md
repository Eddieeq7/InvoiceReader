# Invoice Reader - Backend

Backend service for the Invoice Reader application, providing MCP-compliant invoice extraction and parsing capabilities.

## Overview

The backend implements an MCP (Model Context Protocol) tool for extracting structured invoice data from PDF files. It uses OCR technology to extract text and intelligent parsing to structure the data.

## Architecture

```
backend/
├── mcp_tools/              # MCP tool implementations
│   └── invoice_reader/     # Invoice reader tool
│       ├── __init__.py
│       ├── handler.py      # Main MCP handler
│       ├── ocr.py          # OCR text extraction
│       ├── parser.py       # Invoice parsing logic
│       └── invoice_reader.json  # MCP tool definition
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- **OCR Text Extraction**: Extracts text from PDF invoice files
- **Intelligent Parsing**: Structures extracted text into invoice data
- **MCP Compliance**: Implements Model Context Protocol for tool integration
- **Structured Output**: Returns standardized invoice data format

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### MCP Tool Integration

The invoice reader tool is designed to be used via MCP (Model Context Protocol). The main entry point is the `InvoiceReaderTool.extract()` method in `handler.py`.

### Example Usage

```python
from mcp_tools.invoice_reader.handler import InvoiceReaderTool

tool = InvoiceReaderTool()
invoice_data = tool.extract("path/to/invoice.pdf")

print(invoice_data)
```

### Expected Output Format

```python
{
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "due_date": "2024-02-15",
    "vendor": "Acme Corporation",
    "items": [
        {
            "description": "Product A",
            "quantity": 10,
            "unit_price": 50.0,
            "total": 500.0
        }
    ],
    "subtotal": 500.0,
    "tax": 0.0,
    "total": 500.0,
    "metadata": {
        "confidence": 0.95
    }
}
```

## Development

### Project Structure

- **handler.py**: Main MCP handler that orchestrates OCR and parsing
- **ocr.py**: OCR module for text extraction from PDFs
- **parser.py**: Parsing module for structuring invoice data
- **invoice_reader.json**: MCP tool definition and schema

### Adding Dependencies

When adding new Python packages, update `requirements.txt`:

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Testing

TODO: Add testing framework and test cases

## API Integration

The backend can be integrated with:
- FastAPI server for REST API endpoints
- Direct MCP server implementation
- Standalone Python scripts

## Future Enhancements

- [ ] Implement OCR using Tesseract or cloud OCR APIs
- [ ] Add ML-based invoice parsing
- [ ] Support for multiple invoice formats
- [ ] Fraud detection capabilities
- [ ] Database integration for invoice storage
- [ ] API endpoints for frontend integration

## License

MIT

