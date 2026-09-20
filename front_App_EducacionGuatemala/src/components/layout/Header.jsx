export default function Header({ openChat }) {
  return (
    <header className="fixed top-0 left-72 right-0 h-16 bg-white border-b border-slate-200 z-30 px-6 flex items-center justify-between gap-4">
      <div className="flex items-center gap-6 min-w-0">
        <div className="flex items-center gap-2 text-slate-500 text-sm truncate">
          <span className="material-symbols-outlined text-[20px]">home</span>
          <span className="text-slate-400">/</span>
          <span className="font-semibold text-slate-700">Plataforma Analítica</span>
        </div>
        
        <div className="hidden xl:flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-50 border border-slate-100">
          <span className="w-2 h-2 rounded-full bg-blue-500"></span>
          <span className="text-xs font-semibold text-slate-600 leading-tight">
            4,298,887 Registros<br/>Procesados
          </span>
        </div>
      </div>
      
      <div className="flex items-center gap-3 flex-shrink-0">
        <div className="hidden lg:flex items-center bg-slate-50 border border-slate-200 px-3 py-2 rounded-lg gap-2 cursor-pointer hover:bg-slate-100 transition-colors">
          <span className="material-symbols-outlined text-slate-500 text-[18px]">calendar_today</span>
          <span className="text-sm text-slate-700 font-semibold">Ciclo Escolar Oficial 2024</span>
          <span className="material-symbols-outlined text-slate-400 text-[18px]">expand_more</span>
        </div>
        
        <div className="relative hidden md:block w-64">
          <span className="material-symbols-outlined absolute left-3 top-2 text-[18px] text-slate-400">search</span>
          <input
            className="w-full bg-slate-50 border border-slate-200 pl-9 pr-3 py-2 rounded-lg text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="Buscar indicador, municipio..."
            type="search"
          />
        </div>
        
        <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm font-semibold transition-colors">
          <span className="material-symbols-outlined text-[18px]">download</span>
          <span className="hidden sm:inline">Exportar</span>
        </button>
        
        <button
          onClick={openChat}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0d6efd] hover:bg-blue-600 text-white text-sm font-bold shadow-sm transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">auto_awesome</span>
          <span>Preguntar a EduData AI</span>
        </button>
        
        <div className="w-10 h-10 rounded-full bg-black flex items-center justify-center cursor-pointer hover:bg-slate-800 transition-colors ml-2">
          <span className="material-symbols-outlined text-white text-[20px]">person</span>
        </div>
      </div>
    </header>
  );
}
