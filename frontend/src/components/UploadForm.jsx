import { useState } from 'react'
import { Upload, FileText, X } from 'lucide-react'

const UploadForm = ({ onUpload }) => {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

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
      }
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
      }
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (selectedFile) {
      onUpload(selectedFile)
      setSelectedFile(null)
    }
  }

  const handleRemove = () => {
    setSelectedFile(null)
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
      <form onSubmit={handleSubmit}>
        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
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
            onChange={handleChange}
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
                  onClick={handleRemove}
                  className="ml-auto text-red-600 hover:text-red-700"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <button
                type="submit"
                className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
              >
                Upload Invoice
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
  )
}

export default UploadForm

