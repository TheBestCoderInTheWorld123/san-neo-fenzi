"use client";
import React, { useState, useEffect } from "react";
import Navbar from "../Report/navbar";
import TablePage from "../Report/table";
import { Card, CardBody, CardHeader, Col, Row, Table, Button } from "reactstrap";
import Treeview from "./treeview";

export default function Devices() {
    const [data, setData] = useState([]);
    useEffect(() => {

    }, []);
    return (
        <main className="h-screen">
        <div className="flex flex-col h-full">
            <div id="sheet" className="px-4 py-4 flex justify-between items-center border-b"><Navbar /></div>
            <div className="flex flex-row flex-grow">
    {/* Treeview with Border and Title (30% Width) */}
    <div className="w-[20%] h-full border border-gray-300 overflow-auto">
        <h4 className="text-center text-xl mb-2">Treeview</h4>
        <Treeview />
    </div>

    {/* TablePage with Border and Title (70% Width) */}
    <div className="w-[80%] h-full border border-gray-300 overflow-auto">
        <h4 className="text-center text-xl mb-2">Devices Latest Data</h4>
        <div id="TablePage" className="h-full">
            <TablePage />
        </div>
    </div>
</div>

        </div>
    </main>
    
    
    )
};
