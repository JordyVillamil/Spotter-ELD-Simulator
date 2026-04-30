import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Componente súper profesional que ajusta el zoom a la ruta dinámicamente
function RouteFitter({ routePath }) {
  const map = useMap();
  useEffect(() => {
    if (routePath && routePath.length > 0) {
      const bounds = L.latLngBounds(routePath);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [routePath, map]);
  return null;
}

const MapDisplay = ({ origin, destination, mapData }) => {
  // Coordenadas por defecto (Centro de EE. UU.)
  const defaultCenter = [39.8283, -98.5795];
  
  // Extraemos los datos dinámicos si existen
  const originCoords = mapData?.origin_coords || [25.7617, -80.1918];
  const destCoords = mapData?.destination_coords || [40.7128, -74.0060];
  const routePath = mapData?.route_path && mapData.route_path.length > 0 
                    ? mapData.route_path 
                    : [originCoords, destCoords];

  return (
    <div className="h-full w-full rounded-xl overflow-hidden shadow-inner">
      <MapContainer 
        center={originCoords} 
        zoom={4} 
        scrollWheelZoom={true}
        style={{ height: "400px", width: "100%", zIndex: 0 }}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <RouteFitter routePath={routePath} />

        <Marker position={originCoords}>
          <Popup>Origin: {origin}</Popup>
        </Marker>

        <Marker position={destCoords}>
          <Popup>Destination: {destination}</Popup>
        </Marker>

        {/* Línea dinámica real dibujando las curvas de la carretera */}
        <Polyline positions={routePath} color="#2563eb" weight={4} opacity={0.8} />
      </MapContainer>
    </div>
  );
};

export default MapDisplay;