"use client"

import { useState, useEffect, useCallback } from "react"
import { useAuth } from "@clerk/nextjs"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Sparkles, Loader2, ArrowRight, ShieldAlert, Activity } from "lucide-react"

interface Recommendation {
  title: string;
  type: string;
  expected_impact: string;
  description: string;
  action_steps?: string[];
}

interface RecommendationData {
  priority: string;
  reasoning: string;
  recommendations: Recommendation[];
}

export default function RecommendationsPage() {
  const { getToken } = useAuth()
  const [data, setData] = useState<RecommendationData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

  const fetchRecommendations = useCallback(async () => {
    try {
      const token = await getToken()
      const res = await fetch(`${API_URL}/api/recommendations/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (res.ok) {
        const json = await res.json()
        setData(json)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }, [getToken, API_URL])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchRecommendations()
  }, [fetchRecommendations])

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Recommendations</h1>
        <p className="text-muted-foreground flex items-center">
          <Sparkles className="mr-2 h-4 w-4" /> 
          AI-generated personalized action plans for your wellness.
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center p-12">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      ) : !data || data.recommendations.length === 0 ? (
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardContent className="flex justify-center p-12 text-center flex-col items-center">
            <Activity className="h-10 w-10 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No recommendations available yet. Log some moods or journal entries to get started!</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          <Card className="bg-primary/5 border-primary/20">
            <CardHeader>
              <CardTitle className="text-lg text-primary flex items-center">
                <ShieldAlert className="mr-2 h-5 w-5" /> 
                Priority: {data.priority}
              </CardTitle>
              <CardDescription>{data.reasoning}</CardDescription>
            </CardHeader>
          </Card>

          <div className="grid gap-6">
            {data.recommendations.map((rec: Recommendation, idx: number) => (
              <Card key={idx} className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="text-xl">{rec.title}</CardTitle>
                  <CardDescription className="capitalize">Type: {rec.type} • Expected Impact: {rec.expected_impact}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{rec.description}</p>
                  
                  {rec.action_steps && rec.action_steps.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-sm">Action Steps:</h4>
                      <ul className="space-y-2">
                        {rec.action_steps.map((step: string, i: number) => (
                          <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                            <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-primary shrink-0" />
                            <span className="leading-relaxed">{step}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">
                    Start this activity <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
