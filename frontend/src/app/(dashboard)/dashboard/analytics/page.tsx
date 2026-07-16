"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Loader2, TrendingUp, TrendingDown, Activity, Heart, Brain, Calendar } from "lucide-react"
import { useAuth } from "@clerk/nextjs"

export default function AnalyticsPage() {
  const { getToken } = useAuth()
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [data, setData] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = await getToken()
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/analytics/dashboard`, {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        })
        if (!res.ok) throw new Error("Failed to fetch analytics")
        const result = await res.json()
        setData(result)
      } catch (error) {
        console.error(error)
        setData({
          average_mood: null,
          total_entries: null,
          active_days: null,
          insights: [],
          trends: null
        })
      } finally {
        setIsLoading(false)
      }
    }
    fetchAnalytics()
  }, [getToken])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-[calc(100vh-8rem)]">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Analytics</h1>
        <p className="text-muted-foreground">Insights and trends based on your activity.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Average Mood</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.average_mood || "N/A"}/10</div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center">
              {data?.trends?.mood_trend === 'up' ? (
                <><TrendingUp className="h-3 w-3 text-green-500 mr-1" /> Trending up</>
              ) : data?.trends?.mood_trend === 'down' ? (
                <><TrendingDown className="h-3 w-3 text-red-500 mr-1" /> Trending down</>
              ) : (
                <><Activity className="h-3 w-3 text-yellow-500 mr-1" /> Stable</>
              )}
            </p>
          </CardContent>
        </Card>
        
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Entries</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.total_entries || 0}</div>
            <p className="text-xs text-muted-foreground mt-1">Journal & Mood logs</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Days</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data?.active_days || 0}</div>
            <p className="text-xs text-muted-foreground mt-1">Days this month</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Engagement</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">{data?.trends?.engagement_trend || "N/A"}</div>
            <p className="text-xs text-muted-foreground mt-1">Compared to last week</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="bg-card/50 backdrop-blur-sm border-border/50 col-span-2">
          <CardHeader>
            <CardTitle>Key Insights</CardTitle>
            <CardDescription>What the AI has learned about you recently</CardDescription>
          </CardHeader>
          <CardContent>
            {data?.insights?.length > 0 ? (
              <ul className="space-y-4">
                {data.insights.map((insight: string, i: number) => (
                  <li key={i} className="flex items-start gap-3">
                    <div className="h-6 w-6 rounded-full bg-primary/20 flex items-center justify-center shrink-0 mt-0.5">
                      <Brain className="h-3 w-3 text-primary" />
                    </div>
                    <span className="text-muted-foreground">{insight}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                Not enough data yet. Keep using the app to generate insights!
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
