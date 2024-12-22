import React from "react";
import { Box, Grid } from "@mui/material";
import Plot from "react-plotly.js";
import { useTheme as useCustomTheme } from "../ThemeContext";

const FootfallUsage = ({ data, layout, customLayout }) => {
  const { themes } = useCustomTheme();
  return (
    <Grid
      item
      xs={6}
      sm={2.37}
      md={2.37}
      lg={2.37}
      style={{ display: "flex", marginLeft: "3px", marginRight: "42px" }}
    >
      <Box
        className={`plot-container plot-box ${
          themes === "light" ? "light-mode" : ""
        }`}
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
              text: "Estimated Waste",
              font: {
                family: "Mulish",
                size: 17,
                color: themes === "dark" ? "white" : "black",
              },
              y: 0.95,
              x: 0.03,
              align: "left",
            },
            yaxis: {
              visible: false,
              showticklabels: false, // Hide y-axis values
            },
            annotations: data.layout?.annotations?.map((annotation) => ({
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
    </Grid>
  );
};

export default FootfallUsage;
