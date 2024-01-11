"use client";
import React, { useEffect, useState } from "react";
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
      <div>
        <Navbar />
      </div>
      <div className="flex-grow overflow-auto">
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

        <div className="flex flex-col md:flex-row md:h-1/2">
          <div className="w-full md:w-3/4 relative min-h-[200px] h-full">
            <h3 className="text-center text-2xl text-2f455c mb-2">Alert Details</h3>
            <AlertTable />
          </div>
        </div>
      </div>
    </div>
  );
}
