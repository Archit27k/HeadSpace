import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Brain, Sparkles } from 'lucide-react'
import { SignInButton, SignUpButton, Show, UserButton } from '@clerk/nextjs'

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-16 flex items-center border-b border-border/40 backdrop-blur-sm sticky top-0 z-50">
        <Link className="flex items-center justify-center gap-2" href="#">
          <div className="bg-primary/20 p-2 rounded-full">
            <Brain className="h-6 w-6 text-primary" />
          </div>
          <span className="font-bold text-xl tracking-tight">HeadSpace AI</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6 items-center">
          <Show when="signed-out">
            <SignInButton mode="modal">
              <Button variant="ghost" size="sm">Log in</Button>
            </SignInButton>
            <SignUpButton mode="modal">
              <Button size="sm" className="rounded-full">Get Started</Button>
            </SignUpButton>
          </Show>
          <Show when="signed-in">
            <UserButton />
          </Show>
        </nav>
      </header>
      <main className="flex-1">
        <section className="w-full py-24 md:py-32 lg:py-48 flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-background to-background z-[-1]" />
          <div className="container px-4 md:px-6 flex flex-col items-center text-center space-y-8">
            <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm text-primary mb-4">
              <Sparkles className="h-4 w-4 mr-2" />
              <span>Phase 1 Application Foundation</span>
            </div>
            <div className="space-y-4 max-w-3xl">
              <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
                Your Personal AI <br className="hidden sm:block" /> Mental Health Companion
              </h1>
              <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl leading-relaxed">
                A secure, private, and intelligent space to track your mood, journal your thoughts, and talk through your feelings with an empathetic AI.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <Show when="signed-out">
                <SignUpButton mode="modal">
                  <Button size="lg" className="rounded-full px-8 h-12 text-base shadow-lg shadow-primary/20">
                    Start Your Journey
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </SignUpButton>
              </Show>
              <Show when="signed-in">
                <Link href="/dashboard">
                  <Button size="lg" className="rounded-full px-8 h-12 text-base shadow-lg shadow-primary/20">
                    Go to Dashboard
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
              </Show>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
