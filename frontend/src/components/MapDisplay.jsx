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

// Componente para ajustar el zoom a la ruta dinámicamente
function RouteFitter({ routePath }) {
  const map = useMap();
  useEffect(() => {
    // Escudo: Solo calcula los límites si hay una ruta y las coordenadas son válidas
    if (routePath && Array.isArray(routePath) && routePath.length > 0) {
      // Verificamos que el primer punto no sea nulo ni NaN
      if (routePath[0][0] != null && !isNaN(routePath[0][0])) {
        const bounds = L.latLngBounds(routePath);
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    }
  }, [routePath, map]);
  return null;
}

const MapDisplay = ({ origin, destination, mapData }) => {
  // Helper robusto para evitar que [null, null] o strings rompan Leaflet
  const getValidCoords = (coords, fallback) => {
    if (Array.isArray(coords) && coords.length === 2 && coords[0] != null && !isNaN(coords[0])) {
      return [Number(coords[0]), Number(coords[1])];
    }
    return fallback;
  };

  const defaultOrigin = [25.7617, -80.1918]; // Miami
  const defaultDest = [40.7128, -74.0060];   // NY

  // Pasamos los datos por el helper de validación
  const originCoords = getValidCoords(mapData?.origin_coords, defaultOrigin);
  const destCoords = getValidCoords(mapData?.destination_coords, defaultDest);
  
  // Si la ruta viene vacía (como te pasó en la consola), usa línea recta
  const routePath = mapData?.route_path && mapData.route_path.length > 0 
                    ? mapData.route_path 
                    : [originCoords, destCoords];

  return (
    <div className="h-full w-full rounded-xl overflow-hidden shadow-inner">
      <MapContainer 
        // PRO-TIP: Leaflet no actualiza el 'center' dinámicamente por defecto. 
        // Usar un key basado en las coordenadas fuerza a React a recargar el mapa cuando cambian.
        key={`${originCoords[0]}-${destCoords[0]}`} 
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
          <Popup>Origin: {origin || "Inicio"}</Popup>
        </Marker>

        <Marker position={destCoords}>
          <Popup>Destination: {destination || "Destino"}</Popup>
        </Marker>

        <Polyline positions={routePath} color="#2563eb" weight={4} opacity={0.8} />
      </MapContainer>
    </div>
  );
};

export default MapDisplay;