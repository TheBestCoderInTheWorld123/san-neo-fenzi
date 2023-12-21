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

  const handleClick = (event: SyntheticEvent) => {
    setIsOpen(true);
  };

  const handleClose = (event: SyntheticEvent) => {
    setIsOpen(false);
    if ((event.target as HTMLElement).textContent === "Add") {
      // Add your add logic here
    } else if ((event.target as HTMLElement).textContent === "Update") {
      // Add your update logic here
    } else if ((event.target as HTMLElement).textContent === "Delete") {
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
    <Box sx={{ minHeight: 180, flexGrow: 1, maxWidth: 300 }}>
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
          anchorEl={anchorEl.current}
          open={isOpen}
          onClose={handleClose}
        >
          <MenuItem onClick={handleClose}>Add</MenuItem>
          <MenuItem onClick={handleClose}>Update</MenuItem>
          <MenuItem onClick={handleClose}>Delete</MenuItem>
        </Menu>
      )}

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
    </Box>
  );
}
