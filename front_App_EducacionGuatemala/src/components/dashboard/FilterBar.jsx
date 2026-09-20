import { useState } from 'react';

const DEPARTAMENTOS = [
  "Guatemala", "Alta Verapaz", "Baja Verapaz", "Chimaltenango", "Chiquimula",
  "El Progreso", "Escuintla", "Huehuetenango", "Izabal", "Jalapa", "Jutiapa",
  "Petén", "Quetzaltenango", "Quiché", "Retalhuleu", "Sacatepéquez", "San Marcos",
  "Santa Rosa", "Sololá", "Suchitepéquez", "Totonicapán", "Zacapa"
];

export default function FilterBar() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedDept, setSelectedDept] = useState("Todos los departamentos (22)");
  const [activeLevel, setActiveLevel] = useState("Todos los niveles");

  return (
    <section className="px-8 pt-8 pb-6 bg-white border-b border-slate-200">
      <div className="max-w-7xl mx-auto flex flex-col gap-6">
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-bold bg-[#e0e7ff] text-[#4f46e5] tracking-wider uppercase">
                Tablero Estratégico Ministerial
              </span>
              <span className="text-xs text-slate-500 flex items-center gap-1.5 font-medium">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-[#0d6efd]"></span>
                Corte Anual Consolidado
              </span>
            </div>
            <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mt-1">
              Educación en Guatemala — 2024
            </h1>
            <p className="text-[15px] text-slate-500 max-w-2xl mt-1">
              Explora los datos educativos de Guatemala de forma clara y comprensible para el diseño de políticas públicas de alto impacto.
            </p>
          </div>
          
          <div className="flex items-center gap-3 self-start lg:self-auto bg-slate-50 border border-slate-200 px-4 py-3 rounded-xl">
            <div className="w-8 h-8 rounded-lg bg-[#e0e7ff] flex items-center justify-center text-[#4f46e5]">
              <span className="material-symbols-outlined text-[20px]">dataset</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Muestra Activa</span>
              <span className="text-sm text-slate-900 font-semibold">100% Cobertura Censal INE</span>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-4">
          <div className="flex flex-wrap items-center gap-6">
            <div className="relative inline-block text-left">
              <div 
                className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-[#eff6ff] text-[#0d6efd] font-semibold text-sm cursor-pointer hover:bg-blue-100 transition-colors"
                onClick={() => setIsOpen(!isOpen)}
              >
                <span className="material-symbols-outlined text-[18px]">location_on</span>
                <span>{selectedDept}</span>
                <span className="material-symbols-outlined text-[18px] ml-1">arrow_drop_down</span>
              </div>
              
              {isOpen && (
                <div className="absolute left-0 mt-2 w-64 max-h-72 overflow-y-auto bg-white rounded-xl shadow-xl z-50 p-2 border border-slate-100 flex flex-col gap-0.5">
                  <button 
                    onClick={() => { setSelectedDept("Todos los departamentos (22)"); setIsOpen(false); }}
                    className="w-full text-left px-3 py-2 rounded-lg text-sm font-semibold text-[#0d6efd] hover:bg-slate-50 transition-colors"
                  >
                    Todos los departamentos (22)
                  </button>
                  {DEPARTAMENTOS.map(dept => (
                    <button 
                      key={dept}
                      onClick={() => { setSelectedDept(dept); setIsOpen(false); }}
                      className="w-full text-left px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                    >
                      {dept}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className="flex items-center gap-4">
              {['Todos los niveles', 'Preprimaria', 'Primaria', 'Básico', 'Diversificado', 'Primaria de adultos'].map(lvl => (
                <button 
                  key={lvl}
                  onClick={() => setActiveLevel(lvl)}
                  className={`text-sm font-semibold transition-all ${
                    activeLevel === lvl 
                      ? 'bg-black text-white px-4 py-1.5 rounded-full' 
                      : 'text-slate-500 hover:text-slate-900'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#eff6ff] text-[#0d6efd]">
            <span className="w-2 h-2 rounded-full bg-[#0d6efd] animate-pulse"></span>
            <span className="text-xs font-semibold">
              Filtro activo: {selectedDept === "Todos los departamentos (22)" ? "Nacional" : selectedDept} | {activeLevel}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
