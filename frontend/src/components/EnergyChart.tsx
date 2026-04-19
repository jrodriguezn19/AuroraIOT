import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts'
import type { DataPoint, Metric, TimeRange } from '../types'

interface EnergyChartProps {
  history: DataPoint[]
  metric: Metric
  timeRange: TimeRange
  onMetricChange: (m: Metric) => void
  onRangeChange: (r: TimeRange) => void
}

const METRICS: { value: Metric; label: string; colorVar: string }[] = [
  { value: 'watts', label: 'Power (W)', colorVar: '--color-watts' },
  { value: 'volts', label: 'Voltage (V)', colorVar: '--color-volts' },
  { value: 'amps', label: 'Current (A)', colorVar: '--color-amps' },
  { value: 'frequency', label: 'Frequency (Hz)', colorVar: '--color-frequency' },
  { value: 'power_factor', label: 'Power Factor (%)', colorVar: '--color-pf' },
]

const RANGES: { value: TimeRange; label: string }[] = [
  { value: '1h', label: '1H' },
  { value: '6h', label: '6H' },
  { value: '24h', label: '24H' },
  { value: '7d', label: '7D' },
]

function formatTime(iso: string, range: TimeRange): string {
  const d = new Date(iso)
  if (range === '7d') {
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) +
      ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
  }
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
}

function formatTooltipTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) +
    ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
}

function getValue(point: DataPoint, metric: Metric): number {
  const v = point[metric]
  return typeof v === 'string' ? parseFloat(v) : v
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload, label, metric }: any) {
  if (!active || !payload?.length) return null
  const selected = METRICS.find(m => m.value === metric)
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-time">{formatTooltipTime(label)}</div>
      <div className="chart-tooltip-value" style={{ color: `var(${selected?.colorVar})` }}>
        {Number(payload[0].value).toFixed(2)} {selected?.label.match(/\((.+)\)/)?.[1]}
      </div>
    </div>
  )
}

export function EnergyChart({ history, metric, timeRange, onMetricChange, onRangeChange }: EnergyChartProps) {
  const selected = METRICS.find(m => m.value === metric) ?? METRICS[0]
  const color = `var(${selected.colorVar})`

  return (
    <div className="chart-container">
      <div className="chart-controls">
        <select
          className="chart-select"
          value={metric}
          onChange={e => onMetricChange(e.target.value as Metric)}
        >
          {METRICS.map(m => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
        <div className="range-buttons">
          {RANGES.map(r => (
            <button
              key={r.value}
              className={`range-btn${timeRange === r.value ? ' active' : ''}`}
              onClick={() => onRangeChange(r.value)}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {history.length === 0 ? (
        <div className="chart-empty">No data for this time range</div>
      ) : (
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={history} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis
              dataKey="time"
              tickFormatter={t => formatTime(t, timeRange)}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: 'var(--border)' }}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              width={55}
              domain={(['auto', 'auto'] as [string, string])}
            />
            <Tooltip
              content={<CustomTooltip metric={metric} />}
              cursor={{ stroke: 'var(--border)', strokeWidth: 1 }}
            />
            <Line
              type="monotone"
              dataKey={d => getValue(d as DataPoint, metric)}
              stroke={color}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: color }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
