'use client';

import { useRouter } from 'next/navigation';
import { AuthComponent } from '@/components/ui/sign-up';
import { Gem } from 'lucide-react';
import { decodeJWT } from '@/lib/api';

export default function LoginPage() {
    const router = useRouter();

    const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

        if (mode === 'login') {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch(`${apiUrl}/auth/login`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.detail || 'Invalid credentials');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);

            // Decodes the token to redirect based on role
            const payload = decodeJWT(data.access_token);
            if (payload && payload.role === 'admin') {
                router.push('/admin/tickets');
            } else {
                router.push('/tickets');
            }
        } else {
            // If they toggle to register
            const response = await fetch(`${apiUrl}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, role: 'user' }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.detail || 'Registration failed');
            }

            // Success state managed by component
            setTimeout(() => router.push('/login'), 5000);
        }
    };

    return (
        <AuthComponent
            brandName="AntiGravity"
            logo={<div className="bg-primary text-primary-foreground rounded-md p-1.5"><Gem className="h-4 w-4" /></div>}
            defaultMode="login"
            onAuth={handleAuth}
        />
    );
}
