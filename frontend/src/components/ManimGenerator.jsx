import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:4000/api'; // Or your backend URL

export default function ManimGenerator() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(''); // 'processing', 'done', 'error'
  const [videoUrl, setVideoUrl] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Handle file select
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  // Upload to generate pipeline
  const handleUpload = async () => {
    if (!file) return;

    // Reset state
    setJobId(null);
    setStatus('processing');
    setVideoUrl('');
    setErrorMsg('');

    const formData = new FormData();
    formData.append('document', file);

    try {
      const response = await fetch(`${API_BASE}/pipeline/generate`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to start job');
      }

      setJobId(data.jobId);
    } catch (err) {
      setStatus('error');
      setErrorMsg(err.message);
    }
  };

  // Polling logic
  useEffect(() => {
    let interval;
    if (jobId && status === 'processing') {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/pipeline/status/${jobId}`);
          const data = await res.json();

          if (data.status === 'done') {
            setStatus('done');
            // Construct absolute URL mapping to our express static folder
            setVideoUrl(`http://localhost:4000${data.videoUrl}`);
          } else if (data.status === 'error') {
            setStatus('error');
            setErrorMsg(data.error || 'An unknown error occurred during generation.');
          }
          // if 'processing', or 'queued' do nothing and wait for next tick
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 3000); // Poll every 3 seconds
    }

    return () => clearInterval(interval);
  }, [jobId, status]);

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>Convert Educational PDF to Video</h1>
      
      <div style={{ marginBottom: '1rem' }}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button 
          onClick={handleUpload} 
          disabled={!file || status === 'processing'}
          style={{ marginLeft: '10px', padding: '0.5rem 1rem' }}
        >
          {status === 'processing' && !jobId ? 'Starting...' : 'Generate Video'}
        </button>
      </div>

      {status === 'processing' && jobId && (
        <div style={{ margin: '2rem 0', color: 'blue' }}>
          Pipeline is processing your PDF (Job ID: {jobId}). This may take a few minutes...
        </div>
      )}

      {status === 'error' && (
        <div style={{ margin: '2rem 0', color: 'red', fontWeight: 'bold' }}>
          Error: {errorMsg}
        </div>
      )}

      {status === 'done' && videoUrl && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Generated Video</h2>
          {/* NATIVE HTML5 EXPLICIT REQUIREMENT */}
          <video 
            controls 
            src={videoUrl} 
            style={{ width: '100%', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
          >
            Your browser does not support HTML5 video.
          </video>
        </div>
      )}
    </div>
  );
}
