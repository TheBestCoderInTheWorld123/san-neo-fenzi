import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import { TreeView, TreeItem } from '@mui/x-tree-view';
// import TreeItem from '@mui/lab/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

interface Location {
  location_id: number;
  location_name: string;
  location_root: number;
  children: Location[];
}

export default function FileSystemNavigator() {
  const [data, setLocations] = useState([]);

  useEffect(() => {
    async function fetchData() {
        try {
            const response = await fetch('http://51.20.249.252:8000/locations/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data_x = await response.json();
            setLocations(data_x);
        } catch (error) {
            console.error('Failed to fetch locations:', error);
        }
    }

    fetchData();
  }, []);

  // const buildTree = (data: []) => {
  //   let tree = data.reduce((acc, node) => {
  //     acc[node.location_id] = { ...node, children: [] };
  //     return acc;
  //   }, {});

  //   Object.values(tree).forEach(node => {
  //     if (node.location_root !== node.location_id && tree[node.location_root]) {
  //       tree[node.location_root].children.push(node);
  //     }
  //   });

  //   return Object.values(tree).filter(node => node.location_root === node.location_id);
  // };

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
    <TreeItem key={nodes.location_id} nodeId={nodes.location_id.toString()} label={nodes.location_name}>
      {Array.isArray(nodes.children) && nodes.children.map((node) => renderTree(node))}
    </TreeItem>
  );
  const treeData = buildTree(data);

  return (
    <Box sx={{ minHeight: 180, flexGrow: 1, maxWidth: 300 }}>
      <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
      >
        {treeData.map((node) => renderTree(node))}
      </TreeView>
    </Box>
  );
}