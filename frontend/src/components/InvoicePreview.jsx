import { X, FileText, Calendar, Building2, DollarSign, Hash } from 'lucide-react'

const InvoicePreview = ({ invoice, onClose }) => {
  if (!invoice || !invoice.preview) {
    return null
  }

  const preview = invoice.preview

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <FileText className="h-6 w-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-dark-900">Invoice Preview</h2>
          </div>
          <button
            onClick={onClose}
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
                  <span>{preview.invoiceNumber}</span>
                </div>
                <div className="flex items-center space-x-2 text-dark-700">
                  <Calendar className="h-5 w-5 text-primary-600" />
                  <span className="font-semibold">Date:</span>
                  <span>{preview.date}</span>
                </div>
                <div className="flex items-center space-x-2 text-dark-700">
                  <Calendar className="h-5 w-5 text-primary-600" />
                  <span className="font-semibold">Due Date:</span>
                  <span>{preview.dueDate}</span>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-xl font-bold text-dark-900 mb-4">Vendor Information</h3>
              <div className="flex items-center space-x-2 text-dark-700">
                <Building2 className="h-5 w-5 text-primary-600" />
                <span className="font-semibold">Vendor:</span>
                <span>{preview.vendor}</span>
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
                  {preview.items.map((item, index) => (
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
                <span>{preview.subtotal}</span>
              </div>
              <div className="flex justify-between text-dark-700">
                <span>Tax:</span>
                <span>{preview.tax}</span>
              </div>
              <div className="flex justify-between text-xl font-bold text-dark-900 pt-2 border-t-2 border-gray-300">
                <span>Total:</span>
                <span className="text-primary-600">{preview.total}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end">
          <button
            onClick={onClose}
            className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default InvoicePreview

