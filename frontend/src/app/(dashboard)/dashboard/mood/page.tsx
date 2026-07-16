"use client"

import { useState, useEffect, useCallback } from "react"
import { useAuth } from "@clerk/nextjs"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Smile, Frown, Meh, Loader2 } from "lucide-react"

interface Mood {
  id: string;
  primary_emotion: string;
  created_at: string;
}

export default function MoodPage() {
  const { getToken } = useAuth()
  const [selectedMood, setSelectedMood] = useState<string | null>(null)
  const [isSaving, setIsSaving] = useState(false)
  const [isSaved, setIsSaved] = useState(false)
  const [pastMoods, setPastMoods] = useState<Mood[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

  const fetchMoods = useCallback(async () => {
    try {
      const token = await getToken()
      const res = await fetch(`${API_URL}/api/mood/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (res.ok) {
        const data = await res.json()
        setPastMoods(data)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }, [getToken, API_URL])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchMoods()
  }, [fetchMoods])

  const handleMoodSelect = (mood: string) => {
    setSelectedMood(mood)
  }

  const handleSave = async () => {
    if (!selectedMood) return
    setIsSaving(true)
    
    let score = 5
    if (selectedMood === "Bad") score = 2
    if (selectedMood === "Good") score = 8

    try {
      const token = await getToken()
      const res = await fetch(`${API_URL}/api/mood/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          score,
          primary_emotion: selectedMood,
          notes: `User logged ${selectedMood} mood via dashboard UI.`
        })
      })

      if (res.ok) {
        setIsSaved(true)
        setSelectedMood(null)
        fetchMoods()
        setTimeout(() => setIsSaved(false), 3000)
      }
    } catch (error) {
      console.error("Failed to save mood:", error)
    } finally {
      setIsSaving(false)
    }
  }

  const getMoodIcon = (category: string) => {
    if (category === "Bad") return { icon: Frown, color: "text-red-500" }
    if (category === "Good") return { icon: Smile, color: "text-green-500" }
    return { icon: Meh, color: "text-yellow-500" }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Mood Tracker</h1>
        <p className="text-muted-foreground">Log your daily emotions to build self-awareness.</p>
      </div>

      <Card className="bg-card/50 backdrop-blur-sm border-border/50">
        <CardHeader>
          <CardTitle>How are you feeling right now?</CardTitle>
          <CardDescription>Select the emotion that best matches your current state.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex justify-center gap-4 py-4">
            <Button
              variant="outline"
              className={`h-24 w-24 flex-col gap-2 ${selectedMood === "Bad" ? "border-red-500 bg-red-500/10" : ""}`}
              onClick={() => handleMoodSelect("Bad")}
            >
              <Frown className={`h-10 w-10 ${selectedMood === "Bad" ? "text-red-500" : "text-muted-foreground"}`} />
              <span className={selectedMood === "Bad" ? "text-red-500" : ""}>Bad</span>
            </Button>
            
            <Button
              variant="outline"
              className={`h-24 w-24 flex-col gap-2 ${selectedMood === "Okay" ? "border-yellow-500 bg-yellow-500/10" : ""}`}
              onClick={() => handleMoodSelect("Okay")}
            >
              <Meh className={`h-10 w-10 ${selectedMood === "Okay" ? "text-yellow-500" : "text-muted-foreground"}`} />
              <span className={selectedMood === "Okay" ? "text-yellow-500" : ""}>Okay</span>
            </Button>
            
            <Button
              variant="outline"
              className={`h-24 w-24 flex-col gap-2 ${selectedMood === "Good" ? "border-green-500 bg-green-500/10" : ""}`}
              onClick={() => handleMoodSelect("Good")}
            >
              <Smile className={`h-10 w-10 ${selectedMood === "Good" ? "text-green-500" : "text-muted-foreground"}`} />
              <span className={selectedMood === "Good" ? "text-green-500" : ""}>Good</span>
            </Button>
          </div>
          
          <div className="flex justify-center">
            <Button 
              size="lg" 
              onClick={handleSave} 
              disabled={!selectedMood || isSaving || isSaved}
              className="w-full max-w-xs"
            >
              {isSaving ? (
                <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Saving...</>
              ) : isSaved ? (
                "Saved!"
              ) : (
                "Log Mood"
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-card/50 backdrop-blur-sm border-border/50">
        <CardHeader>
          <CardTitle>Recent History</CardTitle>
          <CardDescription>Your mood timeline</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center p-4"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>
          ) : pastMoods.length === 0 ? (
            <p className="text-muted-foreground text-center p-4">No moods logged yet.</p>
          ) : (
            <div className="space-y-4">
              {pastMoods.map((log: Mood) => {
                const { icon: Icon, color } = getMoodIcon(log.primary_emotion)
                return (
                  <div key={log.id} className="flex items-center justify-between p-3 rounded-lg bg-background border border-border/50">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-full bg-muted`}>
                        <Icon className={`h-5 w-5 ${color}`} />
                      </div>
                      <span className="font-medium">{log.primary_emotion}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      {new Date(log.created_at).toLocaleDateString()}
                    </span>
                  </div>
                )
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
