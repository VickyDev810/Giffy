"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Users, Heart, Briefcase, GraduationCap, User, ChevronDown, Sparkles } from "lucide-react"

interface TargetGroupSelectProps {
  value: string
  onChange: (value: string) => void
}

const TARGET_GROUPS = [
  { value: "friend", label: "Friend", icon: Users, color: "text-blue-400" },
  { value: "family", label: "Family", icon: Heart, color: "text-rose-400" },
  { value: "colleague", label: "Colleague", icon: Briefcase, color: "text-amber-400" },
  { value: "partner", label: "Partner", icon: Sparkles, color: "text-purple-400" },
  { value: "mentor", label: "Mentor", icon: GraduationCap, color: "text-emerald-400" },
  { value: "boss", label: "Boss", icon: User, color: "text-slate-400" },
]

export default function TargetGroupSelect({ value, onChange }: TargetGroupSelectProps) {
  const [isOpen, setIsOpen] = useState(false)
  const selected = TARGET_GROUPS.find((g) => g.value === value) || TARGET_GROUPS[0]

  return (
    <div className="space-y-4 relative">
      <h3 className="font-semibold text-foreground/80">Recipient</h3>

      <div className="relative">
        <motion.button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between bg-secondary/10 border border-white/10 rounded-xl p-4 hover:border-primary/50 transition-colors backdrop-blur-sm group"
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.99 }}
          type="button"
        >
          <div className="flex items-center gap-4">
            <div className={`p-2 rounded-lg bg-background/50 ${selected.color}`}>
              <selected.icon size={24} />
            </div>
            <span className="font-medium text-lg">{selected.label}</span>
          </div>
          <motion.div
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            <ChevronDown className="text-muted-foreground group-hover:text-foreground transition-colors" />
          </motion.div>
        </motion.button>

        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 10, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute top-full left-0 right-0 mt-2 p-2 bg-popover/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl z-50 grid grid-cols-2 gap-2"
            >
              {TARGET_GROUPS.map((group) => (
                <motion.button
                  key={group.value}
                  onClick={() => {
                    onChange(group.value)
                    setIsOpen(false)
                  }}
                  whileHover={{ scale: 1.03, backgroundColor: "rgba(255,255,255,0.05)" }}
                  whileTap={{ scale: 0.97 }}
                  className={`p-3 rounded-lg flex flex-col items-center gap-2 transition-colors border border-transparent
                      ${value === group.value
                      ? "bg-primary/20 border-primary/50"
                      : "hover:border-white/10"
                    }`}
                >
                  <group.icon size={24} className={group.color} />
                  <span className={`text-xs font-medium ${value === group.value ? "text-foreground" : "text-muted-foreground"}`}>
                    {group.label}
                  </span>
                </motion.button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
