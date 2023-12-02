"use client";
import React, { useState, useEffect } from "react";
import Navbar from "./navbar";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";
import Select from "react-select";

export default function Report() {
  const options = [
    { value: "device_serial_number", label: "Sr. No." },
    { value: "latest_recorded_date", label: "Timestamp" },
  ];

  const [data, setData] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState("device_serial_number"); // Initialize selectedColumn state variable
  const [showInput, setShowInput] = useState(false);
  const [filterText, setFilterText] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [showTable, setShowTable] = useState(false);

  useEffect(() => {
    fetch("http://51.20.249.252:8000/get_device_latest_records")
      .then((response) => response.json())
      .then((data) => {
        setData(data.records);
      });
  }, []);

  const handleFilterChange = (event) => {
    setFilterText(event.target.value);
  };

  const handleStartDateChange = (event) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event) => {
    setEndDate(event.target.value);
  };

  const applyFilter = () => {
    const filteredData = data.filter((item) => {
      if (selectedColumn === "device_serial_number") {
        return item.device_serial_number
          .toLowerCase()
          .includes(filterText.toLowerCase());
      } else if (selectedColumn === "latest_recorded_date") {
        const itemDate = new Date(item.latest_recorded_date);
        const startDateObj = new Date(startDate);
        const endDateObj = new Date(endDate);

        return itemDate >= startDateObj && itemDate <= endDateObj;
      } else {
        // Filter for other columns (AQ, HUM, TMP)
        return item[selectedColumn].toLowerCase().includes(filterText.toLowerCase());
      }
    });

    // Update the table data with the filtered data
    setData(filteredData);
  };

  const tableRows = data.map((row) => (
    <tr key={row.device_serial_number}>
      <td>{row.device_serial_number}</td>
      <td>{row.latest_recorded_date}</td>
      <td>{row.tags.AQ}</td>
      <td>{row.tags.HUM}</td>
      <td>{row.tags.TMP}</td>
    </tr>
  ));

  const showTableClick = () => {
    setShowTable(!showTable);
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
            <div className="flex p-6">
              <button id="tablebutton" onClick={() => showTableClick()}>
                Show Table
              </button>
            </div>

            <div className="flex-col mb-3">
              <div className="flex items-center mr-4">
                <label className="mr-2">Filter by:</label>
                <Select
                  className="filter-select"
                  value={selectedColumn}
                  onChange={(event) => setSelectedColumn(event.target.value)}
                  options={options}
                >
                  {options.map((option) => (
                    <option
                      className="filter-select" key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Select>
              </div>

              {showInput && (
                <div className="flex items-center mr-4">
                  <input
                    className="filter-input"
                    type="text"
                    placeholder="Enter filter text"
                    value={filterText}
                    onChange={handleFilterChange}
                  />
                </div>
              )}

              {selectedColumn === "latest_recorded_date" && (
                <div className="flex items-center mr-4">
                  <label className="mr-2">Start Date:</label>
                  <input
                    className="filter-date"
                    type="date"
                    value={startDate}
                    onChange={handleStartDateChange}
                  />
                </div>
              )}

              {selectedColumn === "latest_recorded_date" && (
                <div className="flex items-center mr-4">
                  <label className="mr-2">End Date:</label>
                  <input
                    className="filter-date"
                    type="date"
                    value={endDate}
                    onChange={handleEndDateChange}
                  />
                </div>
              )}

              <Button className="filter-button" color="primary" onClick={applyFilter}>
                Filter
              </Button>

              {showTable && (
                <Row>
                  <Col>
                    <Card className="mb-3 px-6">
                      <CardHeader className="font-extrabold text-lg py-6">Table</CardHeader>

                      <div id="TablePage" className="card card-body">
                        <table id="TablePage" className="table table-hover w-full">
                          <thead>
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
    </main>
  )
};
