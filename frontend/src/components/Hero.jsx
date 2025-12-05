import { Upload, Sparkles, TrendingUp } from 'lucide-react'

const Hero = () => {
  return (
    <section id="home" className="gradient-green text-white py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <Sparkles className="h-16 w-16 text-white" />
          </div>
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            AI-Powered Invoice Extraction
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white/90">
            Transform your invoice processing with intelligent automation. 
            Extract data, detect fraud, and gain insights instantly.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition flex items-center justify-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Invoice
            </button>
            <button className="bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-800 transition flex items-center justify-center gap-2 border-2 border-white">
              <TrendingUp className="h-5 w-5" />
              View Analytics
            </button>
          </div>
        </div>
        
        {/* Hero Image Placeholder */}
        <div className="mt-16 max-w-5xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
            <div className="aspect-video bg-white/5 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <Upload className="h-20 w-20 mx-auto mb-4 text-white/50" />
                <p className="text-white/70">Invoice Processing Dashboard Preview</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero



