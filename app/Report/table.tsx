"use client";
import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

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

const TablePage = () => {
  // Use the DeviceRecord type for the state
  const [data, setData] = useState<DeviceRecord[]>([]);

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

  // Function to return an icon based on the comm_status
  const getStatusIcon = (status: string) => {
    let color = status === 'green' ? 'green' : status === 'red' ? 'red' : 'orange';
    return <span className={`status-icon status-${color}`} />;
  };

  return (
    <div>
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
                  {data.map((row, index) => (
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
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default TablePage;
