'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiFetch, decodeJWT } from '@/lib/api';

interface Message {
    id: string;
    content: string;
    sender_id: string;
    is_internal: boolean;
    created_at: string;
    sentiment?: string;
    summary?: string;
    history_summary?: string;
    draft_response?: string;
    extracted_fields?: Record<string, any>;
    predicted_csat?: number;
    is_chronic?: boolean;
}

interface Ticket {
    id: string;
    title: string;
    status: string;
    priority: string;
}

export default function TicketDetailPage() {
    const params = useParams();
    const router = useRouter();
    const ticketId = params.id as string;

    const [ticket, setTicket] = useState<Ticket | null>(null);

    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [isAdmin, setIsAdmin] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            const payload = decodeJWT(token);
            if (payload) {
                setIsAdmin(payload.role === 'admin');
            }
        }

        async function init() {
            try {
                // Fetch Ticket Details
                const ticketRes = await apiFetch(`/tickets/${ticketId}`);
                if (ticketRes.ok) {
                    const ticketData = await ticketRes.json();
                    setTicket(ticketData);
                }

                // Fetch Messages
                const res = await apiFetch(`/tickets/${ticketId}/messages`);
                if (res.ok) {
                    const data = await res.json();
                    setMessages(data);
                }
            } catch (err) {
                console.error('Failed to fetch data', err);
            } finally {
                setLoading(false);
            }
        }

        init();

        // Setup WebSocket
        const wsBaseUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8001/api/v1';
        const wsUrl = `${wsBaseUrl}/tickets/ws/${ticketId}${token ? `?token=${token}` : ''}`;
        const socket = new WebSocket(wsUrl);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'NEW_MESSAGE') {
                setMessages((prev) => [...prev, data]);
            }
        };

        return () => socket.close();
    }, [ticketId]);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newMessage.trim() || ticket?.status === 'closed') return;

        try {
            const res = await apiFetch(`/tickets/${ticketId}/messages`, {
                method: 'POST',
                body: JSON.stringify({ content: newMessage }),
            });

            if (res.ok) {
                const data = await res.json();
                setMessages((prev) => [...prev, data]);
                setNewMessage('');
            }
        } catch (err) {
            console.error('Failed to send message', err);
        }
    };

    const handleCloseTicket = async () => {
        if (!confirm('Are you sure you want to close this ticket?')) return;
        try {
            const res = await apiFetch(`/tickets/${ticketId}/close`, { method: 'PATCH' });
            if (res.ok) {
                const updatedTicket = await res.json();
                setTicket(updatedTicket);
            }
        } catch (err) {
            console.error('Failed to close ticket', err);
        }
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center h-screen bg-[#020617] gap-4">
            <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">Retrieving Ticket Trace...</p>
        </div>
    );

    const isClosed = ticket?.status === 'closed';

    return (
        <div className="flex flex-col h-screen bg-[#020617] text-slate-200">
            {/* Nav Header */}
            <div className="border-b border-white/5 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
                    <button
                        onClick={() => router.back()}
                        className="text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-white transition flex items-center gap-2"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back
                    </button>
                    <div className="flex items-center gap-2">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Trace Protocol</span>
                        <span className="px-1.5 py-0.5 bg-blue-600/20 text-blue-400 border border-blue-500/30 rounded text-[9px] font-black uppercase tracking-tighter">
                            V2.2 SYNC
                        </span>
                    </div>
                    <div className="flex items-center gap-3">
                        {isAdmin && !isClosed && (
                            <button
                                onClick={handleCloseTicket}
                                className="px-4 py-1.5 bg-red-600/10 text-red-500 border border-red-500/30 rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-red-600 hover:text-white transition"
                            >
                                Close Ticket
                            </button>
                        )}
                        <button
                            onClick={handleLogout}
                            className="px-4 py-1.5 border border-white/10 text-slate-400 hover:text-white hover:bg-white/5 transition text-[10px] font-black uppercase tracking-widest rounded-lg"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div>

            {/* Ticket Subject Banner */}
            <div className="bg-slate-900/30 border-b border-white/5 py-8 px-6">
                <div className="max-w-4xl mx-auto">
                    <div className="flex items-center gap-3 mb-2">
                        <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase border ${ticket?.priority === 'high' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                            ticket?.priority === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                                'bg-blue-500/10 text-blue-400 border-blue-500/20'
                            }`}>
                            {ticket?.priority}
                        </span>
                        {isClosed && (
                            <span className="px-2 py-0.5 bg-slate-800 text-slate-500 border border-white/5 rounded text-[8px] font-black uppercase tracking-widest">
                                RESOLVED
                            </span>
                        )}
                    </div>
                    <h1 className="text-3xl font-black text-white uppercase tracking-tighter leading-none mb-1">
                        {ticket?.title}
                    </h1>
                    <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">
                        Stream ID: <span className="text-slate-400">{ticket?.id}</span>
                    </p>
                </div>
            </div>

            {/* Message Stream */}
            <div className="flex-1 overflow-y-auto bg-[#020617]">
                <div className="max-w-4xl mx-auto p-6 space-y-8">
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`flex flex-col ${msg.is_internal ? 'items-center' : 'items-start'}`}
                        >
                            {/* AI Insights HUD */}
                            {msg.is_internal && (msg.summary || msg.sentiment || msg.is_chronic) && (
                                <div className={`w-[95%] mb-6 p-6 rounded-2xl shadow-2xl border-t-2 transition-all ${msg.is_chronic ? 'bg-red-950/40 border-red-500/50' : 'bg-slate-900/60 border-blue-500/50 backdrop-blur-md'
                                    }`}>
                                    <div className="flex justify-between items-start mb-6">
                                        <div className="flex flex-col gap-1">
                                            <div className="flex items-center gap-2">
                                                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
                                                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-400">
                                                    AI Intelligence Suite
                                                </span>
                                            </div>
                                            {msg.is_chronic && (
                                                <span className="text-[10px] text-red-400 font-bold flex items-center gap-1 animate-pulse mt-1">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                                    </svg>
                                                    CRITICAL: CHRONIC ISSUE DETECTED
                                                </span>
                                            )}
                                        </div>
                                        <div className="flex gap-3">
                                            {msg.predicted_csat && (
                                                <div className="flex items-center gap-1.5 bg-white/5 px-2.5 py-1 rounded-lg border border-white/10">
                                                    <span className="text-[9px] font-black text-slate-500 uppercase tracking-tighter">CSAT</span>
                                                    <div className="flex gap-1">
                                                        {[1, 2, 3, 4, 5].map(star => (
                                                            <div key={star} className={`w-1.5 h-1.5 rounded-full ${star <= (msg.predicted_csat || 0) ? 'bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.5)]' : 'bg-white/10'}`} />
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                            {msg.sentiment && (
                                                <span className={`text-[9px] px-2.5 py-1 rounded-lg font-black tracking-widest uppercase border ${msg.sentiment.toLowerCase().includes('frust') ? 'bg-red-500/20 text-red-500 border-red-500/30' : 'bg-green-500/20 text-green-500 border-green-500/30'
                                                    }`}>
                                                    {msg.sentiment}
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <div className="space-y-4">
                                            {msg.summary && (
                                                <div>
                                                    <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-1.5">Executive Summary</p>
                                                    <p className="text-sm text-slate-200 leading-relaxed font-medium">{msg.summary}</p>
                                                </div>
                                            )}
                                            {msg.extracted_fields && Object.keys(msg.extracted_fields).length > 0 && (
                                                <div>
                                                    <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-1.5">Parsed Context</p>
                                                    <div className="flex flex-wrap gap-1.5">
                                                        {Object.entries(msg.extracted_fields).map(([key, value]) => (
                                                            <span key={key} className="px-2 py-0.5 bg-blue-500/10 text-blue-300 text-[10px] rounded-md border border-blue-500/20 font-bold uppercase tracking-tight">
                                                                {key}: {String(value)}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>

                                        <div className="bg-slate-950/50 rounded-xl p-4 border border-white/5 space-y-3">
                                            <div className="flex justify-between items-center">
                                                <p className="text-[9px] text-blue-400 uppercase font-black tracking-widest">Actionable Draft</p>
                                                <button
                                                    onClick={() => setNewMessage(msg.draft_response || '')}
                                                    className="text-[9px] bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded-lg transition font-black uppercase tracking-widest shadow-lg shadow-blue-600/20"
                                                >
                                                    Use Draft
                                                </button>
                                            </div>
                                            <p className="text-xs text-slate-400 italic leading-relaxed">
                                                "{msg.draft_response || "Analytical model is refining a draft..."}"
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Message Bubble */}
                            <div className={`max-w-[85%] p-5 rounded-3xl transition-all ${msg.is_internal ?
                                'bg-white text-slate-950 border-2 border-blue-500 shadow-[0_0_30px_rgba(37,99,235,0.1)] self-center' :
                                'bg-slate-900/80 text-white border border-white/10 backdrop-blur-sm self-start'
                                }`}>
                                <p className="whitespace-pre-wrap text-sm font-medium leading-relaxed tracking-tight">{msg.content}</p>
                                <div className="flex items-center justify-between mt-4">
                                    <div className="flex items-center gap-2">
                                        <div className={`w-5 h-5 rounded-full flex items-center justify-center text-[8px] font-black ${msg.is_internal ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300'
                                            }`}>
                                            {msg.is_internal ? 'AI' : 'US'}
                                        </div>
                                        <span className={`text-[10px] font-bold uppercase tracking-tighter ${msg.is_internal ? 'text-blue-600' : 'text-slate-500'
                                            }`}>
                                            {msg.is_internal ? 'Productivity Agent' : 'Customer'}
                                        </span>
                                    </div>
                                    <span className="text-[9px] text-slate-500 font-bold uppercase">
                                        {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                    <div ref={scrollRef} className="h-4" />
                </div>
            </div>

            {/* Input Fixed Bottom */}
            <div className="bg-slate-900/50 backdrop-blur-2xl border-t border-white/5 p-6">
                <div className="max-w-4xl mx-auto">
                    {!isClosed ? (
                        <form onSubmit={handleSendMessage} className="relative group">
                            <input
                                type="text"
                                value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                                placeholder="Transmit message to ticket trace..."
                                className="w-full bg-[#020617] border border-white/10 rounded-2xl px-6 py-5 text-white text-sm font-medium focus:outline-none focus:border-blue-500/50 transition-all placeholder:text-slate-600 pr-32"
                            />
                            <button
                                type="submit"
                                className="absolute right-3 top-1/2 -translate-y-1/2 bg-blue-600 text-white px-6 py-2.5 rounded-xl text-[11px] font-black uppercase tracking-widest hover:bg-blue-500 transition shadow-xl shadow-blue-600/30"
                            >
                                Send
                            </button>
                        </form>
                    ) : (
                        <div className="py-4 bg-slate-950/50 border border-slate-800 rounded-2xl text-center">
                            <p className="text-[10px] uppercase font-black tracking-widest text-slate-600">Trace Termination Confirmed • Resolved</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
