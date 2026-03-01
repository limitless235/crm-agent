'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch, API_URL, decodeJWT } from '@/lib/api';
import Link from 'next/link';

console.log('Tickets Page Initialized. API_URL:', API_URL);

interface Ticket {
    id: string;
    title: string;
    status: string;
    priority: string;
    created_at: string;
}

export default function TicketListPage() {
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newTicketTitle, setNewTicketTitle] = useState('');
    const [newTicketMessage, setNewTicketMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isRedirecting, setIsRedirecting] = useState(true);
    const [isAdminSession, setIsAdminSession] = useState(false);
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    const fetchTickets = async () => {
        try {
            const res = await apiFetch('/tickets/');
            if (res.ok) {
                const data = await res.json();
                setTickets(data);
            }
        } catch (err) {
            console.error('Failed to fetch tickets', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            const payload = decodeJWT(token);
            if (payload && payload.role === 'admin') {
                setIsAdminSession(true);
                window.location.replace('/admin/tickets');
                return;
            }
        }
        setIsRedirecting(false);
        fetchTickets();
    }, [router]);

    const handleCreateTicket = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        try {
            const res = await apiFetch('/tickets/', {
                method: 'POST',
                body: JSON.stringify({
                    title: newTicketTitle,
                    initial_message: newTicketMessage,
                    priority: 'medium'
                })
            });
            if (res.ok) {
                setIsModalOpen(false);
                setNewTicketTitle('');
                setNewTicketMessage('');
                fetchTickets();
            } else {
                const data = await res.json();
                alert(data.detail || 'Failed to create ticket');
            }
        } catch (err) {
            console.error('Error creating ticket', err);
            alert('An error occurred');
        } finally {
            setIsSubmitting(false);
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority.toLowerCase()) {
            case 'high': return 'text-red-400 bg-red-400/10 border-red-400/20';
            case 'medium': return 'text-amber-400 bg-amber-400/10 border-amber-400/20';
            default: return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
        }
    };

    if (isRedirecting) return null;

    if (isAdminSession) {
        return (
            <div className="min-h-screen bg-[#020617] flex items-center justify-center p-6 text-center">
                <div className="max-w-md w-full">
                    <h2 className="text-3xl font-black text-white uppercase tracking-tighter mb-2">Admin Session</h2>
                    <button
                        onClick={() => window.location.replace('/admin/tickets')}
                        className="w-full py-4 bg-blue-600 text-white rounded-xl font-bold uppercase"
                    >
                        Enter Console
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#020617] text-slate-200">
            {/* Nav Header */}
            <div className="border-b border-white/5 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white shadow-[0_0_15px_rgba(37,99,235,0.3)]">
                            S
                        </div>
                        <h1 className="text-sm font-black uppercase tracking-widest text-white">My Tickets</h1>
                        <span className="px-1.5 py-0.5 bg-blue-600/20 text-blue-400 border border-blue-500/30 rounded text-[9px] font-black uppercase tracking-tighter ml-2">
                            V2.1 SYNC
                        </span>
                    </div>
                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => setIsModalOpen(true)}
                            className="px-4 py-1.5 bg-blue-600 text-white text-[11px] font-black uppercase tracking-widest rounded-lg hover:bg-blue-500 transition shadow-lg shadow-blue-600/20"
                        >
                            New Ticket
                        </button>
                        <button
                            onClick={handleLogout}
                            className="px-4 py-1.5 border border-white/10 text-slate-400 hover:text-white hover:bg-white/5 transition text-[11px] font-black uppercase tracking-widest rounded-lg"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>

            <main className="max-w-4xl mx-auto p-6 space-y-8">
                {/* AI Global Summary (Experimental) */}
                <div className="bg-slate-900/80 border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <div className="flex items-center gap-2 mb-4">
                        <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
                        <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-400">Systemwide Analysis</h2>
                    </div>
                    <p className="text-sm text-slate-300 leading-relaxed max-w-2xl">
                        AI intelligence protocol is active. Individual ticket summaries are available within each trace.
                        Global account status is currently <span className="text-blue-400 font-bold">Standard</span>.
                    </p>
                </div>

                {loading ? (
                    <div className="flex flex-col items-center justify-center py-20 gap-4">
                        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="text-[10px] uppercase font-black tracking-widest text-slate-500">Retrieving Datapoints...</p>
                    </div>
                ) : (
                    <div className="grid gap-3">
                        {tickets.length === 0 ? (
                            <div className="text-center py-20 bg-white/5 rounded-2xl border border-dashed border-white/10">
                                <p className="text-slate-500 font-bold uppercase tracking-widest text-xs">Zero Tickets Found</p>
                            </div>
                        ) : (
                            tickets.map((ticket) => (
                                <Link key={ticket.id} href={`/tickets/${ticket.id}`} className="block group">
                                    <div className="p-5 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/[0.08] hover:border-blue-500/30 transition-all shadow-xl flex items-center justify-between">
                                        <div className="flex flex-col gap-1.5">
                                            <div className="flex items-center gap-2">
                                                <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase border ${getPriorityColor(ticket.priority)}`}>
                                                    {ticket.priority}
                                                </span>
                                                <span className="text-[9px] text-slate-500 font-bold uppercase">
                                                    {new Date(ticket.created_at).toLocaleDateString()}
                                                </span>
                                            </div>
                                            <h2 className="text-base font-bold text-white group-hover:text-blue-400 transition-colors uppercase tracking-tight leading-none">
                                                {ticket.title}
                                            </h2>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className={`px-2.5 py-1 text-[9px] font-black rounded-lg border uppercase tracking-wider ${ticket.status === 'open' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-slate-800 text-slate-500 border-white/5'
                                                }`}>
                                                {ticket.status}
                                            </span>
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-slate-600 group-hover:text-blue-400 transition-colors" viewBox="0 0 20 20" fill="currentColor">
                                                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                                            </svg>
                                        </div>
                                    </div>
                                </Link>
                            ))
                        )}
                    </div>
                )}
            </main>

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-[#020617]/90 backdrop-blur-sm flex items-center justify-center p-4 z-[100]">
                    <div className="bg-slate-900 border border-white/10 rounded-2xl p-8 max-w-md w-full shadow-2xl">
                        <h2 className="text-xl font-black text-white uppercase tracking-tighter mb-6">Initiate Ticket Trace</h2>
                        <form onSubmit={handleCreateTicket} className="space-y-5">
                            <div>
                                <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Subject</label>
                                <input
                                    type="text"
                                    required
                                    value={newTicketTitle}
                                    onChange={(e) => setNewTicketTitle(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition"
                                    placeholder="Brief technical summary"
                                />
                            </div>
                            <div>
                                <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Full Detail</label>
                                <textarea
                                    required
                                    value={newTicketMessage}
                                    onChange={(e) => setNewTicketMessage(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white h-32 focus:outline-none focus:border-blue-500 transition"
                                    placeholder="Provide all context..."
                                />
                            </div>
                            <div className="flex justify-end gap-4 pt-4">
                                <button
                                    type="button"
                                    onClick={() => setIsModalOpen(false)}
                                    className="px-4 py-2 text-xs font-bold text-slate-500 hover:text-white uppercase transition"
                                >
                                    Abort
                                </button>
                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="bg-blue-600 text-white px-8 py-2 rounded-xl text-xs font-black uppercase tracking-widest hover:bg-blue-500 transition shadow-lg shadow-blue-600/20 disabled:opacity-50"
                                >
                                    {isSubmitting ? 'Transmitting...' : 'Confirm'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
