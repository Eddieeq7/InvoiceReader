# Frontend-Backend Integration Guide

## ✅ **Integration Complete!**

Your Invoice Reader application now has a fully functional frontend-backend integration.

---

## 🎯 **What Was Added**

### **Backend Changes** (`backend/mcp_server.py`)

#### 1. **Upload Endpoint** - `POST /upload`
- Accepts PDF file uploads via multipart/form-data
- Saves files to `backend/uploads/` directory
- Returns server-side file path for MCP tool

```python
POST /upload
Content-Type: multipart/form-data

Response:
{
  "file_url": "/absolute/path/to/uploaded/file.pdf",
  "filename": "original-name.pdf",
  "size": 12345
}
```

### **Frontend Changes**

#### 1. **MCP API Client** (`frontend/src/api/mcp.js`)
New module with functions:
- `uploadInvoice(file)` - Upload PDF to server
- `extractInvoice(fileUrl)` - Extract data via MCP
- `processInvoice(file)` - Upload + Extract in one call
- `listTools()` - List available MCP tools
- `checkHealth()` - Check server health

#### 2. **Updated UploadForm Component** (`frontend/src/components/UploadForm.jsx`)
- Now calls `processInvoice()` on submit
- Shows loading state during processing
- Displays error messages if extraction fails
- Returns extracted invoice data to parent

#### 3. **Updated App Component** (`frontend/src/App.jsx`)
- `handleUpload()` now receives structured invoice data
- Converts MCP response to app format
- Automatically displays extracted invoice
- Adds to invoice list with "processed" status

---

## 🚀 **How to Use**

### **1. Start the Backend**
```bash
cd backend
source venv/bin/activate
python main.py
```
Server runs on: `http://localhost:8001`

### **2. Start the Frontend**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

### **3. Upload an Invoice**
1. Open `http://localhost:5173` in your browser
2. Drag & drop a PDF invoice or click "Browse Files"
3. Click "Upload & Extract Invoice"
4. Wait for processing (OCR + parsing)
5. View extracted data automatically

---

## 📊 **Data Flow**

```
User uploads PDF
    ↓
Frontend: UploadForm.jsx
    ↓
API: uploadInvoice(file)
    ↓
Backend: POST /upload → saves file
    ↓
API: extractInvoice(fileUrl)
    ↓
Backend: POST /mcp → calls extract_invoice tool
    ↓
OCR: Extracts text from PDF
    ↓
Parser: Structures invoice data
    ↓
Backend: Returns JSON response
    ↓
Frontend: Displays invoice data
```

---

## 🔧 **API Configuration**

The frontend API base URL is configured via environment variable:

Create `frontend/.env`:
```bash
VITE_API_BASE=http://localhost:8001
```

For production, change to your deployed backend URL.

---

## 📋 **Example: Extracted Invoice Data**

When you upload an invoice, the MCP server extracts:

```json
{
  "invoice_number": "FR-2025-0099",
  "date": "2025-02-10",
  "due_date": "2025-02-25",
  "vendor": "Tropical Fruit Market",
  "items": [
    {
      "description": "Bananas",
      "quantity": 10.0,
      "unit_price": 0.6,
      "total": 6.0
    }
  ],
  "subtotal": 53.00,
  "tax": 3.71,
  "total": 56.71,
  "currency": "USD",
  "metadata": {
    "confidence": 1.0,
    "text_length": 455,
    "items_found": 4
  }
}
```

---

## 🎨 **UI Features**

### **Upload Form**
- ✅ Drag & drop support
- ✅ File validation (PDF only)
- ✅ Loading indicator during processing
- ✅ Error handling with user-friendly messages
- ✅ File preview before upload

### **Invoice List**
- ✅ Shows newly extracted invoices
- ✅ Status badge (processed/pending)
- ✅ Click to view detailed preview
- ✅ Sorted by most recent first

### **Invoice Preview**
- ✅ Full invoice details
- ✅ Line items table
- ✅ Financial summary
- ✅ Confidence score indicator

---

## 🔒 **Security Notes**

### **Current Setup (Development)**
- CORS allows all origins (`*`)
- Files stored in `backend/uploads/`
- No authentication required

### **Production Recommendations**
1. **CORS**: Restrict to your frontend domain
   ```python
   allow_origins=["https://your-frontend-domain.com"]
   ```

2. **File Upload**:
   - Add file size limits
   - Validate file content (not just extension)
   - Store files outside web root
   - Add virus scanning

3. **Authentication**:
   - Add API keys or OAuth
   - Rate limiting on upload endpoint
   - User-specific file storage

4. **HTTPS**:
   - Use SSL/TLS in production
   - Update API_BASE to `https://`

---

## 🧪 **Testing the Integration**

### **1. Test Upload Endpoint**
```bash
curl -X POST http://localhost:8001/upload \
  -F "file=@/path/to/invoice.pdf"
```

### **2. Test Full Flow**
```bash
# Upload
UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8001/upload \
  -F "file=@/path/to/invoice.pdf")

FILE_URL=$(echo $UPLOAD_RESPONSE | jq -r '.file_url')

# Extract
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"extract_invoice\",
      \"arguments\": {\"file_url\": \"$FILE_URL\"}
    },
    \"id\": 1
  }"
```

### **3. Test Frontend**
1. Open browser console (F12)
2. Upload an invoice
3. Watch network tab for API calls
4. Check console for any errors

---

## 📁 **File Structure**

```
InvoiceProject/
├── backend/
│   ├── main.py                    # Server entrypoint
│   ├── mcp_server.py              # MCP server + upload endpoint ✨
│   ├── uploads/                   # Uploaded PDF files ✨
│   └── mcp_tools/
│       └── invoice_reader/
│           ├── ocr.py             # PDF text extraction
│           └── parser.py          # Invoice data parsing
└── frontend/
    └── src/
        ├── api/
        │   └── mcp.js             # API client ✨
        ├── components/
        │   └── UploadForm.jsx     # Updated with API calls ✨
        └── App.jsx                # Updated data handling ✨
```

---

## ✅ **Integration Checklist**

- [x] Upload endpoint added to backend
- [x] API client module created in frontend
- [x] UploadForm component integrated with API
- [x] App component handles extracted data
- [x] CORS configured for cross-origin requests
- [x] Error handling implemented
- [x] Loading states added
- [x] File validation in place
- [x] Automatic invoice preview on upload

---

## 🎉 **Ready to Use!**

Your Invoice Reader is now a fully integrated web application:

1. **Backend**: MCP server with OCR + parsing + upload endpoint
2. **Frontend**: React UI with drag-drop upload and invoice management
3. **Integration**: Seamless data flow from PDF → structured data → UI

Upload an invoice and watch it get processed in real-time! 🚀

---

**Next Steps**:
- Add more invoice formats to the parser
- Implement invoice editing features
- Add export functionality (CSV, JSON, Excel)
- Create invoice analytics dashboard
- Add user authentication
- Deploy to production

