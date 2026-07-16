"use client"

import { useState, useEffect } from "react"
import { useAuth } from "@clerk/nextjs"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { BrainCircuit, Book, Target, Heart, Loader2, Trash2 } from "lucide-react"

interface Memory {
  id: string;
  category?: string;
  content: string;
}

export default function MemoryPage() {
  const { getToken } = useAuth()
  const [memories, setMemories] = useState<Memory[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

  useEffect(() => {
    const fetchMemories = async () => {
      try {
        const token = await getToken()
        const res = await fetch(`${API_URL}/api/memory/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        if (res.ok) {
          const data = await res.json()
          setMemories(data)
        }
      } catch (e) {
        console.error(e)
      } finally {
        setIsLoading(false)
      }
    }
    fetchMemories()
  }, [getToken, API_URL])

  const handleDelete = async (id: string) => {
    try {
      const token = await getToken()
      const res = await fetch(`${API_URL}/api/memory/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (res.ok) {
        setMemories(memories.filter(m => m.id !== id))
      }
    } catch (e) {
      console.error("Failed to delete memory:", e)
    }
  }

  // Group memories by category
  const groupedMemories = memories.reduce((acc, curr) => {
    const cat = curr.category || "General"
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(curr)
    return acc
  }, {} as Record<string, Memory[]>)

  const getCategoryConfig = (category: string) => {
    if (category.toLowerCase().includes("goal") || category.toLowerCase().includes("aspiration")) {
      return { icon: Target, color: "text-green-500" }
    }
    if (category.toLowerCase().includes("preference") || category.toLowerCase().includes("trigger")) {
      return { icon: Heart, color: "text-rose-500" }
    }
    return { icon: Book, color: "text-blue-500" }
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">AI Memory</h1>
        <p className="text-muted-foreground flex items-center">
          <BrainCircuit className="mr-2 h-4 w-4" /> 
          What the AI has learned about you over time.
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center p-12">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      ) : memories.length === 0 ? (
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardContent className="flex justify-center p-12">
            <p className="text-muted-foreground">The AI hasn&apos;t learned any specific memories yet. Keep journaling and chatting!</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-3">
          {(Object.entries(groupedMemories) as [string, Memory[]][]).map(([category, items]) => {
            const config = getCategoryConfig(category)
            const Icon = config.icon
            return (
              <Card key={category} className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Icon className={`mr-2 h-5 w-5 ${config.color}`} />
                    {category}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-4">
                    {items.map((item, i) => (
                      <li key={item.id || i} className="flex items-start gap-2 text-sm text-muted-foreground group">
                        <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-border shrink-0" />
                        <span className="leading-relaxed flex-1">{item.content}</span>
                        <button 
                          onClick={() => handleDelete(item.id)}
                          className="opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:bg-destructive/10 p-1 rounded"
                          title="Delete Memory"
                        >
                          <Trash2 className="h-3 w-3" />
                        </button>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}

      <Card className="bg-primary/5 border-primary/20">
        <CardHeader>
          <CardTitle className="text-lg text-primary">Privacy & Control</CardTitle>
          <CardDescription>You are in control of your data.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">
            HeadSpace AI continuously learns from your conversations and journals to provide personalized recommendations. 
            All memories are encrypted and stored privately. You can edit or delete specific memories from this dashboard.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
