import React, { useState } from 'react';
import { ChevronLeft, Send, Power } from 'lucide-react';
import Plot from 'react-plotly.js';
import ReactMarkdown from 'react-markdown'; 
import remarkGfm from 'remark-gfm'; 

function App() {
  // Helper to get current time in 10:39 AM format
  const getCurrentTime = () => {
    return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
  };

  // 🚀 Initial message with YOUR newly requested predefined options
  const initialBotMessage = {
    role: 'bot',
    text: 'Welcome to Kirloskar Pneumatic Company Limited! How can I assist you today?\n\nPlease choose from the following options or type your own question:',
    options: [
      "Plot a horizontal bar chart of the top 10 'Dealer Name' by average 'RunHrs'",
      "Plot a line chart showing the total number of complaints logged per year",
      "How many unique Compressor 'Model' types do we have?",
      "Which 'Dealer Name' has the highest number of logged complaints?",
      "How many rows mention the word 'leak' or 'vibration' in the 'Nature of complaint' column?",
      "What is the most frequently mentioned item in the 'Spares / Part Replaced' column?"
    ],
    time: getCurrentTime()
  };

  const [messages, setMessages] = useState([initialBotMessage]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 🧹 Function to clear the chat history (Power Button)
  const handleClearChat = () => {
    if (window.confirm("Are you sure you want to clear the chat history?")) {
      setMessages([{ ...initialBotMessage, time: getCurrentTime() }]);
      setInput(''); // Clear input box too
    }
  };

  // 🚀 sendMessage now accepts 'overrideText' from the buttons
  const sendMessage = async (overrideText = null) => {
    // Use the button text if provided, otherwise use the typed input
    const textToSend = typeof overrideText === 'string' ? overrideText : input;
    
    if (!textToSend.trim()) return;
    
    const userMessage = { role: 'user', text: textToSend, time: getCurrentTime() };
    setMessages(prev => [...prev, userMessage]);
    
    // Only clear the input box if the user typed it manually
    if (typeof overrideText !== 'string') {
      setInput('');
    }
    
    setIsLoading(true);

    try {
      // Pointing to your FastAPI backend
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend, user_id: "admin" })
      });
      
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'bot',
        text: data.answer,
        graph_json: data.graph_json, 
        time: getCurrentTime()
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', text: 'Connection to backend failed. Please ensure your Python server is running.', time: getCurrentTime() }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper to ensure hidden newlines from Python are handled
  const cleanText = (text) => text ? text.replace(/\\n/g, '\n') : '';

  return (
    // Clean, neutral background, centering the app perfectly
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6 font-sans">
      
      {/* Large Centered Chat Window */}
      <div className="w-full max-w-4xl h-[85vh] bg-white rounded-2xl shadow-2xl flex flex-col relative overflow-hidden border border-gray-200">
        
        {/* Header */}
        <div className="bg-[#149486] text-white px-6 py-4 flex items-center justify-between z-10 shrink-0">
          <div className="flex items-center gap-4">
            <ChevronLeft size={28} className="cursor-pointer hover:opacity-80" />
            
            {/* The Logo Container */}
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center overflow-hidden shrink-0">
               <img 
                 src="/kbot-logo.png" 
                 alt="KBot" 
                 className="w-full h-full object-contain"
                 onError={(e) => {
                   e.target.style.display = 'none';
                   e.target.parentElement.innerHTML = '<div class="w-6 h-6 bg-[#149486] rounded-full"></div>';
                 }}
               />
            </div>
            
            <h1 className="font-semibold text-xl tracking-wide">KBot</h1>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 bg-[#fdfdfd] flex flex-col gap-6 relative">
          
          {messages.map((msg, index) => (
            <div key={index} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              
              {/* Sender Name */}
              <span className={`text-xs text-gray-500 mb-1.5 ${msg.role === 'user' ? 'mr-1' : 'ml-1'}`}>
                {msg.role === 'user' ? 'You' : 'KBot'}
              </span>

              {/* Message Bubble */}
              <div className={`p-4 text-[15px] leading-relaxed shadow-sm ${
                msg.graph_json ? 'max-w-[95%] w-full' : 'max-w-[80%]'
              } ${
                msg.role === 'user' 
                  ? 'bg-[#e2f1f0] text-gray-800 rounded-2xl rounded-tr-sm' 
                  : 'bg-[#f4f6f8] text-gray-800 rounded-2xl rounded-tl-sm border border-gray-100'
              }`}>
                
                {/* 🚀 Render Text */}
                {msg.role === 'user' ? (
                  <div style={{ whiteSpace: 'pre-wrap' }}>{cleanText(msg.text)}</div>
                ) : (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({node, ...props}) => <p style={{ marginBottom: '12px', whiteSpace: 'pre-wrap' }} {...props} />,
                      ul: ({node, ...props}) => <ul style={{ listStyleType: 'disc', paddingLeft: '24px', marginBottom: '12px' }} {...props} />,
                      ol: ({node, ...props}) => <ol style={{ listStyleType: 'decimal', paddingLeft: '24px', marginBottom: '12px' }} {...props} />,
                      li: ({node, ...props}) => <li style={{ marginBottom: '6px' }} {...props} />,
                      strong: ({node, ...props}) => <strong style={{ fontWeight: 'bold', color: '#111827' }} {...props} />,
                      em: ({node, ...props}) => <em style={{ fontStyle: 'italic' }} {...props} />,
                    }}
                  >
                    {cleanText(msg.text)}
                  </ReactMarkdown>
                )}

                {/* 🚀 Render Predefined Options */}
                {msg.options && (
                  <div className="flex flex-wrap gap-2 mt-4">
                    {msg.options.map((option, idx) => (
                      <button
                        key={idx}
                        onClick={() => sendMessage(option)}
                        disabled={isLoading}
                        className="px-4 py-2 text-[14px] font-medium border border-[#149486] text-[#149486] bg-white rounded-full hover:bg-[#e2f1f0] transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-left"
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
                
                {/* 🚀 Render INTERACTIVE Plotly Graph */}
                {msg.graph_json && (
                  <div className="mt-4 rounded-lg border border-gray-200 overflow-hidden bg-white p-2">
                    <Plot
                      data={JSON.parse(msg.graph_json).data}
                      layout={{ 
                        ...JSON.parse(msg.graph_json).layout, 
                        autosize: true,
                        margin: { t: 50, r: 20, l: 60, b: 100 }, 
                        paper_bgcolor: 'transparent',
                        plot_bgcolor: 'transparent',
                        font: { family: 'Inter, sans-serif', color: '#475569' },
                        legend: { orientation: 'h', y: -0.4, x: 0 } 
                      }}
                      useResizeHandler={true}
                      style={{ width: "100%", height: "450px" }} 
                      config={{ responsive: true, displayModeBar: false }}
                    />
                  </div>
                )}

                {/* Timestamp inside bubble */}
                <span className="text-[11px] text-gray-400 block text-right mt-2">
                  {msg.time}
                </span>
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex flex-col items-start">
               <span className="text-xs text-gray-500 mb-1.5 ml-1">KBot</span>
               <div className="bg-[#f4f6f8] text-gray-500 p-4 rounded-2xl rounded-tl-sm border border-gray-100">
                 <div className="flex gap-1.5 items-center h-5">
                   <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                   <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                   <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                 </div>
               </div>
            </div>
          )}
        </div>

        {/* Footer / Input Area */}
        <div className="bg-white border-t border-gray-100 flex flex-col z-10 shrink-0">
          
          {/* Quick Menu Icons */}
          <div className="flex justify-end px-4 pt-3 gap-3 text-gray-400">
             <Power 
                size={20} 
                onClick={handleClearChat} 
                title="Restart Session"
                className="cursor-pointer text-orange-400 hover:text-red-500 transition-colors" 
             />
          </div>

          <div className="p-4 flex items-center bg-white gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 text-[15px] outline-none text-gray-700 placeholder-gray-400 bg-transparent py-2"
              placeholder="Choose an option or type your question..."
              disabled={isLoading}
            />
            <button 
              onClick={() => sendMessage()}
              disabled={isLoading || !input.trim()}
              className="p-3 text-[#149486] hover:bg-teal-50 rounded-full transition-colors disabled:opacity-50"
            >
              <Send size={22} />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;