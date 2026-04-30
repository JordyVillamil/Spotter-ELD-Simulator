import React, { useState } from 'react';
import RouteForm from './components/RouteForm';
import { calculateELD } from './services/api';
import MapDisplay from './components/MapDisplay';
import ELDChart from './components/ELDChart';

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async (data) => {
    setLoading(true);
    try {
      const result = await calculateELD(data);
      setLogs(result);
      console.log("Logs recibidos:", result);
    } catch (error) {
      alert("Error al conectar con el servidor. ¿Está encendido Django?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Spotter ELD Simulator</h1>
          <p className="text-gray-600">HOS Rules Compliance & Trip Planning</p>
        </header>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg lg:col-span-1 border border-gray-200">
            <h2 className="text-xl font-bold mb-6 text-gray-800 border-b pb-2">Trip Settings</h2>
            <RouteForm onCalculate={handleCalculate} />
          </div>

          <div className="space-y-6 lg:col-span-2">
            <div className="bg-white p-2 rounded-xl shadow-lg h-96 border border-gray-200 overflow-hidden">
              {loading ? (
                <div className="h-full w-full flex items-center justify-center bg-gray-50">
                   <p className="animate-pulse text-blue-600 font-semibold">Fetching Route Data...</p>
                </div>
              ) : (
                <MapDisplay 
                   origin={formData.current_location || "Miami, FL"} 
                   destination={formData.dropoff_location || "New York, NY"} 
                   mapData={apiResponseData.map_data}
                />
              )}
            </div>
            
            {/* Gráfico ELD (Logbook) */}
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
              <h2 className="text-xl font-bold mb-4 text-gray-800">24-Hour Logbook Grid</h2>
              {logs.length > 0 ? (
                <ELDChart logs={logs} />
              ) : (
                <div className="h-48 flex items-center justify-center bg-gray-50 rounded-lg border border-dashed border-gray-300">
                  <p className="text-gray-400">Genera una ruta para visualizar el gráfico ELD</p>
                </div>
              )}
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 min-h-[300px]">
              <h2 className="text-xl font-bold mb-4 text-gray-800">Electronic Logs (ELD)</h2>
              {logs.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm text-left">
                    <thead className="bg-gray-50 text-gray-700 uppercase font-semibold">
                      <tr>
                        <th className="px-4 py-2">Status</th>
                        <th className="px-4 py-2">Start</th>
                        <th className="px-4 py-2">End</th>
                        <th className="px-4 py-2">Location</th>
                        <th className="px-4 py-2">Remarks</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {logs.map((log, index) => (
                        <tr key={index} className="hover:bg-blue-50 transition-colors">
                          <td className="px-4 py-2 font-medium">{log.status}</td>
                          <td className="px-4 py-2">{new Date(log.start_time).toLocaleString()}</td>
                          <td className="px-4 py-2">{new Date(log.end_time).toLocaleString()}</td>
                          <td className="px-4 py-2">{log.location || 'In Transit'}</td>
                          <td className="px-4 py-2 text-gray-600 italic">{log.remarks}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-400 text-center mt-10">No logs generated yet. Please fill the form.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;