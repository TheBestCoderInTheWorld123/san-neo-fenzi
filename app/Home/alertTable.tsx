import React, { useEffect, useState } from 'react';
import { Card, Col, Row } from 'reactstrap';

interface Alert {
    id: number;
    time: string;
    alert_type: string;
    device_serial_num: string;
    tag_name: string;
    tag_value: number;
}

export default function AlertTable() {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [latestId, setLatestId] = useState<number | null>(null);
    const [blink, setBlink] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://51.20.249.252:8000/latest_alerts');
                const data = await response.json();
                const sortedData = data.sort((a: Alert, b: Alert) => new Date(b.time).getTime() - new Date(a.time).getTime());
                //console.log(sortedData);
                setAlerts(sortedData);
                if (sortedData.length > 0 && sortedData[0].id !== latestId) {
                    setLatestId(sortedData[0].id);
                    setBlink(true);
                    setTimeout(() => setBlink(false), 5000); // Stop blinking after 5 seconds
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData(); // Fetch data initially
        const interval = setInterval(fetchData, 5000); // Fetch data every 15 seconds

        return () => clearInterval(interval); // Cleanup interval on component unmount
    },  [latestId]);

    const formatDate = (dateString: string) => {
        const [date, timeWithTimeZone] = dateString.split('T');
        const [time] = timeWithTimeZone.split('+');
    
        // Combine date and time for the final format
        return `${date} ${time}`;
    };
    const getAlertTypeClassName = (alertType: string) => {
        switch (alertType) {
            case 'CRITICAL':
                return 'alert-critical';
            case 'NORMAL':
                return 'alert-normal';
            default:
                return '';
        }
    };
    const isLatestRecord = (index: number) => {
        return index === 0; // Assuming the first record is the latest
    };

    return (
        <Row>
            <Col>
                <Card className="mb-3 px-6">
                    <div className="card card-body" style={{ minHeight:'250px', maxHeight: '400px', overflowY: 'scroll' }}>
                        <table className="table table-hover w-full">
                            <thead className="bg-blue-200">
                                <tr>
                                    <th>Alert ID</th>
                                    <th>Reported At</th>
                                    <th>Alert Type</th>
                                    <th>Device Sr No</th>
                                    <th>Tag Name</th>
                                    <th>Tag Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                {alerts.map((alert, index) => (
                                    <tr  className={index === 0 && blink ? 'blinking' : ''} key={alert.id}>
                                        <td>{alert.id}</td>
                                        <td>{formatDate(alert.time)}</td>
                                        {/* <td>{alert.alert_type}</td> */}
                                        <td>{alert.alert_type}</td>
                                        <td>{alert.device_serial_num}</td>
                                        <td>{alert.tag_name}</td>
                                        <td>{alert.tag_value}</td>
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
