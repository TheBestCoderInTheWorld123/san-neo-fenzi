import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'reactstrap';

interface Alert {
    id: number;
    time: string;
    alert_type: string;
    device_serial_num: string;
}

export default function AlertTable() {
    const [alerts, setAlerts] = useState<Alert[]>([]);

    useEffect(() => {
        const fetchData = () => {
            fetch('http://51.20.249.252:8000/latest_alerts')
                .then(response => response.json())
                .then(data => {
                    const sortedData = data.sort((a: Alert, b: Alert) => new Date(b.time).getTime() - new Date(a.time).getTime());
                    setAlerts(sortedData);
                })
                .catch(error => console.error('Error fetching data:', error));
        };

        fetchData(); // Fetch data initially
        const interval = setInterval(fetchData, 15000); // Fetch data every 15 seconds

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = {
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit', 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit', 
            hour12: false
        };
        return new Date(dateString).toLocaleString('en-GB', options).replace(/\//g, '-').replace(/, /g, ' ');
    };

    return (
        <Row>
            <Col>
                <Card className="mb-3 px-6 ">
                    <div className="card card-body" style={{ maxHeight: '400px', overflowY: 'scroll' }}>
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
                                {alerts.map(alert => (
                                    <tr key={alert.id}>
                                        <td>{alert.id}</td>
                                        <td>{formatDate(alert.time)}</td>
                                        <td>{alert.alert_type}</td>
                                        <td>{alert.device_serial_num}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </Card>
            </Col>
        </Row>
    );
}
