# Invoice Reader - Quick Start Guide

## 🚀 **Get Started in 3 Steps**

### **Step 1: Start the Backend** (Terminal 1)
```bash
cd backend
source venv/bin/activate
python main.py
```

✅ Server running on: `http://localhost:8001`

---

### **Step 2: Start the Frontend** (Terminal 2)
```bash
cd frontend
npm run dev
```

✅ Frontend running on: `http://localhost:5173`

---

### **Step 3: Upload an Invoice**
1. Open `http://localhost:5173` in your browser
2. Drag & drop a PDF invoice (or click "Browse Files")
3. Click "Upload & Extract Invoice"
4. View the extracted data!

---

## 📝 **What You'll See**

The system will automatically extract:
- Invoice number
- Date and due date
- Vendor information
- Line items (description, quantity, price)
- Subtotal, tax, and total amounts
- Confidence score

---

## 🔧 **Troubleshooting**

### **Backend won't start?**
```bash
# Make sure dependencies are installed
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### **Frontend won't start?**
```bash
# Install dependencies
cd frontend
npm install
```

### **Upload fails?**
- Check both backend and frontend are running
- Check console for errors (F12 in browser)
- Verify PDF file is valid

### **No data extracted?**
- Check the PDF has text (not just images)
- Check backend logs for errors
- Try a different invoice format

---

## 📊 **Test with Sample Invoice**

If you don't have an invoice, the backend already processed this one successfully:
- `/Users/eddie/Documents/fruit_order_invoice.pdf`

Results:
- ✅ Invoice Number: FR-2025-0099
- ✅ Vendor: Tropical Fruit Market
- ✅ 4 line items extracted
- ✅ Total: $56.71
- ✅ 100% confidence

---

## 🎯 **API Endpoints**

Once running, you can test the API directly:

**Health Check:**
```bash
curl http://localhost:8001/health
```

**Upload PDF:**
```bash
curl -X POST http://localhost:8001/upload \
  -F "file=@/path/to/invoice.pdf"
```

**Extract Invoice (after upload):**
```bash
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{
      "name":"extract_invoice",
      "arguments":{"file_url":"/path/from/upload/response"}
    },
    "id":1
  }'
```

---

## 📖 **More Information**

- **Full Integration Details**: See `INTEGRATION_GUIDE.md`
- **MCP Server Details**: See `backend/MCP_VERIFICATION_REPORT.md`
- **OCR Setup**: See `backend/OCR_SETUP_GUIDE.md`

---

## ✨ **That's It!**

Your Invoice Reader is ready to process invoices! 🎉

