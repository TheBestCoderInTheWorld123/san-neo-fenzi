"use client";
import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';
import ReactPaginate from 'react-paginate';
import jsPDF from 'jspdf';
import 'jspdf-autotable';


interface DeviceRecord {
  device_serial_number: string;
  latest_recorded_date: string;
  comm_satus: string;
  tags: {
    AQ: string;
    HUM: string;
    TMP: string;
  };
}

// Extend jsPDF to include autoTable
interface jsPDFWithAutoTable extends jsPDF {
    autoTable: (options: any) => void;
  }
const TableDevices = () => {
  // Use the DeviceRecord type for the state
  const [data, setData] = useState<DeviceRecord[]>([]);
  const [filteredData, setFilteredData] = useState<DeviceRecord[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  const [currentPage, setCurrentPage] = useState(0);
  const itemsPerPage = 10; // Adjust as needed

  // Export Functions
  const exportPDF = () => {
    
    const unit = "pt";
    const size = "A4"; // Use A4 paper size
    const orientation = "landscape"; // Portrait or landscape
  
    const marginLeft = 40;
    const doc = new jsPDF(orientation, unit, size)  as jsPDFWithAutoTable;
  
    doc.setFontSize(15);
  
    const title = `Latest Device Data`;
    const headers = [['Sr. No.', 'Status', 'Timestamp', 'AQ', 'HUM', 'TMP']];
    console.log("Exporting data:", filteredData); // Debugging line
    const data_table = filteredData.map((row, index) => [
        row.device_serial_number,
        row.comm_satus,
        row.latest_recorded_date,
        row.tags.AQ,
        row.tags.HUM,
        row.tags.TMP,
      ]);
      console.log("Data for PDF:", data_table);
    let content = {
      startY: 50,
      head: headers,
      body: data_table,
    };
  
    doc.text(title, marginLeft, 40);
    doc.autoTable(content);
    doc.save("Device_latest_data.pdf");
  };

  interface PageClickEvent {
    selected: number;
  }
  // Pagination Functions
  const handlePageClick = (event: PageClickEvent) => {
    setCurrentPage(event.selected);
  };

  const pageCount = Math.ceil(filteredData.length / itemsPerPage);
  const offset = currentPage * itemsPerPage;
  const currentPageData = filteredData.slice(offset, offset + itemsPerPage);

  const fetchData = () => {
    fetch('http://51.20.249.252:8000/get_device_latest_records')
      .then(response => response.json())
      .then((fetchedData: { records: DeviceRecord[] }) => { // Cast the fetched data to the expected shape
        setData(fetchedData.records);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };

  useEffect(() => {
    fetchData(); // Initial data fetch

    const intervalId = setInterval(fetchData, 50000); // Corrected the comment to match the interval

    // Clear interval on component unmount to prevent memory leaks
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    // Filter data when searchTerm changes
    const lowercasedFilter = searchTerm.toLowerCase();
    const filtered = data.filter(item =>
      Object.keys(item).some(key =>
        typeof item[key as keyof DeviceRecord] === 'string'
          ? (item[key as keyof DeviceRecord] as string).toLowerCase().includes(lowercasedFilter)
          : key === 'tags' && Object.entries(item.tags).some(([tagKey, tagValue]) =>
              // Convert the number to string before calling toLowerCase
              tagValue.toString().toLowerCase().includes(lowercasedFilter)
            )
      )
    );
  setFilteredData(filtered);
  }, [searchTerm, data]);

  // Function to return an icon based on the comm_status
  const getStatusIcon = (status: string) => {
    let color = status === 'green' ? 'green' : status === 'red' ? 'red' : 'orange';
    return <span className={`status-icon status-${color}`} />;
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };


  return (
    <div>
      {/* Search input for all columns */}
      <div className="flex items-center mb-2 md:mb-0 mx-2">
      <label className="mr-2 text-sm md:text-base">Filter:</label>
        <input
          type="text"
          className="form-control border-1"
          placeholder="Search all columns..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
         <div className="flex-grow md:flex md:items-center md:justify-end">
    {/* Export to PDF Button - On medium and larger screens, this will be aligned to the right */}
    <button
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      onClick={exportPDF}>
      Export to PDF
    </button>
  </div>
      </div>

    
      <Row>
        <Col>
          <Card className="mb-3 px-6">
            <CardBody>
              <Table hover>
                <thead className="bg-blue-200">
                  <tr>
                    <th>Sr. No.</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                    <th>AQ</th>
                    <th>HUM</th>
                    <th>TMP</th>
                  </tr>
                </thead>
                <tbody>
                  {currentPageData.map((row, index) => (
                    <tr key={index}>
                      <td>{row.device_serial_number}</td>
                      <td>{getStatusIcon(row.comm_satus)}</td>
                      <td>{row.latest_recorded_date}</td>
                      <td>{row.tags.AQ}</td>
                      <td>{row.tags.HUM}</td>
                      <td>{row.tags.TMP}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
              <div className="flex justify-center mt-4">
                <ReactPaginate
                  previousLabel={'previous'}
                  nextLabel={'next'}
                  breakLabel={'...'}
                  pageCount={pageCount}
                  marginPagesDisplayed={2}
                  pageRangeDisplayed={5}
                  onPageChange={handlePageClick}
                  containerClassName={'pagination'}
                  activeClassName={'active'}
                  className="flex list-none gap-2"
                  pageLinkClassName="py-2 px-3 bg-gray-300 hover:bg-gray-400 rounded"
                  previousLinkClassName="py-2 px-3 bg-gray-300 hover:bg-gray-400 rounded"
                  nextLinkClassName="py-2 px-3 bg-gray-300 hover:bg-gray-400 rounded"
                  breakLinkClassName="py-2 px-3 bg-gray-300 hover:bg-gray-400 rounded"
                  activeLinkClassName="bg-blue-500 text-white rounded"
                />
              {/* </div> */}
      </div>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default TableDevices;