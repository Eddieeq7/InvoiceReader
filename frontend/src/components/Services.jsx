import { Scan, Database, Shield, BarChart3 } from 'lucide-react'

const Services = () => {
  const services = [
    {
      icon: Scan,
      title: 'Automated OCR',
      description: 'Advanced optical character recognition extracts text from any invoice format with 99% accuracy.',
      color: 'text-primary-600',
      bgColor: 'bg-primary-50'
    },
    {
      icon: Database,
      title: 'Metadata Extraction',
      description: 'Intelligently extracts invoice numbers, dates, amounts, vendors, and line items automatically.',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      icon: Shield,
      title: 'Fraud Detection',
      description: 'AI-powered fraud detection identifies suspicious patterns and duplicate invoices in real-time.',
      color: 'text-red-600',
      bgColor: 'bg-red-50'
    },
    {
      icon: BarChart3,
      title: 'Analytics & Insights',
      description: 'Comprehensive analytics dashboard with spending trends, vendor analysis, and financial insights.',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    }
  ]

  return (
    <section id="services" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-dark-900 mb-4">Our Services</h2>
          <p className="text-xl text-dark-600 max-w-2xl mx-auto">
            Powerful AI-driven features to streamline your invoice processing workflow
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((service, index) => {
            const Icon = service.icon
            return (
              <div
                key={index}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 border border-gray-100"
              >
                <div className={`${service.bgColor} w-16 h-16 rounded-xl flex items-center justify-center mb-4`}>
                  <Icon className={`h-8 w-8 ${service.color}`} />
                </div>
                <h3 className="text-xl font-bold text-dark-900 mb-3">{service.title}</h3>
                <p className="text-dark-600">{service.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default Services


