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
        <div className="flex">
          <div className="w-3/5 mt-4">
           <p id="text" className="text-center mb-4 font-black">Devices Data</p>
            <TablePage />
          </div>
          <div className="w-2/5">
            <Pie />
          </div>
        </div>
        <div className="flex flex-row">
          <div className="w-1/2 mt-6 flex-grow">
          <p id="text" className="text-center mb-4 font-black">Map</p>

            <Map />
          </div>
           <div className="w-1/2 flex-grow">
            <AlertTable />
          </div>
        </div> 
      </div>
    </div>
  );
}



  