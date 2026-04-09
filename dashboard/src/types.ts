export interface FloodViewData {
  years: number[]
  reGeneration: number[]
  totalGeneration: number[]
  batteryCapacity: number[]
}

export interface LMPHourlyData {
  hour: number
  cost: number
}

export interface LMPDataPoint {
  scenario: string
  region: string
  month: string
  hourlyData: LMPHourlyData[]
}

export interface LMPAnalysisData {
  scenarios: string[]
  regions: string[]
  months: string[]
  data: LMPDataPoint[]
}

export interface DashboardData {
  floodView: FloodViewData
  lmpAnalysis: LMPAnalysisData
}
