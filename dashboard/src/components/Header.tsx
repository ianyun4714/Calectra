export default function Header() {
  return (
    <header className="border-b border-gray-700 py-8 bg-gradient-to-b from-darker via-darker to-transparent">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-4xl font-bold gradient-text mb-2">
              Calectra CEO Dashboard
            </h1>
            <p className="text-gray-400">
              Energy Market Analysis & Strategic Insights
            </p>
          </div>
          <div className="text-right">
            <div className="text-primary text-sm font-mono">
              NREL Cambium 2024
            </div>
            <div className="text-gray-500 text-xs mt-1">
              Last Updated: {new Date().toLocaleDateString()}
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-opacity-50 bg-blue-900 rounded-lg p-4 border border-blue-500 border-opacity-30">
            <div className="text-xs text-blue-400 uppercase tracking-wider">Our Thesis</div>
            <p className="text-sm mt-2">Renewable capacity will surge, overwhelming battery storage and collapsing prices</p>
          </div>
          <div className="bg-opacity-50 bg-green-900 rounded-lg p-4 border border-green-500 border-opacity-30">
            <div className="text-xs text-green-400 uppercase tracking-wider">The Opportunity</div>
            <p className="text-sm mt-2">Industrial thermal storage solves grid challenges and creates value</p>
          </div>
          <div className="bg-opacity-50 bg-purple-900 rounded-lg p-4 border border-purple-500 border-opacity-30">
            <div className="text-xs text-purple-400 uppercase tracking-wider">Timeline</div>
            <p className="text-sm mt-2">2025-2050 energy transition visible in real-time data</p>
          </div>
        </div>
      </div>
    </header>
  )
}
