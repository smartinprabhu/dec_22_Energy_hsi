import React, { useEffect, useState, useRef } from "react";
import { useMediaQuery } from "@mui/material";
import CardHeader from "../CardHeader/CardHeaderRes";
import Card from "../Card/CardRes";
import axios from "axios";
import Plot from "react-plotly.js";
import PlotTypeSelector from "../EnergyAnalytics/PlottypeSelector";
import {
  Grid,
  Box,
  CircularProgress,
  createTheme,
  ThemeProvider,
} from "@mui/material";
import "../EnergyAnalytics/EnergyAnalytics.css";
import ConfigData from "../../auth/config";
import { useTheme } from "../ThemeContext";

const EnergyAnalytics = ({ defaultDate }) => {
  const [activeGroupFilter, setActiveGroupFilter] = useState(defaultDate);
  const [plotData, setPlotData] = useState({});
  const [error, setError] = useState("");
  const [plotType, setPlotType] = useState("Day");
  const [isLoading, setIsLoading] = useState(false);
  const plotContainerRef = useRef(null);
  const isDropdown = useMediaQuery("(max-width: 576px)");
  const isDropdown932 = useMediaQuery(
    "(max-width: 932px) and (max-height: 430px)"
  );
  const isDropdown820 = useMediaQuery(
    "(max-width: 820px) and (max-height: 1180px)"
  );
  const { themes } = useTheme();

  const [plotDimensions, setPlotDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight * 0.7, // Adjusted to 70% of the viewport height
  });

  useEffect(() => {
    setActiveGroupFilter(defaultDate);
    fetchPlotData();
    handleResize(); // Initial resize
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [defaultDate]);

  const handleResize = () => {
    setPlotDimensions({
      width: window.innerWidth,
      height: window.innerHeight * 0.7, // Adjusted to 70% of the viewport height
    });
  };

  const handlePlotTypeChange = (event) => {
    setPlotType(event.target.value);
  };

  const fetchPlotData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(
        `${ConfigData.API_URL}/python_api/forecast`
      );
      console.log("API Response:", response.data);

      const dataObject = response.data.reduce((acc, [key, value]) => {
        acc[key] = value;
        return acc;
      }, {});

      setPlotData(dataObject);
      setError("");
    } catch (error) {
      console.error("Error:", error);
      setError(
        error.message || "An error occurred while fetching the plot data."
      );
      setPlotData({});
    } finally {
      setIsLoading(false);
    }
  };

  const getColorForRateOfChange = (rate) => {
    if (rate.includes("▲")) {
      return "red";
    } else if (rate.includes("▼")) {
      return "green";
    }
    return "inherit"; // Default color
  };

  const splitRateOfChangeText = (text) => {
    const match = text.match(/([\d.]+)\s?(%?\s?[▼▲]*)/);
    const number = match ? match[1] : text;
    const symbol = match ? match[2] : "";

    const formattedSymbol = symbol.includes("%")
      ? symbol
      : `% ${symbol}`.trim();

    return {
      number: number,
      symbol: formattedSymbol,
    };
  };

  const theme = createTheme({
    components: {
      MuiRadio: {
        styleOverrides: {
          root: {
            color: "#ffffff",
          },
        },
      },
    },
  });

  const currentData = plotData[plotType] || {};

  const customLayout = {
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: {
      color: "#FFFFFF",
    },
    xaxis: {
      showgrid: false,
      zeroline: false,
      showline: false,
    },
    yaxis: {
      showgrid: false,
      zeroline: false,
      showline: false,
    },
    showlegend: true,
  };

  return (
    <ThemeProvider theme={theme}>
      {isLoading ? (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
          }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <Card>
          <CardHeader headerText="Energy Analytics">
            <PlotTypeSelector
              plotType={plotType}
              handlePlotTypeChange={handlePlotTypeChange}
              isDropdown={isDropdown || isDropdown932 || isDropdown820}
            />
          </CardHeader>
          <Grid
            container
            spacing={{ xs: 2, sm: 2, md: 0, lg: 0 }}
            columns={{ xs: 4, sm: 8, md: 12, lg: 12 }}
            className={`main-content-1 ${
              themes === "light" ? "light-mode" : ""
            }`} // Conditionally apply 'dark-mode' class
          >
            <Grid
              item
              xs={12}
              sm={12}
              md={8}
              lg={8}
              className="padding-15px display"
            >
              <Grid item xs={12} sm={12} md={12} lg={12}>
                <div className="responsive-1">
                  {Object.entries(currentData).map(
                    ([key, value]) =>
                      key !== `${plotType.toLowerCase()}_plot` && (
                        <div
                          key={key}
                          className={`box-1 ${
                            themes === "light" ? "light-mode" : ""
                          }`}
                        >
                          <p
                            className={`chart-title-responsive font ${
                              themes === "light" ? "light-mode" : "dark-mode"
                            }`}
                          >
                            {" "}
                            {key.replace(/_/g, " ")}
                          </p>
                          {typeof value === "string" &&
                          (key.includes("Change_in_Consumption") ||
                            key.includes("Change_in_consumption")) ? (
                            <span className="e-span-responsive-alarms size">
                              {splitRateOfChangeText(value).number}
                              <span>{" % "}</span>
                              <span
                                style={{
                                  color: getColorForRateOfChange(value),
                                }}
                              >
                                {splitRateOfChangeText(value)
                                  .symbol.trim()
                                  .replace("%", "")}
                              </span>
                            </span>
                          ) : (
                            <span className="e-span-responsive-alarms size">
                              {typeof value === "number"
                                ? value.toFixed(2)
                                : String(value)}
                            </span>
                          )}
                        </div>
                      )
                  )}
                </div>
              </Grid>
            </Grid>
          </Grid>
          {currentData[`${plotType.toLowerCase()}_plot`] && (
            <Box
              sx={{ overflowX: "hidden", overflowY: "hidden" }}
              className="plot1"
            >
              <Box
                ref={plotContainerRef}
                className={`plot-container1 ${
                  themes === "light" ? "light-mode" : ""
                }`}
              >
                <div className="plot-box">
                  <Plot
                    data={
                      Array.isArray(
                        currentData[`${plotType.toLowerCase()}_plot`]?.data
                      )
                        ? currentData[`${plotType.toLowerCase()}_plot`]?.data
                        : []
                    }
                    layout={{
                       title: {
                          text: "Energy Consumption Trend With Forecaste ",
                          font: {
                            family: "Mulish",
                            size: 17,
                            color: themes === "dark" ? "white" : "black",
                          },
                          y: 0.95,
                          x: 0.02,
                          align: "left",
                        },
                      ...customLayout,
                      ...currentData[`${plotType.toLowerCase()}_plot`]?.layout,
                      annotations: currentData[
                        `${plotType.toLowerCase()}_plot`
                      ]?.layout?.annotations?.map((annotation) => ({
                        ...annotation,
                        font: {
                          ...annotation.font,
                          color: themes === "dark" ? "white" : "black",
                        },
                      })),
                      xaxis: {
                        ...currentData[`${plotType.toLowerCase()}_plot`]?.layout
                          ?.xaxis,
                        title: {
                          ...currentData[`${plotType.toLowerCase()}_plot`]
                            ?.layout?.xaxis?.title,
                          font: {
                            family: "Mulish",
                            size: 14,
                            color: themes === "dark" ? "white" : "black", // Set x-axis title color to black
                          },
                        },
                        tickfont: {
                          family: "Mulish",
                          size: 10,
                          color: themes === "dark" ? "white" : "black", // Set x-axis tick label color to black
                        },
                        showgrid: false, // Hide x-axis grid lines
                      },
                      yaxis: {
                        ...currentData[`${plotType.toLowerCase()}_plot`]?.layout
                          ?.yaxis,
                        title: {
                          ...currentData[`${plotType.toLowerCase()}_plot`]
                            ?.layout?.yaxis?.title,
                          font: {
                            family: "Mulish",
                            size: 14,
                            color: themes === "dark" ? "white" : "black", // Set y-axis title color to black
                          },
                          showticklabels: false,
                          visible: false,
                        },
                        tickfont: {
                          family: "Mulish",
                          size: 10,
                          color: themes === "dark" ? "white" : "black", // Set y-axis tick label color to black
                        },
                        showgrid: false, // Hide x-axis grid lines
                      },
                      font: {
                        color: themes === "dark" ? "white" : "black",
                      },
                    }}
                    style={{
                      width: plotDimensions.width,
                      height: plotDimensions.height,
                    }}
                    config={{
                      displaylogo: false, // Hide the 'Powered by Plotly' logo
                    }}
                    useResizeHandler
                  />
                </div>
              </Box>
            </Box>
          )}
        </Card>
      )}
    </ThemeProvider>
  );
};

export default EnergyAnalytics;
