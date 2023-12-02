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
  const [radioValue, setRadioValue] = useState("");

  const handleRadioChange = (value) => {
    setRadioValue(value);
  };
  useEffect(() => {
    let json;

    fetch('http://51.20.249.252:8000/get_device_pichart_data')
      .then(response => response.json())
      .then(fetchedJson => {
        json = fetchedJson; // Declare and assign json variable here
        setData(fetchedJson); // Use json variable to set data state
      });
  }, []);

  const [data, setData] = useState([]);
  useEffect(() => {
    fetch('http://51.20.249.252:8000/get_device_latest_records')
      .then(response => response.json())
      .then(data => {
        console.log()
        const mytable = document.getElementById('data-container');
        while (mytable.firstChild) {
          mytable.firstChild.remove();
        }


        for (const row of data.records) {
          const newRow = document.createElement('tr');
          var serialTD = document.createElement('td');
          serialTD.textContent = row.device_serial_number;
          var timeTD = document.createElement('td');
          timeTD.textContent = row.latest_recorded_date;
          var AQTD = document.createElement('td');
          AQTD.textContent = row.tags.AQ;
          var HUMTD = document.createElement('td');
          HUMTD.textContent = row.tags.HUM;
          var TMPTD = document.createElement('td');
          TMPTD.textContent = row.tags.TMP;

          newRow.appendChild(serialTD);
          newRow.appendChild(timeTD);
          newRow.appendChild(AQTD);
          newRow.appendChild(HUMTD);
          newRow.appendChild(TMPTD);
          mytable.appendChild(newRow);
        }

      });
  }, []);

  return (
    <div>
      <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
        <Navbar />
      </div>
      <div className="flex flex-wrap">
        <div className="w-full md:w-3/5 p-4">
          <Box>
            <RadioCard setRadioValue={handleRadioChange} />
            {radioValue === "Table" ?(
              <TablePage data={data} />
            ) : (
              <Box className="cursor-pointer border-spacing-4 m-4 display:inline-block">
                <Map />
              </Box>
            )}
          </Box>
        </div>
        <div className="w-full md:w-2/5 p-4 flex justify-center items-center">
          <div className="text-center">
            <h1 id="text" className="font-black text-3xl">Communication Status</h1>
            <Pie data={data} />
          </div>
        </div>
      </div>
      <div>
        <AlertTable />
      </div>
    </div>
  );
}