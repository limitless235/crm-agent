'use client';

import { useRouter } from 'next/navigation';
import { AuthComponent } from '@/components/ui/sign-up';
import { Gem } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

export default function LoginPage() {
    const router = useRouter();

    const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
        if (mode === 'login') {
            const { error, data } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) {
                throw new Error(error.message || 'Invalid credentials');
            }

            // Immediately query the user's role from JWT or assume 'user' for redirect purposes.
            // In a real app we'd verify the role securely or decode the JWT on frontend for navigation hint.
            // For now, redirect to /tickets. The global layout or API will handle unauthorized access.
            router.push('/tickets');

        } else {
            // Register flow
            const { error } = await supabase.auth.signUp({
                email,
                password,
            });

            if (error) {
                throw new Error(error.message || 'Registration failed');
            }

            // Success state managed by component
            setTimeout(() => router.push('/login'), 5000);
        }
    };

    return (
        <AuthComponent
            brandName="Sage"
            logo={<div className="bg-primary text-primary-foreground rounded-md p-1.5"><Gem className="h-4 w-4" /></div>}
            defaultMode="login"
            onAuth={handleAuth}
        />
    );
}
