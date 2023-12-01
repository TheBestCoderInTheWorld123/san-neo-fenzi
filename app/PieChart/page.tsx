"use client";
import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import * as d3 from "d3";
import AnimatedPieHooks from "./AnimatedPieHooks";

const Pie = () => {

  const generateData = (value: any, length = 3) =>
    d3.range(length).map((item, index) => ({
      date: index,
      value: value === null || value === undefined ? Math.random() * 100 : value
    }));

  const [data, setData] = useState(generateData(0));
  const changeData = () => {
    setData(generateData(10));
  };

  let json;

  fetch('http://51.20.249.252:8000/get_device_pichart_data')
    .then(response => response.json())
    .then(fetchedJson => {
      json = fetchedJson; // Declare and assign json variable here
      setData(fetchedJson); // Use json variable to set data state
    });


  useEffect(
    () => {
      setData(generateData(10));
    },
    [!data]
  );

  return (
    <div className="App">
      <div>
        <AnimatedPieHooks
          data={json}
          width={500}
          height={500}
          innerRadius={100}
          outerRadius={150}
        />
      </div>
    </div>
  );
}

// const rootElement = document.getElementById("root");
// ReactDOM.render(<App />, rootElement);
export default Pie;