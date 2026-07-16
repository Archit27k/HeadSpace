"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Loader2, Plus, PenSquare } from "lucide-react"
import { useAuth } from "@clerk/nextjs"

interface JournalEntry {
  id: string
  title: string
  content: string
  created_at: string
}

export default function JournalPage() {
  const { getToken } = useAuth()
  const [entries, setEntries] = useState<JournalEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  
  const [isWriting, setIsWriting] = useState(false)
  const [newTitle, setNewTitle] = useState("")
  const [newContent, setNewContent] = useState("")

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const token = await getToken()
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/journal/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        })
        if (!res.ok) throw new Error("Failed to fetch journal entries")
        const data = await res.json()
        setEntries(data)
      } catch (error) {
        console.error(error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchEntries()
  }, [getToken])

  const saveEntry = async () => {
    if (!newTitle.trim() || !newContent.trim()) return
    setIsSaving(true)
    try {
      const token = await getToken()
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/journal/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title: newTitle, content: newContent }),
      })
      if (!res.ok) throw new Error("Failed to save entry")
      const newEntry = await res.json()
      setEntries([newEntry, ...entries])
      setIsWriting(false)
      setNewTitle("")
      setNewContent("")
    } catch (error) {
      console.error(error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-10">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">My Journal</h1>
          <p className="text-muted-foreground">A safe space for your thoughts.</p>
        </div>
        {!isWriting && (
          <Button onClick={() => setIsWriting(true)}>
            <Plus className="mr-2 h-4 w-4" /> New Entry
          </Button>
        )}
      </div>

      {isWriting && (
        <Card className="bg-card/50 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle>Write a new entry</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input 
              placeholder="Title" 
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              className="font-semibold text-lg"
            />
            <Textarea 
              placeholder="How are you feeling today?" 
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
              className="min-h-[200px] resize-none"
            />
            <div className="flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setIsWriting(false)}>Cancel</Button>
              <Button onClick={saveEntry} disabled={isSaving || !newTitle.trim() || !newContent.trim()}>
                {isSaving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <PenSquare className="mr-2 h-4 w-4" />}
                Save Entry
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {isLoading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      ) : entries.length === 0 && !isWriting ? (
        <div className="text-center py-24 bg-card/50 rounded-xl border border-dashed border-border">
          <h3 className="text-lg font-semibold mb-2">No entries yet</h3>
          <p className="text-muted-foreground mb-4">Start journaling to track your thoughts and get personalized insights.</p>
          <Button onClick={() => setIsWriting(true)}>Write your first entry</Button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {entries.map(entry => (
            <Card key={entry.id} className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/50 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-xl line-clamp-1">{entry.title}</CardTitle>
                <CardDescription>{new Date(entry.created_at).toLocaleDateString()}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground line-clamp-4">{entry.content}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
