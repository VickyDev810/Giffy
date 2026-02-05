interface Message {
  role: "user" | "assistant"
  content: string
  mode?: string
}

interface MessageListProps {
  messages: Message[]
  friendData: any
}

export default function MessageList({ messages, friendData }: MessageListProps) {
  return (
    <div className="space-y-4">
      {messages.map((msg, idx) => (
        <div key={idx} className={`fade-in-up ${msg.role === "user" ? "flex justify-end" : "flex justify-start"}`}>
          <div
            className={`max-w-2xl rounded-xl p-4 smooth-transition ${
              msg.role === "user"
                ? "bg-gradient-to-r from-primary to-secondary text-primary-foreground rounded-br-none glow-purple"
                : msg.mode === "system"
                  ? "bg-card border border-border text-foreground rounded-bl-none pulse-glow"
                  : "bg-card border border-border/50 text-foreground rounded-bl-none glow-cyan"
            }`}
          >
            {msg.role === "assistant" && msg.mode !== "system" && (
              <div className="text-xs font-semibold text-secondary mb-2">✨ Giffy Intelligence</div>
            )}
            <p className="text-sm leading-relaxed">{msg.content}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
