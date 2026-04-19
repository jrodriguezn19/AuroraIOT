interface MetricCardProps {
  label: string
  value: string | number | null
  unit: string
  colorVar: string
}

export function MetricCard({ label, value, unit, colorVar }: MetricCardProps) {
  return (
    <div className="metric-card">
      <div className="metric-value" style={{ color: `var(${colorVar})` }}>
        {value ?? '—'}
        <span className="metric-unit">{unit}</span>
      </div>
      <div className="metric-label">{label}</div>
    </div>
  )
}
