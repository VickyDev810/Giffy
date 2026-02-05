
'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Gift, Users, ArrowUpRight, ArrowDownLeft, Loader2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { auth, gifts, friends } from '@/lib/api';
import Link from 'next/link';

export default function DashboardPage() {
    const [user, setUser] = useState<any>(null);
    const [stats, setStats] = useState({
        sentCount: 0,
        receivedCount: 0,
        friendCount: 0,
    });
    const [recentGifts, setRecentGifts] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [userData, sentData, receivedData, friendsData] = await Promise.all([
                    auth.me(),
                    gifts.sent(),
                    gifts.received(),
                    friends.list(),
                ]);

                setUser(userData);
                setStats({
                    sentCount: sentData?.length || 0,
                    receivedCount: receivedData?.length || 0,
                    friendCount: friendsData?.length || 0,
                });

                // Combine and sort recent gifts
                const allGifts = [
                    ...(sentData || []).map((g: any) => ({ ...g, type: 'sent' })),
                    ...(receivedData || []).map((g: any) => ({ ...g, type: 'received' })),
                ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
                    .slice(0, 5);

                setRecentGifts(allGifts);
            } catch (error) {
                console.error('Failed to fetch dashboard data', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">
                    Hello, {user?.full_name || 'User'}! 👋
                </h1>
                <p className="text-muted-foreground">
                    Here's what's happening with your gifts and friends.
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Gifts Sent</CardTitle>
                        <Gift className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats.sentCount}</div>
                        <p className="text-xs text-muted-foreground">
                            Total gifts sent to friends
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Gifts Received</CardTitle>
                        <Gift className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats.receivedCount}</div>
                        <p className="text-xs text-muted-foreground">
                            Total gifts received from friends
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Friends</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats.friendCount}</div>
                        <p className="text-xs text-muted-foreground">
                            Active connections
                        </p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                        <CardDescription>
                            Your latest gift exchanges.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-8">
                            {recentGifts.length === 0 ? (
                                <div className="text-center text-muted-foreground py-8">
                                    No recent activity. Send a gift to get started!
                                </div>
                            ) : (
                                recentGifts.map((gift) => (
                                    <div key={gift.id} className="flex items-center">
                                        <div className={`flex h-9 w-9 items-center justify-center rounded-full border ${gift.type === 'sent' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400'}`}>
                                            {gift.type === 'sent' ? <ArrowUpRight className="h-4 w-4" /> : <ArrowDownLeft className="h-4 w-4" />}
                                        </div>
                                        <div className="ml-4 space-y-1">
                                            <p className="text-sm font-medium leading-none">
                                                {gift.type === 'sent' ? `Sent to ${gift.recipient_username}` : `Received from ${gift.sender_username}`}
                                            </p>
                                            <p className="text-sm text-muted-foreground">
                                                {gift.vibe_prompt || 'Surprise Gift'}
                                            </p>
                                        </div>
                                        <div className="ml-auto font-medium text-sm">
                                            {gift.status}
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </CardContent>
                </Card>
                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                        <CardDescription>
                            What would you like to do?
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="grid gap-4">
                        <Link href="/gifts/create">
                            <Button className="w-full justify-start" size="lg">
                                <Gift className="mr-2 h-4 w-4" />
                                Send a Gift
                            </Button>
                        </Link>
                        <Link href="/friends">
                            <Button variant="outline" className="w-full justify-start" size="lg">
                                <Users className="mr-2 h-4 w-4" />
                                Find Friends
                            </Button>
                        </Link>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
