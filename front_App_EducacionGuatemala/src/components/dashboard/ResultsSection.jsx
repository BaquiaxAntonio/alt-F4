export default function ResultsSection() {
  return (
    <section className="bg-white rounded-2xl p-8 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col gap-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-2">
        <div className="flex flex-col gap-1">
          <span className="text-[11px] text-slate-500 uppercase font-bold tracking-widest">Eficiencia Terminal y Retención</span>
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">¿Cómo terminó el ciclo escolar 2024?</h2>
        </div>
        <span className="text-sm font-medium text-slate-500">Distribución de finalización académica</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ResultCard 
          title="Promovido" 
          badge="Exitoso" 
          pct="85.2%" 
          count="3,662,651" 
          desc="alumnos promovidos" 
          colorClass="bg-[#0d6efd]" 
          badgeClass="bg-blue-100 text-[#0d6efd]" 
          textColorClass="text-slate-900"
          bgContainer="bg-slate-50 border border-slate-100" 
          trackClass="bg-slate-200"
        />
        <ResultCard 
          title="No Promovido" 
          badge="Repitencia" 
          pct="9.2%" 
          count="395,497" 
          desc="alumnos no promovidos" 
          colorClass="bg-red-500" 
          badgeClass="bg-red-100 text-red-600" 
          textColorClass="text-red-600"
          textDescClass="text-red-900"
          bgContainer="bg-red-50 border border-red-100" 
          trackClass="bg-red-200"
        />
        <ResultCard 
          title="Retirado / Abandono" 
          badge="Deserción" 
          pct="5.5%" 
          count="236,439" 
          desc="alumnos retirados" 
          colorClass="bg-slate-400" 
          badgeClass="bg-slate-200 text-slate-700" 
          textColorClass="text-slate-900"
          bgContainer="bg-slate-50 border border-slate-100" 
          trackClass="bg-slate-200"
        />
      </div>

      <div className="bg-amber-50 border border-amber-100 rounded-xl p-5 flex items-start gap-4">
        <span className="material-symbols-outlined text-amber-600 text-[24px] flex-shrink-0 mt-0.5">warning_amber</span>
        <div className="flex flex-col gap-1.5">
          <span className="text-sm font-bold text-amber-900">Interpretación de Política Pública:</span>
          <p className="text-sm text-amber-900/80 leading-relaxed">
            El 85.2% culminó el ciclo con promoción. Sin embargo, el <strong className="font-bold text-red-600">14.7% acumulado</strong> entre estudiantes no promovidos y retirados representa a <strong>más de 630,000 niños y jóvenes</strong> en situación de vulnerabilidad o rezago académico durante 2024.
          </p>
        </div>
      </div>
    </section>
  );
}

function ResultCard({ title, badge, pct, count, desc, colorClass, badgeClass, textColorClass, textDescClass = "text-slate-700", bgContainer, trackClass }) {
  return (
    <div className={`p-6 rounded-2xl ${bgContainer} flex flex-col justify-between gap-5`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className={`w-3.5 h-3.5 rounded-full ${colorClass}`}></span>
          <span className={`text-sm font-bold ${title === 'No Promovido' ? 'text-red-900' : 'text-slate-800'}`}>{title}</span>
        </div>
        <span className={`px-3 py-1 rounded-full text-[10px] uppercase tracking-wider font-bold ${badgeClass}`}>
          {badge}
        </span>
      </div>
      <div className="flex flex-col gap-1">
        <span className={`text-5xl font-extrabold tracking-tight ${textColorClass}`}>{pct}</span>
        <span className={`text-sm font-medium ${textDescClass}`}>{count} {desc}</span>
      </div>
      <div className={`w-full ${trackClass} h-2.5 rounded-full overflow-hidden mt-1`}>
        <div className={`${colorClass} h-full rounded-full`} style={{ width: pct }}></div>
      </div>
    </div>
  );
}
