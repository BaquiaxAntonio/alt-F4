import { useState } from 'react';
import Layout from './components/layout/Layout';
import FilterBar from './components/dashboard/FilterBar';
import KPICards from './components/dashboard/KPICards';
import DistributionSection from './components/dashboard/DistributionSection';
import DemographicsSection from './components/dashboard/DemographicsSection';
import ResultsSection from './components/dashboard/ResultsSection';
import MapSection from './components/dashboard/MapSection';
import ChatModal from './components/chat/ChatModal';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <Layout openChat={() => setIsChatOpen(true)}>
      <FilterBar />
      
      <div className="max-w-7xl mx-auto w-full px-8 py-8 flex flex-col gap-8">
        <KPICards />
        <DistributionSection />
        <DemographicsSection />
        <ResultsSection />
        <MapSection />

        {/* Visual Storytelling Context Images */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="relative rounded-xl overflow-hidden shadow-sm h-52 bg-surface-container">
            <div 
              className="bg-cover bg-center w-full h-full" 
              style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBKaMYgIVdPdqmfZhbIvhuXUt7-yVjSzb76g6XadfE-vcZK4N-gnBw66gd6_8J4NaQtKUFi5tWR9YlXES7Hh88UDARD2q2hY1a2hO1zS74yNeg24ICVPf1TSVqOZbsE8t3gRqFqqdQoAYRao_fAkEuYc3Irdj1RMj6u02s83aV8lTO8s1ev6v63RgSIhy1XK5Ag99F_-UeLS7uYwho3YJ7fdTdpfS7OxqziA3QA9w')" }}>
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-primary-container/90 via-primary-container/30 to-transparent p-6 flex flex-col justify-end">
              <span className="text-caption-xs font-caption-xs font-semibold text-secondary-fixed uppercase tracking-wider">Cobertura en Primera Infancia y Primaria</span>
              <p className="text-body-md-medium text-body-md-medium text-on-primary mt-1">Más del 56% de la matrícula nacional se encuentra construyendo las bases del aprendizaje escolar en aulas de todo el país.</p>
            </div>
          </div>
          <div className="relative rounded-xl overflow-hidden shadow-sm h-52 bg-surface-container">
            <div 
              className="bg-cover bg-center w-full h-full" 
              style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCmSizw1F9IPJH7UPDR4R1CAXW2JM3ddBTix-_OzKUWHSwajOtpMmiptSOtfwXlcihh9kxdNqOcABLe49RAtYjAGtlIzxFEUK_H7bgd2mUhNTOp8UhyFVIeh9EsUpczP7CF4untVk1EfSuSS7Q_CTzRorkRYVdtnYtNi3hnccPZjtP0WHtnAp9P0PTn5onB5vSh4uj6UA-Kr8Cxc-W_Gwcnqe_7bWqq7ol-6OQctA')" }}>
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-primary-container/90 via-primary-container/30 to-transparent p-6 flex flex-col justify-end">
              <span className="text-caption-xs font-caption-xs font-semibold text-secondary-fixed uppercase tracking-wider">El Desafío de Secundaria y Retención</span>
              <p className="text-body-md-medium text-body-md-medium text-on-primary mt-1">Fortalecer la transición entre Primaria y Ciclo Básico es el eje clave de inversión para el desarrollo laboral sostenible.</p>
            </div>
          </div>
        </div>
      </div>

      <ChatModal isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </Layout>
  );
}

export default App;
