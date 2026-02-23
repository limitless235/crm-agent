'use client';

import { useRouter } from 'next/navigation';
import { AuthComponent } from '@/components/ui/sign-up';
import { Gem } from 'lucide-react';
import { decodeJWT } from '@/lib/api';

export default function RegisterPage() {
    const router = useRouter();

    const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

        if (mode === 'signup') {
            const response = await fetch(`${apiUrl}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, role: 'user' }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.detail || 'Registration failed');
            }

            // On success, the component handles the "Welcome" state
            // and we can redirect after a delay if needed, 
            // but the component itself manages the success state.
            setTimeout(() => router.push('/login'), 5000);
        } else {
            // If they toggle to login from here
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch(`${apiUrl}/auth/login`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.detail || 'Login failed');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            router.push('/tickets');
        }
    };

    const handleGoogleAuth = async (credential: string) => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

        try {
            console.log("Sending Google auth to:", apiUrl);
            const response = await fetch(`${apiUrl}/auth/google`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ credential }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                console.error("Backend auth failed:", data);
                throw new Error(data.detail || 'Google authentication failed');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);

            const payload = decodeJWT(data.access_token);
            if (payload && payload.role === 'admin') {
                router.push('/admin/tickets');
            } else {
                router.push('/tickets');
            }
        } catch (error: any) {
            console.error("Network or fetch error during Google auth:", {
                apiUrl,
                error: error.message,
                stack: error.stack
            });
            throw new Error(`Connection to backend failed. Check API URL or CORS. (${error.message})`);
        }
    };

    return (
        <AuthComponent
            brandName="AntiGravity"
            logo={<div className="bg-primary text-primary-foreground rounded-md p-1.5"><Gem className="h-4 w-4" /></div>}
            defaultMode="signup"
            onAuth={handleAuth}
            onGoogleAuth={handleGoogleAuth}
        />
    );
}
