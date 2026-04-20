import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, File, Activity, Search, CheckCircle, AlertCircle } from 'lucide-react';

const UploadSection = () => {
  const [isHovered, setIsHovered] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  
  // Pipeline State
  const fileInputRef = useRef(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(''); // 'processing', 'done', 'error'
  const [videoUrl, setVideoUrl] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Handle actual file selection
  const handleFileChange = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setStatus('processing');
    setJobId(null);
    setVideoUrl('');
    setErrorMsg('');

    const formData = new FormData();
    formData.append('document', file);

    try {
      // Use environment variable for backend server
      const backendUrl = import.meta.env.VITE_BACKEND_SERVER.endsWith('/') 
        ? import.meta.env.VITE_BACKEND_SERVER 
        : `${import.meta.env.VITE_BACKEND_SERVER}/`;

      const res = await fetch(`${backendUrl}api/pipeline/generate`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to start generation');
      setJobId(data.jobId);
    } catch (err) {
      setStatus('error');
      setErrorMsg(err.message);
      setIsUploading(false);
    }
  };

  const handleBoxClick = () => {
    if (!isUploading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Polling Effect
  useEffect(() => {
    let interval;
    if (jobId && status === 'processing') {
      interval = setInterval(async () => {
        try {
          const backendUrl = import.meta.env.VITE_BACKEND_SERVER.endsWith('/') 
            ? import.meta.env.VITE_BACKEND_SERVER 
            : `${import.meta.env.VITE_BACKEND_SERVER}/`;

          const res = await fetch(`${backendUrl}api/pipeline/status/${jobId}`);
          const data = await res.json();
          if (data.status === 'done') {
            setStatus('done');
            setIsUploading(false);
            setVideoUrl(`${backendUrl.slice(0, -1)}${data.videoUrl}`);
          } else if (data.status === 'error') {
            setStatus('error');
            setIsUploading(false);
            setErrorMsg(data.error || 'Server processing error');
          }
        } catch (err) {
          console.error(err);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [jobId, status]);


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
          onClick={handleBoxClick}
          style={{
            padding: '4rem 2rem',
            textAlign: 'center',
            cursor: isUploading ? 'default' : 'pointer',
            border: isHovered ? '1px solid var(--neon-blue)' : '1px solid var(--glass-border)',
            position: 'relative'
          }}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept=".pdf,.doc,.docx,.ppt,.pptx,.txt" 
            style={{ display: 'none' }} 
          />
          {isHovered && !isUploading && (
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
            {!isUploading && status !== 'done' && status !== 'error' ? (
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
            ) : status === 'done' ? (
              <motion.div
                key="done"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
              >
                <CheckCircle size={50} color="#00ffcc" style={{ marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: '#00ffcc' }}>Generation Complete</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>Your Manim video is ready.</p>
                <video 
                  controls 
                  src={videoUrl} 
                  style={{ width: '100%', maxWidth: '300px', borderRadius: '8px', boxShadow: '0 4px 15px rgba(0,0,0,0.3)' }}
                />
                <button 
                  onClick={(e) => { e.stopPropagation(); setStatus(''); setVideoUrl(''); }}
                  style={{ marginTop: '1rem', padding: '8px 16px', background: 'transparent', border: '1px solid #00ffcc', color: '#00ffcc', borderRadius: '20px', cursor: 'pointer' }}
                >
                  Generate Another
                </button>
              </motion.div>
            ) : status === 'error' ? (
              <motion.div
                key="error"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
              >
                <AlertCircle size={50} color="#ff3366" style={{ marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.4rem', color: '#ff3366' }}>Generation Failed</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.5rem', wordBreak: 'break-word' }}>{errorMsg}</p>
                <button 
                  onClick={(e) => { e.stopPropagation(); setStatus(''); setErrorMsg(''); }}
                  style={{ marginTop: '1rem', padding: '8px 16px', background: 'transparent', border: '1px solid #ff3366', color: '#ff3366', borderRadius: '20px', cursor: 'pointer' }}
                >
                  Try Again
                </button>
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
                <h3 style={{ fontSize: '1.4rem', color: 'var(--neon-violet)' }} className="text-neon">Pipeline Executing...</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.5rem' }}>Extracting text & generating Manim code (Job: {jobId?.substring(0,6)}...)</p>
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
