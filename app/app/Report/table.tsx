"use client";
import React from 'react';
import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

const tableTypes = ['hover'];
const TablePage = () => {
  return (
    <div
      className="TablePage"
    >

      {tableTypes.map((tableType, index) => (
        <Row key={index}>
          <Col>
            <Card className="mb-3 px-6 ">
              <CardHeader className="font-extrabold text-lg py-6">Devices Data</CardHeader>
              <div className="card card-body">
                <table className="table table-hover w-full">
                  <thead>
                    <th>Sr. No.</th>
                    <th>Timestamp</th>
                    <th>AQ</th>
                    <th>HUM</th>
                    <th>TMP</th>
                  </thead>
                  <tbody id="data-container"></tbody>
                </table>
              </div>
            </Card>
          </Col>
        </Row>
      ))}


    </div>
  );
};

export default TablePage;
