export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-72 bg-[#121826] text-slate-400 z-40 flex flex-col justify-between py-6 px-4 border-r border-slate-800">
      <div className="flex flex-col gap-8">
        <div className="flex items-center gap-3 px-3">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-blue-500 rounded flex items-center justify-center text-white font-bold text-xs">
              <span className="material-symbols-outlined text-[16px]">bar_chart</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white font-bold tracking-wide text-sm leading-tight">EduData <span className="text-blue-500 text-xs">GT</span></span>
              <span className="text-[9px] text-slate-500 tracking-widest font-semibold">GUATEMALA - 2024</span>
            </div>
          </div>
          <div className="h-8 w-px bg-slate-700 mx-2"></div>
          <div className="flex flex-col">
            <span className="font-bold text-white tracking-tight text-lg leading-none">
              EduData
            </span>
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider leading-tight mt-0.5">
              REPÚBLICA DE<br/>GUATEMALA
            </span>
          </div>
        </div>

        <div className="h-px w-full bg-slate-800"></div>

        <nav className="flex flex-col gap-2">
          <a
            aria-current="page"
            className="flex items-center justify-between px-4 py-3 bg-[#0d6efd] text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 transition-colors"
            href="#"
          >
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[20px]">public</span>
              <span className="text-[15px]">Panorama Nacional</span>
            </div>
            <span className="text-xs font-bold">2024</span>
          </a>

          <a
            className="flex items-center justify-between px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[20px]">map</span>
              <span className="text-[15px]">Departamentos</span>
            </div>
            <span className="text-xs text-slate-500">22 reg.</span>
          </a>

          <a
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <span className="material-symbols-outlined text-[20px]">school</span>
            <span className="text-[15px]">Niveles Educativos</span>
          </a>

          <a
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <span className="material-symbols-outlined text-[20px]">trending_up</span>
            <span className="text-[15px]">Resultados del Ciclo</span>
          </a>

          <a
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <span className="material-symbols-outlined text-[20px]">stacked_bar_chart</span>
            <span className="text-[15px]">Brechas Educativas</span>
          </a>

          <a
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <span className="material-symbols-outlined text-[20px]">table_chart</span>
            <span className="text-[15px]">Explorador de Datos</span>
          </a>

          <a
            className="flex items-center justify-between px-4 py-3 mt-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all group"
            href="#"
          >
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[20px] text-blue-400 group-hover:text-blue-300">auto_awesome</span>
              <span className="text-[15px]">EduData AI</span>
            </div>
            <span className="bg-blue-500 text-white text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
              IA
            </span>
          </a>
        </nav>
      </div>

      <div className="flex flex-col gap-4 pt-6 border-t border-slate-800">
        <div className="px-4 py-3 rounded-xl bg-[#1e293b] flex flex-col gap-1.5 border border-slate-700/50">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">
            Fuente Primaria
          </span>
          <div className="flex items-center gap-2 text-white">
            <span className="material-symbols-outlined text-[16px]">verified</span>
            <span className="text-sm font-semibold">INE Guatemala & MINEDUC</span>
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <a
            className="flex items-center gap-3 px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800/50 transition-colors"
            href="#"
          >
            <span className="material-symbols-outlined text-[18px]">info</span>
            <span>Información del Dataset</span>
          </a>
          <a
            className="flex items-center gap-3 px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800/50 transition-colors"
            href="#"
          >
            <span className="material-symbols-outlined text-[18px]">settings</span>
            <span>Configuración del Sistema</span>
          </a>
        </div>
      </div>
    </aside>
  );
}
