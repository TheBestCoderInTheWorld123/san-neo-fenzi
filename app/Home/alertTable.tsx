import { Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

export default function AlertTable() {
    return (
        <Row>
            <Col>
                <Card className="mb-3 px-6 ">
                    <CardHeader className="font-extrabold text-lg py-6">Alert Table</CardHeader>
                    <div className="card card-body">
                        <table className="table table-hover w-full">
                            <thead>
                                <th>1</th>
                                <th>2</th>
                                <th>3</th>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Content 1</td>
                                    <td>Content 2</td>
                                    <td>Content 3</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </Card>
            </Col>
        </Row>
    );
}