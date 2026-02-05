
'use client';

import { Repeat } from 'lucide-react';

export default function SubscriptionsPage() {
    return (
        <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
            <div className="p-4 rounded-full bg-muted">
                <Repeat className="h-12 w-12 text-muted-foreground" />
            </div>
            <h1 className="text-2xl font-bold">Gift Subscriptions</h1>
            <p className="text-muted-foreground max-w-md">
                Automate your gift giving for birthdays and anniversaries. This feature is coming soon!
            </p>
        </div>
    );
}
