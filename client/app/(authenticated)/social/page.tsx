
'use client';

import { Instagram } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function SocialPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Social Connections</h1>
                <p className="text-muted-foreground">Connect your social media to get better gift recommendations.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Instagram className="h-5 w-5" /> Instagram
                        </CardTitle>
                        <CardDescription>Connect your Instagram to analyze your vibe.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button variant="outline" className="w-full">Connect Instagram</Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
