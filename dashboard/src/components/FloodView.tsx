import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart } from 'recharts'
import { FloodViewData } from '../types'
import DynamicHeadline from './DynamicHeadline'

interface FloodViewProps {
  data: FloodViewData
}

export default function FloodView({ data }: FloodViewProps) {
  // Prepare data for the chart
  const chartData = data.years.map((year, idx) => ({
    year,
    'RE Generation': data.reGeneration[idx],
    'Total Generation': data.totalGeneration[idx],
    'Battery Capacity': data.batteryCapacity[idx],
  }))

  // Calculate metrics for the headline
  const latestYear = data.years[data.years.length - 1]
  const earliestYear = data.years[0]
  const reGrowth = ((data.reGeneration[data.reGeneration.length - 1] - data.reGeneration[0]) / data.reGeneration[0] * 100).toFixed(0)
  const batteryGrowth = ((data.batteryCapacity[data.batteryCapacity.length - 1] - data.batteryCapacity[0]) / data.batteryCapacity[0] * 100).toFixed(0)
  const totalGap = (data.reGeneration[data.reGeneration.length - 1] / data.batteryCapacity[data.batteryCapacity.length - 1]).toFixed(1)

  return (
    <div className="space-y-8">
      <div>
        <DynamicHeadline
          reGrowth={parseFloat(reGrowth)}
          batteryGrowth={parseFloat(batteryGrowth)}
          gap={parseFloat(totalGap)}
          year={latestYear}
        />
        <p className="text-gray-400 mt-3 text-sm">
          Shows the massive growth in renewable energy generation (TWh) compared to battery storage capacity (TWh).
          The widening gap represents energy curtailment risk and Locational Marginal Price (LMP) collapse opportunities.
        </p>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis 
              dataKey="year" 
              stroke="#888"
              label={{ value: 'Year', position: 'bottom', offset: 10 }}
            />
            <YAxis 
              yAxisId="left"
              stroke="#888"
              label={{ value: 'Generation (TWh)', angle: -90, position: 'insideLeft' }}
            />
            <YAxis 
              yAxisId="right"
              orientation="right"
              stroke="#FF6B35"
              label={{ value: 'Battery Capacity (TWh)', angle: 90, position: 'insideRight' }}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: '#1a1f2e',
                border: '1px solid #00D9FF',
                borderRadius: '8px',
              }}
              formatter={(value: number) => value.toFixed(2)}
            />
            <Legend />
            
            <Bar yAxisId="left" dataKey="RE Generation" fill="#00D9FF" opacity={0.8} />
            <Bar yAxisId="left" dataKey="Total Generation" fill="#00D9FF" opacity={0.4} />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="Battery Capacity" 
              stroke="#FF6B35" 
              strokeWidth={2}
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
          <div className="text-sm text-gray-400 uppercase tracking-wide">RE Generation Growth</div>
          <div className="text-3xl font-bold gradient-text mt-2">{reGrowth}%</div>
          <div className="text-xs text-gray-500 mt-2">From {earliestYear} to {latestYear}</div>
        </div>
        <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
          <div className="text-sm text-gray-400 uppercase tracking-wide">Battery Capacity Growth</div>
          <div className="text-3xl font-bold text-secondary mt-2">{batteryGrowth}%</div>
          <div className="text-xs text-gray-500 mt-2">From {earliestYear} to {latestYear}</div>
        </div>
        <div className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700">
          <div className="text-sm text-gray-400 uppercase tracking-wide">{latestYear} Gap Ratio</div>
          <div className="text-3xl font-bold text-red-500 mt-2">{totalGap}x</div>
          <div className="text-xs text-gray-500 mt-2">RE to Battery Capacity Ratio</div>
        </div>
      </div>
    </div>
  )
}
