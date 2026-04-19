import type { Sensor } from '../types'

interface SensorSelectorProps {
  sensors: Sensor[]
  selectedId: number
  onChange: (id: number) => void
}

export function SensorSelector({ sensors, selectedId, onChange }: SensorSelectorProps) {
  if (sensors.length <= 1) return null
  return (
    <select
      className="chart-select"
      value={selectedId}
      onChange={e => onChange(Number(e.target.value))}
    >
      {sensors.map(s => (
        <option key={s.id} value={s.id}>
          {s.name} — {s.location}
        </option>
      ))}
    </select>
  )
}
