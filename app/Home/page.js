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
    // console.log("MapTable called with value:", value);
    setShowMap(value == "Map");
  };

  return (
    <div>
  <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
    <Navbar />
  </div>
  <div className="flex-grow overflow-auto">
    {/* First Row with Map and Devices Data Table */}
    <div className="flex flex-col md:flex-row md:h-1/2">
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
      </div>
    </div>
  </div>
</div>

  );
}



  