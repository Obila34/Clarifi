import React, { useEffect, useState } from 'react';

const sidebarItems = [
  {
    label: 'Home',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 10.5 12 3l9 7.5" />
        <path d="M5.5 9.5V20h13V9.5" />
      </svg>
    ),
  },
  {
    label: 'History',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 12a9 9 0 1 0 2.64-6.36" />
        <path d="M3 4v4h4" />
        <path d="M12 7v5l3 2" />
      </svg>
    ),
  },
  {
    label: 'Settings',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle cx="12" cy="12" r="3.2" />
        <path d="M19.4 15a1 1 0 0 0 .2 1.1l.1.1a1 1 0 0 1 0 1.4l-.7.7a1 1 0 0 1-1.4 0l-.1-.1a1 1 0 0 0-1.1-.2 1 1 0 0 0-.6.9v.2a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-.2a1 1 0 0 0-.6-.9 1 1 0 0 0-1.1.2l-.1.1a1 1 0 0 1-1.4 0l-.7-.7a1 1 0 0 1 0-1.4l.1-.1a1 1 0 0 0 .2-1.1 1 1 0 0 0-.9-.6h-.2a1 1 0 0 1-1-1v-1a1 1 0 0 1 1-1h.2a1 1 0 0 0 .9-.6 1 1 0 0 0-.2-1.1l-.1-.1a1 1 0 0 1 0-1.4l.7-.7a1 1 0 0 1 1.4 0l.1.1a1 1 0 0 0 1.1.2h.1a1 1 0 0 0 .5-.9V5a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v.2a1 1 0 0 0 .6.9 1 1 0 0 0 1.1-.2l.1-.1a1 1 0 0 1 1.4 0l.7.7a1 1 0 0 1 0 1.4l-.1.1a1 1 0 0 0-.2 1.1v.1a1 1 0 0 0 .9.5h.2a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-.2a1 1 0 0 0-.9.6Z" />
      </svg>
    ),
  },
];

const promptCards = [
  { title: "Find my next 'Vibe Check' career", icon: 'radar' },
  { title: "Build my 'Anti-Resume' (Hobby translator)", icon: 'pen' },
  { title: "Simulate my 'Future Me' timeline", icon: 'timeline' },
  { title: "Take the 'Sweatpants vs. Suit' work quiz", icon: 'balance' },
];

const thinkingStates = [
  'Scanning the latest market trends for you...',
  'Comparing role demand across live sources...',
  'Synthesizing opportunities for your career vibe...',
];

const uploadThinkingStates = [
  'Parsing your resume structure...',
  'Extracting skills and experience signals...',
  'Preparing ATS-friendly rewrite suggestions...',
];

const gapThinkingStates = [
  'Mapping your missing skills to learning paths...',
  'Searching for top free and high-signal courses...',
  'Building your personalized Gap Bridge plan...',
];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function PrismIcon() {
  return (
    <div className="prism" aria-hidden="true">
      <span className="beam beam-a" />
      <span className="beam beam-b" />
      <span className="beam beam-c" />
    </div>
  );
}

function PromptIcon({ type }) {
  if (type === 'radar') {
    return (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle className="pulse-ring" cx="12" cy="12" r="7" />
        <circle cx="12" cy="12" r="2" />
        <path d="M12 12 18 6" />
      </svg>
    );
  }

  if (type === 'pen') {
    return (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="m14 5 5 5" />
        <path d="M6 18.5 5 22l3.5-1L19 10.5 14.5 6 6 14.5Z" />
      </svg>
    );
  }

  if (type === 'timeline') {
    return (
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M4 18h16" />
        <path d="m6 15 4-4 3 2 5-6" />
        <circle cx="6" cy="15" r="1" />
        <circle cx="10" cy="11" r="1" />
        <circle cx="13" cy="13" r="1" />
        <circle cx="18" cy="7" r="1" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M6 8h12" />
      <path d="M12 8v9" />
      <path d="M9 17h6" />
      <path d="M8 8a4 4 0 0 1 8 0" />
    </svg>
  );
}

function buildMockResponse(userPrompt) {
  return {
    mode: 'market_pulse',
    summary: `Here is a first market pulse for "${userPrompt}" with actionable next moves.`,
    cards: [
      {
        title: 'AI Ethics in Frontier Tech — 2026 Snapshot',
        url: 'https://example.com/ai-ethics-space-tech',
        platform_icon: '🌐',
        price: 'Free',
      },
      {
        title: 'Role Demand Trend: Responsible AI Leads',
        url: 'https://example.com/responsible-ai-demand',
        platform_icon: '📊',
        price: '$',
      },
      {
        title: 'Skill Bridge: AI Governance Fundamentals',
        url: 'https://example.com/ai-governance-course',
        platform_icon: '🎓',
        price: 'Free',
      },
    ],
  };
}

async function requestClarifi(prompt) {
  const response = await fetch(`${API_BASE_URL}/api/clarifi/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`Clarifi API failed with status ${response.status}`);
  }

  return response.json();
}

async function uploadResume(file, dreamVibe) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('dream_vibe', dreamVibe);

  const response = await fetch(`${API_BASE_URL}/api/clarifi/resume/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Resume upload failed with status ${response.status}`);
  }

  return response.json();
}

async function requestGapBridge(resumeId, dreamVibe) {
  const response = await fetch(`${API_BASE_URL}/api/clarifi/gap-bridge`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ resume_id: resumeId, dream_vibe: dreamVibe }),
  });

  if (!response.ok) {
    throw new Error(`Gap bridge failed with status ${response.status}`);
  }

  return response.json();
}

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [dreamVibe, setDreamVibe] = useState('AI Career Transition');
  const [selectedFile, setSelectedFile] = useState(null);
  const [thinkingMessages, setThinkingMessages] = useState(thinkingStates);
  const [isThinking, setIsThinking] = useState(false);
  const [thinkingIndex, setThinkingIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [resumeResult, setResumeResult] = useState(null);
  const [gapResult, setGapResult] = useState(null);

  useEffect(() => {
    if (!isThinking) {
      setThinkingIndex(0);
      return undefined;
    }

    const interval = setInterval(() => {
      setThinkingIndex((prev) => (prev + 1) % thinkingMessages.length);
    }, 1400);

    return () => clearInterval(interval);
  }, [isThinking, thinkingMessages.length]);

  async function handleSubmit(event) {
    event.preventDefault();
    const cleanPrompt = prompt.trim();
    if (!cleanPrompt || isThinking) {
      return;
    }

    setThinkingMessages(thinkingStates);
    setIsThinking(true);
    setResult(null);

    try {
      const apiResult = await requestClarifi(cleanPrompt);
      setResult(apiResult);
    } catch (error) {
      setResult(buildMockResponse(cleanPrompt));
    } finally {
      setIsThinking(false);
    }
  }

  function applySuggestion(text) {
    setPrompt(text);
  }

  async function handleResumeUpload() {
    if (!selectedFile || isThinking) {
      return;
    }

    setThinkingMessages(uploadThinkingStates);
    setIsThinking(true);
    setResumeResult(null);
    setGapResult(null);

    try {
      const uploadResult = await uploadResume(selectedFile, dreamVibe);
      setResumeResult(uploadResult);
    } catch (error) {
      setResumeResult({
        mode: 'resume_glowup',
        resume_id: 'mock-resume-id',
        summary:
          'Resume upload endpoint is unavailable right now. Backend fallback mode is active for UI testing.',
        missing_skills: ['system design', 'leadership'],
        rewrites: [
          {
            original: 'Worked on backend API tasks.',
            improved:
              'Delivered backend API improvements that reduced response latency by 28% and increased reliability for core user flows.',
          },
        ],
        cards: buildMockResponse('resume').cards,
      });
    } finally {
      setIsThinking(false);
    }
  }

  async function handleGapBridge() {
    if (!resumeResult?.resume_id || isThinking) {
      return;
    }

    setThinkingMessages(gapThinkingStates);
    setIsThinking(true);
    setGapResult(null);

    try {
      const response = await requestGapBridge(resumeResult.resume_id, dreamVibe);
      setGapResult(response);
    } catch (error) {
      setGapResult({
        mode: 'gap_bridge',
        summary: 'Gap Bridge endpoint is unavailable right now. Showing mock learning bridge cards.',
        missing_skills: ['communication', 'system design'],
        cards: [
          {
            title: 'System Design Fundamentals (Free)',
            url: 'https://www.youtube.com/results?search_query=system+design+fundamentals',
            platform_icon: '🎓',
            price: 'Free',
          },
          {
            title: 'Leadership Communication for Engineers',
            url: 'https://www.coursera.org/',
            platform_icon: '🎤',
            price: 'Free',
          },
        ],
      });
    } finally {
      setIsThinking(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="aurora aurora-teal" />
      <div className="aurora aurora-lavender" />
      <div className="aurora aurora-orange" />

      <aside className="sidebar" aria-label="Primary">
        <div className="brand">
          <PrismIcon />
          <span>Clarifi</span>
        </div>

        <nav className="side-nav">
          {sidebarItems.map((item) => (
            <button className="nav-icon" key={item.label} aria-label={item.label}>
              {item.icon}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main-content">
        <section className="hero">
          <h1>Hey there! Where should we take your career today?</h1>

          <div className="prompt-grid">
            {promptCards.map((card) => (
              <button
                key={card.title}
                className="prompt-card"
                onClick={() => applySuggestion(card.title)}
              >
                <span className={`prompt-icon prompt-icon--${card.icon}`} aria-hidden="true">
                  <PromptIcon type={card.icon} />
                </span>
                <span>{card.title}</span>
              </button>
            ))}
          </div>

          <section className="tool-shell" aria-label="Resume tools">
            <div className="tool-row">
              <input
                type="text"
                value={dreamVibe}
                onChange={(event) => setDreamVibe(event.target.value)}
                placeholder="Dream vibe (e.g. AI Product Leader)"
                aria-label="Dream vibe"
              />
              <label className="file-pick">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
                />
                <span>{selectedFile ? selectedFile.name : 'Choose CV (PDF/DOCX/TXT)'}</span>
              </label>
              <button type="button" onClick={handleResumeUpload} disabled={!selectedFile || isThinking}>
                Resume Glow-Up
              </button>
              <button
                type="button"
                className="secondary"
                onClick={handleGapBridge}
                disabled={!resumeResult?.resume_id || isThinking}
              >
                Gap Bridge
              </button>
            </div>
          </section>

          {(isThinking || result) && (
            <section className="result-shell" aria-live="polite">
              {isThinking && (
                <div className="agent-status">
                  <span className="status-dot" aria-hidden="true" />
                  <span>{thinkingMessages[thinkingIndex]}</span>
                </div>
              )}

              {result && !isThinking && (
                <>
                  <div className="result-header">
                    <h2>Clarifi Signal</h2>
                    <span className="result-mode">{result.mode}</span>
                  </div>
                  <p>{result.summary}</p>

                  <div className="result-grid">
                    {result.cards.map((item) => (
                      <a
                        key={item.url}
                        className="result-card"
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        <div>
                          <h3>{item.title}</h3>
                          <span>{item.url.replace('https://', '')}</span>
                        </div>
                        <div className="result-meta">
                          <span>{item.platform_icon}</span>
                          <strong>{item.price}</strong>
                        </div>
                      </a>
                    ))}
                  </div>
                </>
              )}
            </section>
          )}

          {resumeResult && !isThinking && (
            <section className="result-shell" aria-live="polite">
              <div className="result-header">
                <h2>Resume Glow-Up</h2>
                <span className="result-mode">{resumeResult.mode}</span>
              </div>
              <p>{resumeResult.summary}</p>

              {!!resumeResult.missing_skills?.length && (
                <div className="chip-row">
                  {resumeResult.missing_skills.map((skill) => (
                    <span key={skill} className="skill-chip">
                      {skill}
                    </span>
                  ))}
                </div>
              )}

              {!!resumeResult.rewrites?.length && (
                <div className="rewrite-list">
                  {resumeResult.rewrites.map((rewrite) => (
                    <article key={rewrite.original} className="rewrite-card">
                      <h4>Before</h4>
                      <p>{rewrite.original}</p>
                      <h4>After</h4>
                      <p>{rewrite.improved}</p>
                    </article>
                  ))}
                </div>
              )}
            </section>
          )}

          {gapResult && !isThinking && (
            <section className="result-shell" aria-live="polite">
              <div className="result-header">
                <h2>Gap Bridge</h2>
                <span className="result-mode">{gapResult.mode}</span>
              </div>
              <p>{gapResult.summary}</p>
              {!!gapResult.missing_skills?.length && (
                <div className="chip-row">
                  {gapResult.missing_skills.map((skill) => (
                    <span key={skill} className="skill-chip">
                      {skill}
                    </span>
                  ))}
                </div>
              )}
              <div className="result-grid">
                {gapResult.cards.map((item) => (
                  <a
                    key={`${item.url}-${item.title}`}
                    className="result-card"
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <div>
                      <h3>{item.title}</h3>
                      <span>{item.url.replace('https://', '')}</span>
                    </div>
                    <div className="result-meta">
                      <span>{item.platform_icon}</span>
                      <strong>{item.price}</strong>
                    </div>
                  </a>
                ))}
              </div>
            </section>
          )}
        </section>

        <section className="composer-wrap" aria-label="Command composer">
          <div className="composer-glow" />
          <form className="composer" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Ask Clarifi to map your next move..."
              aria-label="Prompt input"
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
            />
            <button aria-label="Send prompt" type="submit" disabled={isThinking}>
              <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
