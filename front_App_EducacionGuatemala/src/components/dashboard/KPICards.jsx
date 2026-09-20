export default function KPICards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* KPI 1: Matrícula Total */}
      <div className="bg-white rounded-2xl p-6 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-4">
        <div className="flex items-start justify-between">
          <div className="flex flex-col gap-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-widest font-bold">Matrícula Nacional</span>
            <span className="text-4xl font-extrabold text-slate-900">4,298,887</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#eff6ff] flex items-center justify-center text-[#0d6efd]">
            <span className="material-symbols-outlined text-[24px]">school</span>
          </div>
        </div>
        <div className="flex flex-col gap-3 pt-2">
          <div className="flex items-end justify-between gap-1 h-8 text-[#0d6efd]">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none" viewBox="0 0 100 24">
              <path d="M0,18 L15,16 L30,19 L45,13 L60,14 L75,9 L90,11 L100,5" fill="none" stroke="currentColor" strokeLinecap="round" strokeWidth="3"></path>
            </svg>
          </div>
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-500">Registros educativos<br/>totales 2024</span>
            <span className="text-[#0d6efd]">100%<br/>Cobertura INE</span>
          </div>
        </div>
      </div>

      {/* KPI 2: Tasa de Promoción */}
      <div className="bg-white rounded-2xl p-6 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-4">
        <div className="flex items-start justify-between">
          <div className="flex flex-col gap-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-widest font-bold">Tasa de Promoción</span>
            <span className="text-4xl font-extrabold text-slate-900">85.2%</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#eff6ff] flex items-center justify-center text-[#0d6efd]">
            <span className="material-symbols-outlined text-[24px]">verified</span>
          </div>
        </div>
        <div className="flex flex-col gap-3 pt-4">
          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
            <div className="bg-[#0d6efd] h-full rounded-full" style={{ width: '85.2%' }}></div>
          </div>
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-500">Estudiantes<br/>promovidos</span>
            <span className="text-slate-900">3,662,651<br/>aprobados</span>
          </div>
        </div>
      </div>

      {/* KPI 3: Área Rural */}
      <div className="bg-white rounded-2xl p-6 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-4">
        <div className="flex items-start justify-between">
          <div className="flex flex-col gap-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-widest font-bold">Área Rural</span>
            <span className="text-4xl font-extrabold text-slate-900">61.4%</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-[#1e293b] flex items-center justify-center text-[#60a5fa]">
            <span className="material-symbols-outlined text-[24px]">nature_people</span>
          </div>
        </div>
        <div className="flex flex-col gap-3 pt-4">
          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
            <div className="bg-[#1e293b] h-full rounded-full" style={{ width: '61.4%' }}></div>
          </div>
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-500">Registros en el campo</span>
            <span className="text-slate-900">2,639,516 alumnos</span>
          </div>
        </div>
      </div>

      {/* KPI 4: Sector Público */}
      <div className="bg-white rounded-2xl p-6 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-4">
        <div className="flex items-start justify-between">
          <div className="flex flex-col gap-1">
            <span className="text-[11px] text-slate-500 uppercase tracking-widest font-bold">Sector Público</span>
            <span className="text-4xl font-extrabold text-slate-900">74.7%</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-black flex items-center justify-center text-white">
            <span className="material-symbols-outlined text-[24px]">account_balance</span>
          </div>
        </div>
        <div className="flex flex-col gap-3 pt-4">
          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
            <div className="bg-black h-full rounded-full" style={{ width: '74.7%' }}></div>
          </div>
          <div className="flex items-center justify-between text-xs font-semibold">
            <span className="text-slate-500">Sistema estatal MINEDUC</span>
            <span className="text-slate-900">3,211,268 alumnos</span>
          </div>
        </div>
      </div>
    </div>
  );
}
