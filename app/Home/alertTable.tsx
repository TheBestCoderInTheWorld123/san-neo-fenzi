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
                            </thead>
                            <tbody>
                                <tr>
                                    {/* <td>Content 1</td>
                                    <td>Content 2</td>
                                    <td>Content 3</td> */}
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Card>
            </Col>
        </Row>
    );
}