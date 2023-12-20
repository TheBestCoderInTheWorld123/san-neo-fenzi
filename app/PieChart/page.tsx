"use client";
import React, { useState, useEffect } from "react";
import AnimatedPieHooks from "./AnimatedPieHooks";

const Pie = () => {

  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch('http://51.20.249.252:8000/get_device_pichart_data')
      .then(response => response.json())
      .then(fetchedJson => {
        setData(fetchedJson);
        // console.log("Fetched Data: ", fetchedJson); // Log data here, right after setting it
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };

  useEffect(() => {
    fetchData(); // Initial data fetch

    const intervalId = setInterval(() => {
      fetchData(); // Fetch data every 5 seconds
    }, 5000);

    // Clear interval on component unmount to prevent memory leaks
    return () => clearInterval(intervalId);
  }, []); 

  return (
    <div className="App">
  <div className="flex flex-col items-center"> {/* Flex container to align children vertically */}
    {/* <div className="font-extrabold text-lg py-6 text-center w-full">  */}
    {/* Center text */}
       {/* <p id="text">Communication Status</p> 
     </div>  */}
    <AnimatedPieHooks
      data={data}
      width={500}
      height={500}
      innerRadius={50}
      outerRadius={100}
    />
  </div>
</div>
  );
};

export default Pie;
