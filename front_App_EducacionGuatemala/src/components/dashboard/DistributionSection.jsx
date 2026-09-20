export default function DistributionSection() {
  return (
    <section className="flex flex-col gap-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-2">
        <div className="flex flex-col gap-1">
          <span className="text-[11px] text-slate-500 uppercase font-bold tracking-widest">Análisis Estructural</span>
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">¿Cómo se distribuye la educación?</h2>
        </div>
        <span className="text-sm font-medium text-slate-500">Desglose por Niveles Oficiales y Sectores de Gestión</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Columna Izquierda: Nivel Educativo */}
        <div className="bg-white rounded-2xl p-8 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-8">
          <div className="flex flex-col gap-6">
            <div className="flex items-center justify-between">
              <span className="text-lg font-bold text-slate-800">Estudiantes por nivel educativo</span>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Volumen y %</span>
            </div>
            
            <div className="flex flex-col gap-5">
              <LevelBar name="Primaria" pct="56.4" value="2,424,572" colorClass="bg-[#0d6efd]" />
              <LevelBar name="Básico" pct="17.8" value="765,201" colorClass="bg-[#4f46e5]" />
              <LevelBar name="Preprimaria" pct="17.1" value="735,110" colorClass="bg-[#2563eb]" />
              <LevelBar name="Diversificado" pct="8.5" value="365,404" colorClass="bg-[#60a5fa]" />
              <LevelBar name="Primaria de Adultos" pct="0.2" value="8,600" colorClass="bg-slate-300" widthPct="2.5" />
            </div>
          </div>
          <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-5 flex items-start gap-4">
            <span className="text-2xl select-none">💡</span>
            <p className="text-sm text-slate-700 leading-relaxed">
              <strong className="font-bold text-slate-900">Primaria concentra la mayor proporción</strong> de los registros educativos del país (más de la mitad de todos los alumnos). A medida que se avanza hacia el Ciclo Básico y Diversificado, la matrícula se reduce de forma drástica, evidenciando el reto estructural de retención en la transición a secundaria.
            </p>
          </div>
        </div>

        {/* Columna Derecha: Sector Educativo */}
        <div className="bg-white rounded-2xl p-8 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col justify-between gap-8">
          <div className="flex flex-col gap-6">
            <div className="flex items-center justify-between">
              <span className="text-lg font-bold text-slate-800">Sector educativo</span>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Tipología de Prestación</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-12 gap-8 items-center py-4">
              <div className="sm:col-span-5 flex justify-center relative">
                <svg className="w-44 h-44 transform -rotate-90" viewBox="0 0 120 120">
                  <circle className="text-slate-100" cx="60" cy="60" fill="none" r="48" stroke="currentColor" strokeWidth="16"></circle>
                  <circle className="text-[#0d6efd]" cx="60" cy="60" fill="none" r="48" stroke="currentColor" strokeDasharray="225.3 301.6" strokeDashoffset="0" strokeWidth="16"></circle>
                  <circle className="text-[#4f46e5]" cx="60" cy="60" fill="none" r="48" stroke="currentColor" strokeDasharray="63.0 301.6" strokeDashoffset="-225.3" strokeWidth="16"></circle>
                  <circle className="text-[#60a5fa]" cx="60" cy="60" fill="none" r="48" stroke="currentColor" strokeDasharray="12.0 301.6" strokeDashoffset="-288.3" strokeWidth="16"></circle>
                  <circle className="text-slate-300" cx="60" cy="60" fill="none" r="48" stroke="currentColor" strokeDasharray="2 301.6" strokeDashoffset="-300.3" strokeWidth="16"></circle>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-3xl font-extrabold text-slate-900 leading-none">74.7%</span>
                  <span className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mt-1">Público</span>
                </div>
              </div>

              <div className="sm:col-span-7 flex flex-col gap-3">
                <SectorLegend name="Público" pct="74.7%" count="3,211,268" colorClass="bg-[#0d6efd]" />
                <SectorLegend name="Privado" pct="20.9%" count="898,467" colorClass="bg-[#4f46e5]" />
                <SectorLegend name="Cooperativa" pct="4.0%" count="171,955" colorClass="bg-[#60a5fa]" />
                <SectorLegend name="Municipal" pct="0.3%" count="12,897" colorClass="bg-slate-300" />
              </div>
            </div>
          </div>
          <div className="bg-slate-50 border border-slate-100 rounded-xl p-5 flex items-start gap-4">
            <span className="text-2xl select-none">💡</span>
            <p className="text-sm text-slate-700 leading-relaxed">
              <strong className="font-bold text-slate-900">Tres de cada cuatro estudiantes guatemaltecos</strong> asisten a centros educativos del sector público. El sector por cooperativa juega un rol clave en áreas comunitarias semirurales para el sostenimiento del ciclo básico.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

function LevelBar({ name, pct, value, colorClass, widthPct }) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-center text-sm">
        <span className="font-bold text-slate-700 flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${colorClass}`}></span> {name}
        </span>
        <span className="font-bold text-slate-900">{pct}% <span className="text-slate-400 font-medium text-xs ml-1">({value})</span></span>
      </div>
      <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
        <div className={`${colorClass} h-full rounded-full transition-all duration-700`} style={{ width: `${widthPct || pct}%` }}></div>
      </div>
    </div>
  );
}

function SectorLegend({ name, pct, count, colorClass }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-100 transition-colors">
      <div className="flex items-center gap-2.5">
        <span className={`w-3.5 h-3.5 rounded-md ${colorClass}`}></span>
        <span className="text-sm font-bold text-slate-700">{name}</span>
      </div>
      <div className="text-right flex flex-col">
        <span className="text-sm font-extrabold text-slate-900">{pct}</span>
        <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wide">{count} alumnos</span>
      </div>
    </div>
  );
}
