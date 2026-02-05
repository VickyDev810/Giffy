
'use client';

import { useEffect, useState } from 'react';
import { Gift, ArrowUpRight, ArrowDownLeft, Loader2, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { gifts } from '@/lib/api';
import Link from 'next/link';

export default function GiftsPage() {
    const [sentGifts, setSentGifts] = useState<any[]>([]);
    const [receivedGifts, setReceivedGifts] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [sent, received] = await Promise.all([
                    gifts.sent(),
                    gifts.received(),
                ]);
                setSentGifts(sent || []);
                setReceivedGifts(received || []);
            } catch (error) {
                console.error('Failed to fetch gifts', error);
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

    const GiftCard = ({ gift, type }: { gift: any, type: 'sent' | 'received' }) => (
        <Card className="mb-4">
            <CardHeader className="flex flex-row items-start justify-between pb-2">
                <div className="space-y-1">
                    <CardTitle className="text-base font-medium">
                        {type === 'sent' ? `To: ${gift.recipient_username}` : `From: ${gift.sender_username}`}
                    </CardTitle>
                    <CardDescription className="text-xs">
                        {new Date(gift.created_at).toLocaleDateString()}
                    </CardDescription>
                </div>
                <Badge variant={gift.status === 'delivered' ? 'default' : 'secondary'}>
                    {gift.status}
                </Badge>
            </CardHeader>
            <CardContent>
                <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-full ${type === 'sent' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'}`}>
                        <Gift className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                        <p className="text-sm font-medium">{gift.gift_name || 'Surprise Gift'}</p>
                        <p className="text-xs text-muted-foreground line-clamp-1">{gift.vibe_prompt}</p>
                    </div>
                    {gift.gift_price && (
                        <div className="font-bold text-sm">
                            ₹{gift.gift_price}
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Gifts</h1>
                    <p className="text-muted-foreground">View your gift history.</p>
                </div>
                <Link href="/gifts/create">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" /> Send Gift
                    </Button>
                </Link>
            </div>

            <Tabs defaultValue="sent" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="sent">Sent ({sentGifts.length})</TabsTrigger>
                    <TabsTrigger value="received">Received ({receivedGifts.length})</TabsTrigger>
                </TabsList>

                <TabsContent value="sent">
                    {sentGifts.length === 0 ? (
                        <div className="text-center py-12 text-muted-foreground">
                            No gifts sent yet.
                        </div>
                    ) : (
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                            {sentGifts.map((gift) => (
                                <GiftCard key={gift.id} gift={gift} type="sent" />
                            ))}
                        </div>
                    )}
                </TabsContent>

                <TabsContent value="received">
                    {receivedGifts.length === 0 ? (
                        <div className="text-center py-12 text-muted-foreground">
                            No gifts received yet.
                        </div>
                    ) : (
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                            {receivedGifts.map((gift) => (
                                <GiftCard key={gift.id} gift={gift} type="received" />
                            ))}
                        </div>
                    )}
                </TabsContent>
            </Tabs>
        </div>
    );
}
