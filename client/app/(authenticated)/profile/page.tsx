
'use client';

import { useEffect, useState } from 'react';
import { User, Mail, Phone, MapPin, Loader2, Save, Instagram, Sparkles, Zap, Heart, Gift } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { auth } from '@/lib/api';
import { toast } from 'sonner';

export default function ProfilePage() {
    const [user, setUser] = useState<any>(null);
    const [persona, setPersona] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [instaUsername, setInstaUsername] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [analysisResult, setAnalysisResult] = useState<any>(null);

    const handleAnalyze = async () => {
        if (!instaUsername) return;
        setAnalyzing(true);
        try {
            const res = await fetch(`http://localhost:8000/api/social/instagram/analyze-for-gifts?username=${instaUsername}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const data = await res.json();
            if (data.success) {
                setAnalysisResult(data);
                toast.success("Analysis complete!");
            } else {
                toast.error(data.error || "Analysis failed");
            }
        } catch (e) {
            toast.error("Failed to analyze profile");
        } finally {
            setAnalyzing(false);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const userData = await auth.me();
                setUser(userData);

                // Fetch persona
                const res = await fetch('http://localhost:8000/api/persona/me', {
                    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                });
                if (res.ok) {
                    const personaData = await res.json();
                    setPersona(personaData);
                }
            } catch (error) {
                console.error('Failed to fetch profile', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleSave = async () => {
        // Implement update logic
        toast.info("Update functionality coming soon!");
        setIsEditing(false);
    };

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
                <p className="text-muted-foreground">Manage your account and gift preferences.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Personal Information</CardTitle>
                        <CardDescription>Your contact details and identity.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex justify-center mb-6">
                            <Avatar className="h-24 w-24">
                                <AvatarImage src={user?.avatar_url} />
                                <AvatarFallback className="text-2xl">{user?.full_name?.[0]}</AvatarFallback>
                            </Avatar>
                        </div>
                        <div className="space-y-2">
                            <Label>Full Name</Label>
                            <div className="relative">
                                <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input value={user?.full_name} disabled={!isEditing} className="pl-9" />
                            </div>
                        </div>
                        <div className="space-y-2">
                            <Label>Email</Label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input value={user?.email} disabled className="pl-9" />
                            </div>
                        </div>
                        <div className="space-y-2">
                            <Label>Phone</Label>
                            <div className="relative">
                                <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input value={user?.phone} disabled={!isEditing} className="pl-9" />
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter>
                        {isEditing ? (
                            <Button onClick={handleSave} className="w-full"><Save className="mr-2 h-4 w-4" /> Save Changes</Button>
                        ) : (
                            <Button variant="outline" onClick={() => setIsEditing(true)} className="w-full">Edit Profile</Button>
                        )}
                    </CardFooter>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Gift Persona</CardTitle>
                        <CardDescription>How AI selects gifts for you.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div>
                            <Label className="text-muted-foreground mb-2 block">Vibe Tags</Label>
                            <div className="flex flex-wrap gap-2">
                                {persona?.vibe_tags?.map((tag: string) => (
                                    <Badge key={tag} variant="secondary">{tag}</Badge>
                                )) || <span className="text-sm text-muted-foreground">No vibes set yet.</span>}
                            </div>
                        </div>

                        <div>
                            <Label className="text-muted-foreground mb-2 block">Interests</Label>
                            <div className="flex flex-wrap gap-2">
                                {persona?.interests?.map((tag: string) => (
                                    <Badge key={tag} variant="outline">{tag}</Badge>
                                )) || <span className="text-sm text-muted-foreground">No interests set yet.</span>}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label className="text-muted-foreground">Shirt Size</Label>
                                <div className="font-medium mt-1">{persona?.shirt_size || '-'}</div>
                            </div>
                            <div>
                                <Label className="text-muted-foreground">Shoe Size</Label>
                                <div className="font-medium mt-1">{persona?.shoe_size || '-'}</div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>Default Address</Label>
                            <div className="relative">
                                <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input value={persona?.default_address} disabled className="pl-9" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="md:col-span-2 border-yellow-500/20 shadow-lg">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Sparkles className="text-yellow-400 fill-yellow-400" />
                            AI Persona Analysis
                        </CardTitle>
                        <CardDescription>
                            Enter an Instagram username to generate a gift persona using Gemini AI.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex gap-4">
                            <div className="relative flex-1">
                                <Instagram className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input
                                    placeholder="Instagram Username (e.g. vicky_codes)"
                                    className="pl-9"
                                    value={instaUsername}
                                    onChange={(e) => setInstaUsername(e.target.value)}
                                />
                            </div>
                            <Button onClick={handleAnalyze} disabled={analyzing} className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white border-0">
                                {analyzing ? <Loader2 className="animate-spin mr-2" /> : <Sparkles className="mr-2 h-4 w-4" />}
                                Analyze
                            </Button>
                        </div>

                        {analysisResult && (
                            <div className="space-y-4 border rounded-xl p-6 bg-muted/30">
                                <div className="flex items-center gap-4">
                                    <Avatar className="h-16 w-16 border-2 border-yellow-400">
                                        <AvatarImage src={analysisResult.profile_summary.profile_pic_url} />
                                        <AvatarFallback>IG</AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <h3 className="font-bold text-lg">{analysisResult.profile_summary.full_name}</h3>
                                        <p className="text-sm text-muted-foreground">@{analysisResult.username}</p>
                                        <div className="flex gap-4 text-xs text-muted-foreground mt-1">
                                            <span>{analysisResult.profile_summary.followers} Followers</span>
                                            <span>{analysisResult.profile_summary.posts} Posts</span>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <Label className="text-xs uppercase text-muted-foreground font-bold">AI Summary</Label>
                                    <p className="text-sm mt-1 italic text-foreground/80">"{analysisResult.ai_summary}"</p>
                                </div>

                                <div className="grid md:grid-cols-3 gap-6 pt-2">
                                    <div className="space-y-2">
                                        <Label className="text-xs uppercase text-muted-foreground font-bold flex items-center gap-1"><Zap size={12} /> Vibe</Label>
                                        <div className="flex flex-wrap gap-1">
                                            {analysisResult.vibe_tags.map((tag: string) => (
                                                <Badge key={tag} variant="secondary" className="text-xs bg-yellow-100 text-yellow-800 hover:bg-yellow-200 border-0">{tag}</Badge>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label className="text-xs uppercase text-muted-foreground font-bold flex items-center gap-1"><Heart size={12} /> Interests</Label>
                                        <div className="flex flex-wrap gap-1">
                                            {analysisResult.detected_interests.map((tag: string) => (
                                                <Badge key={tag} variant="outline" className="text-xs">{tag}</Badge>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label className="text-xs uppercase text-muted-foreground font-bold flex items-center gap-1"><Gift size={12} /> Gift Ideas</Label>
                                        <ul className="text-sm list-disc list-inside space-y-1 text-muted-foreground">
                                            {analysisResult.gift_suggestions.slice(0, 3).map((idea: string) => (
                                                <li key={idea}>{idea}</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
