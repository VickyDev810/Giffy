"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { ArrowRight, Instagram, Twitter, Search, Sparkles } from "lucide-react"

export default function HeroSection({ onStart }: { onStart: (handle: string) => void }) {
    const [handle, setHandle] = useState("")

    return (
        <div className="flex flex-col items-center justify-center min-h-screen text-center p-6 relative overflow-hidden">
            {/* Ambient Background */}
            <div className="absolute inset-0 z-0">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[100px] animate-pulse" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: "2s" }} />
            </div>

            <div className="absolute top-6 right-6 z-20">
                <a href="/login" className="px-6 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 backdrop-blur-md transition-colors text-sm font-medium">
                    Login
                </a>
            </div>

            <div className="z-10 max-w-4xl w-full space-y-12">
                {/* Main Title */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className="space-y-6"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-muted-foreground backdrop-blur-md mb-4">
                        <Sparkles size={14} className="text-yellow-400" />
                        <span>AI-Powered Gift Intelligence</span>
                    </div>

                    <h1 className="text-7xl md:text-9xl font-black tracking-tighter">
                        <span className="block bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/50">
                            GIFFY
                        </span>
                    </h1>
                    <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto font-light">
                        Don't guess. Let our agents scan their digital footprint to find the perfect gift.
                    </p>
                </motion.div>

                {/* Input Area */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                    className="max-w-xl mx-auto relative group"
                >
                    <div className="absolute -inset-1 bg-gradient-to-r from-primary via-purple-500 to-secondary opacity-30 group-hover:opacity-60 blur-lg transition-opacity duration-500" />
                    <div className="relative flex items-center bg-card/80 backdrop-blur-xl border border-white/10 rounded-2xl p-2 shadow-2xl">
                        <div className="pl-4 text-muted-foreground">
                            <Search size={20} />
                        </div>
                        <input
                            type="text"
                            placeholder="Enter Instagram or Twitter handle..."
                            className="flex-1 bg-transparent border-0 px-4 py-4 text-lg placeholder:text-muted-foreground/50 focus:ring-0 focus:outline-none"
                            value={handle}
                            onChange={(e) => setHandle(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handle && onStart(handle)}
                        />
                        <button
                            onClick={() => handle && onStart(handle)}
                            disabled={!handle}
                            className="bg-primary hover:bg-primary/90 text-primary-foreground p-4 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed group-hover:shadow-[0_0_20px_var(--glow-purple)]"
                        >
                            <ArrowRight />
                        </button>
                    </div>

                    <div className="flex justify-center gap-6 mt-6 text-sm text-muted-foreground/60">
                        <span className="flex items-center gap-2"><Instagram size={14} /> Instagram</span>
                        <span className="flex items-center gap-2"><Twitter size={14} /> Twitter/X</span>
                    </div>
                </motion.div>
            </div>
        </div>
    )
}
