import { useState, useEffect } from 'react'

function App() {
  const [url, setUrl] = useState('')
  const [tagline, setTagline] = useState('')
  const [loading, setLoading] = useState(false)
  const [jobId, setJobId] = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let interval;
    if (jobId && loading) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`http://localhost:8000/status/${jobId}`)
          const data = await res.json()

          setProgress(data.progress)
          setStatus(data.status)

          if (data.error) {
            setError(data.error)
            setLoading(false)
            setJobId(null)
          } else if (data.progress === 100 && data.result) {
            setResult(data.result)
            setLoading(false)
            setJobId(null)
          }
        } catch (err) {
          console.error("Polling error", err)
        }
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [jobId, loading])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    setProgress(0)
    setStatus('Starting...')

    try {
      const response = await fetch('http://localhost:8000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          tagline: tagline || null
        }),
      })

      if (!response.ok) {
        const errData = await response.json()
        throw new Error(errData.detail || 'Failed to start process')
      }

      const data = await response.json()
      setJobId(data.job_id)

    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl overflow-hidden border border-gray-700">
        <div className="p-8">
          <h1 className="text-3xl font-bold text-center mb-2 bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-orange-500">
            Reel Generator
          </h1>
          <p className="text-gray-400 text-center mb-8">
            Turn YouTube videos into viral Reels
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                YouTube URL
              </label>
              <input
                type="url"
                required
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                disabled={loading}
                placeholder="https://youtube.com/watch?v=..."
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none transition-all disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Tagline <span className="text-gray-500 font-normal">(Optional)</span>
              </label>
              <input
                type="text"
                value={tagline}
                onChange={(e) => setTagline(e.target.value)}
                disabled={loading}
                placeholder="Leave empty to auto-generate with AI"
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none transition-all disabled:opacity-50"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-bold text-white transition-all transform hover:scale-[1.02] ${loading
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 shadow-lg shadow-red-500/30'
                }`}
            >
              {loading ? 'Processing...' : 'Generate Reel'}
            </button>
          </form>

          {loading && (
            <div className="mt-6 space-y-2">
              <div className="flex justify-between text-sm text-gray-400">
                <span>{status}</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-red-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {error && (
            <div className="mt-6 p-4 bg-red-900/50 border border-red-500/50 rounded-lg text-red-200 text-sm">
              {error}
            </div>
          )}
        </div>
      </div>

      {result && (
        <div className="mt-8 max-w-sm w-full bg-gray-800 rounded-xl shadow-2xl overflow-hidden border border-gray-700 animate-fade-in-up">
          <div className="p-4 border-b border-gray-700">
            <h2 className="text-lg font-semibold text-center">Your Reel is Ready!</h2>
          </div>
          <div className="relative pt-[177.77%] bg-black">
            <video
              src={`http://localhost:8000/download/${result.filename.split('/').pop()}`}
              controls
              className="absolute top-0 left-0 w-full h-full object-contain"
            />
          </div>
          <div className="p-4">
            <a
              href={`http://localhost:8000/download/${result.filename.split('/').pop()}`}
              download
              className="block w-full py-3 px-4 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium text-center transition-colors"
            >
              Download Video
            </a>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
