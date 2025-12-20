'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams } from 'next/navigation';
import { apiFetch } from '@/lib/api';

interface Message {
    id: string;
    content: string;
    sender_id: string;
    is_internal: boolean;
    created_at: string;
}

export default function TicketDetailPage() {
    const params = useParams();
    const ticketId = params.id as string;
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        async function fetchMessages() {
            try {
                const res = await apiFetch(`/tickets/${ticketId}/messages`);
                if (res.ok) {
                    const data = await res.json();
                    setMessages(data);
                }
            } catch (err) {
                console.error('Failed to fetch messages', err);
            } finally {
                setLoading(false);
            }
        }

        fetchMessages();

        // Setup WebSocket
        const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/tickets/ws/${ticketId}`;
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
        if (!newMessage.trim()) return;

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

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto px-4 py-6">
            <h1 className="text-2xl font-bold mb-4">Ticket Trace</h1>

            <div className="flex-1 overflow-y-auto mb-4 bg-white rounded-lg shadow border p-4">
                {loading ? (
                    <div className="text-center py-10">Loading conversation...</div>
                ) : (
                    <div className="space-y-4">
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`flex ${msg.is_internal ? 'justify-center' : 'justify-start'}`}
                            >
                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.is_internal ? 'bg-yellow-50 text-yellow-800 italic text-sm border' :
                                        'bg-blue-50 text-blue-900 border border-blue-100'
                                    }`}>
                                    <p className="whitespace-pre-wrap">{msg.content}</p>
                                    <span className="text-[10px] text-gray-400 mt-1 block">
                                        {new Date(msg.created_at).toLocaleTimeString()}
                                    </span>
                                </div>
                            </div>
                        ))}
                        <div ref={scrollRef} />
                    </div>
                )}
            </div>

            <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Reply to ticket..."
                    className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition"
                >
                    Send
                </button>
            </form>
        </div>
    );
}
