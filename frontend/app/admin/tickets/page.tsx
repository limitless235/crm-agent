'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiFetch, decodeJWT } from '@/lib/api';

interface User {
    id: string;
    email: string;
    created_at: string;
}

interface Ticket {
    id: string;
    title: string;
    status: string;
    priority: string;
    created_at: string;
}

export default function AdminTicketsPage() {
    const [users, setUsers] = useState<User[]>([]);
    const [selectedUser, setSelectedUser] = useState<User | null>(null);
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadingTickets, setLoadingTickets] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/admin/login');
            return;
        }

        // Quick check if token is admin
        const payload = decodeJWT(token);
        if (!payload || payload.role !== 'admin') {
            localStorage.removeItem('token');
            router.push('/admin/login');
            return;
        }

        async function fetchUsers() {
            try {
                const res = await apiFetch('/users');
                if (res.ok) {
                    const data = await res.json();
                    setUsers(data);
                } else if (res.status === 401) {
                    router.push('/admin/login');
                }
            } catch (err) {
                console.error('Failed to fetch users', err);
            } finally {
                setLoading(false);
            }
        }

        fetchUsers();
    }, [router]);

    const handleSelectUser = async (user: User) => {
        console.log('Admin Dashboard: Selecting user:', user.email);
        setSelectedUser(user);
        setLoadingTickets(true);
        try {
            const res = await apiFetch(`/tickets?user_id=${user.id}`);
            if (res.ok) {
                const data = await res.json();
                console.log(`Admin Dashboard: Retrieved ${data.length} tickets for ${user.email}`);
                setTickets(data);
            } else {
                console.error('Admin Dashboard: Failed to fetch tickets', await res.text());
            }
        } catch (err) {
            console.error('Admin Dashboard: API Error', err);
        } finally {
            setLoadingTickets(false);
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority.toLowerCase()) {
            case 'high': return 'bg-red-900/30 text-red-400 border-red-500/20';
            case 'medium': return 'bg-amber-900/30 text-amber-400 border-amber-500/20';
            default: return 'bg-blue-900/30 text-blue-400 border-blue-500/20';
        }
    };

    const getStatusColor = (status: string) => {
        return status.toLowerCase() === 'open'
            ? 'bg-green-900/30 text-green-400 border-green-500/20'
            : 'bg-slate-800 text-slate-400 border-white/10';
    };

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-200">
            {/* Header */}
            <div className="border-b-2 border-blue-500 bg-slate-900 shadow-2xl sticky top-0 z-20">
                <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center font-black text-white text-xl shadow-[0_0_20px_rgba(37,99,235,0.4)]">
                            ADM
                        </div>
                        <div>
                            <h1 className="text-xl font-black text-white tracking-widest uppercase">Admin Control Center</h1>
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                                <p className="text-[10px] text-blue-400 font-bold tracking-tighter uppercase">Authorized Session Active</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-6">
                        <button
                            onClick={() => { localStorage.removeItem('token'); router.push('/admin/login'); }}
                            className="px-4 py-2 border border-white/10 rounded-lg text-xs font-bold text-slate-400 hover:text-white hover:bg-white/5 transition uppercase tracking-widest"
                        >
                            Emergency Logout
                        </button>
                    </div>
                </div>
            </div>

            <main className="max-w-7xl mx-auto px-6 py-10">
                {!selectedUser ? (
                    <>
                        <div className="mb-8 font-bold">
                            <h2 className="text-3xl text-white">System Users</h2>
                            <p className="text-slate-400 mt-1">Select a user to manage their tickets.</p>
                        </div>

                        {loading ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="h-32 bg-white/5 animate-pulse rounded-2xl border border-white/5"></div>
                                ))}
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {users.map(user => (
                                    <button
                                        key={user.id}
                                        onClick={() => handleSelectUser(user)}
                                        className="text-left p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/[0.08] transition shadow-xl group"
                                    >
                                        <div className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-600 transition-colors">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-slate-400 group-hover:text-white" viewBox="0 0 20 20" fill="currentColor">
                                                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                                            </svg>
                                        </div>
                                        <h3 className="text-white font-bold truncate mb-1">{user.email}</h3>
                                        <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Joined: {new Date(user.created_at).toLocaleDateString()}</p>
                                    </button>
                                ))}
                            </div>
                        )}
                    </>
                ) : (
                    <>
                        <button
                            onClick={() => setSelectedUser(null)}
                            className="flex items-center gap-2 text-blue-400 text-sm font-bold uppercase tracking-widest mb-6 hover:text-blue-300 transition"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
                            </svg>
                            Back to Users
                        </button>

                        <div className="mb-8">
                            <h2 className="text-3xl text-white font-extrabold">{selectedUser.email.split('@')[0].toUpperCase()}'s Tickets</h2>
                            <p className="text-slate-400 mt-1">Viewing all interaction history for this specific account.</p>
                        </div>

                        {loadingTickets ? (
                            <div className="flex flex-col items-center justify-center py-20 bg-white/5 rounded-2xl border border-white/10">
                                <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                                <p className="text-blue-400 font-bold uppercase tracking-widest text-xs">Retrieving Interaction History...</p>
                            </div>
                        ) : tickets.length === 0 ? (
                            <div className="bg-white/5 border border-dashed border-white/10 rounded-2xl p-20 text-center">
                                <p className="text-slate-500 font-medium">This user has not submitted any tickets yet.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-4">
                                {tickets.map(ticket => (
                                    <div key={ticket.id} className="p-6 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/[0.07] transition-all flex items-center justify-between group">
                                        <div className="flex items-center gap-6">
                                            <div className="flex flex-col gap-2">
                                                <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase border w-fit ${getPriorityColor(ticket.priority)}`}>
                                                    {ticket.priority}
                                                </span>
                                                <h3 className="text-white font-bold uppercase tracking-tight group-hover:text-blue-400 transition-colors">
                                                    {ticket.title}
                                                </h3>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-6">
                                            <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase border ${getStatusColor(ticket.status)}`}>
                                                {ticket.status}
                                            </span>
                                            <Link
                                                href={`/tickets/${ticket.id}`}
                                                className="px-6 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl hover:bg-blue-500 transition shadow-lg shadow-blue-600/20"
                                            >
                                                Audit
                                            </Link>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </>
                )}
            </main>
        </div>
    );
}
