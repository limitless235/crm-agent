'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/api';
import Link from 'next/link';

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

    useEffect(() => {
        async function fetchTickets() {
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
        }
        fetchTickets();
    }, []);

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">My Tickets</h1>
                <button className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">
                    New Ticket
                </button>
            </div>

            {loading ? (
                <div className="text-center py-10">Loading tickets...</div>
            ) : (
                <div className="grid gap-4">
                    {tickets.length === 0 ? (
                        <div className="text-center py-10 text-gray-500">No tickets found.</div>
                    ) : (
                        tickets.map((ticket) => (
                            <Link key={ticket.id} href={`/tickets/${ticket.id}`} className="block">
                                <div className="p-4 bg-white rounded-lg shadow border hover:border-blue-500 transition">
                                    <div className="flex justify-between items-start">
                                        <h2 className="text-lg font-semibold">{ticket.title}</h2>
                                        <span className={`px-2 py-1 text-xs font-bold rounded ${ticket.status === 'open' ? 'bg-green-100 text-green-700' :
                                                ticket.status === 'in_progress' ? 'bg-blue-100 text-blue-700' :
                                                    'bg-gray-100 text-gray-700'
                                            }`}>
                                            {ticket.status.toUpperCase()}
                                        </span>
                                    </div>
                                    <div className="mt-2 text-sm text-gray-500">
                                        Priority: {ticket.priority} • Created at: {new Date(ticket.created_at).toLocaleString()}
                                    </div>
                                </div>
                            </Link>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
