import { MetricCard } from './MetricCard'
import type { DataPoint } from '../types'

interface MetricGridProps {
  latest: DataPoint | null
}

export function MetricGrid({ latest }: MetricGridProps) {
  const pf = latest ? Math.round(latest.power_factor) : null

  return (
    <div className="metric-grid">
      <MetricCard label="Voltage" value={latest?.volts ?? null} unit="V" colorVar="--color-volts" />
      <MetricCard label="Current" value={latest ? Number(latest.amps).toFixed(2) : null} unit="A" colorVar="--color-amps" />
      <MetricCard label="Power" value={latest ? Number(latest.watts).toFixed(0) : null} unit="W" colorVar="--color-watts" />
      <MetricCard label="Energy" value={latest ? Number(latest.energy).toFixed(2) : null} unit="kWh" colorVar="--color-energy" />
      <MetricCard label="Frequency" value={latest?.frequency ?? null} unit="Hz" colorVar="--color-frequency" />
      <MetricCard label="Power Factor" value={pf} unit="%" colorVar="--color-pf" />
    </div>
  )
}
