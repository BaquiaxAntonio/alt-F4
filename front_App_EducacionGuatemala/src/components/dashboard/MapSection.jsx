import { useState } from 'react';

const deptDescriptions = {
  "Petén": "El departamento más extenso del país cuenta con una dispersión geográfica alta, exigiendo esfuerzos logísticos prioritarios para la entrega de alimentación escolar y textos en zonas de reserva.",
  "Huehuetenango": "Presenta una de las mayores poblaciones estudiantiles rurales con un 78.5%. El multilingüismo (Mam, Q'anjob'al, Chuj, Akateko) exige una oferta docente bilingüe reforzada.",
  "Quiché": "Alta concentración rural (81.2%) con fuerte demanda de cobertura en Ciclo Básico para prevenir la migración temprana en comunidades del norte.",
  "Alta Verapaz": "Registra una de las tasas de deserción más sensibles (7.4%) debido a factores climáticos y estacionales agrícolas. Prioridad nacional para becas de retención.",
  "Izabal": "Comportamiento bimodal entre puertos urbanos y comunidades rurales de cuenca hidrográfica. El retiro escolar se acentúa en la transición a nivel diversificado.",
  "Quetzaltenango": "Constituye el polo educativo del suroccidente con sólida retención urbana e importante presencia de institutos experimentales y carreras técnicas.",
  "Departamento de Guatemala": "El departamento de Guatemala concentra la mayor infraestructura privada y diversificada del país. Presenta los indicadores de promoción más favorables del territorio nacional, con la menor tasa de rezago en nivel primario.",
  "Escuintla": "Corredor agroindustrial con tasa de promoción estable de 86.9%. El sector municipal complementa la oferta técnica en áreas periurbanas costeras."
};

const defaultDept = {
  name: "Departamento de Guatemala",
  pct: "21.5%",
  reg: "924,110",
  prom: "89.1%",
  ret: "3.8%",
  rural: "14.2%"
};

export default function MapSection() {
  const [activeDept, setActiveDept] = useState(defaultDept);
  const [tooltip, setTooltip] = useState({ show: false, x: 0, y: 0, name: '', data: '' });

  const handleMouseMove = (e, name, reg, pct) => {
    // Get relative position in the SVG container
    const rect = e.currentTarget.getBoundingClientRect();
    setTooltip({
      show: true,
      x: e.clientX - rect.left + 15,
      y: e.clientY - rect.top - 15,
      name,
      data: `${reg} alumnos (${pct})`
    });
  };

  const handleMouseLeave = () => {
    setTooltip({ ...tooltip, show: false });
  };

  const handleClick = (name, pct, reg, prom, ret, rural) => {
    setActiveDept({ name, pct, reg, prom, ret, rural });
  };

  const mapData = [
    { id: "map-peten", path: "M170,30 L360,30 L360,160 L240,160 L240,180 L180,180 L150,120 Z", color: "fill-blue-200 hover:fill-blue-600", name: "Petén", pct: "4.9%", prom: "84.2%", reg: "210,400", ret: "6.3%", rural: "72.1%", textX: 250, textY: 100, text: "PETÉN", textFill: "#0f172a", textSize: 11 },
    { id: "map-huehue", path: "M70,180 L160,180 L170,240 L110,250 L60,230 Z", color: "fill-blue-400 hover:fill-blue-600", name: "Huehuetenango", pct: "9.0%", prom: "84.6%", reg: "388,412", ret: "6.1%", rural: "78.5%", textX: 115, textY: 215, text: "HUEHUETENANGO", textFill: "#ffffff", textSize: 9 },
    { id: "map-quiche", path: "M160,180 L220,180 L230,260 L170,255 L165,220 Z", color: "fill-blue-400 hover:fill-blue-600", name: "Quiché", pct: "7.3%", prom: "82.8%", reg: "312,450", ret: "6.8%", rural: "81.2%", textX: 195, textY: 225, text: "QUICHÉ", textFill: "#ffffff", textSize: 9 },
    { id: "map-altaverapaz", path: "M220,170 L340,170 L330,230 L230,245 Z", color: "fill-blue-400 hover:fill-blue-600", name: "Alta Verapaz", pct: "9.2%", prom: "81.3%", reg: "395,200", ret: "7.4%", rural: "82.4%", textX: 280, textY: 205, text: "ALTA VERAPAZ", textFill: "#ffffff", textSize: 10 },
    { id: "map-izabal", path: "M340,170 L460,210 L440,260 L330,240 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Izabal", pct: "3.5%", prom: "83.1%", reg: "148,900", ret: "6.0%", rural: "66.5%", textX: 390, textY: 225, text: "IZABAL", textFill: "#0f172a", textSize: 10 },
    { id: "map-sanmarcos", path: "M30,230 L90,240 L80,300 L20,280 Z", color: "fill-blue-200 hover:fill-blue-600", name: "San Marcos", pct: "6.7%", prom: "86.1%", reg: "290,120", ret: "5.2%", rural: "76.0%", textX: 55, textY: 270, text: "S. MARCOS", textFill: "#0f172a", textSize: 8 },
    { id: "map-quetzaltenango", path: "M80,250 L130,250 L125,295 L75,295 Z", color: "fill-blue-200 hover:fill-blue-600", name: "Quetzaltenango", pct: "5.1%", prom: "88.4%", reg: "218,500", ret: "4.2%", rural: "49.8%", textX: 102, textY: 275, text: "QUETZAL.", textFill: "#0f172a", textSize: 8 },
    { id: "map-totonicapan", path: "M130,245 L170,250 L165,280 L125,280 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Totonicapán", pct: "3.0%", prom: "87.9%", reg: "128,400", ret: "4.8%", rural: "68.0%", textX: 146, textY: 266, text: "TOTO", textFill: "#0f172a", textSize: 7 },
    { id: "map-solola", path: "M125,285 L165,285 L160,315 L120,310 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Sololá", pct: "3.1%", prom: "87.2%", reg: "134,800", ret: "4.9%", rural: "64.1%", textX: 142, textY: 302, text: "SOLOLÁ", textFill: "#0f172a", textSize: 7 },
    { id: "map-chimaltenango", path: "M165,260 L215,260 L210,305 L160,305 Z", color: "fill-blue-200 hover:fill-blue-600", name: "Chimaltenango", pct: "4.2%", prom: "87.5%", reg: "182,300", ret: "4.5%", rural: "58.2%", textX: 187, textY: 285, text: "CHIMAL.", textFill: "#0f172a", textSize: 7 },
    { id: "map-bajaverapaz", path: "M215,245 L285,245 L275,280 L215,275 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Baja Verapaz", pct: "2.3%", prom: "84.9%", reg: "98,400", ret: "5.8%", rural: "74.2%", textX: 245, textY: 265, text: "B. VERAPAZ", textFill: "#0f172a", textSize: 8 },
    { id: "map-elprogreso", path: "M275,260 L330,260 L320,295 L270,290 Z", color: "fill-slate-200 hover:fill-blue-600", name: "El Progreso", pct: "1.3%", prom: "88.0%", reg: "54,200", ret: "4.1%", rural: "52.0%", textX: 298, textY: 280, text: "EL PROGRESO", textFill: "#0f172a", textSize: 7 },
    { id: "map-zacapa", path: "M330,250 L400,250 L390,295 L325,290 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Zacapa", pct: "1.8%", prom: "86.3%", reg: "76,800", ret: "4.9%", rural: "59.0%", textX: 360, textY: 275, text: "ZACAPA", textFill: "#0f172a", textSize: 8 },
    { id: "map-chiquimula", path: "M350,295 L415,295 L400,345 L345,335 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Chiquimula", pct: "2.8%", prom: "84.1%", reg: "122,100", ret: "6.3%", rural: "71.0%", textX: 375, textY: 320, text: "CHIQUIMULA", textFill: "#0f172a", textSize: 8 },
    { id: "map-guatemala", path: "M210,295 L265,290 L260,345 L205,340 Z", color: "fill-blue-600 hover:fill-blue-700", name: "Departamento de Guatemala", pct: "21.5%", prom: "89.1%", reg: "924,110", ret: "3.8%", rural: "14.2%", textX: 235, textY: 322, text: "GUATEMALA", textFill: "#ffffff", textSize: 9 },
    { id: "map-sacatepequez", path: "M190,305 L215,305 L210,335 L185,330 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Sacatepéquez", pct: "2.3%", prom: "89.5%", reg: "98,900", ret: "3.6%", rural: "22.0%", textX: 200, textY: 322, text: "SACAT.", textFill: "#0f172a", textSize: 6 },
    { id: "map-jalapa", path: "M270,295 L335,295 L330,345 L265,340 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Jalapa", pct: "2.6%", prom: "84.7%", reg: "112,600", ret: "5.9%", rural: "69.4%", textX: 298, textY: 322, text: "JALAPA", textFill: "#0f172a", textSize: 8 },
    { id: "map-suchitepequez", path: "M80,310 L150,315 L140,365 L70,355 Z", color: "fill-blue-200 hover:fill-blue-600", name: "Suchitepéquez", pct: "3.8%", prom: "85.4%", reg: "164,700", ret: "5.4%", rural: "62.5%", textX: 110, textY: 340, text: "SUCHITEPÉQUEZ", textFill: "#0f172a", textSize: 8 },
    { id: "map-retalhuleu", path: "M30,305 L80,310 L70,360 L25,345 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Retalhuleu", pct: "2.2%", prom: "86.5%", reg: "96,500", ret: "5.0%", rural: "58.7%", textX: 50, textY: 335, text: "RETAL.", textFill: "#0f172a", textSize: 7 },
    { id: "map-escuintla", path: "M150,340 L235,345 L225,395 L140,385 Z", color: "fill-blue-200 hover:fill-blue-600", name: "Escuintla", pct: "5.0%", prom: "86.9%", reg: "214,300", ret: "4.8%", rural: "48.1%", textX: 185, textY: 370, text: "ESCUINTLA", textFill: "#0f172a", textSize: 9 },
    { id: "map-santarosa", path: "M235,345 L300,345 L290,395 L225,390 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Santa Rosa", pct: "2.7%", prom: "85.7%", reg: "118,200", ret: "5.2%", rural: "66.8%", textX: 260, textY: 370, text: "SANTA ROSA", textFill: "#0f172a", textSize: 8 },
    { id: "map-jutiapa", path: "M300,345 L375,340 L360,395 L290,395 Z", color: "fill-slate-200 hover:fill-blue-600", name: "Jutiapa", pct: "3.4%", prom: "85.9%", reg: "146,800", ret: "5.3%", rural: "67.3%", textX: 330, textY: 370, text: "JUTIAPA", textFill: "#0f172a", textSize: 8 },
  ];

  return (
    <section className="bg-white rounded-2xl p-8 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col gap-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-2">
        <div className="flex flex-col gap-1">
          <span className="text-[11px] text-slate-500 uppercase font-bold tracking-widest">Territorialidad Geográfica</span>
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Educación por departamento (22 departamentos)</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-slate-500">Interactúa con el mapa o la tarjeta de selección</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Choropleth SVG Map Representation */}
        <div className="lg:col-span-7 bg-slate-50 border border-slate-100 rounded-2xl p-6 flex flex-col items-center justify-center relative min-h-[460px]">
          <div className="absolute top-4 left-4 z-10 flex flex-col gap-1.5 bg-white/90 backdrop-blur-md p-4 rounded-xl shadow-sm border border-slate-100">
            <span className="text-[10px] font-bold text-slate-900 uppercase tracking-widest mb-1">Quintiles de Matrícula</span>
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
              <span className="w-3.5 h-3.5 rounded-sm bg-blue-600"></span> <span>&gt; 500k (Muy Alta)</span>
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
              <span className="w-3.5 h-3.5 rounded-sm bg-blue-400"></span> <span>300k - 500k (Alta)</span>
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
              <span className="w-3.5 h-3.5 rounded-sm bg-blue-200"></span> <span>150k - 300k (Media)</span>
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
              <span className="w-3.5 h-3.5 rounded-sm bg-slate-200"></span> <span>&lt; 150k (Baja)</span>
            </div>
          </div>

          <svg className="w-full max-w-md h-auto drop-shadow-sm select-none relative z-0" fill="none" viewBox="0 0 500 480" xmlns="http://www.w3.org/2000/svg">
            {mapData.map((d) => (
              <g key={d.id}>
                <path 
                  id={d.id}
                  className={`cursor-pointer transition-all duration-200 stroke-white stroke-[1.5px] ${d.color}`}
                  d={d.path}
                  onMouseMove={(e) => handleMouseMove(e, d.name, d.reg, d.pct)}
                  onMouseLeave={handleMouseLeave}
                  onClick={() => handleClick(d.name, d.pct, d.reg, d.prom, d.ret, d.rural)}
                />
                <text fill={d.textFill} fontSize={d.textSize} fontWeight="800" pointerEvents="none" textAnchor="middle" x={d.textX} y={d.textY}>{d.text}</text>
              </g>
            ))}
          </svg>

          {/* Tooltip */}
          {tooltip.show && (
            <div 
              className="absolute pointer-events-none z-30 bg-[#1e293b] text-white px-3 py-2 rounded-lg text-xs font-medium shadow-xl flex flex-col gap-0.5 border border-slate-700"
              style={{ left: tooltip.x, top: tooltip.y }}
            >
              <span className="font-bold text-blue-400">{tooltip.name}</span>
              <span>{tooltip.data}</span>
            </div>
          )}
        </div>

        {/* Right: Dynamic Detailed Department Card */}
        <div className="lg:col-span-5 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between gap-6">
          <div className="flex flex-col gap-5">
            <div className="flex items-start justify-between">
              <div className="flex flex-col gap-1">
                <span className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Resumen Territorial</span>
                <h3 className="text-2xl font-extrabold text-slate-900">{activeDept.name}</h3>
              </div>
              <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-[10px] font-bold uppercase tracking-wider">
                {activeDept.pct} del País
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Matrícula</span>
                <span className="text-xl font-extrabold text-slate-900 mt-1 block">{activeDept.reg}</span>
                <span className="text-xs text-slate-500 font-medium mt-1 block">estudiantes</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Promoción</span>
                <span className="text-xl font-extrabold text-slate-900 mt-1 block">{activeDept.prom}</span>
                <span className="text-xs text-[#0d6efd] font-bold mt-1 block">+3.9% vs Promedio</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Deserción</span>
                <span className="text-xl font-extrabold text-slate-900 mt-1 block">{activeDept.ret}</span>
                <span className="text-xs text-slate-500 font-medium mt-1 block">Bajo la media</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Área Rural</span>
                <span className="text-xl font-extrabold text-slate-900 mt-1 block">{activeDept.rural}</span>
                <span className="text-xs text-slate-500 font-medium mt-1 block">Mayormente urbano</span>
              </div>
            </div>

            <div className="p-5 rounded-xl bg-blue-50 border border-blue-100 flex flex-col gap-2 mt-2">
              <span className="text-sm font-bold text-blue-900 flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px] text-blue-600">insights</span>
                Hallazgo Departamental
              </span>
              <p className="text-sm text-blue-900/80 leading-relaxed font-medium">
                {deptDescriptions[activeDept.name] || `Indicadores oficiales para el departamento de ${activeDept.name} consolidados a partir del corte censal 2024 del Ministerio de Educación de Guatemala.`}
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 mt-2 border-t border-slate-100">
            <span className="text-xs text-slate-500 font-medium pr-4">Haz clic sobre cualquier departamento del mapa para ver sus detalles.</span>
            <button 
              className="px-5 py-2.5 rounded-xl bg-[#0d6efd] text-white text-sm font-bold shadow-sm hover:bg-blue-600 transition-colors flex items-center gap-2 flex-shrink-0"
              onClick={() => alert('Explorando microdatos del departamento')}
            >
              <span>Municipios</span>
              <span className="material-symbols-outlined text-[18px]">chevron_right</span>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
