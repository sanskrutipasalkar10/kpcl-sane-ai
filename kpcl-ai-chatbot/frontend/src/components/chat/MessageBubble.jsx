import React, { useState } from 'react';
import { User, Bot, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const [showReasoning, setShowReasoning] = useState(false);

  return (
    <div className={`message-row ${isUser ? 'user-row' : 'bot-row'}`}>
      <div className={`avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-content">
        {/* Main Text Answer */}
        <div className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}>
          {message.text}
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