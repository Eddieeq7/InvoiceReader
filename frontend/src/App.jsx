import { useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import StatsCards from './components/StatsCards'
import Services from './components/Services'
import InvoiceList from './components/InvoiceList'
import UploadForm from './components/UploadForm'
import InvoicePreview from './components/InvoicePreview'

function App() {
  const [invoices, setInvoices] = useState([
    {
      id: 1,
      filename: 'invoice_001.pdf',
      vendor: 'Acme Corporation',
      date: '2024-01-15',
      amount: '$1,250.00',
      status: 'processed',
      preview: {
        invoiceNumber: 'INV-2024-001',
        date: '2024-01-15',
        dueDate: '2024-02-15',
        vendor: 'Acme Corporation',
        items: [
          { description: 'Product A', quantity: 10, price: '$50.00', total: '$500.00' },
          { description: 'Product B', quantity: 5, price: '$150.00', total: '$750.00' }
        ],
        subtotal: '$1,250.00',
        tax: '$0.00',
        total: '$1,250.00'
      }
    },
    {
      id: 2,
      filename: 'invoice_002.pdf',
      vendor: 'Tech Solutions Inc.',
      date: '2024-01-20',
      amount: '$2,500.00',
      status: 'processed',
      preview: {
        invoiceNumber: 'INV-2024-002',
        date: '2024-01-20',
        dueDate: '2024-02-20',
        vendor: 'Tech Solutions Inc.',
        items: [
          { description: 'Software License', quantity: 1, price: '$2,000.00', total: '$2,000.00' },
          { description: 'Support Package', quantity: 1, price: '$500.00', total: '$500.00' }
        ],
        subtotal: '$2,500.00',
        tax: '$0.00',
        total: '$2,500.00'
      }
    },
    {
      id: 3,
      filename: 'invoice_003.pdf',
      vendor: 'Global Supplies',
      date: '2024-01-25',
      amount: '$1,825.50',
      status: 'pending',
      preview: {
        invoiceNumber: 'INV-2024-003',
        date: '2024-01-25',
        dueDate: '2024-02-25',
        vendor: 'Global Supplies',
        items: [
          { description: 'Office Supplies', quantity: 50, price: '$25.00', total: '$1,250.00' },
          { description: 'Shipping', quantity: 1, price: '$575.50', total: '$575.50' }
        ],
        subtotal: '$1,825.50',
        tax: '$0.00',
        total: '$1,825.50'
      }
    }
  ])

  const [selectedInvoice, setSelectedInvoice] = useState(null)

  const handleUpload = (invoiceData) => {
    // Convert the extracted invoice data to the app's format
    const newInvoice = {
      id: invoices.length + 1,
      filename: `${invoiceData.invoice_number || 'invoice'}.pdf`,
      vendor: invoiceData.vendor || 'Unknown Vendor',
      date: invoiceData.date || new Date().toISOString().split('T')[0],
      amount: `$${invoiceData.total.toFixed(2)}`,
      status: 'processed',
      preview: {
        invoiceNumber: invoiceData.invoice_number || 'N/A',
        date: invoiceData.date || 'N/A',
        dueDate: invoiceData.due_date || 'N/A',
        vendor: invoiceData.vendor || 'Unknown',
        items: invoiceData.items.map(item => ({
          description: item.description,
          quantity: item.quantity,
          price: `$${item.unit_price.toFixed(2)}`,
          total: `$${item.total.toFixed(2)}`
        })),
        subtotal: `$${invoiceData.subtotal.toFixed(2)}`,
        tax: `$${invoiceData.tax.toFixed(2)}`,
        total: `$${invoiceData.total.toFixed(2)}`,
        currency: invoiceData.currency,
        confidence: invoiceData.metadata.confidence
      }
    }
    
    setInvoices([newInvoice, ...invoices])
    
    // Automatically select the newly uploaded invoice
    setSelectedInvoice(newInvoice)
  }

  const handleInvoiceClick = (invoice) => {
    if (invoice.preview) {
      setSelectedInvoice(invoice)
    }
  }

  const handleClosePreview = () => {
    setSelectedInvoice(null)
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <StatsCards invoices={invoices} />
      <Services />
      
      <section id="invoices" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-dark-900 mb-4">Invoice Management</h2>
              <p className="text-xl text-dark-600 max-w-2xl mx-auto">
                Upload and manage your invoices with ease
              </p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-1">
                <UploadForm onUpload={handleUpload} />
              </div>
              <div className="lg:col-span-2">
                <InvoiceList invoices={invoices} onInvoiceClick={handleInvoiceClick} />
              </div>
            </div>
          </div>
        </div>
      </section>

      {selectedInvoice && (
        <InvoicePreview invoice={selectedInvoice} onClose={handleClosePreview} />
      )}
    </div>
  )
}

export default App

