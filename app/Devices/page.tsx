"use client";
import React, { useState, useEffect } from "react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";
import FileSystemNavigator from "./treeview";
// import { use } from 'next/navigation';


export default function Devices() {
    return (
        <main className="h-screen">
            <div className="flex flex-col h-full">
                <div className="px-4 py-4 flex justify-between items-center border-b">
                    <Navbar />
                </div>
                <div className="flex flex-col md:flex-row flex-grow">
                    <div className="w-full md:w-[20%] h-auto md:h-full border border-gray-300 overflow-auto">
                        <h4 className="text-center text-xl mb-2">Devices by Locations</h4>
                        <FileSystemNavigator />
                    </div>

                    <div className="w-full md:w-[80%] h-auto md:h-full border border-gray-300 overflow-auto mt-4 md:mt-0">
                        <h4 className="text-center text-xl mb-2">Devices Latest Data</h4>
                        <div className="h-full">
                            <TablePage />
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
