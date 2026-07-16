"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Bot, User, Loader2, Paperclip } from "lucide-react"
import { useAuth } from "@clerk/nextjs"

interface Message {
  id: string
  content: string
  sender_type: "USER" | "AI"
  created_at: string
}

export default function ChatPage() {
  const { getToken } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const initializeConversation = async () => {
    try {
      const token = await getToken()
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat/conversations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ summary: "New Chat" }),
      })
      if (!res.ok) throw new Error("Failed to initialize conversation")
      const data = await res.json()
      setConversationId(data.id)
      return data.id
    } catch (error) {
      console.error(error)
      return null
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      const token = await getToken()
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/documents/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      })
      if (res.ok) {
        // Just add a quick success message locally to the chat UI
        setMessages(prev => [...prev, {
          id: Date.now().toString(),
          content: `Document uploaded and processed: ${file.name}`,
          sender_type: "AI",
          created_at: new Date().toISOString()
        }])
      } else {
        throw new Error("Upload failed")
      }
    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: `Error uploading document: ${file.name}`,
        sender_type: "AI",
        created_at: new Date().toISOString()
      }])
    } finally {
      setIsUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ""
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const messageText = inputValue.trim()
    setInputValue("")
    
    // Optimistically add user message
    const tempUserMsg: Message = {
      id: Date.now().toString(),
      content: messageText,
      sender_type: "USER",
      created_at: new Date().toISOString()
    }
    
    setMessages((prev) => [...prev, tempUserMsg])
    setIsLoading(true)

    try {
      let currentConvId = conversationId
      if (!currentConvId) {
        currentConvId = await initializeConversation()
      }

      if (!currentConvId) throw new Error("No conversation ID")

      const token = await getToken()
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat/conversations/${currentConvId}/messages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content: messageText, role: "user" }),
      })
      
      if (!res.ok || !res.body) throw new Error("Failed to send message")
      
      const aiMsgId = Date.now().toString() + "-ai"
      setMessages((prev) => [...prev, {
        id: aiMsgId,
        content: "",
        sender_type: "AI",
        created_at: new Date().toISOString()
      }])
      setIsLoading(false)

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let aiContent = ""
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '').trim()
            if (dataStr === '[DONE]') break
            
            try {
              const data = JSON.parse(dataStr)
              if (data.content) {
                aiContent += data.content
                setMessages((prev) => 
                  prev.map(m => m.id === aiMsgId ? { ...m, content: aiContent } : m)
                )
              }
            } catch {
              // Ignore partial JSON parse errors
            }
          }
        }
      }
      
    } catch (error) {
      console.error(error)
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">AI Companion</h1>
        <p className="text-muted-foreground">Chat with your empathetic AI assistant.</p>
      </div>

      <Card className="flex-1 flex flex-col bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-muted-foreground space-y-4 opacity-50">
              <Bot className="h-12 w-12" />
              <p>Send a message to start chatting</p>
            </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={msg.id || i} className={`flex ${msg.sender_type === "USER" ? "justify-end" : "justify-start"}`}>
              <div className={`flex gap-3 max-w-[80%] ${msg.sender_type === "USER" ? "flex-row-reverse" : "flex-row"}`}>
                <div className={`h-8 w-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender_type === "USER" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                  {msg.sender_type === "USER" ? <User className="h-5 w-5" /> : <Bot className="h-5 w-5" />}
                </div>
                <div className={`rounded-2xl px-4 py-2 ${msg.sender_type === "USER" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex gap-3 max-w-[80%] flex-row">
                <div className="h-8 w-8 rounded-full flex items-center justify-center shrink-0 bg-muted">
                  <Bot className="h-5 w-5" />
                </div>
                <div className="rounded-2xl px-4 py-2 bg-muted flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                  <p className="text-sm text-muted-foreground">Thinking...</p>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-border/50 bg-background/50">
          <form onSubmit={sendMessage} className="flex gap-2">
            <input 
              type="file" 
              accept=".pdf" 
              className="hidden" 
              ref={fileInputRef}
              onChange={handleFileUpload}
            />
            <Button 
              type="button" 
              variant="outline" 
              size="icon" 
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading || isUploading}
            >
              {isUploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Paperclip className="h-4 w-4" />}
            </Button>
            <Input 
              value={inputValue} 
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..." 
              className="flex-1 bg-background"
              disabled={isLoading || isUploading}
            />
            <Button type="submit" size="icon" disabled={!inputValue.trim() || isLoading || isUploading}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  )
}
