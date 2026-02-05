"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, ScrollText, MessageCircleHeart, Users, Settings2, X, Sparkles, ArrowRight, Gift, Sun, Moon, ShoppingBag, ExternalLink, ThumbsUp } from "lucide-react"
import { Slider } from "@/components/ui/slider"
import EmotionSlider from "@/components/emotion-slider"
import TargetGroupSelect from "@/components/target-group-select"
import { useTheme } from "next-themes"

interface ChatInterfaceProps {
  friendData: any
  onBack: () => void
}

type Mode = "curator" | "partner" | "council"
type Theme = "light" | "dark"

const MODES = [
  {
    id: "curator",
    label: "The Curator",
    desc: "Data-driven top picks.",
    icon: ScrollText,
    color: "text-emerald-500",
    bg: "bg-emerald-500/10",
  },
  {
    id: "partner",
    label: "The Partner",
    desc: "Collaborative brainstorming.",
    icon: MessageCircleHeart,
    color: "text-rose-500",
    bg: "bg-rose-500/10",
  },
  {
    id: "council",
    label: "The Council",
    desc: "A team of experts.",
    icon: Users,
    color: "text-purple-500",
    bg: "bg-purple-500/10",
  },
] as const

interface Product {
  id: string
  name: string
  price: string
  category: string
  reason: string
}

export default function ChatInterface({ friendData, onBack }: ChatInterfaceProps) {
  const [mode, setMode] = useState<Mode>("partner")
  const [hasSelectedMode, setHasSelectedMode] = useState(false)
  const { setTheme, theme } = useTheme()

  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<any[]>([])
  const [isTyping, setIsTyping] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  // Mission Control State
  const [budget, setBudget] = useState(100)
  const [vibe, setVibe] = useState(50)
  const [target, setTarget] = useState("friend")

  const scrollRef = useRef<HTMLDivElement>(null)

  // Initial Greeting
  useEffect(() => {
    if (!hasSelectedMode) return

    const handle = friendData?.friendName || friendData?.initialHandle || "your friend"
    let greetingContent = ""
    let products: Product[] = []
    let agentName = "AI"

    if (mode === 'curator') {
      greetingContent = `I've analyzed ${handle}'s profile. Based on a $${budget} budget, these items have the highest compatibility score:`
      products = [
        { id: "1", name: "Keychron K2 Wireless", price: "$79.00", category: "Tech", reason: "Matches 'setup' interest" },
        { id: "2", name: "Analog Wood Stand", price: "$45.00", category: "Decor", reason: "Aesthetic match" },
      ]
    } else if (mode === 'partner') {
      greetingContent = `Hey! I looked through ${handle}'s posts. They have such a specific clean vibe! \n\nI found a couple of things that fit the $${budget} budget perfectly. What do you think of these?`
      products = [
        { id: "3", name: "Neon Desk Light", price: "$32.00", category: "Vibe", reason: "Adds personality" },
        { id: "4", name: "Custom Keycap", price: "$25.00", category: "Gaming", reason: "Highly personal" },
      ]
    } else {
      greetingContent = `The team has convened. \n\n@TrendHunter suggests something viral, while @Pragmatist wants utility. We've shortlisted these two candidates for ${handle}:`
      products = [
        { id: "5", name: "Field Notes Ltd Ed.", price: "$14.95", category: "Utility", reason: "Practical & Collectible" },
        { id: "6", name: "Retro Calm Lamp", price: "$65.00", category: "Home", reason: "Trending on Pinterest" },
      ]
    }

    setMessages([{
      id: 0,
      role: "assistant",
      content: greetingContent,
      products: products,
      agent: agentName
    }])

  }, [hasSelectedMode, mode, friendData, budget])

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const userMsg = { id: Date.now(), role: "user", content: input }
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setIsTyping(true)

    // Simulate response delay
    setTimeout(() => {
      let responseContent = ""
      let products: Product[] = []

      if (mode === "curator") {
        responseContent = `Understood. Refining based on "${input}".\n\nAdding these alternatives to your selection:`
        products = [{ id: "7", name: "Smart Coffee Warmer", price: "$35.00", category: "Utility", reason: "Keywords match" }]
      } else if (mode === "partner") {
        responseContent = `Ooh, good call! If they like ${input}, they will absolutely LOVE this:`
        products = [{ id: "8", name: "Limited Artisan Cap", price: "$120.00", category: "Collectibles", reason: "Premium pick" }]
      } else {
        responseContent = `Argument noted. @BudgetBot is worried about the price, but @VibeCheck says "Do it".\n\nCheck this out:`
        products = [{ id: "9", name: "Sony XM4 (Refurb)", price: "$180.00", category: "Audio", reason: "Best value" }]
      }

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: "assistant",
        content: responseContent,
        products: products,
        agent: "AI"
      }])
      setIsTyping(false)
    }, 1500)
  }

  // --- RENDERING HELPERS ---

  const ProductCard = ({ product }: { product: Product }) => (
    <div className="flex flex-col p-4 rounded-xl border border-border shadow-sm transition-all hover:shadow-md bg-card text-card-foreground">
      <div className="h-32 rounded-lg mb-3 flex items-center justify-center bg-muted/50">
        <ShoppingBag className="opacity-20" size={32} />
      </div>
      <div className="flex justify-between items-start mb-1">
        <h4 className="font-bold text-sm line-clamp-1">{product.name}</h4>
        <span className="font-mono text-xs font-semibold opacity-70">{product.price}</span>
      </div>
      <div className="text-xs opacity-60 mb-4 line-clamp-1">{product.reason}</div>
      <button className="w-full py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition-colors bg-primary text-primary-foreground hover:bg-primary/90">
        View Deal <ExternalLink size={10} />
      </button>
    </div>
  )

  // 1. Mode Selection Screen
  if (!hasSelectedMode) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden transition-colors duration-500 bg-background text-foreground">
        {/* Toggle in corner */}
        <div className="absolute top-4 right-4 z-20">
          <button
            onClick={() => setTheme(prev => prev === 'light' ? 'dark' : 'light')}
            className="p-2 rounded-full border border-border bg-background hover:bg-muted transition-colors"
          >
            {theme === 'light' ? <Sun size={20} className="text-amber-500" /> : <Moon size={20} className="text-blue-400" />}
          </button>
        </div>

        <div className="max-w-4xl w-full space-y-12 relative z-10">
          <div className="text-center space-y-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center justify-center p-4 rounded-2xl mb-4 shadow-xl bg-card text-primary"
            >
              <Gift size={40} />
            </motion.div>
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-4xl md:text-6xl font-black tracking-tight"
            >
              Who's shopping?
            </motion.h1>
            <p className="text-lg opacity-60 max-w-lg mx-auto">
              Select your AI assistant style.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {MODES.map((m, i) => (
              <motion.button
                key={m.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + (i * 0.1) }}
                whileHover={{ y: -8 }}
                onClick={() => {
                  setMode(m.id as Mode)
                  setHasSelectedMode(true)
                }}
                className={`flex flex-col items-center text-center p-6 rounded-3xl border border-border bg-card hover:bg-muted/50 transition-all hover:shadow-2xl group`}
              >
                <div className={`p-4 rounded-2xl mb-6 transition-transform group-hover:scale-110 ${m.bg} ${m.color}`}>
                  <m.icon size={32} />
                </div>
                <h3 className="text-xl font-bold mb-2">{m.label}</h3>
                <p className="text-sm opacity-60 leading-relaxed mb-6">
                  {m.desc}
                </p>
              </motion.button>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // 2. Main Chat Interface
  return (
    <div className="min-h-screen flex flex-col font-sans transition-colors duration-500 overflow-hidden relative bg-background text-foreground">

      {/* Settings Panel */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="absolute inset-y-0 right-0 w-full sm:w-96 z-50 shadow-2xl overflow-y-auto border-l border-border bg-background/95 backdrop-blur-xl"
          >
            <div className="p-6 space-y-8">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold flex items-center gap-2">
                  <Settings2 /> Parameters
                </h2>
                <button onClick={() => setShowSettings(false)} className="hover:rotate-90 transition-transform">
                  <X />
                </button>
              </div>

              <div className="space-y-4">
                <label className="text-xs font-bold opacity-70">Budget</label>
                <div className="flex items-center gap-4">
                  <span className="text-2xl font-mono">${budget}</span>
                  <Slider
                    value={[budget]}
                    onValueChange={(v) => setBudget(v[0])}
                    min={10} max={1000} step={10}
                    className="flex-1"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <EmotionSlider value={vibe} onChange={setVibe} />
              </div>

              <div className="space-y-4">
                <TargetGroupSelect value={target} onChange={setTarget} />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="px-4 py-3 border-b border-border flex justify-between items-center backdrop-blur-md sticky top-0 z-20 bg-background/80">
        <div className="flex items-center gap-4">
          <button onClick={() => setHasSelectedMode(false)} className="text-xs font-bold hover:underline opacity-60 hover:opacity-100 flex items-center gap-1">
            ← MODES
          </button>

          <div className="h-4 w-px bg-border" />

          <div className="flex items-center gap-2 text-sm font-bold">
            {mode === 'curator' && <><ScrollText size={16} className="text-emerald-500" /> The Curator</>}
            {mode === 'partner' && <><MessageCircleHeart size={16} className="text-rose-500" /> The Partner</>}
            {mode === 'council' && <><Users size={16} className="text-purple-500" /> The Council</>}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setTheme(prev => prev === 'light' ? 'dark' : 'light')}
            className="p-1.5 rounded-full border border-border bg-background hover:bg-muted transition-colors"
          >
            {theme === 'light' ? <Sun size={14} className="text-amber-500" /> : <Moon size={14} className="text-blue-400" />}
          </button>
          <button
            onClick={() => setShowSettings(true)}
            className="flex items-center gap-2 text-xs font-bold border border-border px-3 py-1.5 rounded-full transition-colors bg-background hover:bg-muted"
          >
            <Settings2 size={14} />
            <span className="hidden sm:inline">FILTERS</span>
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-20 space-y-8">
        <AnimatePresence initial={false}>
          {messages.map((msg, i) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex flex-col w-full gap-2 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              {/* Text Bubble */}
              <div className={`max-w-[85%] sm:max-w-[70%] text-sm sm:text-base leading-relaxed p-4 rounded-2xl shadow-sm border
                 ${msg.role === 'user'
                  ? 'bg-primary text-primary-foreground border-primary rounded-br-none'
                  : 'bg-card text-card-foreground border-border rounded-bl-none'
                }
               `}>
                {msg.role === 'assistant' && (
                  <div className="mb-2 flex items-center gap-2 opacity-50 text-xs font-bold uppercase tracking-wider">
                    {mode === 'council' ? <Users size={12} /> : <Sparkles size={12} />}
                    {msg.agent}
                  </div>
                )}
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>

              {/* Product Cards (if any) */}
              {msg.products && msg.products.length > 0 && (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 w-full sm:max-w-[80%] mt-2">
                  {msg.products.map((p: Product) => (
                    <ProductCard key={p.id} product={p} />
                  ))}
                </div>
              )}
            </motion.div>
          ))}

          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-2 items-center text-xs opacity-50 ml-4 h-8 font-bold"
            >
              <span className="w-2 h-2 bg-current rounded-full animate-bounce" />
              <span className="w-2 h-2 bg-current rounded-full animate-bounce delay-100" />
              <span className="w-2 h-2 bg-current rounded-full animate-bounce delay-200" />
            </motion.div>
          )}
          <div ref={scrollRef} />
        </AnimatePresence>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border bg-background">
        <div className="max-w-3xl mx-auto flex gap-3 p-2 rounded-2xl border border-border bg-muted/20 focus-within:ring-2 focus-within:ring-primary/20 transition-all">
          <button className="p-2 rounded-xl transition-colors hover:bg-muted text-muted-foreground">
            <Gift size={20} />
          </button>

          <input
            className="flex-1 bg-transparent border-none focus:ring-0 text-base px-2 py-2 text-foreground placeholder:text-muted-foreground"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            autoFocus
          />
          <button
            onClick={handleSend}
            className="p-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
