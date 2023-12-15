"use client"
import React from 'react';
import Navbar from "../Report/navbar";
import Dropdown from "./devicetype"
import LocDropdown from "./location"

import Select from "react-select";
import { useState, useEffect, useMemo } from "react";


const App = () => {
    const [options, setOptions] = useState([]);
    const [selectedColumn, setSelectedColumn] = useState("device_serial_number"); // Initialize selectedColumn state variable
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://51.20.249.252:8000/devices");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const device_data = await response.json();

                // Since device_data is the array, map directly over it
                if (Array.isArray(device_data)) {
                    const newOptions = device_data.map((device) => ({
                        value: device.device_serial_number,
                        label: device.device_serial_number
                    }));
                    setOptions(newOptions);
                    // setDeviceData(device_data); // Assuming you still want to set this state
                } else {
                    console.log("device_data is not an array");
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }

        };

        fetchData();
    }, []);

    return (
        <main>
            <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
                <Navbar />
            </div>
            <div className='flex' >
                <Dropdown />
                {/* </div>
                <div className='px-40 py-24'> */}
                <LocDropdown />
                <div className="flex items-center mb-4 mt-0">
                    <label className="mr-2 text-sm md:text-base">Sr. No.</label>
                    <Select
                        className="flex w-full md:w-40 filter-select" // Added flex class
                        value={options.find(option => option.value === selectedColumn)}
                        onChange={(option) => setSelectedColumn(option.value)}
                        options={options}
                    />
                </div>
            </div>

        </main>
    );
}

export default App;
