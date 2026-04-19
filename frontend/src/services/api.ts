import type { Sensor, DataPoint } from '../types'

const BASE = `${import.meta.env.VITE_API_URL ?? ''}/api`

async function get<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export async function fetchSensors(): Promise<Sensor[]> {
  const data = await get<{ results: Sensor[] }>(`${BASE}/sensors/`)
  return data.results
}

export async function fetchLatest(sensorId: number): Promise<DataPoint | null> {
  const data = await get<{ results: DataPoint[] }>(
    `${BASE}/sensors/${sensorId}/data/?page_size=1`
  )
  return data.results[0] ?? null
}

export async function fetchHistory(
  sensorId: number,
  from: Date,
  to: Date
): Promise<DataPoint[]> {
  const params = new URLSearchParams({
    page_size: '1000',
    time__gt: from.toISOString(),
    time__lt: to.toISOString(),
  })
  const data = await get<{ results: DataPoint[] }>(
    `${BASE}/sensors/${sensorId}/data/?${params}`
  )
  // API returns newest-first; reverse for chronological chart display
  return data.results.slice().reverse()
}
