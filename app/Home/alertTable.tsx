import React, { useState } from 'react';
import { Card, Col, Row } from 'reactstrap';

interface AlertTableProps {
  searchTerm: string;
  handleSearchChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const AlertTable: React.FC<AlertTableProps> = ({ searchTerm, handleSearchChange }) => {
  return (
    <Row>
      <Col>
        <Card className="mb-3 px-6">
          <div className="card card-body">
            <div className="flex items-center mb-2 mx-2">
              <label className="mr-2 text-sm ml-4 md:text-base">Filter:</label>
              <input
                type="text"
                className="form-control border-1"
                placeholder="Search all columns..."
                value={searchTerm}
                onChange={handleSearchChange}
              />
            </div>
            <table className="table table-hover w-full">
              <thead className="bg-blue-200">
                <tr>
                  <th>Alert ID</th>
                  <th>Reported At</th>
                  <th>Alert Type</th>
                  <th>Device Sr No</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>A00001</td>
                  <td>2023-12-05 01:35:00</td>
                  <td>Critical</td>
                  <td>862174069140333</td>
                </tr>
                <tr>
                  <td>A00002</td>
                  <td>2023-12-03 01:35:00</td>
                  <td>Normal</td>
                  <td>862174069141333</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default AlertTable;
