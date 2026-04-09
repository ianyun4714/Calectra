import { useState, useEffect } from 'react'
import FloodView from './components/FloodView'
import LMPAnalysis from './components/LMPAnalysis'
import Header from './components/Header'
import { DashboardData } from './types'

function App() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        // Load the processed data from the data directory
        const response = await fetch('./data/dashboard_data.json')
        if (!response.ok) throw new Error('Failed to load data')
        const jsonData = await response.json()
        setData(jsonData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        console.error('Error loading data:', err)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-darker flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin">
            <div className="w-12 h-12 border-4 border-primary border-t-secondary rounded-full"></div>
          </div>
          <p className="mt-4 text-primary text-lg">Loading Dashboard...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-darker flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 text-lg">⚠️ {error || 'Failed to load dashboard data'}</p>
          <p className="text-gray-400 mt-2">Please ensure the data files are in the correct location.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-darker text-white">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Flood View Section */}
        <section className="mb-12">
          <FloodView data={data.floodView} />
        </section>

        {/* LMP Analysis Section */}
        <section>
          <LMPAnalysis data={data.lmpAnalysis} />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-700 mt-16 py-8">
        <div className="container mx-auto px-4 max-w-7xl text-center text-gray-500 text-sm">
          <p>Powered by NREL Cambium 2024 Data | Calectra © 2024</p>
        </div>
      </footer>
    </div>
  )
}

export default App
