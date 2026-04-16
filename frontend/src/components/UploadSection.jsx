import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, File, Activity, Search } from 'lucide-react';

const UploadSection = () => {
  const [isHovered, setIsHovered] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = () => {
    setIsUploading(true);
    setTimeout(() => {
      setIsUploading(false);
    }, 3000);
  };

  return (
    <section>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Initiate <span style={{ color: 'var(--neon-blue)' }}>Data Ingestion</span></h2>
        <p style={{ color: 'var(--text-muted)' }}>Upload source material to prime the RAG pipeline.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', alignItems: 'start' }}>
        {/* Upload Box */}
        <motion.div 
          className="glass-panel"
          whileHover={{ scale: 1.02 }}
          onHoverStart={() => setIsHovered(true)}
          onHoverEnd={() => setIsHovered(false)}
          onClick={handleUpload}
          style={{
            padding: '4rem 2rem',
            textAlign: 'center',
            cursor: 'pointer',
            border: isHovered ? '1px solid var(--neon-blue)' : '1px solid var(--glass-border)',
            position: 'relative'
          }}
        >
          {isHovered && (
            <motion.div 
              layoutId="glowBorder"
              style={{
                position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
                boxShadow: 'inset 0 0 40px rgba(0, 210, 255, 0.1)',
                zIndex: -1
              }}
            />
          )}

          <AnimatePresence mode="wait">
            {!isUploading ? (
              <motion.div
                key="uploadData"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <div style={{ 
                  background: 'rgba(0, 210, 255, 0.1)', 
                  width: '80px', height: '80px', 
                  borderRadius: '50%', 
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  margin: '0 auto 1.5rem auto'
                }}>
                  <UploadCloud size={40} color="var(--neon-blue)" />
                </div>
                <h3 style={{ fontSize: '1.4rem', marginBottom: '0.5rem' }}>Drag & Drop Document</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Supports PDF, TXT, DOCX</p>
                <div style={{ marginTop: '2rem' }}>
                  <motion.div 
                    animate={isHovered ? { y: [0, -5, 0] } : {}}
                    transition={{ repeat: Infinity, duration: 1.5 }}
                  >
                    <File size={24} color={isHovered ? "var(--neon-cyan)" : "var(--text-muted)"} />
                  </motion.div>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="analyzing"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
              >
                <Activity size={50} color="var(--neon-violet)" style={{ marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: 'var(--neon-violet)' }} className="text-neon">AI Analyzing...</h3>
                <div style={{ display: 'flex', gap: '4px', marginTop: '1.5rem' }}>
                  {[...Array(5)].map((_, i) => (
                    <motion.div 
                      key={i}
                      animate={{ height: ['10px', '40px', '10px'] }}
                      transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.1 }}
                      style={{ width: '6px', background: 'var(--neon-cyan)', borderRadius: '3px' }}
                    />
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Topic Input section */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-panel" style={{ padding: '2rem' }}>
            <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Search size={20} color="var(--neon-cyan)" /> Target Concept
            </h3>
            <div style={{ position: 'relative' }}>
              <input 
                type="text" 
                placeholder="What should the AI focus on?"
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  background: 'rgba(0,0,0,0.4)',
                  border: '1px solid var(--glass-border)',
                  borderRadius: '12px',
                  color: '#fff',
                  fontSize: '1rem',
                  outline: 'none',
                  transition: 'all 0.3s'
                }}
                onFocus={e => {
                  e.target.style.borderColor = 'var(--neon-cyan)';
                  e.target.style.boxShadow = '0 0 15px rgba(0, 255, 204, 0.2)';
                }}
                onBlur={e => {
                  e.target.style.borderColor = 'var(--glass-border)';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>
            
            <div style={{ mt: '1.5rem', paddingTop: '1.5rem' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>AI Suggested Angles:</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {["History of Neural Nets", "Backpropagation Deep Dive", "Transformer Architecture"].map((topic, i) => (
                  <motion.span 
                    key={i}
                    whileHover={{ scale: 1.05, background: 'rgba(138, 43, 226, 0.2)', borderColor: 'var(--neon-violet)' }}
                    style={{
                      padding: '8px 16px',
                      background: 'var(--glass-bg)',
                      border: '1px solid var(--glass-border)',
                      borderRadius: '20px',
                      fontSize: '0.85rem',
                      cursor: 'pointer',
                      transition: 'all 0.2s'
                    }}
                  >
                    {topic}
                  </motion.span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default UploadSection;
