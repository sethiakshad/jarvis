import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Pause, Maximize, Download, Film, Layers, CheckCircle, AlertCircle, HelpCircle, ChevronDown, ChevronUp, Activity, Lightbulb, Cpu } from 'lucide-react';
import { useVideo } from '../App';

// ── Isolated Components ──────────────────────────────────────────────────────

const CountdownRing = React.memo(({ timeLeft }) => {
  const dashArray = 163.3;
  const offset = dashArray - (timeLeft / 20) * dashArray;

  return (
    <div style={{ position: 'relative', width: '60px', height: '60px' }}>
      <svg width="60" height="60" viewBox="0 0 60 60">
        <circle cx="30" cy="30" r="26" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="4" />
        <motion.circle 
          cx="30" cy="30" r="26" fill="none" 
          stroke={timeLeft < 5 ? '#ff3366' : 'var(--neon-cyan)'} 
          strokeWidth="4"
          strokeDasharray={dashArray}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'linear' }}
          strokeLinecap="round"
          transform="rotate(-90 30 30)"
        />
      </svg>
      <div style={{ 
        position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '1.2rem', fontWeight: 900, color: timeLeft < 5 ? '#ff3366' : '#fff'
      }}>
        {timeLeft}
      </div>
    </div>
  );
});

const BACKEND = () => {
  const raw = import.meta.env.VITE_BACKEND_SERVER || 'http://localhost:4000';
  return raw.endsWith('/') ? raw.slice(0, -1) : raw;
};


const VideoPreview = () => {
  const { videoData } = useVideo();
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);

  // Quiz state
  const [questions, setQuestions] = useState([]);
  const [userAnswers, setUserAnswers] = useState({}); // { qId: { result: null, score: null, feedback: null, showAnswer: false } }
  const [isFetchingQuestions, setIsFetchingQuestions] = useState(false);

  // Gamified System State
  const [currentLevel, setCurrentLevel] = useState(1);
  const [unlockedLevel, setUnlockedLevel] = useState(() => {
    return parseInt(localStorage.getItem('iiit_pune_quiz_unlocked_level')) || 1;
  });
  const [totalScore, setTotalScore] = useState(() => {
    return parseInt(localStorage.getItem('iiit_pune_quiz_total_score')) || 0;
  });
  const [levelStatus, setLevelStatus] = useState(null); // 'success' | 'retry' | null
  const [timeLeft, setTimeLeft] = useState(20); // 20s per question
  const [activeQuestionId, setActiveQuestionId] = useState(null);
  const [activeQuestionIdx, setActiveQuestionIdx] = useState(0);
  const [quizStarted, setQuizStarted] = useState(false);
  const [streak, setStreak] = useState(0);
  const [showFeedback, setShowFeedback] = useState(null); // { type: 'success' | 'error', text: string }
  const [xpPopup, setXpPopup] = useState(null); // { x: number, y: number, text: string }
  const timerRef = useRef(null);

  // Persistence
  React.useEffect(() => {
    localStorage.setItem('iiit_pune_quiz_unlocked_level', unlockedLevel);
  }, [unlockedLevel]);

  React.useEffect(() => {
    localStorage.setItem('iiit_pune_quiz_total_score', totalScore);
  }, [totalScore]);

  React.useEffect(() => {
    const levelQs = questions.filter(q => q.level === currentLevel);
    const firstUnanswered = levelQs.findIndex(q => userAnswers[q.id]?.correct === undefined);
    
    if (firstUnanswered !== -1) {
      setActiveQuestionIdx(firstUnanswered);
      setLevelStatus(null);
      // Auto-start if they are resuming a partially answered level
      if (firstUnanswered > 0) setQuizStarted(true);
      else setQuizStarted(false);
    } else if (levelQs.length > 0) {
      // All answered
      setActiveQuestionIdx(levelQs.length - 1);
      setQuizStarted(true);
      checkLevelCompletion();
    }
    setActiveQuestionId(null);
    setShowFeedback(null);
  }, [currentLevel, questions]); // questions added here to handle initial load


  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = () => {
    if (!videoRef.current) return;
    const pct = (videoRef.current.currentTime / videoRef.current.duration) * 100;
    setProgress(isNaN(pct) ? 0 : pct);
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) setDuration(videoRef.current.duration);
  };

  const handleSeek = (e) => {
    if (!videoRef.current) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    videoRef.current.currentTime = pct * videoRef.current.duration;
  };

  const handleFullscreen = () => {
    videoRef.current?.requestFullscreen?.();
  };

  // ── Quiz Logic ────────────────────────────────────────────────────────────
  React.useEffect(() => {
    if (videoData?.jobId) {
      fetchQuestions(videoData.jobId);
    }
  }, [videoData?.jobId]);

  // Debug log to terminal when question changes
  React.useEffect(() => {
    const levelQs = questions.filter(q => q.level === currentLevel);
    const q = levelQs[activeQuestionIdx];
    if (q && quizStarted) {
      fetch(`${BACKEND()}/api/questions/log-current`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q.question, answer: q.correct_answer || q.answer })
      }).catch(() => {});
    }
  }, [activeQuestionIdx, currentLevel, questions, quizStarted]);

  const fetchQuestions = async (id) => {
    setIsFetchingQuestions(true);
    try {
      const res = await fetch(`${BACKEND()}/api/questions/${id}`);
      if (res.ok) {
        const data = await res.json();
        setQuestions(data.questions || []);
      }
    } catch (err) {
      console.error("Failed to fetch questions:", err);
    } finally {
      setIsFetchingQuestions(false);
    }
  };

  const handleMcqClick = async (q, option) => {
    stopTimer();
    try {
      const res = await fetch(`${BACKEND()}/api/questions/check-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'mcq',
          userAnswer: option,
          correctAnswer: q.correct_answer
        })
      });
      const result = await res.json();
      if (result.correct) {
        setTotalScore(prev => prev + 10);
        setStreak(prev => prev + 1);
        triggerFeedback('success', 'Perfect!', 10);
      } else {
        setStreak(0);
        triggerFeedback('error', 'Incorrect', 0);
      }
      setUserAnswers(prev => ({
        ...prev,
        [q.id]: { selected: option, ...result }
      }));

      // Auto-advance
      setTimeout(nextQuestion, 2000);
    } catch (err) {
      console.error("MCQ check failed:", err);
    }
  };

  const handleShortSubmit = async (q, answer) => {
    if (!answer.trim()) return;
    stopTimer();
    setUserAnswers(prev => ({
      ...prev,
      [q.id]: { ...prev[q.id], submitting: true }
    }));

    try {
      const res = await fetch(`${BACKEND()}/api/questions/check-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'short',
          userAnswer: answer,
          correctAnswer: q.answer
        })
      });
      const result = await res.json();
      if (result.score && result.score >= 70) {
        setTotalScore(prev => prev + 10);
        setStreak(prev => prev + 1);
        triggerFeedback('success', `${result.score}% Accuracy!`, 10);
      } else {
        setStreak(0);
        triggerFeedback('error', 'Low Accuracy', 0);
      }
      setUserAnswers(prev => ({
        ...prev,
        [q.id]: { submitted: answer, ...result, submitting: false }
      }));

      // Auto-advance
      setTimeout(nextQuestion, 2000);
    } catch (err) {
      console.error("Short answer check failed:", err);
      setUserAnswers(prev => ({
        ...prev,
        [q.id]: { ...prev[q.id], submitting: false }
      }));
    }
  };


  const toggleShowHint = (qId) => {
    if (!userAnswers[qId]?.showHint) {
      setTotalScore(prev => Math.max(0, prev - 2)); // Penalty for hint
    }
    setUserAnswers(prev => ({
      ...prev,
      [qId]: { ...prev[qId], showHint: !prev[qId]?.showHint }
    }));
  };

  const toggleShowAnswer = (qId) => {
    setUserAnswers(prev => ({
      ...prev,
      [qId]: { 
        ...prev[qId], 
        showAnswer: !prev[qId]?.showAnswer,
        everRevealed: true // Mark that they've seen it at least once
      }
    }));
  };

  // Timer Logic
  const startTimer = (qId) => {
    stopTimer();
    setTimeLeft(20);
    setActiveQuestionId(qId);
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          stopTimer();
          handleTimerEnd(qId);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const stopTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current);
  };

  const handleTimerEnd = (qId) => {
    const q = questions.find(item => item.id === qId);
    if (!q) return;
    
    setStreak(0);
    triggerFeedback('error', "TIME'S UP!");

    setUserAnswers(prev => ({
      ...prev,
      [qId]: { 
        ...prev[qId], 
        selected: 'TIMEOUT', 
        correct: false, 
        feedback: "Time's up! Marked as incorrect." 
      }
    }));

    // Auto-advance
    setTimeout(nextQuestion, 2000);
  };

  const retryLevel = async () => {
    setLevelStatus('refreshing'); // UI state for loading
    try {
      const res = await fetch(`${BACKEND()}/api/questions/refresh-level`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobId: videoData.jobId, level: currentLevel })
      });
      if (res.ok) {
        const data = await res.json();
        setQuestions(data.questions);
        
        // Reset level-specific answers
        const levelQIds = data.questions.filter(q => q.level === currentLevel).map(q => q.id);
        setUserAnswers(prev => {
          const next = { ...prev };
          levelQIds.forEach(id => delete next[id]);
          return next;
        });

        setLevelStatus(null);
        setActiveQuestionIdx(0);
        setActiveQuestionId(null);
        setStreak(0);
        setQuizStarted(false); // Show Start button again
        setTotalScore(0); // Reset score as requested
      }
    } catch (err) {
      console.error("Level refresh failed:", err);
      setLevelStatus('retry');
    }
  };

  React.useEffect(() => {
    const levelQs = questions.filter(q => q.level === currentLevel);
    if (levelQs.length === 0) return;

    const allAnswered = levelQs.every(q => userAnswers[q.id]?.correct !== undefined);
    
    if (allAnswered && !levelStatus) {
      const timer = setTimeout(() => {
        checkLevelCompletion();
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [userAnswers, questions, currentLevel, levelStatus]);

  const checkLevelCompletion = () => {
    const levelQuestions = questions.filter(q => q.level === currentLevel);
    const allCorrect = levelQuestions.every(q => userAnswers[q.id]?.correct === true || (userAnswers[q.id]?.score && userAnswers[q.id]?.score >= 70));
    
    if (allCorrect) {
      setLevelStatus('success');
      if (currentLevel === unlockedLevel && unlockedLevel < 3) {
        setUnlockedLevel(prev => prev + 1);
      }
    } else {
      setLevelStatus('retry');
    }
  };


  const goToNextLevel = () => {
    if (currentLevel < 3) {
      setCurrentLevel(prev => prev + 1);
      setLevelStatus(null);
      setActiveQuestionId(null);
      setActiveQuestionIdx(0);
    }
  };

  const nextQuestion = () => {
    const levelQs = questions.filter(q => q.level === currentLevel);
    if (activeQuestionIdx < levelQs.length - 1) {
      setActiveQuestionIdx(prev => prev + 1);
      setShowFeedback(null);
    }
    // checkLevelCompletion is now handled by useEffect with a delay
  };

  const triggerFeedback = (type, text, points = 0) => {
    setShowFeedback({ type, text });
    if (points !== 0) {
      setXpPopup({ text: points > 0 ? `+${points} XP` : `${points} XP` });
      setTimeout(() => setXpPopup(null), 1000);
    }
  };



  const fmtTime = (s) => {
    if (!s || isNaN(s)) return '0:00';
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60).toString().padStart(2, '0');
    return `${m}:${sec}`;
  };

  return (
    <section id="video-preview-section">
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
          Final <span style={{ color: 'var(--neon-cyan)' }}>Render</span>
        </h2>
        <p style={{ color: 'var(--text-muted)' }}>
          {videoData
            ? 'Your AI-generated educational video is ready.'
            : 'The fully synthesized educational video ready for deployment.'}
        </p>
      </div>

      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <AnimatePresence mode="wait">

          {/* ── Real Video Player ─────────────────────────────────────────── */}
          {videoData ? (
            <motion.div
              key="real-player"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.6 }}
              className="glass-panel"
              style={{
                padding: 0, overflow: 'hidden',
                boxShadow: '0 0 60px rgba(0, 255, 204, 0.15), 0 20px 50px rgba(0,0,0,0.5)',
                border: '1px solid rgba(0,255,204,0.3)'
              }}
            >
              {/* Status badge */}
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 20px',
                background: 'rgba(0,255,204,0.05)',
                borderBottom: '1px solid rgba(0,255,204,0.1)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <motion.div
                    animate={{ scale: [1, 1.3, 1], opacity: [0.7, 1, 0.7] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00ffcc', boxShadow: '0 0 8px #00ffcc' }}
                  />
                  <span style={{ color: '#00ffcc', fontSize: '0.85rem', fontWeight: 600 }}>
                    {videoData.statusMessage || 'Video Ready'}
                  </span>
                </div>
                {videoData.scenesRendered !== undefined && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Layers size={14} color="var(--text-muted)" />
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                      {videoData.scenesRendered}/{videoData.scenesTotal} scenes rendered
                    </span>
                  </div>
                )}
              </div>

              {/* Video element */}
              <div style={{
                width: '100%', aspectRatio: '16/9',
                background: '#000', position: 'relative',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <video
                  ref={videoRef}
                  src={videoData.url}
                  style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                  onTimeUpdate={handleTimeUpdate}
                  onLoadedMetadata={handleLoadedMetadata}
                  onEnded={() => setIsPlaying(false)}
                  onClick={togglePlay}
                />

                {/* Play overlay when paused */}
                <AnimatePresence>
                  {!isPlaying && (
                    <motion.div
                      key="overlay"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      onClick={togglePlay}
                      style={{
                        position: 'absolute',
                        width: '80px', height: '80px', borderRadius: '50%',
                        background: 'rgba(0,210,255,0.2)',
                        border: '1px solid var(--neon-blue)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        cursor: 'pointer',
                        boxShadow: '0 0 30px rgba(0,210,255,0.4)',
                        backdropFilter: 'blur(4px)'
                      }}
                    >
                      <Play size={36} color="var(--neon-cyan)" style={{ marginLeft: '4px' }} />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Controls */}
              <div style={{ padding: '1.2rem 1.5rem', background: 'rgba(0,0,0,0.7)' }}>
                {/* Seek bar */}
                <div
                  onClick={handleSeek}
                  style={{
                    width: '100%', height: '6px',
                    background: 'var(--glass-border)',
                    borderRadius: '3px',
                    marginBottom: '1rem',
                    cursor: 'pointer',
                    position: 'relative', overflow: 'hidden'
                  }}
                >
                  <motion.div
                    style={{
                      width: `${progress}%`, height: '100%',
                      background: 'linear-gradient(90deg, var(--neon-blue), var(--neon-cyan))',
                      position: 'absolute', left: 0, top: 0,
                      transition: 'width 0.2s linear'
                    }}
                  />
                </div>

                {/* Button row */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', gap: '1.2rem', alignItems: 'center' }}>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={togglePlay}
                      style={{
                        background: 'none', border: 'none', cursor: 'pointer',
                        display: 'flex', alignItems: 'center'
                      }}
                    >
                      {isPlaying
                        ? <Pause size={26} color="#fff" />
                        : <Play size={26} color="#fff" />}
                    </motion.button>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                      {fmtTime(videoRef.current?.currentTime)} / {fmtTime(duration)}
                    </span>
                  </div>

                  <div style={{ display: 'flex', gap: '1.2rem', alignItems: 'center' }}>
                    <motion.a
                      href={videoData.url}
                      download="educational_video.mp4"
                      whileHover={{ scale: 1.1 }}
                      style={{ display: 'flex', alignItems: 'center', color: 'var(--text-muted)' }}
                      title="Download"
                    >
                      <Download size={20} />
                    </motion.a>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      onClick={handleFullscreen}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                      title="Fullscreen"
                    >
                      <Maximize size={20} color="var(--text-muted)" />
                    </motion.button>
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (

            /* ── Placeholder (no video yet) ────────────────────────────────── */
            <motion.div
              key="placeholder"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="glass-panel"
              style={{ padding: 0, overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.5)' }}
            >
              <div style={{
                width: '100%', aspectRatio: '16/9',
                background: 'radial-gradient(circle at center, #111827 0%, #030712 100%)',
                position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexDirection: 'column', gap: '1rem'
              }}>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                  style={{
                    position: 'absolute', top: '20%', left: '25%',
                    width: '150px', height: '150px',
                    border: '2px solid rgba(255,255,255,0.05)', borderRadius: '30%'
                  }}
                />
                <motion.div
                  animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }}
                  transition={{ duration: 4, repeat: Infinity }}
                  style={{
                    position: 'absolute', bottom: '30%', right: '25%',
                    width: '100px', height: '100px',
                    background: 'rgba(138,43,226,0.15)', borderRadius: '50%', filter: 'blur(10px)'
                  }}
                />
                <Film size={48} color="rgba(255,255,255,0.15)" />
                <p style={{ color: 'rgba(255,255,255,0.25)', fontSize: '0.95rem' }}>
                  Upload a document above to generate your video
                </p>
              </div>

              {/* Static controls bar */}
              <div style={{ padding: '1.5rem', background: 'rgba(0,0,0,0.6)' }}>
                <div style={{
                  width: '100%', height: '6px',
                  background: 'var(--glass-border)', borderRadius: '3px',
                  marginBottom: '1rem', overflow: 'hidden'
                }}>
                  <div style={{ width: '0%', height: '100%', background: 'linear-gradient(90deg, var(--neon-blue), var(--neon-cyan))' }} />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', gap: '1.2rem', alignItems: 'center' }}>
                    <Play size={26} color="rgba(255,255,255,0.2)" />
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>0:00 / 0:00</span>
                  </div>
                  <div style={{ display: 'flex', gap: '1.2rem' }}>
                    <Download size={20} color="rgba(255,255,255,0.15)" />
                    <Maximize size={20} color="rgba(255,255,255,0.15)" />
                  </div>
                </div>
              </div>
            </motion.div>
          )}

        </AnimatePresence>

        {/* ── Knowledge Assessment (Quiz) ─────────────────────────────────── */}
        {videoData && (questions.length > 0 || isFetchingQuestions) && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            style={{ marginTop: '5rem', marginBottom: '4rem' }}
          >
            <div style={{ marginBottom: '3rem' }}>
              {/* Game HUD */}
              <div className="glass-panel" style={{ 
                padding: '1.5rem 2.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                border: '1px solid var(--neon-cyan)', boxShadow: '0 0 20px rgba(0,255,204,0.1)',
                borderRadius: '20px', position: 'relative', overflow: 'hidden'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                  <div>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem', fontWeight: 800, letterSpacing: '1px' }}>TOTAL XP</span>
                    <div style={{ fontSize: '2rem', fontWeight: 900, color: '#fff', textShadow: '0 0 10px rgba(0,255,204,0.5)' }}>
                      {totalScore}
                    </div>
                  </div>
                  <div style={{ width: '2px', height: '40px', background: 'var(--glass-border)' }} />
                  <div>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem', fontWeight: 800, letterSpacing: '1px' }}>STREAK</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ fontSize: '2rem', fontWeight: 900, color: streak > 2 ? 'var(--neon-yellow)' : '#fff' }}>
                        {streak}
                      </div>
                      {streak > 2 && (
                        <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1 }}>
                          🔥
                        </motion.div>
                      )}
                    </div>
                  </div>
                </div>

                <div style={{ flex: 1, maxWidth: '300px', margin: '0 3rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.7rem', fontWeight: 700 }}>
                    <span style={{ color: 'var(--neon-violet)' }}>LEVEL {currentLevel} PROGRESS</span>
                    <span>{questions.filter(q => q.level === currentLevel).length > 0 ? Math.round((activeQuestionIdx / questions.filter(q => q.level === currentLevel).length) * 100) : 0}%</span>
                  </div>
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.1)' }}>
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${(activeQuestionIdx / (questions.filter(q => q.level === currentLevel).length || 1)) * 100}%` }}
                      style={{ height: '100%', background: 'linear-gradient(90deg, var(--neon-violet), var(--neon-blue))' }}
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  {[1, 2, 3].map(lvl => (
                    <motion.div
                      key={lvl}
                      whileHover={lvl <= unlockedLevel ? { scale: 1.1 } : {}}
                      onClick={() => lvl <= unlockedLevel && setCurrentLevel(lvl)}
                      style={{
                        width: '40px', height: '40px', borderRadius: '10px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        background: currentLevel === lvl ? 'var(--neon-blue)' : 'rgba(255,255,255,0.05)',
                        border: '1px solid',
                        borderColor: currentLevel === lvl ? 'var(--neon-cyan)' : 'var(--glass-border)',
                        color: lvl <= unlockedLevel ? '#fff' : 'rgba(255,255,255,0.2)',
                        cursor: lvl <= unlockedLevel ? 'pointer' : 'not-allowed',
                        fontSize: '0.9rem', fontWeight: 800, transition: 'all 0.3s'
                      }}
                    >
                      {lvl}
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>

              <div style={{ position: 'relative', minHeight: '500px' }}>
                <AnimatePresence mode="wait">
                  {/* Loading State */}
                  {isFetchingQuestions && (
                    <motion.div 
                      key="loading"
                      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                      style={{ textAlign: 'center', padding: '5rem' }}
                    >
                      <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}>
                        <HelpCircle size={60} color="var(--neon-blue)" style={{ opacity: 0.3 }} />
                      </motion.div>
                      <h3 style={{ color: 'var(--text-muted)', marginTop: '2rem', letterSpacing: '2px' }}>CALIBRATING CHALLENGE...</h3>
                    </motion.div>
                  )}

                  {/* Empty State */}
                  {!isFetchingQuestions && questions.filter(q => q.level === currentLevel).length === 0 && !levelStatus && (
                    <motion.div 
                      key="empty"
                      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                      className="glass-panel"
                      style={{ padding: '4rem', textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}
                    >
                      <AlertCircle size={48} color="#ff3366" style={{ marginBottom: '1.5rem' }} />
                      <h3>No questions available for this level.</h3>
                      <button onClick={retryLevel} className="btn-primary" style={{ marginTop: '2rem' }}>
                        Try Regenerating
                      </button>
                    </motion.div>
                  )}

                  {/* Start Screen */}
                  {!isFetchingQuestions && !quizStarted && questions.filter(q => q.level === currentLevel).length > 0 && !levelStatus && (
                    <motion.div
                      key="start-screen"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 1.1 }}
                      className="glass-panel"
                      style={{
                        padding: '4rem', textAlign: 'center', maxWidth: '800px', margin: '0 auto',
                        border: '1px solid var(--neon-blue)', background: 'rgba(10, 15, 30, 0.9)'
                      }}
                    >
                      <div style={{ marginBottom: '2.5rem' }}>
                        <div style={{ 
                          width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(0,210,255,0.1)',
                          display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem'
                        }}>
                          <Cpu size={40} color="var(--neon-cyan)" />
                        </div>
                        <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Sector {currentLevel} <span style={{ color: 'var(--neon-blue)' }}>Briefing</span></h2>
                        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
                          Analysis complete. The system has generated {questions.filter(q => q.level === currentLevel).length} tactical challenges based on your document.
                        </p>
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '3rem', textAlign: 'left' }}>
                        <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)' }}>
                          <div style={{ color: 'var(--neon-cyan)', fontSize: '0.8rem', fontWeight: 800, marginBottom: '0.5rem' }}>OBJECTIVE</div>
                          <div style={{ fontSize: '0.9rem' }}>Demonstrate 100% accuracy to unlock the next intelligence sector.</div>
                        </div>
                        <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)' }}>
                          <div style={{ color: 'var(--neon-violet)', fontSize: '0.8rem', fontWeight: 800, marginBottom: '0.5rem' }}>RESTRICTIONS</div>
                          <div style={{ fontSize: '0.9rem' }}>20s per node. Answers are final once committed.</div>
                        </div>
                      </div>

                      <button 
                        onClick={() => setQuizStarted(true)}
                        className="btn-primary"
                        style={{ padding: '15px 60px', fontSize: '1.2rem', fontWeight: 800 }}
                      >
                        Start Simulation
                      </button>
                    </motion.div>
                  )}

                  {/* Active Question Card */}
                  {quizStarted && questions.filter(q => q.level === currentLevel).length > 0 && !levelStatus && (
                    <motion.div
                      key={questions.filter(q => q.level === currentLevel)[activeQuestionIdx]?.id || 'no-q'}
                      initial={{ opacity: 0, x: 50, scale: 0.95 }}
                      animate={{ 
                        opacity: 1, x: 0, scale: 1,
                        rotateY: showFeedback?.type === 'error' ? [0, -5, 5, -5, 5, 0] : 0
                      }}
                      exit={{ opacity: 0, x: -50, scale: 0.95 }}
                      transition={{ 
                        type: 'spring', damping: 20, stiffness: 100,
                        rotateY: { duration: 0.4 }
                      }}
                      onViewportEnter={() => {
                        const q = questions.filter(q => q.level === currentLevel)[activeQuestionIdx];
                        if (q && userAnswers[q.id]?.correct === undefined) startTimer(q.id);
                      }}
                      className="glass-panel"
                      style={{
                        padding: '3rem',
                        border: '2px solid',
                        borderColor: showFeedback?.type === 'success' ? '#00ffcc' : showFeedback?.type === 'error' ? '#ff3366' : 'var(--glass-border)',
                        boxShadow: showFeedback?.type === 'success' ? '0 0 40px rgba(0,255,204,0.2)' : showFeedback?.type === 'error' ? '0 0 40px rgba(255,51,102,0.2)' : '0 20px 50px rgba(0,0,0,0.3)',
                        maxWidth: '800px', margin: '0 auto', position: 'relative',
                        background: 'rgba(10, 15, 30, 0.8)'
                      }}
                    >
                      {/* XP Popup */}
                      <AnimatePresence>
                        {xpPopup && (
                          <motion.div
                            initial={{ opacity: 0, y: 0 }}
                            animate={{ opacity: 1, y: -100 }}
                            exit={{ opacity: 0 }}
                            style={{
                              position: 'absolute', top: '20%', left: '50%', transform: 'translateX(-50%)',
                              fontSize: '2.5rem', fontWeight: 900, color: 'var(--neon-cyan)',
                              textShadow: '0 0 20px var(--neon-cyan)', pointerEvents: 'none', zIndex: 100
                            }}
                          >
                            {xpPopup.text}
                          </motion.div>
                        )}
                      </AnimatePresence>

                      {/* Timer & Progress Header */}
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span style={{ 
                            background: 'rgba(255,255,255,0.1)', padding: '4px 12px', borderRadius: '20px',
                            fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)'
                          }}>
                            NODE {activeQuestionIdx + 1} OF {questions.filter(q => q.level === currentLevel).length}
                          </span>
                        </div>
                        
                        {/* Countdown Ring */}
                        <CountdownRing timeLeft={timeLeft} />
                      </div>

                      {/* Question Content */}
                      {(() => {
                        const currentLevelQs = questions.filter(q => q.level === currentLevel);
                        const q = currentLevelQs[activeQuestionIdx];
                        
                        if (!q) return (
                          <div style={{ textAlign: 'center', padding: '2rem' }}>
                            <AlertCircle size={40} color="#ff3366" />
                            <p>Resource Error: Question node not found.</p>
                          </div>
                        );

                        const isAnswered = userAnswers[q.id]?.correct !== undefined;
                        const isRevealed = !!userAnswers[q.id]?.everRevealed;

                        return (
                          <>
                            <h3 style={{ fontSize: '1.8rem', color: '#fff', lineHeight: 1.4, marginBottom: '2.5rem', fontWeight: 700 }}>
                              {q.question}
                            </h3>

                            {q.type === 'mcq' ? (
                              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.2rem' }}>
                                {q.options && q.options.length > 0 ? q.options.map(opt => {
                                  const isSelected = userAnswers[q.id]?.selected === opt;
                                  const isCorrect = userAnswers[q.id]?.correct && isSelected;
                                  const isWrong = userAnswers[q.id]?.correct === false && isSelected;

                                  return (
                                    <motion.button
                                      key={opt}
                                      whileHover={!isAnswered ? { scale: 1.02, x: 5 } : {}}
                                      whileTap={!isAnswered ? { scale: 0.98 } : {}}
                                      onClick={() => !isAnswered && handleMcqClick(q, opt)}
                                      disabled={isAnswered}
                                      style={{
                                        padding: '1.2rem 1.5rem', textAlign: 'left', borderRadius: '15px',
                                        border: '1px solid',
                                        borderColor: isCorrect ? '#00ffcc' : isWrong ? '#ff3366' : isSelected ? 'var(--neon-blue)' : 'var(--glass-border)',
                                        background: isCorrect ? 'rgba(0,255,204,0.1)' : isWrong ? 'rgba(255,51,102,0.1)' : isSelected ? 'rgba(0,210,255,0.1)' : 'rgba(255,255,255,0.03)',
                                        color: isCorrect ? '#00ffcc' : isWrong ? '#ff3366' : '#eee',
                                        cursor: isAnswered ? 'default' : 'pointer', transition: 'all 0.3s',
                                        fontSize: '1rem', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '15px'
                                      }}
                                    >
                                      <div style={{ 
                                        width: '24px', height: '24px', borderRadius: '50%', 
                                        border: `2px solid ${isCorrect ? '#00ffcc' : isWrong ? '#ff3366' : '#555'}`,
                                        display: 'flex', alignItems: 'center', justifyContent: 'center'
                                      }}>
                                        {isSelected && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} style={{ width: '12px', height: '12px', borderRadius: '50%', background: isCorrect ? '#00ffcc' : isWrong ? '#ff3366' : 'var(--neon-blue)' }} />}
                                      </div>
                                      {opt}
                                    </motion.button>
                                  );
                                }) : (
                                  <div style={{ gridColumn: 'span 2', color: 'var(--text-muted)' }}>No options provided for this question.</div>
                                )}
                              </div>
                            ) : (
                              <div>
                                <textarea 
                                  id={`short-ans-${q.id}`}
                                  disabled={isAnswered || isRevealed}
                                  placeholder={isRevealed ? "Answer revealed — points lost." : "Synthesize your response here..."}
                                  style={{ 
                                    width: '100%', padding: '20px', borderRadius: '15px', 
                                    background: 'rgba(0,0,0,0.3)', border: '1px solid var(--glass-border)',
                                    color: '#fff', fontSize: '1.1rem', minHeight: '120px', outline: 'none', transition: 'all 0.3s'
                                  }}
                                />
                                {!isAnswered && (
                                  <button 
                                    onClick={() => handleShortSubmit(q, document.getElementById(`short-ans-${q.id}`).value)}
                                    className="btn-primary"
                                    style={{ marginTop: '1.5rem', width: '100%', padding: '15px' }}
                                  >
                                    Submit for AI Analysis
                                  </button>
                                )}
                              </div>
                            )}

                            {/* Help Actions */}
                            <div style={{ marginTop: '3rem', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--glass-border)', paddingTop: '1.5rem' }}>
                              <div style={{ display: 'flex', gap: '20px' }}>
                                {q.hint && !isAnswered && (
                                  <button 
                                    onClick={() => {
                                      if (confirm("Using a hint will deduct 2 XP. Continue?")) {
                                        toggleShowHint(q.id);
                                      }
                                    }}
                                    style={{ 
                                      display: 'flex', alignItems: 'center', gap: '8px',
                                      fontSize: '0.85rem', color: userAnswers[q.id]?.showHint ? 'var(--neon-yellow)' : 'var(--text-muted)', 
                                      background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600
                                    }}
                                  >
                                    <Lightbulb size={18} />
                                    {userAnswers[q.id]?.showHint ? 'Hint Active' : 'Need a Hint? (-2 XP)'}
                                  </button>
                                )}
                              </div>
                              <button 
                                onClick={() => toggleShowAnswer(q.id)}
                                style={{ color: 'var(--text-muted)', background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.85rem' }}
                              >
                                {userAnswers[q.id]?.showAnswer ? 'Hide Key' : 'Reveal Solution'}
                              </button>
                            </div>

                            {/* Answer Key / Hint Display */}
                            <AnimatePresence>
                              {userAnswers[q.id]?.showHint && (
                                <motion.div key="hint" initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} style={{ overflow: 'hidden', marginTop: '1rem' }}>
                                  <div className="glass-panel" style={{ padding: '1rem', borderColor: 'var(--neon-yellow)', background: 'rgba(255,255,0,0.05)', color: 'var(--neon-yellow)' }}>
                                    <strong>HINT:</strong> {q.hint}
                                  </div>
                                </motion.div>
                              )}
                              {userAnswers[q.id]?.showAnswer && (
                                <motion.div key="ans" initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} style={{ overflow: 'hidden', marginTop: '1rem' }}>
                                  <div className="glass-panel" style={{ padding: '1rem', borderColor: 'var(--neon-cyan)', background: 'rgba(0,255,204,0.05)', color: 'var(--neon-cyan)' }}>
                                    <strong>KEY:</strong> {q.type === 'mcq' ? q.correct_answer : q.answer}
                                  </div>
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </>
                        );
                      })()}
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Level Status & Actions */}
                <AnimatePresence>
                  {levelStatus && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 1.1 }}
                      className="glass-panel"
                      style={{
                        marginTop: '2rem', padding: '4rem', textAlign: 'center',
                        border: levelStatus === 'success' ? '2px solid #00ffcc' : '2px solid #ff3366',
                        background: levelStatus === 'success' ? 'rgba(0,255,204,0.05)' : 'rgba(255,51,102,0.05)',
                        boxShadow: levelStatus === 'success' ? '0 0 50px rgba(0,255,204,0.2)' : '0 0 50px rgba(255,51,102,0.2)'
                      }}
                    >
                      {levelStatus === 'refreshing' ? (
                        <div style={{ padding: '2rem' }}>
                          <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}>
                            <HelpCircle size={40} color="var(--neon-blue)" />
                          </motion.div>
                          <h3 style={{ marginTop: '1.5rem', color: '#fff' }}>Regenerating Level Challenge...</h3>
                        </div>
                      ) : (
                        <>
                          <h3 style={{ fontSize: '2.5rem', color: levelStatus === 'success' ? '#00ffcc' : '#ff3366', marginBottom: '1rem', fontWeight: 900 }}>
                            {levelStatus === 'success' ? 'LEVEL CLEARED!' : 'MISSION FAILED'}
                          </h3>
                          <p style={{ color: 'var(--text-muted)', marginBottom: '2.5rem', fontSize: '1.1rem' }}>
                            {levelStatus === 'success' 
                              ? (currentLevel < 3 ? 'Excellence demonstrated. The next sector is now accessible.' : 'All sectors cleared. Your mastery is absolute.')
                              : 'Minimum accuracy threshold not met. Tactical reset recommended.'}
                          </p>
                          
                          <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem' }}>
                            {levelStatus === 'retry' && (
                              <button 
                                onClick={retryLevel}
                                className="btn-primary" 
                                style={{ background: '#ff3366', borderColor: '#ff3366', padding: '15px 40px' }}
                              >
                                Try Again (New Questions)
                              </button>
                            )}
                            {levelStatus === 'success' && currentLevel < 3 && (
                              <button onClick={goToNextLevel} className="btn-primary" style={{ padding: '15px 40px' }}>
                                Unlock Level {currentLevel + 1}
                              </button>
                            )}
                          </div>
                        </>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Final Completion Screen */}
                <AnimatePresence>
                  {levelStatus === 'success' && currentLevel === 3 && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      style={{
                        marginTop: '4rem', padding: '5rem', textAlign: 'center',
                        background: 'radial-gradient(circle at center, rgba(0,210,255,0.1) 0%, transparent 70%)',
                        borderRadius: '30px', border: '1px solid var(--neon-cyan)',
                        boxShadow: '0 0 100px rgba(0,255,204,0.1)'
                      }}
                    >
                      <motion.div 
                        animate={{ rotate: [0, 10, -10, 10, 0], scale: [1, 1.1, 1] }} 
                        transition={{ repeat: Infinity, duration: 5 }}
                      >
                        <CheckCircle size={100} color="var(--neon-cyan)" style={{ marginBottom: '2rem' }} />
                      </motion.div>
                      <h2 style={{ fontSize: '4rem', marginBottom: '1.5rem', fontWeight: 900 }}>
                        MISSION <span style={{ color: 'var(--neon-cyan)' }}>ACCOMPLISHED</span>
                      </h2>
                      <div style={{ fontSize: '2rem', color: 'var(--text-muted)', marginBottom: '3rem' }}>
                        FINAL XP: <span style={{ color: '#fff', fontWeight: 900, fontSize: '3rem' }}>{totalScore}</span>
                      </div>
                      
                      <div style={{ 
                        display: 'inline-block', padding: '20px 60px', borderRadius: '40px',
                        background: 'rgba(255,255,255,0.05)', border: '2px solid var(--neon-violet)',
                        fontSize: '1.5rem', fontWeight: 800, color: '#fff',
                        boxShadow: '0 0 30px rgba(138,43,226,0.2)'
                      }}>
                        RANK: {totalScore >= 40 ? 'GRANDMASTER' : totalScore >= 25 ? 'ELITE VOYAGER' : 'INITIATE'}
                      </div>

                      <div style={{ marginTop: '5rem' }}>
                        <button 
                          onClick={() => {
                            setUnlockedLevel(1);
                            setCurrentLevel(1);
                            setTotalScore(0);
                            setUserAnswers({});
                            setLevelStatus(null);
                            setStreak(0);
                            setActiveQuestionIdx(0);
                          }}
                          style={{
                            background: 'none', border: 'none', color: 'var(--text-muted)',
                            textDecoration: 'underline', cursor: 'pointer', fontSize: '1rem', opacity: 0.6
                          }}
                        >
                          Reset Simulation Data
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default VideoPreview;
