import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix para los iconos de Leaflet en React/Vite
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Componente para re-centrar el mapa cuando cambian los datos
function ChangeView({ center }) {
  const map = useMap();
  map.setView(center, map.getZoom());
  return null;
}

const MapDisplay = ({ origin, destination }) => {
  // Coordenadas por defecto (Centro de EE. UU. si no hay datos)
  const defaultCenter = [39.8283, -98.5795];
  
  // En una prueba técnica real, usarías coordenadas devueltas por el backend.
  // Por ahora, usaremos coordenadas estáticas para Miami y NY para visualizar la ruta.
  const miamiCoords = [25.7617, -80.1918];
  const nyCoords = [40.7128, -74.0060];
  const routePath = [miamiCoords, nyCoords];

  return (
    <div className="h-full w-full rounded-xl overflow-hidden shadow-inner">
      <MapContainer 
        center={miamiCoords} 
        zoom={4} 
        scrollWheelZoom={true}
        style={{ height: "400px", width: "100%", zIndex: 0 }}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <ChangeView center={miamiCoords} />

        <Marker position={miamiCoords}>
          <Popup>Origin: {origin}</Popup>
        </Marker>

        <Marker position={nyCoords}>
          <Popup>Destination: {destination}</Popup>
        </Marker>

        {/* Línea que conecta los puntos */}
        <Polyline positions={routePath} color="blue" weight={3} opacity={0.7} dashArray="10, 10" />
      </MapContainer>
    </div>
  );
};

export default MapDisplay;