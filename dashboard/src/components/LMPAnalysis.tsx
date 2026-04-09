import { useState, useMemo } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { LMPAnalysisData } from '../types'

interface LMPAnalysisProps {
  data: LMPAnalysisData
}

export default function LMPAnalysis({ data }: LMPAnalysisProps) {
  const [selectedScenario, setSelectedScenario] = useState(data.scenarios[0])
  const [selectedRegion, setSelectedRegion] = useState(data.regions[0])
  const [selectedMonth, setSelectedMonth] = useState(data.months[0])

  // Filter data based on selections
  const chartData = useMemo(() => {
    const filtered = data.data.find(
      d => d.scenario === selectedScenario && 
           d.region === selectedRegion && 
           d.month === selectedMonth
    )
    
    return filtered ? filtered.hourlyData : []
  }, [data, selectedScenario, selectedRegion, selectedMonth])

  // Calculate statistics
  const stats = useMemo(() => {
    if (chartData.length === 0) return { min: 0, max: 0, avg: 0, minHour: 0, maxHour: 0 }
    
    const costs = chartData.map(d => d.cost)
    const min = Math.min(...costs)
    const max = Math.max(...costs)
    const avg = costs.reduce((a, b) => a + b, 0) / costs.length
    const minHour = chartData.find(d => d.cost === min)?.hour || 0
    const maxHour = chartData.find(d => d.cost === max)?.hour || 0
    
    return { min, max, avg, minHour, maxHour }
  }, [chartData])

  // Determine if there's significant price collapse (duck curve)
  const hasDuckCurve = stats.max > 0 && stats.max / (stats.min || 1) > 2

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold gradient-text mb-2">
          Interactive LMP Analysis: The Duck Curve
        </h2>
        <p className="text-gray-400">
          Explore how Locational Marginal Prices ($/MWh) vary by hour under different scenarios, regions, and months.
          The "Duck Curve" shows the classic renewable energy pattern with midday price collapse.
        </p>
      </div>

      {/* Filter Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-gray-800 bg-opacity-50 p-6 rounded-lg border border-gray-700">
        <div>
          <label className="block text-sm font-semibold text-primary mb-2">Scenario</label>
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white hover:border-primary transition"
          >
            {data.scenarios.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-semibold text-primary mb-2">Region</label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white hover:border-primary transition"
          >
            {data.regions.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-semibold text-primary mb-2">Month</label>
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white hover:border-primary transition"
          >
            {data.months.map(m => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Warning for Duck Curve */}
      {hasDuckCurve && (
        <div className="p-4 bg-orange-900 bg-opacity-20 border border-orange-500 border-opacity-50 rounded-lg">
          <p className="text-orange-400 text-sm font-semibold">
            🦆 Duck Curve Detected: Price range of ${stats.min.toFixed(0)} - ${stats.max.toFixed(0)}/MWh
            represents a {(stats.max / stats.min).toFixed(1)}x variance, typical during high renewable penetration.
          </p>
        </div>
      )}

      {/* Chart */}
      <div className="chart-container">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis 
                dataKey="hour" 
                stroke="#888"
                label={{ value: 'Hour of Day', position: 'bottom', offset: 10 }}
              />
              <YAxis 
                stroke="#888"
                label={{ value: '$/MWh', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1a1f2e',
                  border: '1px solid #00D9FF',
                  borderRadius: '8px',
                }}
                formatter={(value: number) => [`$${value.toFixed(2)}/MWh`, 'Price']}
                labelFormatter={(label) => `Hour ${label}`}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="cost" 
                stroke="#00D9FF" 
                strokeWidth={3}
                dot={{ fill: '#FF6B35', r: 3 }}
                activeDot={{ r: 5 }}
                name="LMP ($/MWh)"
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-96 flex items-center justify-center text-gray-400">
            No data available for the selected filters
          </div>
        )}
      </div>

      {/* Statistics Cards */}
      {chartData.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
            <div className="text-sm text-gray-400 uppercase tracking-wide">Min Price</div>
            <div className="text-2xl font-bold text-green-400 mt-2">${stats.min.toFixed(2)}</div>
            <div className="text-xs text-gray-500 mt-1">Hour {stats.minHour}</div>
          </div>
          <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
            <div className="text-sm text-gray-400 uppercase tracking-wide">Max Price</div>
            <div className="text-2xl font-bold text-red-400 mt-2">${stats.max.toFixed(2)}</div>
            <div className="text-xs text-gray-500 mt-1">Hour {stats.maxHour}</div>
          </div>
          <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
            <div className="text-sm text-gray-400 uppercase tracking-wide">Average Price</div>
            <div className="text-2xl font-bold text-primary mt-2">${stats.avg.toFixed(2)}</div>
            <div className="text-xs text-gray-500 mt-1">All Hours</div>
          </div>
          <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
            <div className="text-sm text-gray-400 uppercase tracking-wide">Price Range</div>
            <div className="text-2xl font-bold text-secondary mt-2">{(stats.max / (stats.min || 1)).toFixed(1)}x</div>
            <div className="text-xs text-gray-500 mt-1">Max/Min Ratio</div>
          </div>
        </div>
      )}
    </div>
  )
}
