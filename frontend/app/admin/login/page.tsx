'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { decodeJWT } from '@/lib/api';
import { AuthUI, Label, Input, PasswordInput, Button } from '@/components/ui/auth-fuse';

export default function AdminLoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';
            const response = await fetch(`${apiUrl}/auth/login`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.detail || 'Invalid admin credentials');
            }

            const data = await response.json();

            // Decodes the token to check role (simple check for UX)
            const payload = decodeJWT(data.access_token);
            if (!payload || payload.role !== 'admin') {
                throw new Error('Access denied: User is not an administrator');
            }

            localStorage.setItem('token', data.access_token);
            router.push('/admin/tickets');
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : 'Login failed');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthUI
            isSignIn={true}
            onToggle={() => router.push('/login')}
            signInContent={{
                image: {
                    src: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop",
                    alt: "Electronic circuit board"
                },
                quote: {
                    text: "Control is the essence of administrative power.",
                    author: "System Architect"
                }
            }}
        >
            <form onSubmit={handleLogin} className="flex flex-col gap-8">
                <div className="flex flex-col items-center gap-2 text-center">
                    <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center mb-2 shadow-lg shadow-blue-500/20">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M2.166 4.9L10 .3l7.834 4.6a1 1 0 01.5 1.175l-1.735 9.012a2 2 0 01-1.592 1.577l-5.007 1.02a1 1 0 01-.4 0l-5.007-1.02a2 2 0 01-1.592-1.577L1.666 6.075a1 1 0 01.5-1.175zM10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                        </svg>
                    </div>
                    <h1 className="text-2xl font-bold uppercase tracking-tight">Admin Gateway</h1>
                    <p className="text-balance text-sm text-muted-foreground uppercase tracking-widest text-[10px] font-bold">Authorized Access Only</p>
                </div>
                <div className="grid gap-4">
                    {error && <div className="p-3 text-sm text-red-400 bg-red-900/10 border border-red-900/20 rounded-lg">{error}</div>}
                    <div className="grid gap-2">
                        <Label htmlFor="email">Admin Email</Label>
                        <Input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="admin@sage.internal"
                            required
                            autoComplete="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <PasswordInput
                        name="password"
                        label="Access Key"
                        required
                        autoComplete="current-password"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <Button type="submit" variant="default" className="mt-2 py-6 text-md" disabled={isLoading}>
                        {isLoading ? 'Authorizing...' : 'Sign In to Console'}
                    </Button>
                </div>
                <div className="text-center pt-4 border-t border-border">
                    <Link href="/login" className="text-xs text-muted-foreground hover:text-primary flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 15l-3-3m0 0l3-3m-3 3h8M3 12a9 9 0 1118 0 8 8 0 01-18 0z" />
                        </svg>
                        Back to User Portal
                    </Link>
                </div>
            </form>
        </AuthUI>
    );
}
