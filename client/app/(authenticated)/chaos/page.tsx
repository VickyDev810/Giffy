
'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Send, Sparkles, ShoppingBag, Loader2, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { agent } from '@/lib/api';
import { toast } from 'sonner';

type Message = {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
};

export default function ChaosPage() {
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [initializing, setInitializing] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const startSession = async () => {
        setInitializing(true);
        try {
            const res = await agent.quickChaos({
                vibe_prompt: "Something totally random and chaotic",
                budget_min: 100,
                budget_max: 2000
            });
            setSessionId(res.session_id);
            setMessages([
                { role: 'user', content: res.initial_prompt, timestamp: new Date().toISOString() },
                { role: 'assistant', content: res.agent_response, timestamp: new Date().toISOString() }
            ]);
        } catch (error) {
            toast.error('Failed to start Chaos Agent');
        } finally {
            setInitializing(false);
        }
    };

    const sendMessage = async (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!input.trim() || !sessionId) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg, timestamp: new Date().toISOString() }]);
        setLoading(true);

        try {
            const res = await agent.chat(sessionId, userMsg);
            setMessages(prev => [...prev, { role: 'assistant', content: res.content, timestamp: res.timestamp }]);
        } catch (error) {
            toast.error('Agent failed to respond');
        } finally {
            setLoading(false);
        }
    };

    if (!sessionId) {
        return (
            <div className="flex flex-col items-center justify-center h-[80vh] space-y-8 p-4">
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ type: "spring", bounce: 0.5 }}
                    className="text-center space-y-4"
                >
                    <div className="relative inline-block">
                        <div className="absolute inset-0 bg-yellow-400 blur-xl opacity-50 animate-pulse rounded-full" />
                        <div className="relative bg-yellow-400 p-6 rounded-full text-black shadow-xl">
                            <Zap size={64} strokeWidth={2.5} />
                        </div>
                    </div>
                    <h1 className="text-4xl font-black tracking-tighter uppercase">
                        Chaos <span className="text-yellow-500">Blinkit</span> Agent
                    </h1>
                    <p className="text-muted-foreground max-w-md mx-auto text-lg">
                        Need a gift in 10 minutes? Don't know what to get? Let our chaotic AI agent take the wheel.
                    </p>
                </motion.div>

                <Button
                    size="lg"
                    className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold text-lg px-8 py-6 rounded-full shadow-[0_0_20px_rgba(250,204,21,0.4)] hover:shadow-[0_0_30px_rgba(250,204,21,0.6)] transition-all"
                    onClick={startSession}
                    disabled={initializing}
                >
                    {initializing ? (
                        <>
                            <Loader2 className="mr-2 h-6 w-6 animate-spin" />
                            Igniting Chaos...
                        </>
                    ) : (
                        <>
                            <Sparkles className="mr-2 h-6 w-6" />
                            Start Chaos Mode
                        </>
                    )}
                </Button>
            </div>
        );
    }

    return (
        <div className="h-[calc(100vh-6rem)] flex flex-col gap-4 max-w-4xl mx-auto">
            <div className="flex items-center justify-between p-4 border rounded-xl bg-card/50 backdrop-blur-sm">
                <div className="flex items-center gap-3">
                    <div className="bg-yellow-400 p-2 rounded-full text-black">
                        <Zap size={20} />
                    </div>
                    <div>
                        <h2 className="font-bold">Chaos Agent Active</h2>
                        <p className="text-xs text-muted-foreground">Session ID: {sessionId.slice(0, 8)}...</p>
                    </div>
                </div>
                <Button variant="ghost" size="icon" onClick={() => setSessionId(null)} title="Reset">
                    <RefreshCw size={18} />
                </Button>
            </div>

            <Card className="flex-1 flex flex-col overflow-hidden border-yellow-500/20 shadow-2xl">
                <ScrollArea className="flex-1 p-4" ref={scrollRef}>
                    <div className="space-y-4">
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {msg.role === 'assistant' && (
                                    <Avatar className="h-8 w-8 border-2 border-yellow-400">
                                        <AvatarFallback className="bg-yellow-400 text-black">AI</AvatarFallback>
                                    </Avatar>
                                )}
                                <div
                                    className={`rounded-2xl px-4 py-2 max-w-[80%] ${msg.role === 'user'
                                            ? 'bg-primary text-primary-foreground rounded-tr-none'
                                            : 'bg-muted rounded-tl-none'
                                        }`}
                                >
                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                                </div>
                                {msg.role === 'user' && (
                                    <Avatar className="h-8 w-8">
                                        <AvatarFallback>ME</AvatarFallback>
                                    </Avatar>
                                )}
                            </motion.div>
                        ))}
                        {loading && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="flex gap-3 justify-start"
                            >
                                <Avatar className="h-8 w-8 border-2 border-yellow-400">
                                    <AvatarFallback className="bg-yellow-400 text-black">AI</AvatarFallback>
                                </Avatar>
                                <div className="bg-muted rounded-2xl rounded-tl-none px-4 py-3">
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <span className="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <span className="w-2 h-2 bg-yellow-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </div>
                </ScrollArea>
                <div className="p-4 border-t bg-background/50 backdrop-blur-sm">
                    <form onSubmit={sendMessage} className="flex gap-2">
                        <Input
                            placeholder="Type your chaotic request..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={loading}
                            className="flex-1"
                            autoFocus
                        />
                        <Button type="submit" disabled={loading || !input.trim()} className="bg-yellow-400 hover:bg-yellow-500 text-black">
                            <Send size={18} />
                        </Button>
                    </form>
                </div>
            </Card>
        </div>
    );
}
