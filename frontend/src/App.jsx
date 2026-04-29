import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Spotter ELD Simulator
        </h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Panel Lateral: Formulario */}
          <div className="bg-white p-6 rounded-lg shadow-md lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Route Planner</h2>
            <p className="text-gray-500">Formulario próximamente...</p>
          </div>

          {/* Panel Principal: Mapa y Logbook */}
          <div className="space-y-6 lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-md h-96 flex items-center justify-center">
              <p className="text-gray-500">Mapa interactivo próximamente...</p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md h-64 flex items-center justify-center">
              <p className="text-gray-500">Gráfico ELD Logbook próximamente...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;