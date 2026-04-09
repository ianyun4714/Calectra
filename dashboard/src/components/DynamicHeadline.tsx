interface DynamicHeadlineProps {
  reGrowth: number
  batteryGrowth: number
  gap: number
  year: number
}

export default function DynamicHeadline({ reGrowth, batteryGrowth, gap, year }: DynamicHeadlineProps) {
  const generateHeadline = () => {
    const gapPercent = ((gap - 1) * 100).toFixed(0)
    
    if (gap > 5) {
      return `Batteries Cannot Contain the Flood: ${gapPercent}% Gap in ${year}`
    } else if (gap > 3) {
      return `The Energy Deluge: Battery Storage Falls Behind by ${gapPercent}%`
    } else if (gap > 2) {
      return `Curtailment Crisis Looming: RE Grows ${reGrowth}% Faster Than Storage`
    } else {
      return `The Renewable Surge: ${reGrowth}% Growth Outpaces +${batteryGrowth}% Battery Expansion`
    }
  }

  return (
    <div className="mb-6">
      <h2 className="text-3xl font-bold gradient-text leading-tight">
        {generateHeadline()}
      </h2>
      <div className="mt-4 p-4 bg-red-900 bg-opacity-20 border border-red-500 border-opacity-50 rounded-lg">
        <p className="text-red-400 text-sm font-semibold">
          ⚠️ Key Insight: In {year}, renewable generation is {gap.toFixed(1)}x larger than battery storage capacity.
          This massive imbalance drives curtailment and price collapse during peak generation periods.
        </p>
      </div>
    </div>
  )
}
