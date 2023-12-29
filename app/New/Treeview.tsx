"use client"
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
// import "./styles.css"; // Import your styles file

interface Location {
  location_id: number;
  location_name: string;
  location_root: number;
  children: Location[];
}

export default function FileSystemNavigator() {
  const [location, setLocations] = useState([]);
  const [expanded, setExpanded] = useState<string[]>([]);
  const [selected, setSelected] = useState("");
  const anchorEl = useRef<HTMLElement>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isDeleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [isAddDivVisible, setIsAddDivVisible] = useState(false);
  const [isUpdateDivVisible, setIsUpdateDivVisible] = useState(false);
  const [contextMenu, setContextMenu] = useState<{
    mouseX: number;
    mouseY: number;
  } | null>(null);


  const handleClick = (event: React.MouseEvent) => {
    setIsOpen(!isOpen);
    event.preventDefault(); // to prevent the browser's context menu from opening
    setContextMenu(
      contextMenu === null
        ? { mouseX: event.clientX - 2, mouseY: event.clientY - 4 }
        : // repeated contextmenu when it is already open closes it with Chrome 84 on Ubuntu
        // Other native context menus might behave different.
        // With this behavior we prevent contextmenu from the backdrop to re-locale existing context menus.
        null,
    );
  };

  const handleClose = (event: SyntheticEvent) => {
    setIsOpen(false);
    if ((event.target as HTMLElement).textContent === "Add") {
      setIsUpdateDivVisible(false);
      setIsAddDivVisible(true);
    } else if ((event.target as HTMLElement).textContent === "Update") {
      setIsAddDivVisible(false);
      setIsUpdateDivVisible(true);
    } else if ((event.target as HTMLElement).textContent === "Delete") {
      setDeleteDialogOpen(true);
    }
    setContextMenu(null);
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

  const handleToggle = (event: SyntheticEvent, nodeIds: string[]) => {
    setExpanded(nodeIds);
  };

  const handleSelect = (event: SyntheticEvent, nodeId: string) => {
    setSelected(nodeId);
    console.log("Selected node ID:", nodeId);
  };

  const buildTree = (data: Location[]) => {
    let tree: { [key: number]: Location } = {};

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

  const renderTree = (nodes: Location) => (
    <TreeItem
      key={nodes.location_id}
      nodeId={nodes.location_id.toString()}
      label={nodes.location_name}
      onContextMenu={handleClick}
    >
      {Array.isArray(nodes.children) && nodes.children.map((node) => renderTree(node))}
    </TreeItem>
  );

  const treeData = buildTree(location);

  return (
    <div className="flex bg-cyan-950 p-2 w-full h-full">
      <Box sx={{ height: '100%', flexGrow: 1, maxWidth: 350 }}>
        <div className="px-2 mb-6 text-lg font-extrabold text-white items-center justify-center">
          <p className="py-2 px-2">Locations</p>
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
        {isOpen && (
          <Menu
            anchorReference="anchorPosition"
            anchorPosition={
              contextMenu !== null
                ? { top: contextMenu.mouseY, left: contextMenu.mouseX }
                : undefined
            }
            open={contextMenu !== null}
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
      <div>
        {isAddDivVisible && (
          <main>
            <div className="border-cyan-950 bg-white w-full border-4 rounded-2xl px-8 py-4 shadow-xl">
              <p className="text-cyan-950 font-medium text-md my-2">Location Root: Penguin</p>

              <p className="text-cyan-950 font-medium text-md mt-3 mb-1">Serial Number</p>
              <input type="text" className="px-4 py-2 rounded-3xl border-cyan-950 border-2 text-cyan-950 text-sm font-medium" />

              <p className="text-cyan-950 font-medium text-md mt-3 mb-1">Device ID</p>
              <input type="text" className="px-4 py-2 rounded-3xl border-cyan-950 border-2 text-cyan-950 text-sm font-medium" />
<p></p>
              <button className="text-white font-medium rounded-lg text-sm px-4 py-2 bg-blue-500 hover:bg-blue-700 ml-24 mt-4">Add Device</button>
            </div>

            
          </main>
        )}
      </div>
      <div>
        {isUpdateDivVisible && (
          <div id="myDiv" className="m-4">
            <div className="flex">
              <input type="text" placeholder="Update" className="px-2 py-2 placeholder-gray-400 mr-2 rounded-lg text-cyan-950 border-cyan-700 border-2 text-sm font-medium" />
              <button className="text-white font-medium rounded-lg text-sm px-4 bg-blue-500 hover:bg-blue-700">Update</button>
            </div>
          </div>
        )}
      </div>
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
  );
}
