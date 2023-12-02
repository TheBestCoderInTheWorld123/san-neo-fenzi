"use client";
import React, { useState, useEffect } from "react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";

export default function Devices() {
    const [data, setData] = useState([]);
    useEffect(() => {
        fetch('http://51.20.249.252:8000/get_device_latest_records')
            .then(response => response.json())
            .then(data => {
                console.log()
                const mytable = document.getElementById('data-container');
                while (mytable.firstChild) {
                    mytable.firstChild.remove();
                }


                for (const row of data.records) {
                    const newRow = document.createElement('tr');
                    var serialTD = document.createElement('td');
                    serialTD.textContent = row.device_serial_number;
                    var timeTD = document.createElement('td');
                    timeTD.textContent = row.latest_recorded_date;
                    var AQTD = document.createElement('td');
                    AQTD.textContent = row.tags.AQ;
                    var HUMTD = document.createElement('td');
                    HUMTD.textContent = row.tags.HUM;
                    var TMPTD = document.createElement('td');
                    TMPTD.textContent = row.tags.TMP;

                    newRow.appendChild(serialTD);
                    newRow.appendChild(timeTD);
                    newRow.appendChild(AQTD);
                    newRow.appendChild(HUMTD);
                    newRow.appendChild(TMPTD);
                    mytable.appendChild(newRow);
                }

            });
    }, []);
    return (
        <main>
            <div>
                <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b"><Navbar /></div>
                <div>
                    <Row>
                        <Col>
                            <Card className="mb-3 px-6">
                                <CardHeader className="font-extrabold text-lg py-6">Table</CardHeader>
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
