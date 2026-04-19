import { useState, useEffect } from 'react'
import { fetchSensors } from './services/api'
import { useLiveData } from './hooks/useLiveData'
import { MetricGrid } from './components/MetricGrid'
import { EnergyChart } from './components/EnergyChart'
import { SensorSelector } from './components/SensorSelector'
import type { Sensor, Metric, TimeRange } from './types'

export default function App() {
  const [sensors, setSensors] = useState<Sensor[]>([])
  const [sensorId, setSensorId] = useState<number>(1)
  const [metric, setMetric] = useState<Metric>('watts')
  const [timeRange, setTimeRange] = useState<TimeRange>('1h')

  useEffect(() => {
    fetchSensors()
      .then(data => {
        setSensors(data)
        if (data.length > 0) setSensorId(data[0].id)
      })
      .catch(() => {})
  }, [])

  const { latest, history, loading, error, lastUpdated } = useLiveData(sensorId, timeRange)

  const activeSensor = sensors.find(s => s.id === sensorId)

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <span className="header-title">AuroraIOT</span>
          {activeSensor && (
            <span className="header-subtitle">{activeSensor.name} · {activeSensor.location}</span>
          )}
        </div>
        <div className="header-right">
          <SensorSelector sensors={sensors} selectedId={sensorId} onChange={setSensorId} />
          {lastUpdated && (
            <span className="last-updated">
              {lastUpdated.toLocaleTimeString('en-US', { timeZone: 'America/Bogota', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })}
            </span>
          )}
          <div className={`status-dot ${error ? 'error' : loading ? 'loading' : 'live'}`} title={error ?? 'Live'} />
        </div>
      </header>

      <main className="main">
        <MetricGrid latest={latest} />
        <EnergyChart
          history={history}
          metric={metric}
          timeRange={timeRange}
          onMetricChange={setMetric}
          onRangeChange={setTimeRange}
        />
      </main>
    </div>
  )
}
