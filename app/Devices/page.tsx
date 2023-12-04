"use client";
import React, { useState, useEffect } from "react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";

export default function Devices() {
    const [data, setData] = useState([]);
    useEffect(() => {
        
    }, []);
    return (
        <main>
            <div>
                <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b"><Navbar /></div>
                <div>
                    <Row>
                        <Col>
                            <Card className="mb-3 px-6">
                            <div className="font-extrabold text-lg py-6 text-center w-full"> {/* Center text */}
                            <h4>Devices Latest Data</h4>
                            </div>
  
                                <div id="TablePage" className="card card-body">
                                    <TablePage />
                                </div>
                            </Card>
                        </Col>
                    </Row>
                </div>
            </div>
        </main>
    )
};
