"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Loader2, Calendar as CalendarIcon, Lightbulb, CheckCircle2 } from "lucide-react"
import { useAuth } from "@clerk/nextjs"

interface Report {
  summary: string;
  insights: string[];
  areas_of_focus: string[];
  period: string;
}

export default function ReportsPage() {
  const { getToken } = useAuth()
  const [report, setReport] = useState<Report | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const token = await getToken()
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/analytics/reports/weekly`, {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        })
        if (!res.ok) throw new Error("Failed to fetch weekly report")
        const data = await res.json()
        setReport(data)
      } catch (error) {
        console.error(error)
        setReport({
          summary: "No summary available for this week.",
          insights: [],
          areas_of_focus: [],
          period: "This Week"
        })
      } finally {
        setIsLoading(false)
      }
    }
    fetchReport()
  }, [getToken])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-[calc(100vh-8rem)]">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Weekly Report</h1>
        <p className="text-muted-foreground flex items-center">
          <CalendarIcon className="mr-2 h-4 w-4" /> {report?.period || "This Week"}
        </p>
      </div>

      <Card className="bg-card/50 backdrop-blur-sm border-border/50">
        <CardHeader>
          <CardTitle>Executive Summary</CardTitle>
          <CardDescription>An overview of your mental health journey this week.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-foreground leading-relaxed">
            {report?.summary || "No summary available for this week."}
          </p>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="mr-2 h-5 w-5 text-amber-500" /> 
              Key Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            {report?.insights?.length > 0 ? (
              <ul className="space-y-3">
                {report.insights.map((insight: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-muted-foreground">
                    <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-amber-500 shrink-0" />
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted-foreground">Not enough data to generate insights.</p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircle2 className="mr-2 h-5 w-5 text-green-500" /> 
              Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            {report?.areas_of_focus?.length > 0 ? (
              <ul className="space-y-3">
                {report.areas_of_focus.map((rec: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-muted-foreground">
                    <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-green-500 shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted-foreground">No specific recommendations at this time.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
