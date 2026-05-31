import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Target, Zap, Clock, Brain, Activity } from 'lucide-react';

const BACKEND = () => {
    const raw = import.meta.env.VITE_BACKEND_SERVER || 'http://localhost:4000';
    return raw.endsWith('/') ? raw.slice(0, -1) : raw;
};

const MODES = [
    { id: 'quick_mcq', icon: Zap, label: 'Quick MCQ Test', desc: '5 MCQs, timed.' },
    { id: 'standard', icon: Target, label: 'Standard Quiz', desc: 'Mixed format, balanced.' },
    { id: 'challenge', icon: Brain, label: 'Challenge Mode', desc: 'Harder questions, less time.' },
    { id: 'short_answers', icon: Clock, label: 'Short Answers', desc: '5 short answer questions.' }
];

const PracticeModal = ({ jobId, title, onClose, onComplete }) => {
    const [mode, setMode] = useState(null);
    const [loading, setLoading] = useState(false);
    const [questions, setQuestions] = useState([]);
    
    // Simplistic quiz state for demo
    const [activeIdx, setActiveIdx] = useState(0);
    const [score, setScore] = useState(0);
    const [weakTopics, setWeakTopics] = useState([]);
    const [finished, setFinished] = useState(false);
    const [answerText, setAnswerText] = useState('');

    const startPractice = async (selectedMode) => {
        setMode(selectedMode);
        setLoading(true);
        try {
            const res = await fetch(`${BACKEND()}/api/learning/projects/${jobId}/practice`, {
                method: 'POST',
                headers: { 
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ mode: selectedMode })
            });
            const data = await res.json();
            if (data.success) {
                setQuestions(data.questions);
            }
        } catch (err) {
            console.error(err);
        }
        setLoading(false);
    };

    const handleAnswer = async (isCorrect, q, optionStr = null) => {
        if (isCorrect) {
            setScore(prev => prev + 1);
        } else {
            // Track weak topic (using hint or generic)
            setWeakTopics(prev => [...prev, q.hint || q.question.substring(0,20)]);
        }

        if (activeIdx < questions.length - 1) {
            setActiveIdx(prev => prev + 1);
            setAnswerText('');
        } else {
            // Finished
            setFinished(true);
            const finalScore = Math.round(((score + (isCorrect ? 1 : 0)) / questions.length) * 100);
            
            // Save attempt
            try {
                await fetch(`${BACKEND()}/api/learning/projects/${jobId}/attempt`, {
                    method: 'POST',
                    headers: { 
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        mode,
                        score: finalScore,
                        totalQuestions: questions.length,
                        correctAnswers: score + (isCorrect ? 1 : 0),
                        weakTopics
                    })
                });
                if (onComplete) onComplete();
            } catch (e) {}
        }
    };

    const handleShortSubmit = async (q) => {
        try {
            const res = await fetch(`${BACKEND()}/api/questions/check-answer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: 'short', userAnswer: answerText, correctAnswer: q.answer })
            });
            const data = await res.json();
            handleAnswer(data.score >= 70, q);
        } catch (e) {
            handleAnswer(false, q);
        }
    };

    return (
        <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            style={{
                position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                background: 'rgba(5, 11, 20, 0.95)', backdropFilter: 'blur(10px)',
                zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}
        >
            <div className="glass-panel" style={{ width: '100%', maxWidth: '700px', padding: '3rem', position: 'relative' }}>
                <button onClick={onClose} style={{ position: 'absolute', top: 20, right: 20, background: 'none', border: 'none', cursor: 'pointer' }}>
                    <X size={24} color="#fff" />
                </button>

                {!mode ? (
                    <div>
                        <h2 style={{ fontSize: '2rem', textAlign: 'center', marginBottom: '0.5rem' }}>Practice <span style={{ color: 'var(--neon-cyan)' }}>Arena</span></h2>
                        <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginBottom: '2rem' }}>{title}</p>
                        
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            {MODES.map(m => {
                                const Icon = m.icon;
                                return (
                                    <div 
                                        key={m.id}
                                        onClick={() => startPractice(m.id)}
                                        style={{
                                            padding: '1.5rem', background: 'rgba(255,255,255,0.05)',
                                            border: '1px solid var(--glass-border)', borderRadius: '12px',
                                            cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '10px'
                                        }}
                                        onMouseOver={e => e.currentTarget.style.borderColor = 'var(--neon-cyan)'}
                                        onMouseOut={e => e.currentTarget.style.borderColor = 'var(--glass-border)'}
                                    >
                                        <Icon size={32} color="var(--neon-blue)" />
                                        <h4 style={{ fontSize: '1.1rem' }}>{m.label}</h4>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{m.desc}</p>
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                ) : loading ? (
                    <div style={{ textAlign: 'center', padding: '3rem 0' }}>
                        <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}>
                            <Activity size={50} color="var(--neon-violet)" />
                        </motion.div>
                        <p style={{ marginTop: '1rem' }}>Generating fresh questions...</p>
                    </div>
                ) : finished ? (
                    <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                        <h2 style={{ fontSize: '2.5rem', color: 'var(--neon-cyan)', marginBottom: '1rem' }}>
                            {Math.round((score / questions.length) * 100)}%
                        </h2>
                        <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>You answered {score} out of {questions.length} correctly.</p>
                        <button onClick={onClose} className="btn-primary">Return to Library</button>
                    </div>
                ) : questions.length > 0 ? (
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                            <span>Question {activeIdx + 1} of {questions.length}</span>
                            <span>Score: {score}</span>
                        </div>
                        <h3 style={{ fontSize: '1.4rem', marginBottom: '2rem', lineHeight: '1.5' }}>
                            {questions[activeIdx].question}
                        </h3>

                        {questions[activeIdx].type === 'mcq' ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                {questions[activeIdx].options.map((opt, i) => (
                                    <div 
                                        key={i}
                                        onClick={() => handleAnswer(opt === questions[activeIdx].correct_answer, questions[activeIdx], opt)}
                                        style={{
                                            padding: '16px', background: 'rgba(255,255,255,0.05)',
                                            border: '1px solid var(--glass-border)', borderRadius: '8px', cursor: 'pointer'
                                        }}
                                        onMouseOver={e => e.currentTarget.style.background = 'rgba(0, 210, 255, 0.1)'}
                                        onMouseOut={e => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                                    >
                                        {opt}
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <textarea 
                                    value={answerText}
                                    onChange={e => setAnswerText(e.target.value)}
                                    placeholder="Type your answer here..."
                                    style={{
                                        width: '100%', height: '120px', padding: '16px',
                                        background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)',
                                        color: '#fff', borderRadius: '8px', marginBottom: '1rem', fontFamily: 'inherit'
                                    }}
                                />
                                <button 
                                    onClick={() => handleShortSubmit(questions[activeIdx])}
                                    className="btn-primary"
                                    style={{ width: '100%', justifyContent: 'center' }}
                                >
                                    Submit Answer
                                </button>
                            </div>
                        )}
                    </div>
                ) : (
                    <div style={{ textAlign: 'center' }}>Error loading questions.</div>
                )}
            </div>
        </motion.div>
    );
};

export default PracticeModal;
