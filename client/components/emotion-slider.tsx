"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Heart, Sparkles, Gem } from "lucide-react"

interface EmotionSliderProps {
  value: number // 0 to 100
  onChange: (value: number) => void
}

export default function EmotionSlider({ value, onChange }: EmotionSliderProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
    onChange(Math.round(percent * 100))
  }

  // Determine active icon based on value
  const getActiveIcon = () => {
    if (value < 33) return <Heart className="w-6 h-6 text-rose-400 fill-rose-400/20" />
    if (value < 66) return <Sparkles className="w-6 h-6 text-purple-400 fill-purple-400/20" />
    return <Gem className="w-6 h-6 text-cyan-400 fill-cyan-400/20" />
  }

  // Dynamic gradient based on value
  const getGradient = () => {
    if (value < 33) return "from-rose-500/20 to-rose-500/20"
    if (value < 66) return "from-purple-500/20 to-purple-500/20"
    return "from-cyan-500/20 to-cyan-500/20"
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-foreground/90 flex items-center gap-2">
          {value < 33 ? <Heart size={16} className="text-rose-400" /> :
            value < 66 ? <Sparkles size={16} className="text-purple-400" /> :
              <Gem size={16} className="text-cyan-400" />}
          Gift Vibe
        </h3>
        <span className="text-xs font-mono font-bold text-muted-foreground uppercase tracking-widest bg-secondary/30 px-2 py-1 rounded">
          {value < 33 ? "Sentimental" : value < 66 ? "Trending" : "Luxury"}
        </span>
      </div>

      <div
        className="relative h-14 bg-secondary/10 border border-white/5 rounded-full cursor-pointer touch-none group overflow-hidden"
        onPointerDown={handlePointerDown}
        onPointerMove={(e) => {
          if (e.buttons > 0) handlePointerDown(e)
        }}
      >
        {/* Track Fill */}
        <div className="absolute inset-0 rounded-full overflow-hidden">
          <motion.div
            className={`h-full bg-gradient-to-r opacity-50 transition-colors duration-500 ${getGradient()}`}
            style={{ width: `${value}%` }}
          />
        </div>

        {/* Labels Track */}
        <div className="absolute inset-0 flex items-center justify-between px-6 pointer-events-none opacity-30 text-[10px] font-bold uppercase tracking-widest">
          <span>Heart</span>
          <span>Trend</span>
          <span>Luxe</span>
        </div>

        {/* Draggable Thumb */}
        <motion.div
          className="absolute top-1 bottom-1 w-12 h-12 bg-background/80 backdrop-blur-md rounded-full shadow-lg flex items-center justify-center border border-white/10 z-10"
          animate={{
            left: `calc(${value}% - 24px)`,
            scale: isDragging ? 1.1 : 1,
            boxShadow: isDragging ? "0 0 20px rgba(255,255,255,0.1)" : "0 4px 10px rgba(0,0,0,0.1)"
          }}
          transition={{ type: "spring", stiffness: 300, damping: 28 }}
          onPointerDown={() => setIsDragging(true)}
          onPointerUp={() => setIsDragging(false)}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={value < 33 ? "heart" : value < 66 ? "sparkle" : "gem"}
              initial={{ scale: 0, rotate: -20 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, rotate: 20 }}
              transition={{ duration: 0.2 }}
            >
              {getActiveIcon()}
            </motion.div>
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  )
}
