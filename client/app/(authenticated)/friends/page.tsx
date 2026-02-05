
'use client';

import { useEffect, useState } from 'react';
import { Search, UserPlus, UserCheck, UserX, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { friends, auth } from '@/lib/api';
import { toast } from 'sonner';

export default function FriendsPage() {
    const [friendList, setFriendList] = useState<any[]>([]);
    const [requests, setRequests] = useState<any[]>([]);
    const [searchResults, setSearchResults] = useState<any[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        try {
            const [friendsData, requestsData] = await Promise.all([
                friends.list(),
                friends.requests(),
            ]);
            setFriendList(friendsData || []);
            setRequests(requestsData || []);
        } catch (error) {
            console.error('Failed to fetch friends data', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        try {
            // We need to implement search in api.ts
            // Assuming api.ts has a generic request method, we can use it here or add a search method.
            // Let's assume we add it or use raw fetch for now if api.ts doesn't have it.
            // Actually api.ts doesn't have search exposed yet. I'll add it inline or update api.ts later.
            // Let's just use the apiRequest helper if I exported it? I did export apiRequest.
            // But I can't import it easily if it's not exported or if I want to keep it clean.
            // I'll update api.ts to include search.
            // For now, I'll assume I can call a search endpoint.
            // The docs say: GET /users/search?q={query}

            const res = await fetch(`http://localhost:8000/api/users/search?q=${searchQuery}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await res.json();
            setSearchResults(data);
        } catch (error) {
            toast.error('Search failed');
        }
    };

    const sendRequest = async (userId: number) => {
        try {
            await friends.request({ receiver_id: userId, message: "Let's be friends!" });
            toast.success('Friend request sent!');
            setSearchResults(searchResults.filter(u => u.id !== userId));
        } catch (error) {
            toast.error('Failed to send request');
        }
    };

    const respondToRequest = async (requestId: number, action: 'accept' | 'reject') => {
        try {
            // We need to add this to api.ts or call directly
            await fetch(`http://localhost:8000/api/friends/requests/${requestId}/respond`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ action })
            });

            toast.success(`Request ${action}ed`);
            fetchData(); // Refresh lists
        } catch (error) {
            toast.error(`Failed to ${action} request`);
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
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Friends</h1>
                <p className="text-muted-foreground">Manage your connections and find new people.</p>
            </div>

            <Tabs defaultValue="list" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="list">My Friends</TabsTrigger>
                    <TabsTrigger value="requests">
                        Requests
                        {requests.length > 0 && (
                            <span className="ml-2 rounded-full bg-primary px-2 py-0.5 text-xs text-primary-foreground">
                                {requests.length}
                            </span>
                        )}
                    </TabsTrigger>
                    <TabsTrigger value="add">Add Friend</TabsTrigger>
                </TabsList>

                <TabsContent value="list" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {friendList.length === 0 ? (
                            <div className="col-span-full text-center text-muted-foreground py-12">
                                You haven't added any friends yet.
                            </div>
                        ) : (
                            friendList.map((friend) => (
                                <Card key={friend.id}>
                                    <CardHeader className="flex flex-row items-center gap-4">
                                        <Avatar>
                                            <AvatarImage src={friend.friend_avatar_url} />
                                            <AvatarFallback>{friend.friend_username?.[0]?.toUpperCase()}</AvatarFallback>
                                        </Avatar>
                                        <div>
                                            <CardTitle className="text-base">{friend.friend_full_name}</CardTitle>
                                            <CardDescription>@{friend.friend_username}</CardDescription>
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-sm text-muted-foreground">Nickname: {friend.nickname || 'None'}</p>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>

                <TabsContent value="requests" className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {requests.length === 0 ? (
                            <div className="col-span-full text-center text-muted-foreground py-12">
                                No pending requests.
                            </div>
                        ) : (
                            requests.map((req) => (
                                <Card key={req.id}>
                                    <CardHeader>
                                        <CardTitle>{req.sender_username}</CardTitle>
                                        <CardDescription>wants to be your friend</CardDescription>
                                    </CardHeader>
                                    <CardContent className="flex gap-2">
                                        <Button className="flex-1" onClick={() => respondToRequest(req.id, 'accept')}>
                                            <UserCheck className="mr-2 h-4 w-4" /> Accept
                                        </Button>
                                        <Button variant="outline" className="flex-1" onClick={() => respondToRequest(req.id, 'reject')}>
                                            <UserX className="mr-2 h-4 w-4" /> Reject
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>

                <TabsContent value="add" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Find People</CardTitle>
                            <CardDescription>Search for users by username or email.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSearch} className="flex gap-2">
                                <Input
                                    placeholder="Search username..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                                <Button type="submit">
                                    <Search className="mr-2 h-4 w-4" /> Search
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {searchResults.map((user) => (
                            <Card key={user.id}>
                                <CardHeader className="flex flex-row items-center gap-4">
                                    <Avatar>
                                        <AvatarImage src={user.avatar_url} />
                                        <AvatarFallback>{user.username[0].toUpperCase()}</AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <CardTitle className="text-base">{user.full_name}</CardTitle>
                                        <CardDescription>@{user.username}</CardDescription>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <Button className="w-full" onClick={() => sendRequest(user.id)}>
                                        <UserPlus className="mr-2 h-4 w-4" /> Add Friend
                                    </Button>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}
