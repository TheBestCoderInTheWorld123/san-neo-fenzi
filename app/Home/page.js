"use client";
import React, { useEffect, useState } from "react";
// import RadioCard from "./RadioCard";
import { Box, Table } from "@chakra-ui/react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import Pie from "../PieChart/page";
import AlertTable from "./alertTable";
import Map from "../Map/page";

export default function RadioButton() {

  const [showMap, setShowMap] = useState(true);

  const MapTable = (value) => {
    console.log("MapTable called with value:", value);
    setShowMap(value == "Map");
  };

  return (
    <div>
<<<<<<< Updated upstream
  <div>
    <Navbar />
  </div>
  <div className="flex-grow overflow-auto">
    {/* First Row with Map and Devices Data Table */}
    <div className="flex flex-col md:flex-row md:h-1/2">
=======
      <div>
        <Navbar />
      </div>
      <div className="flex-grow overflow-auto">
        {/* First Row with Map and Devices Data Table */}
        {/* <div className="flex flex-col md:flex-row md:h-1/2">
>>>>>>> Stashed changes
      <div className="w-full md:w-1/2 overflow-hidden">
        <h3 className="text-center text-xl mb-2">Devices on Map</h3>
        <div className="relative min-h-[200px] h-full">
          <Map />
        </div>
      </div>
      <div className="w-full md:w-1/2 overflow-x-auto">
        <h3 className="text-center text-xl mb-2">Devices Data</h3>
        <TablePage />
      </div>
<<<<<<< Updated upstream
    </div>

    {/* Second Row with Alert Table and Pie Chart */}
    <div className="flex flex-col md:flex-row md:h-1/2">
      <div className="w-full md:w-1/2 overflow-x-auto">
        <h3 className="text-center text-xl mb-2">Alert Details</h3>
        <AlertTable />
      </div>
      <div className="w-full md:w-1/2 overflow-hidden">
        <h3 className="text-center text-xl mb-2">Comm Status</h3>
        <div className="relative min-h-[200px] h-full">
          <Pie />
        </div>
=======
    </div> */}
        <div className="flex flex-col md:flex-row md:h-1/2 mt-2">
          <div className="w-full md:w-3/4 overflow-hidden">
            <h3 className="text-center text-2xl text-2f455c mb-2">Devices Data</h3>
            <div className="relative min-h-[200px] h-full">
              <TablePage />
            </div>
          </div>
          <div className="w-full md:w-1/4 overflow-hidden">
            <h3 className="text-center text-2xl text-2f455c mb-2">Communication Status</h3>
            <br></br>
            <div className="relative min-h-[200px] h-full">
              <Pie />
            </div>
          </div>
        </div>


        {/* Second Row with Alert Table and Pie Chart */}
        <div className="flex flex-col md:flex-row md:h-1/2">
          <div className="w-full md:w-3/4 relative min-h-[200px] h-full">
            <h3 className="text-center text-2xl text-2f455c mb-2">Alert Details</h3>
            <AlertTable />
          </div>
          {/* <div className="w-full md:w-1/2 overflow-hidden">
        <h3 className="text-center text-xl mb-2">Communication Status</h3>
        <div className="relative min-h-[200px] h-full">
          <Pie />
        </div>
      </div> */}
        </div>
>>>>>>> Stashed changes
      </div>
    </div>

  );
}



