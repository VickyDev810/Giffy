
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Gift, Loader2, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { friends, gifts } from '@/lib/api';
import { toast } from 'sonner';

export default function CreateGiftPage() {
    const router = useRouter();
    const [friendList, setFriendList] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    const [formData, setFormData] = useState({
        recipient_id: '',
        vibe_prompt: '',
        budget_min: '0',
        budget_max: '500',
        is_surprise: false,
        sender_message: '',
    });

    useEffect(() => {
        const fetchFriends = async () => {
            try {
                const data = await friends.list();
                setFriendList(data || []);
            } catch (error) {
                console.error('Failed to fetch friends', error);
            } finally {
                setLoading(false);
            }
        };
        fetchFriends();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!formData.recipient_id) {
            toast.error('Please select a recipient');
            return;
        }

        setSubmitting(true);
        try {
            await gifts.send({
                ...formData,
                recipient_id: parseInt(formData.recipient_id),
                budget_min: parseInt(formData.budget_min),
                budget_max: parseInt(formData.budget_max),
            });
            toast.success('Gift request sent! AI is on it.');
            router.push('/gifts');
        } catch (error: any) {
            toast.error(error.message || 'Failed to send gift');
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="flex h-full items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Send a Gift</h1>
                <p className="text-muted-foreground">Let our AI find the perfect gift for your friend.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Gift Details</CardTitle>
                    <CardDescription>Tell us about the vibe and budget.</CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-6">
                        <div className="space-y-2">
                            <Label>Recipient</Label>
                            <Select
                                onValueChange={(val) => setFormData({ ...formData, recipient_id: val })}
                                value={formData.recipient_id}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select a friend" />
                                </SelectTrigger>
                                <SelectContent>
                                    {friendList.map((friend) => (
                                        <SelectItem key={friend.friend_id} value={friend.friend_id.toString()}>
                                            {friend.friend_full_name} (@{friend.friend_username})
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Vibe Prompt</Label>
                            <Textarea
                                placeholder="e.g. Something chaotic and funny for a cat lover..."
                                value={formData.vibe_prompt}
                                onChange={(e) => setFormData({ ...formData, vibe_prompt: e.target.value })}
                                required
                            />
                            <p className="text-xs text-muted-foreground">
                                Describe the kind of gift you want. Be creative!
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label>Min Budget (₹)</Label>
                                <Input
                                    type="number"
                                    min="0"
                                    value={formData.budget_min}
                                    onChange={(e) => setFormData({ ...formData, budget_min: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Max Budget (₹)</Label>
                                <Input
                                    type="number"
                                    min="0"
                                    value={formData.budget_max}
                                    onChange={(e) => setFormData({ ...formData, budget_max: e.target.value })}
                                    required
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-between rounded-lg border p-4">
                            <div className="space-y-0.5">
                                <Label className="text-base">Surprise Mode (YOLO)</Label>
                                <p className="text-sm text-muted-foreground">
                                    Skip your approval and order immediately.
                                </p>
                            </div>
                            <Switch
                                checked={formData.is_surprise}
                                onCheckedChange={(checked) => setFormData({ ...formData, is_surprise: checked })}
                            />
                        </div>

                        <div className="space-y-2">
                            <Label>Message (Optional)</Label>
                            <Textarea
                                placeholder="Happy Birthday! Hope you like this..."
                                value={formData.sender_message}
                                onChange={(e) => setFormData({ ...formData, sender_message: e.target.value })}
                            />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button type="submit" className="w-full" disabled={submitting}>
                            {submitting ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Processing...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="mr-2 h-4 w-4" />
                                    Find Gift
                                </>
                            )}
                        </Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
