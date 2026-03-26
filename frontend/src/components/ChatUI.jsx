import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Home, MapPin, Building, CreditCard, Loader2 } from "lucide-react";

export default function ChatUI() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Welcome to Seabreeze by Godrej Bayview! How can I assist you in finding your dream home today?", type: "text" }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input, type: "text" };
    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);
    setInput("");

    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await axios.post(`${API_URL}/chat`, {
        message: input,
        session_id: sessionId
      });

      const botMsg = { sender: "bot", text: res.data.response, type: "text" };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { sender: "bot", text: "Sorry, I am having trouble connecting to the server.", type: "text" }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-white shadow-sm px-6 py-4 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Building className="text-white w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Seabreeze AI</h1>
            <p className="text-sm text-gray-500">by Godrej Bayview</p>
          </div>
        </div>
        
        {/* Quick Highlights */}
        <div className="hidden md:flex gap-4">
          <Badge icon={<MapPin className="w-4 h-4" />} text="Sector 9, Vashi" />
          <Badge icon={<Home className="w-4 h-4" />} text="2 & 3 BHK" />
          <Badge icon={<CreditCard className="w-4 h-4" />} text="₹3.20 Cr+" />
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6 w-full max-w-4xl mx-auto flex flex-col gap-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div 
              className={`max-w-[75%] rounded-2xl px-5 py-3 shadow-sm ${
                msg.sender === "user" 
                ? "bg-blue-600 text-white rounded-br-sm" 
                : "bg-white text-gray-800 border border-gray-100 rounded-bl-sm"
              }`}
            >
              <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
            </div>
          </div>
        ))}
        {isTyping && (
           <div className="flex justify-start">
             <div className="bg-white text-gray-800 border border-gray-100 max-w-[75%] rounded-2xl rounded-bl-sm px-5 py-4 shadow-sm flex items-center gap-2">
               <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
               <span className="text-sm text-gray-500">AI is typing...</span>
             </div>
           </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex items-center gap-2 bg-gray-50 rounded-full p-2 border border-gray-200 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <input
            className="flex-1 bg-transparent border-none outline-none px-4 py-2 text-gray-700"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about 2 BHK pricing, amenities, or location..."
            disabled={isTyping}
          />
          <button 
            onClick={sendMessage} 
            disabled={!input.trim() || isTyping}
            className="bg-blue-600 disabled:bg-blue-300 text-white p-2 sm:px-6 sm:py-2 rounded-full flex items-center gap-2 hover:bg-blue-700 transition-colors"
          >
            <span className="hidden sm:inline">Send</span>
            <Send className="w-4 h-4" />
          </button>
        </div>
      </footer>
    </div>
  );
}

function Badge({ icon, text }) {
  return (
    <div className="flex items-center gap-1.5 bg-gray-100 text-gray-700 px-3 py-1.5 rounded-full text-sm font-medium">
      {icon}
      {text}
    </div>
  )
}
