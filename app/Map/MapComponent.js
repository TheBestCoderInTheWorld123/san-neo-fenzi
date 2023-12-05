import React from 'react';
import { MapContainer } from 'react-leaflet/MapContainer'
import { TileLayer } from 'react-leaflet/TileLayer';
import { Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// import L from 'leaflet';

// delete L.Icon.Default.prototype._getIconUrl;

// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png').default,
//     iconUrl: require('leaflet/dist/images/marker-icon.png').default,
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png').default
// });

const MapComponent = () => {
  const indiaPosition = [18.9814649,73.0293557 ]; // Device 1 coordinates
  const pakistanPosition = [19.143918298343383, 73.07723148801088 ]; // Device 2 icon
  const customIcon = new L.Icon({
    iconUrl: '/images/humidity.png', // Replace with the path to your icon
    iconRetinaUrl: '/images/humidity_1.png', // Optional: for retina displays
    iconSize: [25, 41], // Size of the icon
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
    popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
    // shadowUrl: 'path/to/your/icon-shadow.png', // Optional: Path to your icon shadow image
    // shadowSize: [41, 41] // Size of the shadow
});


  return (
    <div style={{ height: '500px' }}>
      <MapContainer
        center={[17.5, 73.5]}
        zoom={7}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {/* India Marker */}
        <Marker position={indiaPosition} icon={customIcon}>
          <Popup>
            <b>Device-862174069140333</b>
          </Popup>
        </Marker>
        {/* Pakistan Marker */}
        <Marker position={pakistanPosition} icon={customIcon}>
          <Popup>
            <b>Device-862174069141333</b>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapComponent;