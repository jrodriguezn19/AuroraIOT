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

const CHUNKS_PER_RANGE = 10
const POINTS_PER_CHUNK = 100 // 10 chunks × 100 = 1000 total points

export async function fetchHistory(
  sensorId: number,
  from: Date,
  to: Date
): Promise<DataPoint[]> {
  const totalMs = to.getTime() - from.getTime()
  const chunkMs = totalMs / CHUNKS_PER_RANGE

  const chunks = await Promise.all(
    Array.from({ length: CHUNKS_PER_RANGE }, async (_, i) => {
      const chunkFrom = new Date(from.getTime() + i * chunkMs)
      const chunkTo = new Date(from.getTime() + (i + 1) * chunkMs)
      const params = new URLSearchParams({
        page_size: String(POINTS_PER_CHUNK),
        time__gt: chunkFrom.toISOString(),
        time__lt: chunkTo.toISOString(),
      })
      const d = await get<{ results: DataPoint[] }>(
        `${BASE}/sensors/${sensorId}/data/?${params}`
      )
      return d.results.slice().reverse()
    })
  )

  return chunks.flat()
}
