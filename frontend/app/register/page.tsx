'use client';

import { useRouter } from 'next/navigation';
import { AuthComponent } from '@/components/ui/sign-up';
import { Gem } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

export default function RegisterPage() {
    const router = useRouter();

    const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
        if (mode === 'signup') {
            const { error } = await supabase.auth.signUp({
                email,
                password,
            });

            if (error) {
                throw new Error(error.message || 'Registration failed');
            }

            setTimeout(() => router.push('/login'), 5000);
        } else {
            // Toggle to login
            const { error, data } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) {
                throw new Error(error.message || 'Login failed');
            }

            router.push('/tickets');
        }
    };

    return (
        <AuthComponent
            brandName="Sage"
            logo={<div className="bg-primary text-primary-foreground rounded-md p-1.5"><Gem className="h-4 w-4" /></div>}
            defaultMode="signup"
            onAuth={handleAuth}
        />
    );
}
