import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Pause, Maximize, Download, Film, Layers } from 'lucide-react';
import { useVideo } from '../App';

const VideoPreview = () => {
  const { videoData } = useVideo();
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);

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
      </div>
    </section>
  );
};

export default VideoPreview;
