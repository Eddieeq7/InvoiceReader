# Invoice Reader - Frontend

Modern, responsive React frontend for the AI-powered invoice extraction application.

## Features

- 🎨 **Modern UI Design** - Clean green/white/dark theme with responsive layout
- 📄 **Invoice Management** - Upload, view, and manage invoices
- 🔍 **Invoice Preview** - Detailed preview modal with extracted data
- 📊 **Statistics Dashboard** - Real-time stats cards showing invoice metrics
- 🤖 **AI Services Showcase** - Display of OCR, metadata extraction, fraud detection, and analytics
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 16+ and npm (or yarn/pnpm)

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── Navbar.jsx      # Navigation bar
│   │   ├── Hero.jsx        # Hero section
│   │   ├── StatsCards.jsx  # Statistics cards
│   │   ├── Services.jsx    # Services showcase
│   │   ├── InvoiceList.jsx # Invoice list display
│   │   ├── UploadForm.jsx  # PDF upload form
│   │   └── InvoicePreview.jsx # Invoice preview modal
│   ├── pages/              # Page components (for future expansion)
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── postcss.config.js       # PostCSS configuration
```

## Components

### Navbar
Responsive navigation bar with mobile menu support.

### Hero
Eye-catching hero section explaining the AI-powered invoice extraction service.

### StatsCards
Dynamic statistics cards showing total invoices, processed count, pending count, and total value.

### Services
Showcase of four main services:
- Automated OCR
- Metadata Extraction
- Fraud Detection
- Analytics & Insights

### InvoiceList
Displays all uploaded invoices with status indicators and key information.

### UploadForm
Drag-and-drop file upload form with PDF validation.

### InvoicePreview
Modal component displaying detailed invoice information including line items and totals.

## Color Scheme

- **Primary Green**: `#22c55e` (primary-600)
- **Dark**: `#111827` (dark-900)
- **White**: Base background
- **Accent Colors**: Blue, Yellow, Red, Purple for various UI elements

## Development Notes

### Adding New Components

1. Create component file in `src/components/`
2. Export as default
3. Import and use in `App.jsx` or other components

### Styling

- Uses Tailwind CSS utility classes
- Custom colors defined in `tailwind.config.js`
- Global styles in `src/index.css`

### State Management

Currently uses React's `useState` hook. For larger applications, consider:
- Context API
- Redux
- Zustand
- Jotai

## Backend Integration

TODO: Connect frontend to backend API endpoints for:
- File upload
- Invoice processing
- Data fetching

## License

MIT

