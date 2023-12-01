"use client";
import React, { useState, useEffect } from "react";
import Navbar from "./navbar";
import { Card, CardBody, CardHeader, Col, Row, Table } from "reactstrap";
import FilterDropdown from "./filterDropdown";

export default function Report() {
  const [data, setData] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState("device_serial_number"); // Initialize selectedColumn state variable
  const [showInput, setShowInput] = useState(false);

  useEffect(() => {
    fetch("http://51.20.249.252:8000/get_device_latest_records")
      .then((response) => response.json())
      .then((data) => {
        setData(data.records);
      });
  }, []);

  const tableRows = data.map((row) => (
    <tr key={row.device_serial_number}>
      <td>{row.device_serial_number}</td>
      <td>{row.latest_recorded_date}</td>
      <td>{row.tags.AQ}</td>
      <td>{row.tags.HUM}</td>
      <td>{row.tags.TMP}</td>
    </tr>
  ));

  const [showTable, setShowTable] = useState(false);

  const showTableClick = () => {
    setShowTable(!showTable);
  };

  const handleFilterChange = (event) => {
    const filterText = event.target.value;
    // Implement filtering logic based on selectedColumn and filterText
  };

  return (
    <main>
      {/* main div */}
      <div>
        <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b">
          <Navbar />
        </div>

        {/* main page div */}
        <div>
          <div id="TablePage">
            <div className="flex p-6">
              <FilterDropdown
                selectedColumn={selectedColumn} // Pass selectedColumn state variable as prop
                onChange={(selectedValue) => {
                  setSelectedColumn(selectedValue);
                  setShowInput(selectedValue ? true : false);
                }} // Pass setSelectedColumn function as prop and update showInput based on selectedValue
              />
              <button id="tablebutton" onClick={() => showTableClick()}>
                Show Table
              </button>
            </div>

            {showTable && (
              <Row>
                <Col>
                  <Card className="mb-3 px-6 ">
                    <CardHeader className="font-extrabold text-lg py-6">
                      Table
                    </CardHeader>

                    <div id="TablePage" className="card card-body">
                      <table id="TablePage" className="table table-hover w-full">
                        <thead>
                          <th>Sr. No.</th>
                          <th>Timestamp</th>
                          <th>AQ</th>
                          <th>HUM</th>
                          <th>TMP</th>
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

        {/* bottom bar */}
        <div></div>
      </div>
    </main>
  );
}
