import React, { useEffect, useState, useRef } from "react";
import { useMediaQuery } from "@mui/material";
import CardHeader from "../CardHeader/CardHeaderRes";
import Card from "../Card/CardRes";
import axios from "axios";
import Plot from "react-plotly.js";
import {
  useTheme,
  Typography,
  Tooltip,
  IconButton,
  Modal,
  Backdrop,
  Fade,
  Button,
} from "@mui/material";
import CleaningServicesTwoToneIcon from "@mui/icons-material/CleaningServicesTwoTone";

import "./smart.css";
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
import FootfallUsage from "./FootfallUsage";
import { useTheme as useCustomTheme } from "../ThemeContext";


import EstimatedResources from "./EstimatedResources";
import FootfallsPrediction from "./FootfallsPrediction";

const SmartWashroom = ({ defaultDate, setActiveDate }) => {
  const { themes } = useCustomTheme();
  const [activeGroupFilter, setActiveGroupFilter] = useState(defaultDate);
  const [plotData, setPlotData] = useState({});
  const [error, setError] = useState("");
  const [plotType, setPlotType] = useState("Day");
  const [isLoading, setIsLoading] = useState(false);
  const plotContainerRef = useRef(null);
  const isDropdown = useMediaQuery("(max-width: 576px)");

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

  const handleFilter = (filter) => {
    const newFilter = customData?.dateFiltersText?.[filter] ?? "";
    setActiveGroupFilter(newFilter);
    setActiveDate(newFilter);
  };

  const fetchPlotData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${ConfigData.API_URL}/api/forecast`);
      console.log("API Response:", response.data);

      // Ensure the data is in the correct format
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

  const EstimatedConsum = ({
    soFarWorkOrders,
    totalTodayWorkOrders,
    customLayout,
  }) => {
    return (
      <Grid
        item
        xs={6}
        sm={2.37}
        md={2.37}
        lg={2.37}
        style={{ display: "flex", marginLeft: "22px", marginRight: "-5px" }}
      >
        <Box
          sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            marginLeft: "-10px",
            marginRight: "-10px",
            fontFamily: "mulish",
            backgroundColor: themes === "dark" ? "#2E2E2E" : "#FFFEFE",
            padding: "15px",
            borderRadius: "8px",
            color: themes === "dark" ? "white" : "black",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)"
          }}
        >
<Typography
  className="est"
  component="div"
  gutterBottom
  style={{ fontSize: '17px',fontFamily:'mulish',marginTop:'-7px' }} // Adjust size as needed
>
  Estimated Work-Orders
</Typography>
          <div className="plot-box1 ">
            <Box sx={{ height: "16px" }} /> {/* This adds an empty line */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
              <CleaningServicesTwoToneIcon sx={{ color: "#FFA726", mr: 1 }} />
              <Box>
              <div className="plot-text ">
                {/* <Typography
                  variant="body1"
                  sx={{
                    height: "25px",
                    marginLeft: "-10px",
                    fontSize: "15px",
                    fontFamily: "mulish",
                  }}
                > */}
                  Work-Orders So Far{" "}
                {/* </Typography> */}</div>
                <Typography variant="h4" sx={{ color: "#FFA726", ml: 4 }}>
                  {soFarWorkOrders}
                </Typography>{" "}
                {/* Added left margin */}
                <Box sx={{ height: "20px" }} />{" "}
                {/* This creates an empty line with specified height */}
              </Box>
            </Box>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <CleaningServicesTwoToneIcon sx={{ color: "#FFA726", mr: 1 }} />
              <Box>
              <div className="plot-text ">


                  Total Predicted Work-orders
</div>
                <Typography variant="h4" sx={{ color: "#FFA726", ml: 4 }}>
                  {totalTodayWorkOrders}
                </Typography>
                <Box sx={{ height: "20px" }} />{" "}
                {/* This creates an empty line with specified height */}
              </Box>
            </Box>
          </div>
        </Box>
      </Grid>
    );
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
      <CardHeader
        headerText="Smart Washroom"
        handleFilter={handleFilter}
        activeGroupFilter={activeGroupFilter}
      >
        <PlotTypeSelector
          plotType={plotType}
          handlePlotTypeChange={handlePlotTypeChange}
          isDropdown={isDropdown}
        />
      </CardHeader>
      <Grid
        container
        spacing={{ xs: 2, sm: 2, md: 0, lg: 0 }}
        columns={{ xs: 4, sm: 8, md: 12, lg: 12 }}
        className="main-content-1"
        style={{ marginTop: "8px" }} // Add margin top to the entire first row
      >
        <Grid
          item
          xs={12}
          sm={12}
          md={12}
          lg={12}
          className="padding-15px display"
        >
          <Grid
            container
            spacing={0.5}
            style={{
              display: "flex",
              alignItems: "stretch",
              justifyContent:"space-between"
            }} // Added marginLeft to shift the row to the right
          >
            {/* Place Estimated Resources, Footfalls Prediction, Estimated Consum, and Footfall Usage in a single row at the top */}
            {Object.entries(currentData).map(([key, value], index) => {
              if (key === "Estimated_Resources") {
                return (
                  <Grid
                    item
                    xs={12}
                    sm={3}
                    md={3}
                    lg={3}
                    key={key}
                    style={{ display: "flex", marginLeft: "0", marginRight: "17px" }}
                  >
                    <EstimatedResources
                      data={value.data}
                      layout={value.layout}
                      customLayout={customLayout}
                      themes={themes}
                    />
                  </Grid>
                );
              }
              if (key === "Footfalls Prediction") {
                return (
                  <Grid
                    item
                    xs={12}
                    sm={3}
                    md={3}
                    lg={3}
                    key={key}
                    style={{ display: "flex", marginLeft: "10px", marginRight: "30px" }}
                  >
                    <FootfallsPrediction
                      data={value.data}
                      layout={value.layout}
                      customLayout={customLayout}
                      themes={themes}
                    />
                  </Grid>
                );
              }
              if (key === "so_far") {
                const soFarWorkOrders = value.so_far_work_orders || 0;
                const totalTodayWorkOrders = value.total_today_work_orders || 0;
                console.log("so_far_work_orders:", soFarWorkOrders);
                console.log("total_today_work_orders:", totalTodayWorkOrders);
                return (
                  <EstimatedConsum
                    key={key}
                    soFarWorkOrders={soFarWorkOrders}
                    totalTodayWorkOrders={totalTodayWorkOrders}
                    customLayout={customLayout}
                  />
                );
              }
              if (key === "Footfall_Usage") {
                return (
                  <FootfallUsage
                    key={key}
                    data={value.data}
                    layout={value.layout}
                    customLayout={customLayout}
                  />
                );
              }
              return null;
            })}
          </Grid>
        </Grid>

        <Grid item xs={12} sm={12} md={12} lg={12}>
          <div className="responsive-1">
            {/* Render the day_plot in the next row */}
            {Object.entries(currentData).map(([key, value]) => {
              if (key === "day_plot") {
                return (
                  <Box
                    className={`plot-container plot-box ${
                      themes === "light" ? "light-mode" : ""
                    }`}
                    key={key}
                    sx={{ height: "60vh" }}
                  >
                    <Plot
                      data={value.data || []}
                      layout={{
                        ...customLayout,
                        ...value.layout,
                        xaxis: {
                          ...value.layout.xaxis,
                          showgrid: false,
                          zeroline: false,
                        },
                        yaxis: {
                          ...value.layout.yaxis,
                          showgrid: false,
                          zeroline: false,
                        },
                        title: {
                          text: "Footfall Trends ",
                          font: {
                            family: "Mulish",
                            size: 17,
                            color: themes === "dark" ? "white" : "black",
                          },
                          y: 0.95,
                          x: 0.02,
                          align: "left",
                        },
                        annotations: value.layout?.annotations?.map(
                          (annotation) => ({
                            ...annotation,
                            font: {
                              ...annotation.font,
                              color: themes === "dark" ? "white" : "black",
                            },
                          })
                        ),
                        font: {
                          color: themes === "dark" ? "white" : "black",
                        },
                      }}
                      style={{
                        width: 1615,
                        height: 500,
                      }}
                      config={{
                        displaylogo: false,
                      }}
                      useResizeHandler
                    />
                  </Box>
                );
              }
              return null;
            })}
          </div>
        </Grid>
      </Grid>
    </Card>
  )}
</ThemeProvider>
  );
};

export default SmartWashroom;
