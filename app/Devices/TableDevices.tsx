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
    Hydrogen: number;
    Hydrogen_Sulfide: number;
    Ammonia: number;
    Ethanol: number;
    Toluene: number;
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
    const headers = [['Sr. No.', 'Status', 'Timestamp', 'AQ', 'HUM', 'TMP',"H2S","Ammonia","Ethanol","Toluene"]];
    console.log("Exporting data:", filteredData); // Debugging line
    const updatedData = filteredData.map(record => {
      const dependentValues = getDependentValues(parseFloat(record.tags.AQ));
      return {
        ...record,
        tags: {
          ...record.tags,
          ...dependentValues,
        },
      };
    });
    
    const data_table = updatedData.map((row, index) => [
        row.device_serial_number,
        row.comm_satus,
        row.latest_recorded_date,
        row.tags.AQ,
        row.tags.HUM,
        row.tags.TMP,
        // row.tags.Hydrogen,
        row.tags.Hydrogen_Sulfide,
        row.tags.Ammonia,
        row.tags.Ethanol,
        row.tags.Toluene
        
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

  const getDependentValues = (aqValue: number): { Hydrogen: number, Hydrogen_Sulfide: number, Ammonia: number, Ethanol: number, Toluene: number } => {
    let dependentValues: { Hydrogen: number, Hydrogen_Sulfide: number, Ammonia: number, Ethanol: number, Toluene: number } = {
      Hydrogen: 0,
      Hydrogen_Sulfide: 0,
      Ammonia: 0,
      Ethanol: 0,
      Toluene: 0
    };
  
    // Mapping of AQ values to the dependent values
    const mapping = [
      { AQ: 0.01, Hydrogen: 0, Hydrogen_Sulfide: 0, Ammonia: 0, Ethanol: 0, Toluene: 0 },
      { AQ: 0.02, Toluene: 20.85 },
      { AQ: 0.03, Toluene: 11.63 },
      { AQ: 0.04, Toluene: 7.64 },
      { AQ: 0.05, Ethanol: 30, Toluene: 5.68 },
      { AQ: 0.06, Ethanol: 27.49, Toluene: 4.52 },
      { AQ: 0.07, Ethanol: 21.94, Toluene: 3.71 },
      { AQ: 0.08, Ethanol: 18.06, Toluene: 3.11 },
      { AQ: 0.09, Ethanol: 15.8, Toluene: 2.73 },
      { AQ: 0.1, Ammonia: 30, Ethanol: 13.38, Toluene: 2.46 },
      { AQ: 0.2, Ammonia: 11.63, Ethanol: 4.22, Toluene: 1.03 },
      { AQ: 0.3, Ammonia: 6.28, Ethanol: 2.08 },
      { AQ: 0.4, Ammonia: 4, Ethanol: 1.26 },
      { AQ: 0.5, Ammonia: 2.78 },
      { AQ: 0.6, Hydrogen: 30, Hydrogen_Sulfide: 2.45, Ammonia: 1.37 },
      { AQ: 0.7, Hydrogen: 20, Hydrogen_Sulfide: 1.09 },
      { AQ: 0.8, Hydrogen: 14.35, Hydrogen_Sulfide: 0.6 },
      { AQ: 0.9, Hydrogen: 5, Hydrogen_Sulfide: 0.2 },
      { AQ: 1, Hydrogen: 1, Hydrogen_Sulfide: 0.1 }
      // { AQ: Number.POSITIVE_INFINITY } // Handle >1 case
    ];
  
    // Find the closest matching AQ value in the mapping
    const matchedMapping = mapping.find(item => aqValue <= item.AQ);
  
    // Assign the dependent values based on the matched mapping
    if (matchedMapping) {
      dependentValues = {
        ...dependentValues,
        ...matchedMapping // Assign matched values
      };
    }
  
    return dependentValues;
  };
  const fetchData = () => {
    fetch('http://51.20.249.252:8000/get_device_latest_records')
      .then(response => response.json())
      .then((fetchedData: { records: DeviceRecord[] }) => { // Cast the fetched data to the expected shape
        // setData(fetchedData.records);
          // Update DeviceRecord objects with calculated dependent values based on AQ
      const updatedData = fetchedData.records.map(record => {
        const dependentValues = getDependentValues(parseFloat(record.tags.AQ));
        return {
          ...record,
          tags: {
            ...record.tags,
            ...dependentValues,
          },
        };
      });
      setData(updatedData);
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
      <div className="flex items-center mb-2 mx-2">
      <label className="mr-2 text-sm ml-4 md:text-base">Filter:</label>
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
      id='button'
      className=" text-white font-bold py-2 mr-4 px-4 mb-2 rounded"
      onClick={exportPDF}>
      Export to PDF
    </button>
  </div>
      </div>

    
      <Row>
        <Col>
          <Card className="mb-3 px-6">
            <CardBody>
              <Table hover style={{ maxHeight: '400px', overflowY: 'scroll' }}>
                <thead className="bg-blue-200">
                  <tr>
                    <th>Sr. No.</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                    <th>AQ</th>
                    <th>HUM</th>
                    <th>TMP</th>
                    {/* <th>Hydrogen</th> */}
                    <th>H2S</th>
                    <th>Ammonia</th>
                    <th>Ethanol</th>
                    <th>Toluene</th>
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
                       {/* New columns based on updated mapping */}
                      {/* <td>{row.tags.Hydrogen}</td> */}
                      <td>{row.tags.Hydrogen_Sulfide}</td>
                      <td>{row.tags.Ammonia}</td>
                      <td>{row.tags.Ethanol}</td>
                      <td>{row.tags.Toluene}</td>
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