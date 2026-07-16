'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@clerk/nextjs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Zap, LineChart } from 'lucide-react'

interface Trend {
  date: string
  score: number
  category: string
}

interface Insight {
  title: string
  description: string
  confidence: number
  insight_type: string
}

export default function AnalyticsPage() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)

  const { getToken } = useAuth()

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = await getToken()
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/analytics/dashboard`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (res.ok) {
          const data = await res.json()
          setTrends(data.trends || [])
          setInsights(data.insights || [])
        }
      } catch (error) {
        console.error('Failed to fetch analytics', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchAnalytics()
  }, [getToken])

  if (loading) return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading Analytics Engine...</div>

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Analytics & Insights</h1>
        <p className="text-muted-foreground">Explainable, evidence-based patterns from your wellness journey.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Insights Column */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Zap className="h-5 w-5 text-amber-500" /> Discovered Patterns
          </h2>
          {insights.map((insight, idx) => (
            <Card key={idx} className="bg-card/50 backdrop-blur-sm border-amber-500/20">
              <CardHeader>
                <CardTitle className="text-lg">{insight.title}</CardTitle>
                <CardDescription className="flex items-center gap-2">
                    <span className="bg-amber-500/10 text-amber-500 px-2 py-0.5 rounded text-xs">{insight.insight_type}</span>
                    <span>Confidence: {(insight.confidence * 100).toFixed(0)}%</span>
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{insight.description}</p>
                {/* Explainability Hook */}
                <button className="mt-4 text-xs text-primary underline hover:text-primary/80">
                    Why was this generated? (Explainability Engine)
                </button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Trends Column */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <LineChart className="h-5 w-5 text-blue-500" /> Recent Trends
          </h2>
          <Card className="bg-card/50 backdrop-blur-sm">
              <CardHeader>
                  <CardTitle className="text-lg">Stress Timeline</CardTitle>
                  <CardDescription>7-day moving average</CardDescription>
              </CardHeader>
              <CardContent>
                  <div className="h-48 flex items-end gap-2 mt-4">
                      {trends.slice(0, 7).map((t, i) => (
                          <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
                              <div className="w-full bg-blue-500/20 rounded-t-sm relative group-hover:bg-blue-500/40 transition-colors" style={{ height: `${(t.score / 10) * 100}%` }}>
                                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs opacity-0 group-hover:opacity-100 transition-opacity bg-background border rounded px-1">{t.score}</span>
                              </div>
                              <span className="text-[10px] text-muted-foreground truncate w-full text-center">{t.date.split('-').slice(1).join('/')}</span>
                          </div>
                      ))}
                  </div>
              </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
