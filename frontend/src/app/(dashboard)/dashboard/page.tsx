import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MessageSquare, BookOpen, Smile, LineChart, BrainCircuit, Activity } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const cards = [
    {
      title: "AI Chat",
      description: "Talk through your feelings with your empathetic companion.",
      icon: MessageSquare,
      href: "/dashboard/chat",
      color: "text-blue-500",
      bg: "bg-blue-500/10"
    },
    {
      title: "Journal",
      description: "Write down your thoughts securely and privately.",
      icon: BookOpen,
      href: "/dashboard/journal",
      color: "text-purple-500",
      bg: "bg-purple-500/10"
    },
    {
      title: "Mood Tracker",
      description: "Log how you are feeling to track trends over time.",
      icon: Smile,
      href: "/dashboard/mood",
      color: "text-green-500",
      bg: "bg-green-500/10"
    },
    {
      title: "Analytics",
      description: "Understand your mental health with detailed insights.",
      icon: LineChart,
      href: "/dashboard/analytics",
      color: "text-orange-500",
      bg: "bg-orange-500/10"
    },
    {
      title: "Memory",
      description: "Review what the AI has learned about you.",
      icon: BrainCircuit,
      href: "/dashboard/memory",
      color: "text-indigo-500",
      bg: "bg-indigo-500/10"
    },
    {
      title: "Weekly Report",
      description: "Your personalized weekly mental health summary.",
      icon: Activity,
      href: "/dashboard/reports",
      color: "text-rose-500",
      bg: "bg-rose-500/10"
    }
  ]

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Welcome Back</h1>
        <p className="text-muted-foreground">Here is an overview of your mental health journey today.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {cards.map((card) => (
          <Link href={card.href} key={card.title} className="group">
            <Card className="h-full bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/50 transition-all hover:shadow-md hover:shadow-primary/5">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-xl ${card.bg}`}>
                    <card.icon className={`h-6 w-6 ${card.color}`} />
                  </div>
                  <CardTitle className="text-xl group-hover:text-primary transition-colors">{card.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm text-muted-foreground/80 leading-relaxed">
                  {card.description}
                </CardDescription>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
