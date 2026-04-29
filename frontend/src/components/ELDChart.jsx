// frontend/src/components/ELDChart.jsx
import React from 'react';

const ELDChart = ({ logs }) => {
  if (!logs || logs.length === 0) return <p className="text-gray-400 text-center mt-10">No data to display</p>;

  // 1. Calcular el tiempo total del viaje para sacar porcentajes
  const tripStartTime = new Date(logs[0].start_time).getTime();
  const tripEndTime = new Date(logs[logs.length - 1].end_time).getTime();
  const totalDuration = tripEndTime - tripStartTime;

  // 2. Definir los 4 estados oficiales de la FMCSA y sus colores
  const dutyStates = [
    { id: 'OFF_DUTY', label: 'Off Duty', color: 'bg-gray-400' },
    { id: 'SLEEPER_BERTH', label: 'Sleeper Berth', color: 'bg-blue-500' },
    { id: 'DRIVING', label: 'Driving', color: 'bg-green-500' },
    { id: 'ON_DUTY_NOT_DRIVING', label: 'On Duty (Not Driving)', color: 'bg-yellow-500' }
  ];

  return (
    <div className="w-full bg-white border border-gray-200 rounded-lg p-4 overflow-x-auto">
      <div className="min-w-[600px]">
        {/* Encabezado del gráfico */}
        <div className="flex border-b border-gray-300 pb-2 mb-2">
          <div className="w-1/4 font-semibold text-gray-700 text-sm">Duty Status</div>
          <div className="w-3/4 font-semibold text-gray-700 text-sm text-center">Timeline Progression</div>
        </div>

        {/* Filas de la cuadrícula */}
        {dutyStates.map((state) => (
          <div key={state.id} className="flex items-center mb-1 h-8 group">
            {/* Etiqueta del estado */}
            <div className="w-1/4 text-xs font-medium text-gray-600 border-r border-gray-300 pr-2">
              {state.label}
            </div>
            
            {/* Línea de tiempo para este estado */}
            <div className="w-3/4 flex h-full bg-gray-50 border-y border-gray-100 relative">
              {logs.map((log, index) => {
                const logStart = new Date(log.start_time).getTime();
                const logEnd = new Date(log.end_time).getTime();
                const logDuration = logEnd - logStart;
                
                // Calcular qué porcentaje del ancho total representa este evento
                const widthPercent = (logDuration / totalDuration) * 100;

                return (
                  <div 
                    key={index}
                    style={{ width: `${widthPercent}%` }}
                    className={`h-full border-r border-white/50 transition-all duration-300 ${
                      log.status === state.id 
                        ? `${state.color} shadow-sm opacity-90 hover:opacity-100` 
                        : 'bg-transparent'
                    }`}
                    title={log.status === state.id ? `${log.remarks} (${Math.round(logDuration / 3600000)}h)` : ''}
                  ></div>
                );
              })}
            </div>
          </div>
        ))}
        
        {/* Eje X (Indicadores de inicio y fin) */}
        <div className="flex mt-2 text-xs text-gray-400">
          <div className="w-1/4"></div>
          <div className="w-3/4 flex justify-between px-1">
            <span>{new Date(tripStartTime).toLocaleDateString()} Start</span>
            <span>End Trip</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ELDChart;