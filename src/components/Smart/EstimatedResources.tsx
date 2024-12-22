import React from "react";
import Plot from "react-plotly.js";
import { Box } from "@mui/material";

const EstimatedResources = ({ data, layout, customLayout, themes }) => {
  return (
    <Box
      className={`plot-container plot-box ${themes === "light" ? "light-mode" : ""}`}
      sx={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        height: "300px",
      }}
    >
      <Plot
        data={data || []}
        layout={{
          ...customLayout,
          ...layout,
          title: {
            text: "Estimated Man-hours",
            font: {
              family: "Mulish",
              size: 17,
              color: themes === "dark" ? "white" : "black",
            },
            y: 0.95,
            x: 0.03,
            align: "left",
          },
          xaxis: {
            ...layout.xaxis,
            showgrid: false,
            zeroline: false,
          },
          yaxis: {
            ...layout.yaxis,
            showgrid: false,
            zeroline: false,
          },
          annotations: layout?.annotations?.map((annotation) => ({
            ...annotation,
            font: {
              ...annotation.font,
              color: themes === "dark" ? "white" : "black",
            },
          })),
          font: {
            color: themes === "dark" ? "white" : "black",
          },
        }}
        style={{
          width: "110%",
          height: "100%",
        }}
        config={{
          displayModeBar: false,
          displaylogo: false,
        }}
        useResizeHandler
      />
    </Box>
  );
};

export default EstimatedResources;
