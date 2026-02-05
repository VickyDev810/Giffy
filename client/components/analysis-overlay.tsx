"use client"

import { useEffect, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Gift } from "lucide-react"

const FRIENDLY_MESSAGES = [
    "Understanding their vibe...",
    "Scanning for hobbies & interests...",
    "Checking trending gifts...",
    "Curating the perfect selection...",
    "Finishing touches..."
]

export default function AnalysisOverlay({ onComplete }: { onComplete: () => void }) {
    const [currentMessage, setCurrentMessage] = useState(0)

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentMessage(prev => {
                if (prev < FRIENDLY_MESSAGES.length - 1) return prev + 1
                return prev
            })
        }, 800)

        const timeout = setTimeout(() => {
            onComplete()
        }, FRIENDLY_MESSAGES.length * 800 + 500)

        return () => {
            clearInterval(interval)
            clearTimeout(timeout)
        }
    }, [onComplete])

    return (
        <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-xl flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-md text-center space-y-8">

                {/* Bouncing Gift Animation */}
                <motion.div
                    animate={{
                        y: [0, -20, 0],
                        scale: [1, 1.1, 1],
                        rotate: [0, 5, -5, 0]
                    }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                    className="relative inline-flex items-center justify-center w-32 h-32"
                >
                    <div className="absolute inset-0 bg-primary/20 rounded-full blur-3xl animate-pulse" />
                    <Gift size={80} className="text-primary relative z-10 drop-shadow-lg" strokeWidth={1.5} />
                </motion.div>

                {/* Friendly Text */}
                <div className="h-12 relative overflow-hidden">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={currentMessage}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="text-2xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary absolute inset-0 flex items-center justify-center"
                        >
                            {FRIENDLY_MESSAGES[currentMessage]}
                        </motion.div>
                    </AnimatePresence>
                </div>

                {/* Soft Progress Bar */}
                <div className="w-64 h-2 bg-secondary/20 rounded-full mx-auto overflow-hidden relative">
                    <motion.div
                        className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary to-secondary rounded-full"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: FRIENDLY_MESSAGES.length * 0.8, ease: "linear" }}
                    />
                </div>
            </div>
        </div>
    )
}
