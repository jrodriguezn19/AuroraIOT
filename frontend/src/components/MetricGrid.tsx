import { useState, useEffect } from 'react'
import { MetricCard } from './MetricCard'
import type { DataPoint } from '../types'

interface MetricGridProps {
  latest: DataPoint | null
}

function formatAge(iso: string, now: number): string {
  const ageMs = now - new Date(iso).getTime()
  const secs = Math.floor(ageMs / 1000)
  if (secs < 60) return `${secs}s ago`
  const mins = Math.floor(secs / 60)
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}

export function MetricGrid({ latest }: MetricGridProps) {
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(id)
  }, [])

  const pf = latest ? Math.round(latest.power_factor) : null
  const ageMs = latest ? now - new Date(latest.time).getTime() : null
  const stale = ageMs !== null && ageMs > 30_000

  return (
    <div className="metric-grid-wrapper">
      {latest && (
        <div className={`data-age ${stale ? 'stale' : 'fresh'}`}>
          Sensor data: {formatAge(latest.time, now)}{stale ? ' — sensor may be offline' : ''}
        </div>
      )}
      <div className="metric-grid">
        <MetricCard label="Voltage" value={latest?.volts ?? null} unit="V" colorVar="--color-volts" />
        <MetricCard label="Current" value={latest ? Number(latest.amps).toFixed(2) : null} unit="A" colorVar="--color-amps" />
        <MetricCard label="Power" value={latest ? Number(latest.watts).toFixed(0) : null} unit="W" colorVar="--color-watts" />
        <MetricCard label="Energy" value={latest ? Number(latest.energy).toFixed(2) : null} unit="kWh" colorVar="--color-energy" />
        <MetricCard label="Frequency" value={latest?.frequency ?? null} unit="Hz" colorVar="--color-frequency" />
        <MetricCard label="Power Factor" value={pf} unit="%" colorVar="--color-pf" />
      </div>
    </div>
  )
}
