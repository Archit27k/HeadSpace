import { UserProfile } from '@clerk/nextjs'

export default function ProfilePage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Profile & Settings</h1>
        <p className="text-muted-foreground">Manage your account and preferences.</p>
      </div>

      <div className="bg-card border border-border/40 rounded-xl overflow-hidden p-6 shadow-sm">
        <UserProfile routing="hash" />
      </div>
    </div>
  )
}
