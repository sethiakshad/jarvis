import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { X, Activity, BookOpen, Key, Hash, List, ChevronDown, ChevronUp } from 'lucide-react';

const BACKEND = () => {
    const raw = import.meta.env.VITE_BACKEND_SERVER || 'http://localhost:4000';
    return raw.endsWith('/') ? raw.slice(0, -1) : raw;
};

const RevisionModal = ({ jobId, title, onClose }) => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expandedDef, setExpandedDef] = useState(null);

    useEffect(() => {
        const fetchSummary = async () => {
            try {
                // First try to fetch
                const res = await fetch(`${BACKEND()}/api/learning/projects/${jobId}/revision`, {
                    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                });
                const data = await res.json();
                
                if (res.ok && data.summary) {
                    setSummary(data.summary);
                    setLoading(false);
                } else {
                    // Not ready, generate it
                    const genRes = await fetch(`${BACKEND()}/api/learning/projects/${jobId}/revision/generate`, {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                    });
                    if (genRes.ok) {
                        // Poll for it
                        pollForSummary();
                    } else {
                        throw new Error('Failed to start generation');
                    }
                }
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };
        fetchSummary();
    }, [jobId]);

    const pollForSummary = () => {
        const interval = setInterval(async () => {
            const res = await fetch(`${BACKEND()}/api/learning/projects/${jobId}/revision`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const data = await res.json();
            if (res.ok && data.summary) {
                setSummary(data.summary);
                setLoading(false);
                clearInterval(interval);
            }
        }, 3000);
    };

    return (
        <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            style={{
                position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                background: 'rgba(5, 11, 20, 0.9)', backdropFilter: 'blur(10px)',
                zIndex: 1000, overflowY: 'auto', padding: '2rem'
            }}
        >
            <div style={{ maxWidth: '800px', margin: '0 auto', position: 'relative' }}>
                <button 
                    onClick={onClose}
                    style={{ position: 'absolute', top: 0, right: 0, background: 'none', border: 'none', cursor: 'pointer' }}
                >
                    <X size={32} color="#fff" />
                </button>

                <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
                        <BookOpen size={48} color="var(--neon-cyan)" />
                    </div>
                    <h2 style={{ fontSize: '2rem' }}>Smart Revision</h2>
                    <h3 style={{ color: 'var(--neon-blue)' }}>{title}</h3>
                </div>

                {loading ? (
                    <div style={{ textAlign: 'center', padding: '4rem 0' }}>
                        <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}>
                            <Activity size={60} color="var(--neon-violet)" />
                        </motion.div>
                        <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Synthesizing revision material...</p>
                    </div>
                ) : error ? (
                    <div style={{ textAlign: 'center', color: 'var(--neon-error)' }}>{error}</div>
                ) : (
                    summary && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                            {/* Quick Recap */}
                            <div className="glass-panel" style={{ padding: '2rem', borderLeft: '4px solid var(--neon-cyan)' }}>
                                <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', color: 'var(--neon-cyan)' }}>
                                    <Activity size={20} /> 2-Minute Recap
                                </h4>
                                <p style={{ fontSize: '1.1rem', lineHeight: '1.6' }}>{summary.quickRecap}</p>
                            </div>

                            {/* Key Concepts */}
                            {summary.keyConcepts?.length > 0 && (
                                <div className="glass-panel" style={{ padding: '2rem' }}>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', color: 'var(--neon-blue)' }}>
                                        <Key size={20} /> Key Concepts
                                    </h4>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                                        {summary.keyConcepts.map((c, i) => (
                                            <span key={i} style={{ padding: '8px 16px', background: 'rgba(0, 210, 255, 0.1)', border: '1px solid var(--neon-blue)', borderRadius: '20px', fontSize: '0.9rem' }}>
                                                {c}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Formulas */}
                            {summary.formulas?.length > 0 && (
                                <div className="glass-panel" style={{ padding: '2rem' }}>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', color: 'var(--neon-yellow)' }}>
                                        <Hash size={20} /> Formulas
                                    </h4>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                        {summary.formulas.map((f, i) => (
                                            <div key={i} style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', fontFamily: 'monospace', borderLeft: '3px solid var(--neon-yellow)' }}>
                                                {f}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Definitions */}
                            {summary.definitions?.length > 0 && (
                                <div className="glass-panel" style={{ padding: '2rem' }}>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', color: 'var(--neon-violet)' }}>
                                        <BookOpen size={20} /> Definitions
                                    </h4>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                        {summary.definitions.map((def, i) => (
                                            <div key={i} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid var(--glass-border)', borderRadius: '8px' }}>
                                                <div 
                                                    onClick={() => setExpandedDef(expandedDef === i ? null : i)}
                                                    style={{ padding: '12px 16px', display: 'flex', justifyContent: 'space-between', cursor: 'pointer', fontWeight: 'bold' }}
                                                >
                                                    {def.term}
                                                    {expandedDef === i ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                                                </div>
                                                {expandedDef === i && (
                                                    <div style={{ padding: '0 16px 16px 16px', color: 'var(--text-muted)' }}>
                                                        {def.definition}
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Exam Points */}
                            {summary.examPoints?.length > 0 && (
                                <div className="glass-panel" style={{ padding: '2rem', borderBottom: '4px solid #ff3366' }}>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', color: '#ff3366' }}>
                                        <List size={20} /> High-Yield Exam Points
                                    </h4>
                                    <ul style={{ paddingLeft: '1.5rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                        {summary.examPoints.map((pt, i) => (
                                            <li key={i} style={{ color: 'var(--text-main)', lineHeight: '1.5' }}>{pt}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )
                )}
            </div>
        </motion.div>
    );
};

export default RevisionModal;
