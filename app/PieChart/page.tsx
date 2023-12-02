"use client";
import React, { useState, useEffect } from "react";
// import * as d3 from "d3";
import AnimatedPieHooks from "./AnimatedPieHooks";

const Pie = () => {
  // const generateData = (value:any, length = 3) =>
  //   d3.range(length).map((item, index) => ({
  //     date: index,
  //     value: value === null || value === undefined ? Math.random() * 100 : value,
  //   }));

  const [data, setData] = useState([]);

  //   useEffect(() => {
  //   fetchData();
  //   console.log(data);
  // }, []);

  const fetchData = () => {
    fetch('http://51.20.249.252:8000/get_device_pichart_data')
      .then(response => response.json())
      .then(fetchedJson => {
        setData(fetchedJson);
        console.log("Fetched Data: ", fetchedJson); // Log data here, right after setting it
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };
  useEffect(() => {
    fetchData();
  }, []);
 

  return (
    <div className="App">
      <div>
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
