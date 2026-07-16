import Link from 'next/link'
import { UserButton } from '@clerk/nextjs'
import { Brain, LayoutDashboard, MessageSquare, BookOpen, Smile, LineChart, Settings } from 'lucide-react'

import { ModeToggle } from '@/components/mode-toggle'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const routes = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'AI Chat', path: '/dashboard/chat', icon: MessageSquare },
    { name: 'Journal', path: '/dashboard/journal', icon: BookOpen },
    { name: 'Mood Tracker', path: '/dashboard/mood', icon: Smile },
    { name: 'Recommendations', path: '/dashboard/recommendations', icon: Brain },
    { name: 'Memory', path: '/dashboard/memory', icon: Brain },
    { name: 'Analytics', path: '/dashboard/analytics', icon: LineChart },
    { name: 'Reports', path: '/dashboard/reports', icon: BookOpen },
    { name: 'Settings', path: '/dashboard/settings', icon: Settings },
  ]

  return (
    <div className="flex min-h-screen bg-zinc-950/50">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border/40 bg-background/50 backdrop-blur-xl flex flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-border/40 justify-between">
          <Link className="flex items-center gap-2 text-primary hover:opacity-80 transition-opacity" href="/dashboard">
            <Brain className="h-6 w-6" />
            <span className="font-bold text-lg tracking-tight text-foreground">HeadSpace AI</span>
          </Link>
          <ModeToggle />
        </div>
        <nav className="flex-1 py-6 px-4 space-y-1">
          {routes.map((route) => (
            <Link
              key={route.path}
              href={route.path}
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent/50 transition-all font-medium"
            >
              <route.icon className="h-5 w-5" />
              {route.name}
            </Link>
          ))}
        </nav>
        <div className="p-4 border-t border-border/40">
          <div className="flex items-center gap-3 px-3 py-2">
            <UserButton appearance={{ elements: { userButtonAvatarBox: "h-8 w-8" } }} />
            <div className="flex flex-col">
              <span className="text-sm font-medium">My Profile</span>
              <span className="text-xs text-muted-foreground">Manage account</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Mobile Header */}
        <header className="md:hidden h-16 border-b border-border/40 bg-background/50 backdrop-blur-xl flex items-center justify-between px-4">
          <Link className="flex items-center gap-2" href="/dashboard">
            <Brain className="h-6 w-6 text-primary" />
            <span className="font-bold">HeadSpace AI</span>
          </Link>
          <div className="flex items-center gap-2">
            <ModeToggle />
            <UserButton />
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-4 md:p-8">
          {children}
        </div>
      </main>
    </div>
  )
}
