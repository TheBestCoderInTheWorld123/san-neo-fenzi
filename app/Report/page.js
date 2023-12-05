"use client";
import React, { useState, useEffect, useMemo } from "react";
import Navbar from "./navbar";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";
import Select from "react-select";
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

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

  const [currentPage, setCurrentPage] = useState(0);
  const recordsPerPage = 10; // Adjust the number of records per page as needed
  const totalPages = Math.ceil(data.length / recordsPerPage);

  const validateInputs = () => {
    // Basic validation: check if inputs are not empty
    if (!fromDateTime || !toDateTime || !selectedColumn) {
      // console.log("returning false");
      return false;
    }
      // Further validation can be added here (e.g., date range validation)
      // console.log("returning true");
    return true;
  };

  // Export functions
  const exportToPDF = () => {
    const unit = "pt";
    const size = "A4"; // Use A4 paper size
    const orientation = "landscape"; // Portrait or landscape
  
    const marginLeft = 40;
    const doc = new jsPDF(orientation, unit, size);
  
    doc.setFontSize(15);
  
    const title = `Report for Sr. No: ${selectedColumn}`;
    const headers = [["Sr. No.", "Timestamp", "AQ", "HUM", "TMP"]];
  
    const data_table = data.map((elt, index) => [
      index + 1, // Assuming you want to add a row index as "Sr. No."
      elt.latest_recorded_date,
      elt.tags.AQ,
      elt.tags.HUM,
      elt.tags.TMP,
    ]);
  
    let content = {
      startY: 50,
      head: headers,
      body: data_table,
    };
  
    doc.text(title, marginLeft, 40);
    doc.autoTable(content);
    doc.save("report.pdf")
  };

  const exportToExcel = () => {
  // Transform data for Excel if needed (in case of complex or nested structures)
  const worksheet = XLSX.utils.json_to_sheet(data.map(item => ({
    'Sr. No.': item.device_serial_number,
    'Timestamp': item.latest_recorded_date,
    'AQ': item.tags.AQ,
    'HUM': item.tags.HUM,
    'TMP': item.tags.TMP,
  })));
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
  XLSX.writeFile(workbook, 'table-data.xlsx');
};
  // Function to handle the pagination
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  // Calculate the current page data
  const currentTableData = useMemo(() => {
    const firstPageIndex = currentPage * recordsPerPage;
    const lastPageIndex = firstPageIndex + recordsPerPage;
    return data.slice(firstPageIndex, lastPageIndex);
  }, [currentPage, data]);


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



  const tableRows = currentTableData ? currentTableData.map((row) => (
    <tr key={row.latest_recorded_date}>
      <td>{row.device_serial_number}</td>
      <td>{row.latest_recorded_date}</td>
      <td>{row.tags.AQ}</td>
      <td>{row.tags.HUM}</td>
      <td>{row.tags.TMP}</td>
    </tr>
  )) : null;

    const showTableClick = async () => {

      // Clear existing data
    setData([]);

      // Check if inputs are valid
    if (!validateInputs()) {
       alert('Please fill in all required fields correctly.');
       return;
    }  
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

                <button className="tablebutton" onClick={() => showTableClick()} disabled={!validateInputs()}>
                  Show Data
                </button>
              </div>

              <div>
                {showTable && (
                  <>
                   <div className="flex justify-end mb-2">
                   <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2" onClick={exportToPDF}>Export to PDF</button>
                   <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={exportToExcel}>Export to Excel</button>
                 </div>
                  <Row>
                    <Col>
                      <Card className="mb-3">
                        {/* <CardHeader className="font-extrabold text-lg py-6"></CardHeader> */}

                        <div className="overflow-auto" style={{ maxHeight: '600px' }}>
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
                  <div className="flex justify-between items-center mt-4">
              <div>
                <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-l" onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 0}>Previous</button>
                <span className="mx-2">Page {currentPage + 1} of {totalPages}</span>
                <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-r" onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage >= totalPages - 1}>Next</button>
              </div>
              <div className="text-sm">
                Total Records: {data.length}
              </div>
            </div>
          </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </main> 
  )
};
