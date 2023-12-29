"use client";
import React, { useState, useEffect } from "react";
import Navbar from "../Report/navbar";
import TableDevices from "./TableDevices";
// import { use } from 'next/navigation';


export default function Devices() {
    return (
        <main className="h-screen">
            <div>
                <Navbar />
            </div>
            <div className="flex flex-col h-full">

                <div className="flex flex-col md:flex-row flex-grow">
                    <div className="w-full md:w-[100%] h-auto md:h-full border border-gray-300 overflow-auto mt-4 md:mt-0">
                        <h4 className="text-center text-xl mb-2">Devices Latest Data</h4>
                        <div className="h-full">
                            <TableDevices />
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
