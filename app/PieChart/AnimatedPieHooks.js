import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const AnimatedPieHooks = (props) => {
  const ref = useRef(null);
  const cache = useRef(props.data);
  const createPie = d3.pie().value((d) => d.value).sort(null);
  const innerRadius = 50; // Adjust the inner radius for the donut shape
  const outerRadius = 100; // Adjust the outer radius

  useEffect(() => {
    const { live_perc, offline_perc } = props.data;

    const pieData = [
      { label: "live", value: live_perc },
      { label: "offline", value: 100 - live_perc }
    ];

    const svg = d3.select(ref.current);

    const arc = d3
      .arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    const group = svg
      .append("g")
      .attr("class", "pieGroup")
      .attr("transform", `translate(${outerRadius}, ${outerRadius})`);

    const path = group
      .selectAll(".arc")
      .data(createPie(pieData))
      .enter()
      .append("path")
      .attr("class", "arc")
      .attr("fill", (d) => (d.data.label === "live" ? "green" : "red"))
      .attr("d", arc);

    // Show counts and percentages as text in the center
    svg.select(".countsText").remove();
    svg
      .append("text")
      .attr("class", "countsText")
      .attr("x", outerRadius)
      .attr("y", outerRadius)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .style("font-size", "10px")
      .text(`${live_perc}% live / ${offline_perc}% offline`);
  }, [props.data]);

  return (
    <div style={{ width: '200px', margin: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
    <svg ref={ref} width={outerRadius * 2} height={outerRadius * 2}>
    </svg>
    <div style={{ textAlign: 'center', marginTop: '10px' }}>
    {isNaN(props.data.live) || isNaN(props.data.offline)
      ? '-'
      : `${props.data.live} / ${props.data.offline + props.data.live}`}
    </div>
  </div>
  );
};

export default AnimatedPieHooks;
