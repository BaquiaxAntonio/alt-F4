export default function DemographicsSection() {
  return (
    <section className="bg-white rounded-2xl p-8 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col gap-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-2">
        <div className="flex flex-col gap-1">
          <span className="text-[11px] text-slate-500 uppercase font-bold tracking-widest">Territorio y Demografía</span>
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">¿Dónde estudian los estudiantes?</h2>
        </div>
        <span className="text-sm font-medium text-slate-500">Equilibrio territorial rural-urbano 2024</span>
      </div>

      <div className="flex flex-col gap-4">
        <div className="w-full h-10 rounded-xl overflow-hidden flex bg-slate-100 shadow-inner">
          <div className="bg-[#1e293b] h-full flex items-center justify-start pl-5 text-white text-sm font-bold transition-all duration-700" style={{ width: '61.4%' }}>
            61.4% Rural
          </div>
          <div className="bg-[#0d6efd] h-full flex items-center justify-end pr-5 text-white text-sm font-bold transition-all duration-700" style={{ width: '38.6%' }}>
            38.6% Urbana
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div className="p-5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-xl bg-[#1e293b]/10 text-[#1e293b] flex items-center justify-center">
                <span className="material-symbols-outlined text-[32px]">agriculture</span>
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold text-slate-900">Área Rural (61.4%)</span>
                <span className="text-xs text-slate-500 font-medium">Comunidades rurales, aldeas y caseríos</span>
              </div>
            </div>
            <div className="text-right flex flex-col">
              <span className="text-2xl font-extrabold text-slate-900">2,639,516</span>
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wide mt-0.5">alumnos inscritos</span>
            </div>
          </div>

          <div className="p-5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-xl bg-[#0d6efd]/10 text-[#0d6efd] flex items-center justify-center">
                <span className="material-symbols-outlined text-[32px]">apartment</span>
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold text-slate-900">Área Urbana (38.6%)</span>
                <span className="text-xs text-slate-500 font-medium">Cabeceras y centros metropolitanos</span>
              </div>
            </div>
            <div className="text-right flex flex-col">
              <span className="text-2xl font-extrabold text-slate-900">1,659,371</span>
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wide mt-0.5">alumnos inscritos</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-blue-50/50 border border-blue-100 p-5 rounded-xl flex items-start gap-4">
        <span className="material-symbols-outlined text-[#0d6efd] text-[24px] flex-shrink-0 mt-0.5">analytics</span>
        <div className="flex flex-col gap-1.5">
          <span className="text-sm font-bold text-slate-900">Lo que muestran los datos:</span>
          <p className="text-sm text-slate-700 leading-relaxed">
            Los registros educativos de 2024 presentan una mayor proporción de estudiantes en áreas rurales (61.4%) que en áreas urbanas (38.6%), demandando un enfoque prioritario en infraestructura descentralizada, bilingüe e intercultural.
          </p>
        </div>
      </div>
    </section>
  );
}
