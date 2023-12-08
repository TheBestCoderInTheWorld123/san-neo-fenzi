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
    <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
      <Navbar />
    </div>
    <div className="mb-4 h-screen">
      {/* First Row with Map and Devices Data Table */}
      <div className="flex flex-col md:flex-row h-[50vh]">
        {/* Map (50% Width) with Border and Title */}
        <div className="md:w-1/2 w-full overflow-auto border border-gray-300">
          <h3 className="text-center text-xl mb-2">Devices on Map</h3>
          <Map />
        </div>

        {/* Devices Data Table (50% Width) with Border and Title */}
        <div className="md:w-1/2 w-full overflow-auto border border-gray-300">
          <h3 className="text-center text-xl mb-2">Devices Data</h3>
          <TablePage />
        </div>
      </div>

      {/* Second Row with Alert Table and Pie Chart */}
      <div className="flex flex-col md:flex-row h-[50vh]">
        {/* Alert Table (50% Width) with Border and Title */}
        <div className="md:w-1/2 w-full overflow-auto border border-gray-300">
          <h3 className="text-center text-xl mb-2">Alert Details</h3>
          <AlertTable />
        </div>

        {/* Pie Chart (50% Width) with Border and Title */}
        <div className="md:w-1/2 w-full overflow-auto border border-gray-300">
          <h3 className="text-center text-xl mb-2">Comm Status</h3>
          <Pie />
        </div>
      </div> 
    </div>
</div>


  );
}



  