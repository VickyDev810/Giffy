"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import GiftFinderForm from "@/components/gift-finder-form"
import ChatInterface from "@/components/chat-interface"
import HeroSection from "@/components/hero-section"
import AnalysisOverlay from "@/components/analysis-overlay"

type ViewState = "hero" | "analyzing" | "form" | "chat"

export default function Home() {
  const [view, setView] = useState<ViewState>("hero")
  const [friendData, setFriendData] = useState<any>(null)
  // Store the handle from hero section to pass to form
  const [initialHandle, setInitialHandle] = useState("")

  const handleHeroStart = (handle: string) => {
    setInitialHandle(handle)
    setView("analyzing")
  }

  const handleAnalysisComplete = () => {
    setView("form")
  }

  const handleFormSubmit = (data: any) => {
    setFriendData(data)
    setTimeout(() => setView("chat"), 500)
  }

  const handleBackToForm = () => {
    setView("form")
    setFriendData(null)
  }

  const handleBackToHero = () => {
    setView("hero")
    setInitialHandle("")
  }

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      <AnimatePresence mode="wait">

        {view === "hero" && (
          <motion.div
            key="hero"
            exit={{ opacity: 0, scale: 1.1, filter: "blur(10px)", transition: { duration: 0.5 } }}
            className="w-full"
          >
            <HeroSection onStart={handleHeroStart} />
          </motion.div>
        )}

        {view === "analyzing" && (
          <motion.div
            key="analyzing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, transition: { duration: 0.5 } }}
            className="w-full"
          >
            <AnalysisOverlay onComplete={handleAnalysisComplete} />
          </motion.div>
        )}

        {view === "form" && (
          <motion.div
            key="form"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, x: -50, transition: { duration: 0.3 } }}
            className="w-full"
          >
            <GiftFinderForm onSubmit={handleFormSubmit} initialHandle={initialHandle} />
          </motion.div>
        )}

        {view === "chat" && (
          <motion.div
            key="chat"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="w-full"
          >
            <ChatInterface
              friendData={{ ...friendData, initialHandle }}
              onBack={handleBackToHero}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
