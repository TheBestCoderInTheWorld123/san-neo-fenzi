"use client";
import React, { SyntheticEvent, useState, useEffect, useRef } from "react";
import Box from "@mui/material/Box";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Button from "@mui/material/Button";
import { TreeView, TreeItem } from "@mui/x-tree-view";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import Navbar from "../Report/navbar";
import Dropdown from "./devicetype";
import LocDropdown from "./location";
import Select from "react-select";

const Location = {
    location_id: Number,
    location_name: String,
    location_root: Number,
    children: Array,
};


const App = () => {
    const [options, setOptions] = useState([]);
    const [selectedColumn, setSelectedColumn] = useState("device_serial_number");
    const [location, setLocations] = useState([]);
    const [expanded, setExpanded] = useState([]);
    const [selected, setSelected] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [isDeleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [isAddDivVisible, setIsAddDivVisible] = useState(false);
    const [isUpdateDivVisible, setIsUpdateDivVisible] = useState(false);
    const [showDetailsDiv, setShowDetailsDiv] = useState(false);
    const [deviceDetails, setDeviceDetails] = useState(null);
    const [contextMenu, setContextMenu] = useState(null);
    const [selectedTreeItemName, setSelectedTreeItemName] = useState("");

    const handleClick = (treeItemName, event) => {
        event.preventDefault();
        event.stopPropagation();
        setSelectedTreeItemName(treeItemName);
        setContextMenu(
            contextMenu === null
                ? { mouseX: event.clientX, mouseY: event.clientY }
                : null
        );
        setIsOpen(!isOpen);
    };

    const handleClose = (event) => {
        setIsOpen(false);
        setContextMenu(null);

        const action = event.target.textContent;
        if (action === "Add") {
            setIsUpdateDivVisible(false);
            setIsAddDivVisible(true);
        } else if (action === "Update") {
            setIsAddDivVisible(false);
            setIsUpdateDivVisible(true);
        } else if (action === "Delete") {
            setIsAddDivVisible(false);
            setIsUpdateDivVisible(false);
            setDeleteDialogOpen(true);
        }
    };

    const handleDeleteConfirm = () => {
        // Add your delete logic here
        setDeleteDialogOpen(false);
    };

    const handleDeleteCancel = () => {
        setDeleteDialogOpen(false);
    };

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetch("http://51.20.249.252:8000/locations/");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data_x = await response.json();
                setLocations(data_x);
            } catch (error) {
                console.error("Failed to fetch locations:", error);
            }
        }

        fetchData();
    }, []);

    const handleToggle = (event, nodeIds) => {
        setExpanded(nodeIds);
    };

    const handleSelect = (event, nodeId) => {
        setSelected(nodeId);
        const selectedNode = event.target.textContent;
        setSelectedTreeItemName(selectedNode);
        console.log("Selected node ID:", nodeId, "Name:", selectedNode);
    
        fetchDeviceDetails(nodeId);
        setShowDetailsDiv(true);
        console.log('Show Details Div set to true');
    };
    
    const fetchDeviceDetails = async (nodeId) => {
        try {
            const response = await fetch(`http://51.20.249.252:8000/get_device_latest_records`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setDeviceDetails(data);
            console.log('Device Details:', data);
        } catch (error) {
            console.error("Error fetching device details:", error);
        }
    };

    const buildTree = (data) => {
        let tree = {};

        data.forEach((node) => {
            tree[node.location_id] = { ...node, children: [] };
        });

        Object.values(tree).forEach((node) => {
            if (node.location_root !== node.location_id && tree[node.location_root]) {
                tree[node.location_root].children.push(node);
            }
        });

        return Object.values(tree).filter((node) => node.location_root === node.location_id);
    };

    const renderTree = (nodes) => (
        <TreeItem
            key={nodes.location_id}
            nodeId={nodes.location_id.toString()}
            label={nodes.location_name}
            onContextMenu={(event) => handleClick(nodes.location_name, event)}
        >
            {Array.isArray(nodes.children) && nodes.children.map((node) => renderTree(node))}
        </TreeItem>
    );

    const treeData = buildTree(location);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://51.20.249.252:8000/devices");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const device_data = await response.json();
                if (Array.isArray(device_data)) {
                    const newOptions = device_data.map((device) => ({
                        value: device.device_serial_number,
                        label: device.device_serial_number
                    }));
                    setOptions(newOptions);
                } else {
                    console.log("device_data is not an array");
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }

        };

        fetchData();
    }, []);

    return (
        <main className='h-full min-h-screen'>
            <div className="w-full overflow-hidden">
                <Navbar />
            </div>
            <div className='flex h-full'>
                {/* Tree View */}
                <div className="flex bg-cyan-950 w-1/5 h-full shadow-inner shadow-black">
                    <Box sx={{ height: '100%', flexGrow: 1, maxWidth: 350 }}>
                        <div className="px-2 mb-6 text-lg font-extrabold text-white items-center justify-center">
                            <p className="py-2 px-2 mt-2">Locations</p>
                            <div className="w-full py-1 border-b-2 border-slate-200"></div>
                        </div>
                        <TreeView
                            aria-label="file system navigator"
                            defaultCollapseIcon={<ExpandMoreIcon />}
                            defaultExpandIcon={<ChevronRightIcon />}
                            expanded={expanded}
                            selected={selected}
                            onNodeToggle={handleToggle}
                            onNodeSelect={handleSelect}
                        >
                            {treeData.map((node) => renderTree(node))}
                        </TreeView>
                        {contextMenu !== null && (
                            <Menu
                                open={contextMenu !== null}
                                anchorReference="anchorPosition"
                                anchorPosition={
                                    { top: contextMenu.mouseY, left: contextMenu.mouseX }
                                }
                                onClose={handleClose}
                                PaperProps={{
                                    style: {
                                        maxHeight: '216px',
                                        width: '20ch',
                                    },
                                }}
                            >
                                <MenuItem id="addButton" onClick={handleClose}>Add</MenuItem>
                                <MenuItem onClick={handleClose}>Update</MenuItem>
                                <MenuItem onClick={handleClose}>Delete</MenuItem>
                            </Menu>
                        )}
                    </Box>
                    <Dialog
                        open={isDeleteDialogOpen}
                        onClose={handleDeleteCancel}
                        aria-labelledby="customized-dialog-title"
                        maxWidth="xs"
                        fullWidth
                    >
                        <DialogTitle id="customized-dialog-title" sx={{ background: "#2f455c", color: "#fff" }}>
                            Delete Confirmation
                        </DialogTitle>
                        <DialogContent dividers>
                            <DialogContentText sx={{ color: "#333" }}>
                                Are you sure you want to delete?
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button autoFocus onClick={handleDeleteCancel} color="primary">
                                Cancel
                            </Button>
                            <Button onClick={handleDeleteConfirm} color="error">
                                Delete
                            </Button>
                        </DialogActions>
                    </Dialog>
                </div>
                <div className='h-full'>
                    <div className="flex flex-grow">
                        <Dropdown />
                        <LocDropdown />
                        <div className="flex mr-2 itmes-center mb-4">

                            <label className="mr-4 text-sm py-4 md:text-base">Sr. No.</label>
                            <Select
                                className="py-4"
                                value={options.find(option => option.value === selectedColumn)}
                                onChange={(option) => setSelectedColumn(option.value)}
                                options={options}
                            />

                        </div>
                    </div>
                    <div>
                        <div>
                            {isAddDivVisible && (
                                <main>
                                    <div className="w-80 border-cyan-950 border-4 mx-4 rounded-2xl px-6 py-4 shadow-neutral-600 shadow-lg font-medium text-md flex flex-col items-center">
                                        <div>
                                            <p className="my-2">Adding Device Under: {selectedTreeItemName}</p>
                                            <p className="mt-3 mb-1">Device Status: Active</p>
                                            <p className="mt-3 mb-1">Serial Number</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Description</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Model Number</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Brand Name</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Device Type</p>
                                            <input type="text" className="add_device_input" />

                                            <p></p>
                                            <div className="text-right">
                                                <button id="button" className="mt-5 mb-2 shadow-md shadow-neutral-600 hover:shadow-lg hover:shadow-neutral-600 focus:shadow-md focus:shadow-neutral-600 text-white font-medium rounded-lg text-sm px-4 py-2">Add Device</button>
                                            </div>
                                        </div>
                                    </div>
                                </main>

                            )}
                        </div>
                        <div>
                            {isUpdateDivVisible && (
                                <main>
                                    <div className="w-80 border-cyan-950 border-4 mx-4 rounded-2xl px-6 py-4 shadow-neutral-600 shadow-lg font-medium text-md flex flex-col items-center">
                                        <div>
                                            <p className="my-2">Updating: {selectedTreeItemName}</p>
                                            <p className="mt-3 mb-1">Device Status: Active</p>
                                            <p className="mt-3 mb-1">Serial Number</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Description</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Model Number</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Brand Name</p>
                                            <input type="text" className="add_device_input" />
                                            <p className="mt-3 mb-1">Device Type</p>
                                            <input type="text" className="add_device_input" />

                                            <p></p>
                                            <div className="text-right">
                                                <button id="button" className="mt-5 mb-2 shadow-md shadow-neutral-600 hover:shadow-lg hover:shadow-neutral-600 focus:shadow-md focus:shadow-neutral-600 text-white font-medium rounded-lg text-sm px-4 py-2">Update</button>
                                            </div>
                                        </div>
                                    </div>
                                </main>
                            )}
                            {showDetailsDiv && deviceDetails && (
                                <div className="w-full text-bold ml-4">
                                    <div className="bg-gray-0 group block space-y-2 rounded-md border border-gray-200 p-6 pt-5 shadow-md shadow-black/5 transition-shadow duration-300 hover:shadow-lg">
                                    <p>Details for : {selectedTreeItemName}</p>
                                    <p>Device ID : {deviceDetails.device_serial_number}</p>
                                    <p>{deviceDetails.tags}</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}

export default App;
