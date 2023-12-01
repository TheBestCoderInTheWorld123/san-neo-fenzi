import React from 'react';
import { MapContainer } from 'react-leaflet/MapContainer'
import { TileLayer } from 'react-leaflet/TileLayer';
import { Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
// import L from 'leaflet';

// delete L.Icon.Default.prototype._getIconUrl;

// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png').default,
//     iconUrl: require('leaflet/dist/images/marker-icon.png').default,
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png').default
// });

const MapComponent = () => {
  const indiaPosition = [20.5937, 78.9629]; // India's coordinates
  const pakistanPosition = [30.3753, 69.3451]; // Pakistan's coordinates

  return (
    <div style={{ height: '500px' }}>
      <MapContainer
        center={[23.5, 79]}
        zoom={5}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {/* India Marker */}
        <Marker position={indiaPosition}>
          <Popup>
            <b>India</b>
          </Popup>
        </Marker>
        {/* Pakistan Marker */}
        <Marker position={pakistanPosition}>
          <Popup>
            <b>Pakistan</b>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapComponent;