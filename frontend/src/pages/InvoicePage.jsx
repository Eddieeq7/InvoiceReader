import { useState } from 'react'
import { Menu, X, FileText, Upload, AlertCircle, Calendar, DollarSign, CheckCircle, Clock, Loader, Building2, Hash } from 'lucide-react'
import { processInvoice } from '../api/mcp'

const InvoicePage = () => {
  // State management
  const [isMenuOpen, setIsMenuOpen] = useState(false)
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
  
  // Upload form state
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Upload handlers
  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        setError('')
      } else {
        setError('Only PDF files are supported')
      }
    }
  }

  const handleFileChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        setError('')
      } else {
        setError('Only PDF files are supported')
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedFile) return

    setLoading(true)
    setError('')

    try {
      // Process the invoice (upload + extract) - CONNECTS TO BACKEND
      const invoiceData = await processInvoice(selectedFile)
      
      // Convert backend response to frontend format
      const newInvoice = {
        id: invoices.length + 1,
        filename: selectedFile.name,
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
          confidence: invoiceData.metadata?.confidence
        }
      }
      
      setInvoices([newInvoice, ...invoices])
      setSelectedInvoice(newInvoice)
      setSelectedFile(null)
    } catch (err) {
      console.error('Invoice processing failed:', err)
      setError(err.message || 'Failed to process invoice. Make sure the backend is running on http://localhost:8001')
    } finally {
      setLoading(false)
    }
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    setError('')
  }

  // Invoice list handlers
  const getStatusIcon = (status) => {
    switch (status) {
      case 'processed':
        return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-600" />
      case 'processing':
        return <Loader className="h-5 w-5 text-blue-600 animate-spin" />
      default:
        return <Clock className="h-5 w-5 text-gray-600" />
    }
  }

  const getStatusBadge = (status) => {
    const styles = {
      processed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800'
    }
    return styles[status] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <FileText className="h-8 w-8 text-primary-600" />
              <span className="text-2xl font-bold text-dark-900">InvoiceReader</span>
            </div>
            
            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#home" className="text-dark-700 hover:text-primary-600 transition">Home</a>
              <a href="#invoices" className="text-dark-700 hover:text-primary-600 transition">Invoices</a>
              <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
                Get Started
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden text-dark-700"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden pb-4">
              <div className="flex flex-col space-y-4">
                <a href="#home" className="text-dark-700 hover:text-primary-600 transition">Home</a>
                <a href="#invoices" className="text-dark-700 hover:text-primary-600 transition">Invoices</a>
                <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition w-full">
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <section id="invoices" className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-dark-900 mb-4">Invoice Management</h2>
              <p className="text-xl text-dark-600 max-w-2xl mx-auto">
                Upload and manage your invoices with ease
              </p>
            </div>
            
            {/* Upload & List Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Upload Form */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                  <form onSubmit={handleSubmit}>
                    {error && (
                      <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2">
                        <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm font-semibold text-red-800">Error</p>
                          <p className="text-sm text-red-700">{error}</p>
                        </div>
                      </div>
                    )}
                    
                    <div
                      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                        dragActive
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-300 hover:border-primary-400'
                      } ${loading ? 'opacity-50 pointer-events-none' : ''}`}
                      onDragEnter={handleDrag}
                      onDragLeave={handleDrag}
                      onDragOver={handleDrag}
                      onDrop={handleDrop}
                    >
                      <input
                        type="file"
                        id="file-upload"
                        className="hidden"
                        accept=".pdf"
                        onChange={handleFileChange}
                      />
                      
                      {selectedFile ? (
                        <div className="space-y-4">
                          <div className="flex items-center justify-center space-x-3 bg-primary-50 rounded-lg p-4">
                            <FileText className="h-8 w-8 text-primary-600" />
                            <div className="text-left">
                              <p className="font-semibold text-dark-900">{selectedFile.name}</p>
                              <p className="text-sm text-dark-500">
                                {(selectedFile.size / 1024).toFixed(2)} KB
                              </p>
                            </div>
                            <button
                              type="button"
                              onClick={handleRemoveFile}
                              className="ml-auto text-red-600 hover:text-red-700"
                            >
                              <X className="h-5 w-5" />
                            </button>
                          </div>
                          <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {loading ? 'Processing...' : 'Upload & Extract Invoice'}
                          </button>
                        </div>
                      ) : (
                        <div>
                          <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                          <p className="text-dark-700 mb-2">
                            Drag and drop your PDF invoice here, or
                          </p>
                          <label
                            htmlFor="file-upload"
                            className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition cursor-pointer"
                          >
                            Browse Files
                          </label>
                          <p className="text-sm text-dark-500 mt-4">Only PDF files are supported</p>
                        </div>
                      )}
                    </div>
                  </form>
                </div>
              </div>

              {/* Invoice List */}
              <div className="lg:col-span-2">
                <div className="space-y-4">
                  {invoices.length === 0 ? (
                    <div className="text-center py-12 bg-white rounded-xl shadow-md">
                      <FileText className="h-16 w-16 mx-auto text-gray-400 mb-4" />
                      <p className="text-dark-600">No invoices uploaded yet</p>
                    </div>
                  ) : (
                    invoices.map((invoice) => (
                      <div
                        key={invoice.id}
                        onClick={() => setSelectedInvoice(invoice)}
                        className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-all cursor-pointer border border-gray-100 hover:border-primary-300"
                      >
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-3">
                            <div className="bg-primary-50 p-3 rounded-lg">
                              <FileText className="h-6 w-6 text-primary-600" />
                            </div>
                            <div>
                              <h3 className="font-semibold text-dark-900">{invoice.filename}</h3>
                              <p className="text-sm text-dark-500">{invoice.vendor}</p>
                            </div>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${getStatusBadge(invoice.status)}`}>
                            {getStatusIcon(invoice.status)}
                            {invoice.status}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 mt-4">
                          <div className="flex items-center space-x-2 text-dark-600">
                            <Calendar className="h-4 w-4" />
                            <span className="text-sm">{invoice.date}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-dark-600">
                            <DollarSign className="h-4 w-4" />
                            <span className="text-sm font-semibold">{invoice.amount}</span>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Invoice Preview Modal */}
      {selectedInvoice && selectedInvoice.preview && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="h-6 w-6 text-primary-600" />
                <h2 className="text-2xl font-bold text-dark-900">Invoice Preview</h2>
              </div>
              <button
                onClick={() => setSelectedInvoice(null)}
                className="text-gray-500 hover:text-gray-700 transition"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Content */}
            <div className="p-6">
              {/* Invoice Header */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                  <h3 className="text-xl font-bold text-dark-900 mb-4">Invoice Details</h3>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-dark-700">
                      <Hash className="h-5 w-5 text-primary-600" />
                      <span className="font-semibold">Invoice #:</span>
                      <span>{selectedInvoice.preview.invoiceNumber}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-dark-700">
                      <Calendar className="h-5 w-5 text-primary-600" />
                      <span className="font-semibold">Date:</span>
                      <span>{selectedInvoice.preview.date}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-dark-700">
                      <Calendar className="h-5 w-5 text-primary-600" />
                      <span className="font-semibold">Due Date:</span>
                      <span>{selectedInvoice.preview.dueDate}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-dark-900 mb-4">Vendor Information</h3>
                  <div className="flex items-center space-x-2 text-dark-700">
                    <Building2 className="h-5 w-5 text-primary-600" />
                    <span className="font-semibold">Vendor:</span>
                    <span>{selectedInvoice.preview.vendor}</span>
                  </div>
                </div>
              </div>

              {/* Items Table */}
              <div className="mb-6">
                <h3 className="text-xl font-bold text-dark-900 mb-4">Line Items</h3>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="border border-gray-200 px-4 py-3 text-left text-dark-900 font-semibold">Description</th>
                        <th className="border border-gray-200 px-4 py-3 text-center text-dark-900 font-semibold">Quantity</th>
                        <th className="border border-gray-200 px-4 py-3 text-right text-dark-900 font-semibold">Price</th>
                        <th className="border border-gray-200 px-4 py-3 text-right text-dark-900 font-semibold">Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedInvoice.preview.items.map((item, index) => (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="border border-gray-200 px-4 py-3 text-dark-700">{item.description}</td>
                          <td className="border border-gray-200 px-4 py-3 text-center text-dark-700">{item.quantity}</td>
                          <td className="border border-gray-200 px-4 py-3 text-right text-dark-700">{item.price}</td>
                          <td className="border border-gray-200 px-4 py-3 text-right text-dark-700 font-semibold">{item.total}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Totals */}
              <div className="flex justify-end">
                <div className="w-full md:w-1/3 space-y-2">
                  <div className="flex justify-between text-dark-700">
                    <span>Subtotal:</span>
                    <span>{selectedInvoice.preview.subtotal}</span>
                  </div>
                  <div className="flex justify-between text-dark-700">
                    <span>Tax:</span>
                    <span>{selectedInvoice.preview.tax}</span>
                  </div>
                  <div className="flex justify-between text-xl font-bold text-dark-900 pt-2 border-t-2 border-gray-300">
                    <span>Total:</span>
                    <span className="text-primary-600">{selectedInvoice.preview.total}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end">
              <button
                onClick={() => setSelectedInvoice(null)}
                className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default InvoicePage

