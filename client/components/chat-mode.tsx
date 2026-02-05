"use client"

interface ChatModeProps {
  name: string
  emoji: string
  description: string
  isActive: boolean
  onClick: () => void
}

export default function ChatMode({ name, emoji, description, isActive, onClick }: ChatModeProps) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-3 rounded-lg smooth-transition hover-lift button-press ${
        isActive
          ? "bg-primary text-primary-foreground glow-purple scale-105"
          : "bg-input border border-border hover:border-primary"
      }`}
    >
      <div className="text-xl mb-1">{emoji}</div>
      <div className="text-sm font-semibold">{name}</div>
      <div className="text-xs opacity-75">{description}</div>
    </button>
  )
}
