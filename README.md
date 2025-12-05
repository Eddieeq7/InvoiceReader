# Invoice Reader

A professional, full-stack invoice processing application with AI-powered extraction capabilities. This project separates frontend and backend concerns for maintainability and scalability.

## 🏗️ Project Structure

```
InvoiceProject/
├── frontend/          # React + Vite frontend application
│   ├── src/          # Source code
│   ├── package.json  # Frontend dependencies
│   └── README.md     # Frontend documentation
├── backend/          # Python backend service
│   ├── mcp_tools/   # MCP tool implementations
│   ├── requirements.txt  # Python dependencies
│   └── README.md     # Backend documentation
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## ✨ Features

- **Frontend**: Modern React UI with Tailwind CSS
- **Backend**: MCP-compliant invoice extraction service
- **OCR**: Text extraction from PDF invoices
- **Intelligent Parsing**: Structured data extraction
- **Responsive Design**: Works on all devices

## 🚀 Quick Start

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to see the frontend.

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 Documentation

- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Lucide React (Icons)

### Backend
- Python 3.8+
- MCP (Model Context Protocol)
- OCR capabilities (TBD)
- Invoice parsing (TBD)

## 📋 Development Roadmap

- [ ] Complete OCR implementation
- [ ] Implement invoice parsing logic
- [ ] Connect frontend to backend API
- [ ] Add database integration
- [ ] Implement fraud detection
- [ ] Add analytics dashboard
- [ ] Add user authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT

## 📧 Contact

For questions or support, please open an issue in the repository.
