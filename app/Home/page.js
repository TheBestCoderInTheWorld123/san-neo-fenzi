"use client";
import React, { useEffect, useState } from "react";
import RadioCard from "./RadioCard";
import { Box, Table } from "@chakra-ui/react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import Pie from "../PieChart/page";
import AlertTable from "./alertTable";
import Map from "../Map/page";

export default function RadioButton() {

  const [showMap, setShowMap] = useState(true);

  const toggleMapTable = (value) => {
    console.log("toggleMapTable called with value:", value);
    setShowMap(value == "Map");
  };

  return (
<div>
  <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
    <Navbar />
  </div>
  <div className="flex flex-row mb-4 h-screen"> 
    <div className="w-1/2 h-full p-4 border overflow-auto">
      <RadioCard setRadioValue={toggleMapTable} />
      {showMap ? <Map className="h-full" /> : <TablePage className="h-full" />}
    </div>
    {/* <!-- Second column for Pie and Alert Table with fixed 50% width --> */}
    <div className="w-1/2 h-full p-4 border flex flex-col">
      {/* <!-- Header Information --> */}
      <div className="mb-4">
      </div>
      {/* <!-- Pie chart section --> */}
      <div className="h-0.5/3 mb-4"> 
      {/* <!-- Adjust height as needed --> */}
        <Pie className="w-full h-full" />
         {/* <!-- Pie chart fills the container --> */}
      </div>
      {/* <!-- Alert table section --> */}
      <div className="h-2/4 overflow-auto">
        <AlertTable className="w-full h-full" /> 
      </div>
    </div>
  </div>
</div>

  );
}