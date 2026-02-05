"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { motion, AnimatePresence, type Variants } from "framer-motion"
import { Input } from "@/components/ui/input"
import { Slider } from "@/components/ui/slider"
import EmotionSlider from "@/components/emotion-slider"
import TargetGroupSelect from "@/components/target-group-select"
import { Instagram, Twitter, Linkedin, ChevronRight, ChevronLeft, Check, Sparkles } from "lucide-react"

interface FormData {
  friendName: string
  instagramHandle: string
  twitterHandle: string
  linkedinHandle: string
  description: string
  budget: number
  emotionValue: number // 0-100
  targetGroup: string
}

interface GiftFinderFormProps {
  onSubmit: (data: FormData) => void
  initialHandle?: string
}

const STEPS = [
  { id: 1, title: "Identity", subtitle: "Who are we analyzing?" },
  { id: 2, title: "The Vibe", subtitle: "Define the energy." },
  { id: 3, title: "Constraints", subtitle: "Set the parameters." },
]

export default function GiftFinderForm({ onSubmit, initialHandle }: GiftFinderFormProps) {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState<FormData>({
    friendName: "",
    instagramHandle: "",
    twitterHandle: "",
    linkedinHandle: "",
    description: "",
    budget: 100,
    emotionValue: 50,
    targetGroup: "friend",
  })

  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    if (initialHandle) {
      if (initialHandle.toLowerCase().includes("twitter") || initialHandle.toLowerCase().includes("x.com")) {
        setFormData(prev => ({ ...prev, twitterHandle: initialHandle }))
      } else {
        setFormData(prev => ({ ...prev, instagramHandle: initialHandle }))
      }
    }
  }, [initialHandle])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleNext = () => {
    if (step < 3) setStep(step + 1)
    else handleSubmit()
  }

  const handleBack = () => {
    if (step > 1) setStep(step - 1)
  }

  const handleSubmit = () => {
    if (formData.friendName || step === 3) {
      setSubmitted(true)
      setTimeout(() => {
        onSubmit(formData)
      }, 1500)
    }
  }

  // Animation Variants
  const slideVariants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 50 : -50,
      opacity: 0
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 50 : -50,
      opacity: 0
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Ambient Background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: "1s" }} />
      </div>

      <AnimatePresence mode="wait">
        {!submitted ? (
          <motion.div
            className="w-full max-w-2xl relative z-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9 }}
            key="wizard-container"
          >
            {/* Steps Progress */}
            <div className="flex justify-between mb-8 px-4">
              {STEPS.map((s, i) => (
                <div key={s.id} className="flex flex-col items-center relative z-10">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors duration-500
                    ${step >= s.id ? 'bg-primary text-primary-foreground' : 'bg-white/5 text-muted-foreground border border-white/10'}
                  `}>
                    {step > s.id ? <Check size={14} /> : s.id}
                  </div>
                  <div className="text-[10px] mt-2 font-mono uppercase tracking-wider opacity-60">
                    {s.title}
                  </div>
                </div>
              ))}
              {/* Progress Bar Line */}
              <div className="absolute top-4 left-0 w-full h-[1px] bg-white/5 -z-0 px-12">
                <div
                  className="h-full bg-primary transition-all duration-500 ease-out"
                  style={{ width: `${((step - 1) / (STEPS.length - 1)) * 100}%` }}
                />
              </div>
            </div>

            {/* Main Card */}
            <div className="bg-card/50 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden min-h-[500px] flex flex-col">

              {/* Step Header */}
              <div className="mb-6">
                <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">
                  {STEPS[step - 1].title}
                </h2>
                <p className="text-muted-foreground">{STEPS[step - 1].subtitle}</p>
              </div>

              {/* Form Content */}
              <div className="flex-1 relative">
                <AnimatePresence mode="wait" custom={step}>

                  {/* Step 1: Identity */}
                  {step === 1 && (
                    <motion.div
                      key="step1"
                      custom={step}
                      variants={slideVariants}
                      initial="enter"
                      animate="center"
                      exit="exit"
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      className="space-y-6"
                    >
                      <div className="space-y-4">
                        <label className="text-sm font-medium text-muted-foreground ml-1">Name / Alias</label>
                        <Input
                          name="friendName"
                          placeholder="e.g. Alex"
                          value={formData.friendName}
                          onChange={handleChange}
                          className="text-2xl font-bold bg-transparent border-0 border-b-2 border-primary/30 rounded-none px-0 focus-visible:ring-0 focus-visible:border-primary placeholder:text-muted-foreground/50 h-16 transition-all"
                          autoFocus
                        />
                      </div>

                      <div className="space-y-4 pt-4">
                        <label className="text-sm font-medium text-muted-foreground ml-1">Digital Footprint</label>
                        <div className="space-y-3">
                          <div className="relative group">
                            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                              <Instagram size={18} />
                            </div>
                            <Input
                              name="instagramHandle"
                              placeholder="@instagram"
                              value={formData.instagramHandle}
                              onChange={handleChange}
                              className="pl-10 bg-white/5 border-white/10 rounded-xl"
                            />
                          </div>
                          <div className="relative group">
                            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-muted-foreground">
                              <Twitter size={18} />
                            </div>
                            <Input
                              name="twitterHandle"
                              placeholder="@twitter"
                              value={formData.twitterHandle}
                              onChange={handleChange}
                              className="pl-10 bg-muted/50 border-input rounded-xl focus:bg-background transition-colors"
                            />
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {/* Step 2: Vibe Check */}
                  {step === 2 && (
                    <motion.div
                      key="step2"
                      custom={step}
                      variants={slideVariants}
                      initial="enter"
                      animate="center"
                      exit="exit"
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      className="space-y-8"
                    >
                      <div className="space-y-4">
                        <label className="text-sm font-medium text-muted-foreground">Relationship</label>
                        <TargetGroupSelect
                          value={formData.targetGroup}
                          onChange={(val) => setFormData(prev => ({ ...prev, targetGroup: val }))}
                        />
                      </div>

                      <div className="space-y-4 pt-4">
                        <label className="text-sm font-medium text-muted-foreground">Energy Level</label>
                        <EmotionSlider
                          value={formData.emotionValue}
                          onChange={(val) => setFormData(prev => ({ ...prev, emotionValue: val }))}
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Step 3: Constraints */}
                  {step === 3 && (
                    <motion.div
                      key="step3"
                      custom={step}
                      variants={slideVariants}
                      initial="enter"
                      animate="center"
                      exit="exit"
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      className="space-y-8"
                    >
                      <div className="space-y-4">
                        <div className="flex justify-between items-center mb-2">
                          <label className="text-sm font-medium text-muted-foreground">Budget Cap</label>
                          <span className="text-2xl font-mono text-primary">${formData.budget}</span>
                        </div>
                        <Slider
                          value={[formData.budget]}
                          onValueChange={(val) => setFormData(prev => ({ ...prev, budget: val[0] }))}
                          min={10} max={1000} step={10}
                          className="py-4"
                        />
                      </div>

                      <div className="space-y-4">
                        <label className="text-sm font-medium text-muted-foreground">Additional Context</label>
                        <textarea
                          name="description"
                          value={formData.description}
                          onChange={handleChange}
                          placeholder="Any specific interests, dislikes, or inside jokes?"
                          className="w-full bg-muted/50 border border-input rounded-xl p-4 text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-primary/20 min-h-[120px] resize-none focus:bg-background transition-colors"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Footer / Navigation */}
              <div className="flex justify-between items-center pt-8 border-t border-border mt-auto">
                {step > 1 ? (
                  <button
                    onClick={handleBack}
                    className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors px-4 py-2"
                  >
                    <ChevronLeft size={16} /> Back
                  </button>
                ) : (
                  <div />
                )}

                <button
                  onClick={handleNext}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 rounded-xl font-medium flex items-center gap-2 transition-all hover:scale-105 active:scale-95 group"
                >
                  {step === 3 ? "Initialize Agents" : "Next Step"}
                  <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
                </button>
              </div>

            </div>
          </motion.div>
        ) : (
          <motion.div
            key="loading"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center justify-center text-center z-50 p-8"
          >
            {/* Same loading animation as before */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              className="text-8xl mb-6 relative flex items-center justify-center"
            >
              <div className="absolute inset-0 blur-xl bg-primary/30 rounded-full animate-pulse" />
              <Sparkles className="w-24 h-24 text-primary" strokeWidth={1} />
            </motion.div>
            <h2 className="text-3xl font-bold mb-2">Syncing Data...</h2>
            <p className="text-muted-foreground">Agents are compiling your request.</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
