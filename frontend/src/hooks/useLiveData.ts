import { useState, useEffect, useRef } from 'react'
import { fetchLatest, fetchHistory } from '../services/api'
import type { DataPoint, TimeRange } from '../types'

const POLL_INTERVAL = 5000

function rangeToWindow(range: TimeRange): number {
  const hours = { '1h': 1, '6h': 6, '24h': 24, '7d': 168 }
  return hours[range] * 60 * 60 * 1000
}

export function useLiveData(sensorId: number, timeRange: TimeRange) {
  const [latest, setLatest] = useState<DataPoint | null>(null)
  const [history, setHistory] = useState<DataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadHistory() {
      const to = new Date()
      const from = new Date(to.getTime() - rangeToWindow(timeRange))
      try {
        const data = await fetchHistory(sensorId, from, to)
        if (!cancelled) setHistory(data)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Failed to load history')
      }
    }

    async function pollLatest() {
      try {
        const data = await fetchLatest(sensorId)
        if (!cancelled) {
          setLatest(data)
          setError(null)
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : 'Connection lost')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    setLoading(true)
    pollLatest()
    loadHistory()

    timerRef.current = setInterval(pollLatest, POLL_INTERVAL)

    return () => {
      cancelled = true
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [sensorId, timeRange])

  return { latest, history, loading, error }
}
