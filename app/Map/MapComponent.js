// import React from 'react';
// import { MapContainer } from 'react-leaflet/MapContainer'
// import { TileLayer } from 'react-leaflet/TileLayer';
// import { Marker, Popup } from 'react-leaflet';
// import 'leaflet/dist/leaflet.css';
// import L from 'leaflet';

// const MapComponent = () => {
//   const indiaPosition = [18.9814649,73.0293557 ]; // Device 1 coordinates
//   const pakistanPosition = [19.143918298343383, 73.07723148801088 ]; // Device 2 icon
//   const customIcon = new L.Icon({
//     iconUrl: '/images/humidity.png', // Replace with the path to your icon
//     iconRetinaUrl: '/images/humidity_1.png', // Optional: for retina displays
//     iconSize: [25, 41], // Size of the icon
//     iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
//     popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
//     // shadowUrl: 'path/to/your/icon-shadow.png', // Optional: Path to your icon shadow image
//     // shadowSize: [41, 41] // Size of the shadow
// });


//   return (
//     <div style={{ height: '500px' }}>
//       <MapContainer
//         center={[18.5, 74.5]}
//         zoom={6}
//         style={{ height: '100%', width: '100%' }}
//       >
//         <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
//         {/* India Marker */}
//         <Marker position={indiaPosition} icon={customIcon}>
//           <Popup>
//             <b>Device-862174069140333</b>
//           </Popup>
//         </Marker>
//         {/* Pakistan Marker */}
//         <Marker position={pakistanPosition} icon={customIcon}>
//           <Popup>
//             <b>Device-862174069141333</b>
//           </Popup>
//         </Marker>
//       </MapContainer>
//     </div>
//   );
// };

// export default MapComponent;

import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const MapComponent = () => {
  const [locations, setLocations] = useState([]);
  const [devices, setDevices] = useState([]);
  const [deviceRecords, setDeviceRecords] = useState({});

  // Function to fetch locations
  const fetchLocations = async () => {
    try {
      const response = await fetch('http://51.20.249.252:8000/locations/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setLocations(data.filter(location => location.location_type_id === 0));
    } catch (error) {
      console.error('There was a problem fetching locations:', error);
    }
  };

  // Function to fetch devices
  const fetchDevices = async () => {
    try {
      const response = await fetch('http://51.20.249.252:8000/devices/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setDevices(data);
    } catch (error) {
      console.error('There was a problem fetching devices:', error);
    }
  };

  // Function to fetch device latest records
  const fetchDeviceRecords = async () => {
    try {
      const response = await fetch('http://51.20.249.252:8000/get_device_latest_records/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const recordsMap = data.records.reduce((map, record) => {
        map[record.device_serial_number] = record;
        return map;
      }, {});
      setDeviceRecords(recordsMap);
    } catch (error) {
      console.error('There was a problem fetching device records:', error);
    }
  };

  // Function to update all data
  const updateData = () => {
    fetchLocations();
    fetchDevices();
    fetchDeviceRecords();
  };

  useEffect(() => {
    updateData(); // Initial data fetch

    const interval = setInterval(() => {
      updateData(); // Update data every 10 seconds
    }, 5000);

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  // Fetch locations, devices, and device records on component mount
  useEffect(() => {
    fetchLocations();
    fetchDevices();
    fetchDeviceRecords();
  }, []);

  // Map location_id to device_serial_number
  const locationToDeviceMap = devices.reduce((map, device) => {
    map[device.location_id] = device.device_serial_number;
    return map;
  }, {});

  // Custom icon setup
  const customIcon = new L.Icon({
    iconUrl: '/images/humidity.png', // Replace with the path to your icon
    iconRetinaUrl: '/images/humidity_1.png', // Optional: for retina displays
    iconSize: [25, 41], // Size of the icon
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
    popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
  });

  const icons = {
    green: new L.Icon({
      iconUrl: '/images/humidity_green.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
    }),
    orange: new L.Icon({
      iconUrl: '/images/humidity_orange.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
    }),
    red: new L.Icon({
      iconUrl: '/images/humidity_red.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
    }),
  };

  return (
    <div style={{ height: '500px' }}>
    <MapContainer
      center={[18.5, 74.5]}
      zoom={6}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {locations.map((location) => {
        const serialNumber = locationToDeviceMap[location.location_id];
        const deviceRecord = deviceRecords[serialNumber];
        const commStatus = deviceRecord ? deviceRecord.comm_satus : 'red'; // Default to red if no data
        const icon = icons[commStatus] || icons.red; // Default icon if status is not recognized

        return (
          <Marker
            key={location.location_id}
            position={[location.latitude, location.longitude]}
            icon={icon}
          >
            <Popup>
              <b>{location.location_name}</b><br />
              Serial Number: {serialNumber}<br />
              {deviceRecord ? (
                <>
                  Temperature: {deviceRecord.tags.TMP} °C<br />
                  Air Quality: {deviceRecord.tags.AQ}<br />
                  Humidity: {deviceRecord.tags.HUM} %<br />
                  Last updated Date Time: {deviceRecord.latest_recorded_date}<br />
                  Communication Status: {deviceRecord.comm_satus}
                </>
              ) : 'Loading data...'}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  </div>
  );
};

export default MapComponent;
