'use client'
import React, { useState, useEffect } from 'react'

const LocDropdown = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleLocDropdown = () => {
        setIsOpen(!isOpen);
    };


    const closeLocDropdown = () => {
        setIsOpen(false);
    };

    return (
        <div className='py-3 px-4 pb-8'>
            <div className="relative inline-block">
                <button
                    type="button"
                    id="button"
                    className="px-4 py-2 text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm inline-flex items-center"
                    onClick={toggleLocDropdown}
                >

                    Location <svg className="w-2.5 h-2.5 ml-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
                    </svg>
                </button>
{/* 
                {isOpen && (
                    <div className="origin-top-right absolute right-0 mt-2 w-44 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                        <ul role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                            <li>
                                <a
                                    href="#"
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    onClick={closeLocDropdown}
                                >
                                    <button id="addButton">   Add</button>
                                </a>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    onClick={closeLocDropdown}
                                >
                                    Update
                                </a>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    onClick={closeLocDropdown}
                                >
                                    Delete
                                </a>
                            </li>
                        </ul>
                    </div>
                )} */}
            </div>
        </div >
    )
}

export default LocDropdown;