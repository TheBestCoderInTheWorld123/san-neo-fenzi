import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

export default function AlertTable() {
    return (
                
        <Row>
            <div className="font-extrabold text-lg mt-2 py-6 text-center w-full"> {/* Center text */}
                    <p id="text">Alert Data</p>
        </div>
        
            <Col>
                <Card className="mb-3 px-6 ">
                    <div className="card card-body">
                        <table className="table table-hover w-full">
                            <thead className="bg-blue-200">
                                <th>Alert ID</th>
                                <th>Reported At</th>
                                <th>Alert Type</th>
                                <th>Device Sr No</th>
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
}