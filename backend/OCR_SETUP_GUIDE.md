# OCR Setup Guide

## Dependencies Installed

The `ocr.py` module now includes real OCR functionality with a two-stage approach:

### Stage 1: Direct PDF Text Extraction
- Uses **pdfplumber** to extract text from text-based PDFs
- Fast and accurate for PDFs with embedded text

### Stage 2: Image-Based OCR Fallback
- Uses **pdf2image** to convert PDF pages to images
- Uses **pytesseract** to perform OCR on images
- Works for scanned PDFs and image-based documents

---

## Installation Steps

### 1. Install Python Dependencies

```bash
cd /Users/eddie/Documents/InvoiceProject/InvoiceReader/backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Tesseract (macOS)

Tesseract is required for image-based OCR:

```bash
brew install tesseract
```

### 3. Install Poppler (for pdf2image)

Poppler is required to convert PDFs to images:

```bash
brew install poppler
```

---

## How It Works

### Function: `extract_text(file_url: str) -> str`

1. **Validates** the file exists and is a PDF
2. **Stage 1**: Tries to extract text using pdfplumber (fast)
3. **Stage 2**: If no text found (< 10 chars), falls back to OCR (slower)
4. **Returns**: Full text content with page separators

### Features

✅ **Multi-page support** - Handles PDFs with multiple pages
✅ **Page markers** - Separates pages with "--- Page N ---" headers
✅ **Error handling** - Gracefully handles failures, returns empty string
✅ **Logging** - Detailed logging for debugging
✅ **Fallback strategy** - Automatically tries OCR if direct extraction fails

---

## Testing

Test the OCR on your invoice:

```python
from mcp_tools.invoice_reader.ocr import extract_text

text = extract_text("/Users/eddie/Documents/fruit_order_invoice.pdf")
print(text)
```

Or via the MCP server:

```bash
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "extract_invoice",
      "arguments": {
        "file_url": "/Users/eddie/Documents/fruit_order_invoice.pdf"
      }
    },
    "id": 1
  }'
```

---

## Troubleshooting

### "tesseract not found"
```bash
brew install tesseract
```

### "poppler not found" or pdf2image errors
```bash
brew install poppler
```

### Import errors
```bash
pip install pdfplumber pytesseract pdf2image pillow
```

---

## Performance Notes

- **Text-based PDFs**: Very fast (~100ms)
- **Scanned PDFs**: Slower (~2-5 seconds per page)
- The module automatically chooses the best method

---

## Code Structure

```
ocr.py
├── extract_text(file_url)           # Main function
├── _extract_text_from_pdf()         # Stage 1: Direct extraction
└── _extract_text_from_images()      # Stage 2: OCR fallback
```

