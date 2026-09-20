import { useState, useRef, useEffect } from 'react';
import { API_URL } from '../../config/api';

export default function ChatModal({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Hola, soy tu asistente de datos para el ciclo escolar 2024 de Guatemala. He procesado los **4.29M de registros**.',
      note: 'Puedes preguntarme sobre brechas departamentales, deserciones o proyecciones.'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const streamRef = useRef(null);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (queryParam) => {
    const query = queryParam || inputValue.trim();
    if (!query) return;

    setInputValue('');
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setIsLoading(true);

    try {
      // Future integration with real API:
      // const res = await fetch(`${API_URL}/buscar`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ query })
      // });
      // const data = await res.json();
      
      // Mocked response for demo:
      setTimeout(() => {
        let answer = 'Analizando los 4,298,887 registros: En 2024, la cobertura primaria se mantiene en 56.4% con 85.2% de promoción global. La mayor disparidad se ubica en la transición a Diversificado.';
        if (query.includes('departamentos')) {
          answer = 'Según la base oficial: Alta Verapaz (81.3%), Quiché (82.8%) e Izabal (83.1%) presentan las tasas de aprobación con mayor necesidad de refuerzo pedagógico y becas de permanencia.';
        }
        setMessages(prev => [...prev, { role: 'bot', content: answer }]);
        setIsLoading(false);
      }, 1000);
      
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: 'Lo siento, hubo un error de conexión con la base de datos.' }]);
      setIsLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-8 z-50 flex items-center">
        <button 
          onClick={onClose} 
          className="flex items-center gap-2.5 px-4 py-3 rounded-full bg-secondary text-on-secondary shadow-xl hover:bg-secondary/90 transition-all transform hover:scale-105"
        >
          <span className="material-symbols-outlined text-[20px] text-tertiary-fixed-dim animate-spin" style={{ animationDuration: '4s' }}>auto_awesome</span>
          <span className="font-label-sm text-label-sm font-bold tracking-wide">Preguntar a EduData AI</span>
        </button>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-scrim/40 backdrop-blur-sm bg-black/30">
      <div className="bg-surface-container-lowest w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh] animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-5 py-4 bg-primary-container text-on-primary flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="material-symbols-outlined text-tertiary-fixed-dim text-[22px]">auto_awesome</span>
            <div className="flex flex-col">
              <span className="font-title-sm text-title-sm leading-none font-bold">EduData AI</span>
              <span className="text-caption-xs font-caption-xs text-on-primary-container mt-0.5">Asistente Ejecutivo para Políticas</span>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1 rounded-lg text-on-primary-container hover:text-on-primary hover:bg-surface-container-high/10 transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Chat Body */}
        <div className="flex-1 p-5 overflow-y-auto flex flex-col gap-4 bg-surface" ref={streamRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'items-start gap-3'}`}>
              {msg.role === 'bot' && (
                <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center text-on-secondary flex-shrink-0 mt-0.5 shadow-sm">
                  <span className="material-symbols-outlined text-[18px]">smart_toy</span>
                </div>
              )}
              <div className={`${msg.role === 'user' ? 'bg-secondary text-on-secondary rounded-tr-none' : 'bg-surface-container-lowest border border-outline-variant/20 text-on-surface rounded-tl-none'} p-4 rounded-2xl shadow-sm flex flex-col gap-1.5 max-w-[85%]`}>
                <p className="font-body-md text-body-md leading-relaxed" dangerouslySetInnerHTML={{ __html: msg.content.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>') }}></p>
                {msg.note && <span className="text-caption-xs font-caption-xs text-outline">{msg.note}</span>}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center text-on-secondary flex-shrink-0 mt-0.5 shadow-sm">
                <span className="material-symbols-outlined text-[18px]">smart_toy</span>
              </div>
              <div className="bg-surface-container-lowest border border-outline-variant/20 p-4 rounded-2xl rounded-tl-none shadow-sm flex gap-1 items-center">
                <span className="w-2 h-2 rounded-full bg-secondary animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-secondary animate-bounce delay-75"></span>
                <span className="w-2 h-2 rounded-full bg-secondary animate-bounce delay-150"></span>
              </div>
            </div>
          )}

          {messages.length === 1 && (
            <div className="flex flex-col gap-2 pt-4 border-t border-outline-variant/10 mt-2">
              <span className="text-caption-xs font-caption-xs text-outline uppercase font-semibold">Preguntas sugeridas:</span>
              <button 
                onClick={() => handleSend("¿Cuáles son los 3 departamentos con menor tasa de aprobación?")}
                className="text-left p-3 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover:bg-surface-container-low hover:border-secondary/30 text-body-md font-body-md text-on-surface transition-all shadow-sm flex gap-2 items-center"
              >
                <span className="text-lg">📉</span> ¿Cuáles son los 3 departamentos con menor tasa de aprobación?
              </button>
              <button 
                onClick={() => handleSend("¿Cuál es la brecha de retención entre área rural y urbana?")}
                className="text-left p-3 rounded-xl bg-surface-container-lowest border border-outline-variant/20 hover:bg-surface-container-low hover:border-secondary/30 text-body-md font-body-md text-on-surface transition-all shadow-sm flex gap-2 items-center"
              >
                <span className="text-lg">🌾</span> ¿Cuál es la brecha de retención entre área rural y urbana?
              </button>
            </div>
          )}
        </div>

        {/* Footer Input */}
        <div className="p-4 bg-surface-container-low border-t border-outline-variant/10 flex items-center gap-2">
          <input 
            className="flex-1 bg-surface-container-lowest px-4 py-3 rounded-xl text-body-md font-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-secondary border border-outline-variant/20 transition-all shadow-sm"
            placeholder="Escribe tu pregunta sobre el ciclo escolar..." 
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={() => handleSend()}
            disabled={!inputValue.trim() || isLoading}
            className="p-3 rounded-xl bg-secondary text-on-secondary hover:bg-secondary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex items-center justify-center"
          >
            <span className="material-symbols-outlined text-[20px]">send</span>
          </button>
        </div>

      </div>
    </div>
  );
}
