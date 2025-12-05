import { FileText, Calendar, DollarSign, Building2, CheckCircle, Clock, Loader } from 'lucide-react'

const InvoiceList = ({ invoices, onInvoiceClick }) => {
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
    <div className="space-y-4">
      {invoices.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-xl">
          <FileText className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <p className="text-dark-600">No invoices uploaded yet</p>
        </div>
      ) : (
        invoices.map((invoice) => (
          <div
            key={invoice.id}
            onClick={() => onInvoiceClick(invoice)}
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
  )
}

export default InvoiceList

