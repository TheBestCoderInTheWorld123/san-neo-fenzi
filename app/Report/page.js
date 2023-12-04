"use client";
import React, { useState, useEffect } from "react";
import Navbar from "./navbar";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";
import Select from "react-select";

export default function Report() {
  const [data, setData] = useState([]);
  // const [rowData, setTableRows] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState("device_serial_number"); // Initialize selectedColumn state variable
  const [showInput, setShowInput] = useState(false);
  const [filterText, setFilterText] = useState("");
  const [fromDateTime, setStartDateTime] = useState("");
  const [toDateTime, setEndDateTime] = useState("");
  const [showTable, setShowTable] = useState(false);
  // const [options, setOptions, setDeviceData] = useState([]);
  const [options, setOptions] = useState([]);
  const [selectedSerialNumber, setSelectedSerialNumber] = useState('');

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

  useEffect(() => {
    console.log("Options updated:", options);
  }, [options]);



  // useEffect(() => {
  //   fetch("http://51.20.249.252:8000/history_by_device_serial_no")
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setData(data.records);
  //     });
  // }, []);

  const handleFilterChange = (event) => {
    setFilterText(event.target.value);
  };

  const handleStartDateTimeChange = (e) => setStartDateTime(e.target.value);
  const handleEndDateTimeChange = (e) => setEndDateTime(e.target.value);



  const tableRows = data ? data.map((row) => (
    <tr key={row.device_serial_number}>
      <td>{row.device_serial_number}</td>
      <td>{row.latest_recorded_date}</td>
      <td>{row.tags.AQ}</td>
      <td>{row.tags.HUM}</td>
      <td>{row.tags.TMP}</td>
    </tr>
  )) : null;

  // const showTableClick = async () => {
  //   // Construct the query parameters
  //   console.log(fromDateTime, toDateTime);
  //   const queryParams = new URLSearchParams({
  //     sno: selectedSerialNumber, // The serial number selected from the dropdown
  //     tdate: toDateTime, // Assuming this state holds the 'to' date
  //     fdate: fromDateTime // Assuming this state holds the 'from' date
  //   });

  //   try {
  //     const response = await fetch(`http://51.20.249.252:8000/history_by_device_serial_no?${queryParams}`);
  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }
  //     const historyData = await response.json();
  //     console.log(historyData);
  //     setData(historyData.records); // Be sure this is the correct place to set data
  //     setShowTable(true); // Update state to show table
  //   } catch (error) {
  //     console.error('Error fetching history data:', error);
  //   }
  // };

  const showTableClick = async () => {
    const formattedToDateTime = new Date(toDateTime).toISOString().replace(/\.\d{3}Z$/, '').replace('T', ' '); 
    const formattedFromDateTime = new Date(fromDateTime).toISOString().replace(/\.\d{3}Z$/, '').replace('T', ' '); 

    console.log(formattedFromDateTime, formattedToDateTime, selectedColumn);

    const queryParams = new URLSearchParams({
      sno: selectedColumn,
      tdate: formattedToDateTime,
      fdate: formattedFromDateTime
    });

    try {
      const response = await fetch(`http://51.20.249.252:8000/history_by_device_serial_no?${queryParams}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const historyData = await response.json();
      console.log(historyData);
      setData(historyData.records);
      setShowTable(true);
    } catch (error) {
      console.error('Error fetching history data:', error);
    }
  };



  return (
    <main>
      {/* Main div */}
      <div>
        <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
          <Navbar />
        </div>

        {/* Main page div */}
        <div>
          <div id="TablePage">
            <div className="flex-col m-4">
              <div className="flex items-center mr-4">
                <label className="mr-2">Sr. No.</label>
                <Select
                  className="filter-select"
                  value={options.find(option => option.value === selectedColumn)}
                  onChange={(option) => setSelectedColumn(option.value)}
                  options={options}
                />
                <label>Start Date and Time:</label>
                <input
                  className="filter-date"
                  type="datetime-local"
                  value={fromDateTime}
                  onChange={handleStartDateTimeChange}
                />

                <label>End Date and Time:</label>
                <input
                  className="filter-date"
                  type="datetime-local"
                  value={toDateTime}
                  onChange={handleEndDateTimeChange}
                />

                <button className="tablebutton" onClick={() => showTableClick()} >
                  Show Data
                </button>
              </div>

              <div>
                {showTable && (
                  <Row>
                    <Col>
                      <Card className="mb-3 px-6">
                        <CardHeader className="font-extrabold text-lg py-6">Table</CardHeader>

                        <div id="TablePage" className="card card-body">
                          <table id="TablePage" className="table table-hover w-full">
                            <thead className="bg-blue-200">
                              <tr>
                                <th>Sr. No.</th>
                                <th>Timestamp</th>
                                <th>AQ</th>
                                <th>HUM</th>
                                <th>TMP</th>
                              </tr>
                            </thead>
                            <tbody>{tableRows}</tbody>
                          </table>
                        </div>
                      </Card>
                    </Col>
                  </Row>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
};
