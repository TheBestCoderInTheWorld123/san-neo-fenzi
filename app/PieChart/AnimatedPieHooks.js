"use client";
import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const AnimatedPieHooks = (props) => {
  const ref = useRef(null);
  const cache = useRef(props.data);
  const createPie = d3
    .pie()
    .value((d) => d.value)
    .sort(null);
  const createArc = d3
    .arc()
    .innerRadius(props.innerRadius)
    .outerRadius(props.outerRadius + 50);
  const colors = d3.scaleOrdinal(["yellow", "red", "green"]);
  const format = d3.format(".2f");

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('http://51.20.249.252:8000/get_device_pichart_data');

        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }

        const data = await response.json();
        return data;
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return null;
      }
    }

    async function handleData() {
      const fetchedData = await fetchData();
      if (fetchedData) {
        console.log('Fetched Data:', fetchedData);
      } else {
        console.error('Failed to fetch data.');
      }

      const svg = d3.select(ref.current);
      const group = svg.select('.pieGroup');

      const groupWithData = group.selectAll('g.arc').data(fetchedData);

      groupWithData.exit().remove();

      const groupWithUpdate = groupWithData
        .enter()
        .append("g")
        .attr("class", "arc");

      const path = groupWithUpdate
        .append("path")
        .merge(groupWithData.select("path.arc"));

      const arcTween = (d, i) => {
        const interpolator = d3.interpolate(prevData[i], d);

        return (t) => createArc(interpolator(t));
      };

      path
        .attr("class", "arc")
        .attr("fill", (d, i) => colors(i))
        .transition()
        .attrTween("d", arcTween);

      const text = groupWithUpdate
        .append("text")
        .merge(groupWithData.select("text"));

      text
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .style("fill", "black")
        .style("font-size", 20)
        .style("font-weight", "bold")
        .transition()
        .attr("transform", (d) => `translate(${createArc.centroid(d)})`)
        .tween("text", (d, i, nodes) => {
          const interpolator = d3.interpolate(prevData[i], d);

          return (t) => d3.select(nodes[i]).text(format(interpolator(t).value));
        });

      cache.current = props.data;
    }

    handleData();
  }, [props.data]);

  return (
    <svg ref={ref} width={600} height={600}>
      <g className="pieGroup"></g>
    </svg>
  );
};

export default AnimatedPieHooks;
