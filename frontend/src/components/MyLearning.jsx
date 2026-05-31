import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Play, BookOpen, Clock, Activity, Bookmark, Trash2, Search, Target, Video } from 'lucide-react';
import RevisionModal from './RevisionModal';
import PracticeModal from './PracticeModal';

const BACKEND = () => {
    const raw = import.meta.env.VITE_BACKEND_SERVER || 'http://localhost:4000';
    return raw.endsWith('/') ? raw.slice(0, -1) : raw;
};

const MyLearning = () => {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [filter, setFilter] = useState('all'); // all, bookmarked, weak
    const [activeRevision, setActiveRevision] = useState(null); // jobId
    const [activePractice, setActivePractice] = useState(null); // jobId
    const navigate = useNavigate();

    const fetchProjects = async () => {
        try {
            const res = await fetch(`${BACKEND()}/api/learning/projects`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const data = await res.json();
            if (data.success) {
                setProjects(data.projects);
            }
        } catch (err) {
            console.error(err);
        }
        setLoading(false);
    };

    useEffect(() => {
        if (!localStorage.getItem('token')) {
            navigate('/login');
            return;
        }
        fetchProjects();
    }, [navigate]);

    const toggleBookmark = async (jobId) => {
        try {
            await fetch(`${BACKEND()}/api/learning/projects/${jobId}/bookmark`, {
                method: 'PATCH',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            // optimistic update
            setProjects(projects.map(p => p.jobId === jobId ? { ...p, bookmarked: !p.bookmarked } : p));
        } catch (err) {}
    };

    const deleteProject = async (jobId) => {
        if (!window.confirm("Are you sure you want to remove this project from your library?")) return;
        try {
            await fetch(`${BACKEND()}/api/learning/projects/${jobId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            setProjects(projects.filter(p => p.jobId !== jobId));
        } catch (err) {}
    };

    const navigateToVideo = (jobId) => {
        // Just a simple routing if we wanted, or we could load it in a modal.
        // For now, alert that it would load the VideoPreview.
        alert(`Opening video player for job ${jobId}`);
    };

    // Filter logic
    const filteredProjects = projects.filter(p => {
        if (search && !p.title.toLowerCase().includes(search.toLowerCase()) && !p.focusTopic.toLowerCase().includes(search.toLowerCase())) return false;
        if (filter === 'bookmarked' && !p.bookmarked) return false;
        if (filter === 'weak' && p.masteryScore > 0 && p.masteryScore < 60) return true; // only low mastery
        if (filter === 'weak' && p.masteryScore >= 60) return false;
        return true;
    });

    // Spaced repetition check
    const spacedRepetitionProject = projects.find(p => {
        if (!p.lastWatched) return false;
        const days = (new Date() - new Date(p.lastWatched)) / (1000 * 60 * 60 * 24);
        return days > 3 && p.masteryScore < 80;
    });

    return (
        <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem' }}>
            <div className="app-container">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '2rem' }}>
                    <div>
                        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Learning <span style={{ color: 'var(--neon-violet)' }}>Library</span></h1>
                        <p style={{ color: 'var(--text-muted)' }}>Your personalized AI knowledge vault.</p>
                    </div>
                    
                    <button onClick={() => navigate('/dashboard')} className="btn-primary" style={{ padding: '10px 20px', fontSize: '0.9rem' }}>
                        + Generate New Topic
                    </button>
                </div>

                {/* Spaced Repetition Banner */}
                {spacedRepetitionProject && (
                    <motion.div 
                        initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
                        className="glass-panel" style={{ padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(138, 43, 226, 0.1)', border: '1px solid var(--neon-violet)', marginBottom: '3rem' }}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                            <div style={{ padding: '10px', background: 'rgba(138, 43, 226, 0.2)', borderRadius: '50%' }}>
                                <Clock size={24} color="var(--neon-violet)" />
                            </div>
                            <div>
                                <h4 style={{ color: 'var(--neon-violet)', marginBottom: '4px' }}>Spaced Repetition Alert</h4>
                                <p style={{ fontSize: '0.9rem' }}>You learned <strong>{spacedRepetitionProject.title}</strong> a few days ago. Time for a quick revision!</p>
                            </div>
                        </div>
                        <button onClick={() => setActiveRevision(spacedRepetitionProject)} style={{ padding: '8px 16px', background: 'var(--neon-violet)', color: '#fff', border: 'none', borderRadius: '20px', cursor: 'pointer', fontWeight: 'bold' }}>
                            Revise Now
                        </button>
                    </motion.div>
                )}

                {/* Filters */}
                <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                    <div style={{ position: 'relative', flex: 1, maxWidth: '400px' }}>
                        <Search size={18} style={{ position: 'absolute', top: '50%', left: '16px', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                        <input 
                            type="text" 
                            placeholder="Search topics..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            style={{ width: '100%', padding: '12px 16px 12px 48px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', color: '#fff', borderRadius: '8px' }}
                        />
                    </div>
                    <select 
                        value={filter} onChange={e => setFilter(e.target.value)}
                        style={{ padding: '12px 16px', background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)', color: '#fff', borderRadius: '8px' }}
                    >
                        <option value="all" style={{color: '#000'}}>All Topics</option>
                        <option value="bookmarked" style={{color: '#000'}}>Bookmarked</option>
                        <option value="weak" style={{color: '#000'}}>Needs Revision (Low Mastery)</option>
                    </select>
                </div>

                {/* Grid */}
                {loading ? (
                    <div style={{ textAlign: 'center', padding: '4rem' }}><Activity size={40} className="text-neon" color="var(--neon-cyan)" /></div>
                ) : filteredProjects.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '5rem', background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px dashed var(--glass-border)' }}>
                        <BookOpen size={48} color="var(--text-muted)" style={{ marginBottom: '1rem', opacity: 0.5 }} />
                        <h3 style={{ color: 'var(--text-muted)' }}>No projects found.</h3>
                    </div>
                ) : (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '2rem' }}>
                        <AnimatePresence>
                            {filteredProjects.map(p => (
                                <motion.div 
                                    layout
                                    initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }}
                                    key={p.jobId} 
                                    className="glass-panel"
                                    style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
                                >
                                    {/* Thumbnail Placeholder */}
                                    <div style={{ height: '160px', background: 'radial-gradient(circle at top right, rgba(0, 210, 255, 0.2), #050b14)', borderBottom: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                                        <div style={{ position: 'absolute', top: 12, right: 12, cursor: 'pointer' }} onClick={() => toggleBookmark(p.jobId)}>
                                            <Bookmark size={24} color={p.bookmarked ? 'var(--neon-yellow)' : 'rgba(255,255,255,0.3)'} fill={p.bookmarked ? 'var(--neon-yellow)' : 'none'} />
                                        </div>
                                        <div style={{ position: 'absolute', top: 12, left: 12, background: 'rgba(0,0,0,0.6)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', border: '1px solid var(--glass-border)' }}>
                                            {p.audioLanguage.toUpperCase()}
                                        </div>
                                        <Video size={48} color="rgba(0, 255, 204, 0.2)" />
                                    </div>
                                    
                                    <div style={{ padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                                        <h3 style={{ fontSize: '1.2rem', marginBottom: '4px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                            {p.title}
                                        </h3>
                                        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                                            Generated {new Date(p.createdAt).toLocaleDateString()}
                                        </p>

                                        {/* Progress bars */}
                                        <div style={{ marginBottom: '1rem' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px' }}>
                                                <span style={{ color: 'var(--text-muted)' }}>Mastery Score</span>
                                                <span style={{ color: 'var(--neon-cyan)', fontWeight: 'bold' }}>{p.masteryScore}%</span>
                                            </div>
                                            <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                                                <div style={{ width: `${p.masteryScore}%`, height: '100%', background: 'var(--neon-cyan)' }} />
                                            </div>
                                        </div>

                                        {/* Weak concepts alert */}
                                        {p.weakConcepts?.length > 0 && (
                                            <div style={{ background: 'rgba(255, 68, 68, 0.1)', border: '1px solid rgba(255, 68, 68, 0.3)', padding: '10px', borderRadius: '8px', fontSize: '0.8rem', marginBottom: '1.5rem', color: '#ffaaaa' }}>
                                                <strong>Needs Work:</strong> {p.weakConcepts.slice(0, 2).join(', ')}
                                            </div>
                                        )}

                                        <div style={{ flex: 1 }} />

                                        {/* Actions */}
                                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '8px' }}>
                                            <button onClick={() => navigateToVideo(p.jobId)} style={{ padding: '8px', background: 'rgba(0, 210, 255, 0.1)', border: '1px solid var(--neon-blue)', color: 'var(--neon-blue)', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '0.85rem' }}>
                                                <Play size={14} /> Watch
                                            </button>
                                            <button onClick={() => setActiveRevision(p)} style={{ padding: '8px', background: 'rgba(138, 43, 226, 0.1)', border: '1px solid var(--neon-violet)', color: 'var(--neon-violet)', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '0.85rem' }}>
                                                <BookOpen size={14} /> Revise
                                            </button>
                                        </div>
                                        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: '8px' }}>
                                            <button onClick={() => setActivePractice(p)} style={{ padding: '8px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid var(--glass-border)', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '0.85rem' }}>
                                                <Target size={14} /> Practice Questions
                                            </button>
                                            <button onClick={() => deleteProject(p.jobId)} style={{ padding: '8px', background: 'none', border: '1px solid var(--glass-border)', color: 'var(--text-muted)', borderRadius: '6px', cursor: 'pointer' }}>
                                                <Trash2 size={14} />
                                            </button>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                )}
            </div>

            {/* Modals */}
            <AnimatePresence>
                {activeRevision && (
                    <RevisionModal jobId={activeRevision.jobId} title={activeRevision.title} onClose={() => setActiveRevision(null)} />
                )}
                {activePractice && (
                    <PracticeModal jobId={activePractice.jobId} title={activePractice.title} onClose={() => setActivePractice(null)} onComplete={fetchProjects} />
                )}
            </AnimatePresence>
        </div>
    );
};

export default MyLearning;
