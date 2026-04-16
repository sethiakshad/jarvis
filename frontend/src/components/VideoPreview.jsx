import React from 'react';
import { motion } from 'framer-motion';
import { Play, Pause, SkipBack, SkipForward, Maximize, Settings } from 'lucide-react';

const VideoPreview = () => {
  return (
    <section>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Final <span style={{ color: 'var(--neon-cyan)' }}>Render</span></h2>
        <p style={{ color: 'var(--text-muted)' }}>The fully synthesized educational video ready for deployment.</p>
      </div>

      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        <div className="glass-panel" style={{ padding: '0', overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.5)' }}>
          {/* Mock Video Area */}
          <div style={{ 
            width: '100%', 
            aspectRatio: '16/9', 
            background: 'radial-gradient(circle at center, #111827 0%, #030712 100%)',
            position: 'relative',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            {/* Play Button Overlay */}
            <motion.div 
              whileHover={{ scale: 1.1 }}
              style={{
                width: '80px', height: '80px',
                borderRadius: '50%',
                background: 'rgba(0, 210, 255, 0.2)',
                border: '1px solid var(--neon-blue)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                cursor: 'pointer',
                boxShadow: '0 0 30px rgba(0, 210, 255, 0.4)'
              }}
            >
              <Play size={40} color="var(--neon-cyan)" style={{ marginLeft: '6px' }} />
            </motion.div>

            {/* Mock Visual Elements (Shapes representing Manim output) */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              style={{
                position: 'absolute', top: '20%', left: '25%',
                width: '150px', height: '150px',
                border: '2px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '30%'
              }}
            />
            <motion.div
              animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }}
              transition={{ duration: 4, repeat: Infinity }}
              style={{
                position: 'absolute', bottom: '30%', right: '25%',
                width: '100px', height: '100px',
                background: 'rgba(138, 43, 226, 0.2)',
                borderRadius: '50%',
                filter: 'blur(10px)'
              }}
            />
          </div>

          {/* Controls Area */}
          <div style={{ padding: '1.5rem', background: 'rgba(0,0,0,0.6)' }}>
            {/* Timeline */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>01:24</span>
              <div style={{ flex: 1, height: '6px', background: 'var(--glass-border)', borderRadius: '3px', position: 'relative', overflow: 'hidden' }}>
                <div style={{ width: '45%', height: '100%', background: 'linear-gradient(90deg, var(--neon-blue), var(--neon-cyan))', position: 'absolute', left: 0, top: 0 }} />
                
                {/* Scene Markers */}
                <div style={{ width: '2px', height: '100%', background: '#fff', position: 'absolute', left: '20%' }} />
                <div style={{ width: '2px', height: '100%', background: '#fff', position: 'absolute', left: '45%' }} />
                <div style={{ width: '2px', height: '100%', background: '#fff', position: 'absolute', left: '75%' }} />
              </div>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>03:00</span>
            </div>

            {/* Buttons */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                <SkipBack size={20} color="var(--text-muted)" style={{ cursor: 'pointer' }} />
                <Pause size={24} color="#fff" style={{ cursor: 'pointer' }} />
                <SkipForward size={20} color="var(--text-muted)" style={{ cursor: 'pointer' }} />
                
                <div style={{ width: '1px', height: '24px', background: 'var(--glass-border)', margin: '0 10px' }} />
                
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '4px 12px', background: 'rgba(138, 43, 226, 0.2)', borderRadius: '12px' }}>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--neon-violet)', boxShadow: '0 0 8px var(--neon-violet)' }} />
                  <span style={{ fontSize: '0.8rem', color: '#fff' }}>Audio-Visual Sync: <span style={{ color: 'var(--neon-cyan)' }}>100%</span></span>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                <Settings size={20} color="var(--text-muted)" style={{ cursor: 'pointer' }} />
                <Maximize size={20} color="var(--text-muted)" style={{ cursor: 'pointer' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default VideoPreview;
