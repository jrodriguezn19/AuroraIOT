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
  { value: '30d', label: '30D' },
  { value: '6m', label: '6M' },
  { value: '1y', label: '1Y' },
]

function formatAxisTick(ts: number, range: TimeRange): string {
  const d = new Date(ts)
  if (range === '1y' || range === '6m') {
    return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
  }
  if (range === '30d' || range === '7d') {
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
}

function formatTooltipTime(ts: number): string {
  const d = new Date(ts)
  return (
    d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) +
    ' ' +
    d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
  )
}

function computeTicks(range: TimeRange, data: DataPoint[]): number[] {
  if (data.length === 0) return []
  const first = new Date(data[0].time).getTime()
  const last = new Date(data[data.length - 1].time).getTime()
  const ticks: number[] = []
  const d = new Date(first)

  if (range === '1y' || range === '6m') {
    d.setDate(1); d.setHours(0, 0, 0, 0)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setMonth(d.getMonth() + 1) }
  } else if (range === '30d') {
    d.setHours(0, 0, 0, 0)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setDate(d.getDate() + 7) }
  } else if (range === '7d') {
    d.setHours(0, 0, 0, 0)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setDate(d.getDate() + 1) }
  } else if (range === '24h') {
    d.setMinutes(0, 0, 0); d.setHours(Math.ceil(d.getHours() / 4) * 4 % 24)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setHours(d.getHours() + 4) }
  } else if (range === '6h') {
    d.setMinutes(0, 0, 0)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setHours(d.getHours() + 1) }
  } else {
    d.setSeconds(0, 0); d.setMinutes(Math.ceil(d.getMinutes() / 15) * 15)
    while (d.getTime() <= last) { ticks.push(d.getTime()); d.setMinutes(d.getMinutes() + 15) }
  }

  return ticks
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
      <div className="chart-tooltip-time">{formatTooltipTime(label as number)}</div>
      <div className="chart-tooltip-value" style={{ color: `var(${selected?.colorVar})` }}>
        {Number(payload[0].value).toFixed(2)} {selected?.label.match(/\((.+)\)/)?.[1]}
      </div>
    </div>
  )
}

export function EnergyChart({ history, metric, timeRange, onMetricChange, onRangeChange }: EnergyChartProps) {
  const selected = METRICS.find(m => m.value === metric) ?? METRICS[0]
  const color = `var(${selected.colorVar})`
  const ticks = computeTicks(timeRange, history)

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
              dataKey={(d: DataPoint) => new Date(d.time).getTime()}
              type="number"
              scale="time"
              domain={['dataMin', 'dataMax']}
              ticks={ticks}
              tickFormatter={(t: number) => formatAxisTick(t, timeRange)}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: 'var(--border)' }}
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
