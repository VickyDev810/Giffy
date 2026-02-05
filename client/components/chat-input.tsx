"use client"

import { useState } from "react"

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled: boolean
}

export default function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input)
      setInput("")
    }
  }

  return (
    <div className="border-t border-border p-4 bg-card/50 backdrop-blur-sm">
      <div className="max-w-4xl mx-auto">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask for more gift ideas or refine your search..."
            disabled={disabled}
            className="flex-1 bg-input border border-border rounded-xl p-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50 smooth-transition"
          />
          <button
            onClick={handleSend}
            disabled={disabled || !input.trim()}
            className="px-6 py-3 bg-gradient-to-r from-secondary to-primary hover:from-secondary/90 hover:to-primary/90 disabled:from-muted disabled:to-muted text-secondary-foreground font-semibold rounded-xl smooth-transition hover-lift button-press glow-duo"
          >
            {disabled ? "✨" : "→"}
          </button>
        </div>
      </div>
    </div>
  )
}
