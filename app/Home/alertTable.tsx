import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

export default function AlertTable() {
    return (
                
        <Row>
            <div className="font-extrabold text-lg py-6 text-center w-full"> {/* Center text */}
                    <h4>Alert Data</h4>
        </div>
        
            <Col>
                <Card className="mb-3 px-6 ">
                    <div className="card card-body">
                        <table className="table table-hover w-full">
                            <thead className="bg-blue-200">
                                <th>Alert ID</th>
                                <th>Alert Type</th>
                                <th>Device Sr No</th>
                                <th>Reported At</th>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>A00001</td>
                                    <td>Max temperature recorded</td>
                                    <td>862174069140333</td>
                                    <td>2023-12-05 01:35:00</td>
                                </tr>
                                <tr>
                                    <td>A00002</td>
                                    <td>Max Pressure recorded</td>
                                    <td>862174069141333</td>
                                    <td>2023-12-03 01:35:00</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Card>
            </Col>
        </Row>
    );
}