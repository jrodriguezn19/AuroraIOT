export interface Sensor {
  id: number
  name: string
  brand: string
  location: string
}

export interface DataPoint {
  id: number
  sensor_id: number
  time: string
  volts: number
  amps: number
  frequency: number
  watts: number
  energy: number
  power_factor: number
}

export type TimeRange = '1h' | '6h' | '24h' | '7d' | '30d' | '6m' | '1y'

export type Metric = 'watts' | 'volts' | 'amps' | 'frequency' | 'power_factor'
