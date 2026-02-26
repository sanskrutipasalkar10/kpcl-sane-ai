import React, { useState } from 'react';
import { User, Bot, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const [showReasoning, setShowReasoning] = useState(false);

  // 🚀 CUSTOM FORMATTER: No libraries needed. Fixes Tailwind CSS reset issues instantly.
  const renderFormattedText = (text) => {
    if (!text) return "";
    
    // Fix any escaped newlines coming from the Python backend
    const normalizedText = text.replace(/\\n/g, '\n');
    const lines = normalizedText.split('\n');
    
    return lines.map((line, index) => {
      // 1. Detect Bullet Points
      const isBullet = line.trim().startsWith('* ') || line.trim().startsWith('- ');
      const cleanLine = isBullet ? line.trim().substring(2) : line;
      
      // 2. Detect Bold Text (**text**)
      const boldParts = cleanLine.split(/(\*\*.*?\*\*)/g);
      const formattedLine = boldParts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          // Inline style guarantees it stays bold even if Tailwind tries to reset it
          return <strong key={i} style={{ fontWeight: '700', color: '#111827' }}>{part.slice(2, -2)}</strong>;
        }
        return part;
      });

      // 3. Render Bullet Points with nice spacing
      if (isBullet) {
        return (
          <div key={index} style={{ display: 'flex', gap: '8px', marginBottom: '6px', marginLeft: '16px' }}>
            <span style={{ color: '#3b82f6', fontWeight: 'bold' }}>•</span>
            <span style={{ lineHeight: '1.6' }}>{formattedLine}</span>
          </div>
        );
      }

      // 4. Render Normal Paragraphs and Line Breaks
      return (
        <div key={index} style={{ marginBottom: line.trim() === '' ? '0' : '10px', lineHeight: '1.6' }}>
          {formattedLine || <div style={{ height: '8px' }}></div>}
        </div>
      );
    });
  };

  return (
    <div className={`message-row ${isUser ? 'user-row' : 'bot-row'}`}>
      <div className={`avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-content">
        {/* Main Text Answer */}
        <div className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}>
          {/* 🚀 Apply the custom formatter only to the bot's messages */}
          {isUser ? message.text : renderFormattedText(message.text)}
        </div>

        {/* Display Graph if Agent generated one */}
        {message.graph_base64 && (
          <div className="graph-container">
            <img 
              src={`data:image/png;base64,${message.graph_base64}`} 
              alt="Data Visualization" 
              className="generated-graph"
            />
          </div>
        )}

        {/* S.A.N.E.-AI Trust & Traceability Panel */}
        {!isUser && message.confidence && (
          <div className="metadata-panel">
            <span className={`confidence-badge ${message.confidence.toLowerCase()}`}>
              Confidence: {message.confidence}
            </span>
            
            <button 
              className="reasoning-toggle"
              onClick={() => setShowReasoning(!showReasoning)}
            >
              Decision Path {showReasoning ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
            </button>
            
            {showReasoning && (
              <div className="reasoning-box">
                <strong>Executed Logic:</strong>
                <pre>{message.reasoning}</pre>
                {message.error && (
                  <div className="error-text">
                    <AlertTriangle size={14}/> {message.error}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}