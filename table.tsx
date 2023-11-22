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
              <CardHeader className = "font-extrabold text-lg pt-6">Table</CardHeader>
              <div className="card card-body">
                <table className="table table-hover w-3/5">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>First Name</th>
                      <th>Last Name</th>
                      <th>Username</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">1</th>
                      <td>Mark</td>
                      <td>Otto</td>
                      <td>@mdo</td>
                    </tr>
                    <tr>
                      <th scope="row">2</th>
                      <td>Jacob</td>
                      <td>Thornton</td>
                      <td>@fat</td>
                    </tr>
                    <tr>
                      <th scope="row">3</th>
                      <td>Larry</td>
                      <td>the Bird</td>
                      <td>@twitter</td>
                    </tr>
                  </tbody>
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