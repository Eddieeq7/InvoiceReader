import { FileText, CheckCircle, Clock, DollarSign } from 'lucide-react'

const StatsCards = ({ invoices }) => {
  const stats = [
    {
      icon: FileText,
      label: 'Total Invoices',
      value: invoices.length,
      color: 'text-primary-600',
      bgColor: 'bg-primary-50'
    },
    {
      icon: CheckCircle,
      label: 'Processed',
      value: invoices.filter(inv => inv.status === 'processed').length,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      icon: Clock,
      label: 'Pending',
      value: invoices.filter(inv => inv.status === 'pending' || inv.status === 'processing').length,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50'
    },
    {
      icon: DollarSign,
      label: 'Total Value',
      value: '$5,575.50',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    }
  ]

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <div
                key={index}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
              >
                <div className={`${stat.bgColor} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <h3 className="text-3xl font-bold text-dark-900 mb-2">{stat.value}</h3>
                <p className="text-dark-600">{stat.label}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default StatsCards



