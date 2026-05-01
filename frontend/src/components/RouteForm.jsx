import React, { useState } from 'react';

const RouteForm = ({ onCalculate }) => {
  const [formData, setFormData] = useState({
    current_location: 'Miami, FL',
    pickup_location: 'Orlando, FL',
    dropoff_location: 'New York, NY',
    current_cycle_used: 0
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Si el usuario lo dejó vacío al enviar, lo tomamos como 0 por seguridad
    const dataToSend = {
      ...formData,
      current_cycle_used: formData.current_cycle_used === '' ? 0 : formData.current_cycle_used
    };
    onCalculate(dataToSend);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Current Location</label>
        <input 
          type="text" 
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.current_location}
          onChange={(e) => setFormData({...formData, current_location: e.target.value})}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Pickup Location</label>
        <input 
          type="text" 
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.pickup_location}
          onChange={(e) => setFormData({...formData, pickup_location: e.target.value})}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Drop-off Location</label>
        <input 
          type="text" 
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.dropoff_location}
          onChange={(e) => setFormData({...formData, dropoff_location: e.target.value})}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Cycle Hours Used (70h limit)</label>
        <input 
          type="number" 
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.current_cycle_used}
          // AQUÍ ESTÁ LA MAGIA: Operador ternario para evitar el NaN
          onChange={(e) => setFormData({
            ...formData, 
            current_cycle_used: e.target.value === '' ? '' : parseFloat(e.target.value)
          })}
        />
      </div>
      <button 
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors font-semibold"
      >
        Generate Trip Logs
      </button>
    </form>
  );
};

export default RouteForm;