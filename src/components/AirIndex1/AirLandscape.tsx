import React, { useState, useLayoutEffect, useEffect } from "react";
import Plot from "react-plotly.js";
import styled from "styled-components";
import "./AirRen.css";
import Skeleton from "@mui/material/Skeleton";
import { useMediaQuery } from "@mui/material";
import axios from "axios";
import ConfigData from "../../auth/config";
import SyncTwoToneIcon from "@mui/icons-material/SyncTwoTone";
import LoadingSkeleton from "./LoadingSkeleton"; // Import the loading skeleton component
import { useTheme as useCustomTheme } from "../ThemeContext";

// Main grid container
const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr; /* Two equal columns */
  gap: 20px;
  height: 90vh; /* Full height */
  width: 100vw; /* Full width */
  padding: 20px;
  background-color: black;
  color: white;
  overflow: auto; /* Prevent scrolling */

  @media (max-width: 768px) {
    grid-template-columns: 1fr; /* Single column on small screens in portrait mode */
    grid-template-rows: auto auto 1fr; /* Stack vertically in portrait */
  }

  @media (orientation: landscape) {
    grid-template-columns: 1fr 1fr; /* Two columns in landscape */
  }
`;

// Top section for building image and air quality index
const TopSection = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #282828;
  padding: 20px;
  font-size: 20px;
  border-radius: 10px;
  height: 100%; /* Ensures equal height with the air quality container */

  @media (max-width: 768px) {
    height: auto; /* Flexible height in portrait mode */
  }
`;

const AirQualityContainer = styled(TopSection)`
  text-align: center;
  height: 100%;

  @media (max-width: 768px) {
    grid-column: 1; /* Full width in portrait mode */
  }

  @media (orientation: landscape) {
    grid-column: 1; /* Left side in landscape mode */
  }
`;

// Middle section for Indoor/Outdoor, DotsMenu, and rendered metrics
const MetricsContainer = styled.div`
  grid-column: 2; /* Right column in landscape mode */
  display: flex;
  flex-direction: column; /* Stack indoor/outdoor and metrics vertically */
  background-color: #black;
  border-radius: 10px;
  gap: 10px;

  @media (max-width: 768px) {
    grid-column: 1; /* Full width in portrait mode */
    flex-direction: column; /* Stack vertically in portrait */
  }

  @media (orientation: landscape) {
    grid-column: 2; /* Right side in landscape mode */
  }
`;

// Card for individual metrics (Temperature, Humidity, etc.)
// Indoor and Outdoor Section
const IndoorOutdoorContainer = styled.div`
  display: flex;
  justify-content: space-between;

  @media (orientation: landscape) {
    flex-direction: row; /* Horizontal layout in landscape */
    font-size: 20px;
  }

  @media (max-width: 768px) {
    flex-direction: column; /* Stack vertically in portrait */
  }
`;

// Card for individual metrics (Temperature, Humidity, etc.)
const MetricCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  border-radius: 10px;
  padding: 20px;
  margin: 5px;

  .icon {
    font-size: 10px;
    margin-bottom: 10px;
  }

  .metric {
    font-size: 10px;
    margin-bottom: 5px;
  }

  .status {
    font-size: 14px;
    color: #aaa;
  }
  @media (max-width: 1366px) {
    padding: 0px;
  }
`;

// DotsMenu for switching views
const DotsMenu = styled.div`
  display: flex;
  justify-content: center;
  margin: 10px 0;

  .dot {
    height: 12px;
    width: 12px;
    background-color: white;
    border-radius: 50%;
    display: inline-block;
    margin: 0 5px;
    cursor: pointer;

    &.active {
      background-color: green;
    }
  }
`;

// Indoor and Outdoor sections take equal width

const Air = () => {
  const { themes } = useCustomTheme();
  const [currentView, setCurrentView] = useState("TEMP_METRICS");
  const samlltv = useMediaQuery("(max-width: 1366px)");
  const [plotWidth, setPlotWidth] = useState(window.innerWidth);
  const [airQualityData, setAirQualityData] = useState({
    indoor: null,
    outdoor: null,
    city: null,
  });
  const [lastUpdated, setLastUpdated] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleResize = () => setPlotWidth(window.innerWidth);

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useLayoutEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `${ConfigData.API_URL}/air/air-quality`
        );
        const data = response.data;
        console.log(data); // Log the data to verify the structure
        setAirQualityData({
          indoor: data[0][1],
          outdoor: data[1][1],
          city: data[0][1].city,
        });
        setLastUpdated(new Date());
      } catch (error) {
        console.error("Error fetching air quality data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 300000); // 5 minutes

    // Switch tabs every 10 seconds
    const tabInterval = setInterval(() => {
      setCurrentView((prevView) => {
        switch (prevView) {
          case "TEMP_METRICS":
            return "HUMIDITY_METRICS";
          case "HUMIDITY_METRICS":
            return "PSYCHROMETRIC_CHART";
          case "PSYCHROMETRIC_CHART":
            return "TEMP_METRICS";
          default:
            return "TEMP_METRICS";
        }
      });
    }, 10000); // 5000 milliseconds = 5 seconds

    // Force re-render after initial load
    window.dispatchEvent(new Event("resize"));

    return () => {
      clearInterval(interval);
      clearInterval(tabInterval);
    };
  }, []);

  // Helper functions to get colors and labels based on values
  const getTemperatureColor = (value) => {
    if (value >= 0 && value <= 19) return "#339933";
    if (value >= 19.01 && value <= 22) return "#ffe510";
    if (value >= 22.01 && value <= 27) return "#ffc000";
    if (value >= 27.01 && value <= 50) return "#ff0000";
    return "black";
  };

  const getHumidityColor = (value) => {
    if (value >= 30 && value <= 60) return "#339933";
    if (value >= 0 && value <= 30) return "#ffe510";
    if (value >= 60.01 && value <= 100) return "#ff0000";
    return "black";
  };

  const getPM1Color = (value) => {
    if (value >= 0 && value <= 54) return "#339933";
    if (value >= 55 && value <= 154) return "#ffe510";
    if (value >= 155 && value <= 254) return "#ffc000";
    if (value >= 255 && value <= 354) return "#ff0000";
    if (value >= 355 && value <= 424) return "#9900ff";
    if (value >= 425 && value <= 604) return "#cc0000";
    return "black";
  };

  const getPM25Color = (value) => {
    if (value >= 0 && value <= 12.09) return "#339933";
    if (value >= 12.1 && value <= 35.49) return "#ffe510";
    if (value >= 35.5 && value <= 55.49) return "#ffc000";
    if (value >= 55.5 && value <= 150.49) return "#ff0000";
    if (value >= 150.5 && value <= 250.9) return "#9900ff";
    if (value >= 250.5 && value <= 500.4) return "#cc0000";
    return "black";
  };

  const getCarbonMonoxideColor = (value) => {
    if (value >= 0 && value <= 5) return "#339933";
    if (value >= 5.01 && value <= 15) return "#ffe510";
    if (value >= 15.01 && value <= 35) return "#ff0000";
    return "black";
  };

  const getOzoneColor = (value) => {
    if (value >= 0 && value <= 50) return "#339933";
    if (value >= 51 && value <= 100) return "#ffe510";
    if (value >= 101 && value <= 150) return "#ffc000";
    if (value >= 151 && value <= 200) return "#ff0000";
    if (value >= 201 && value <= 300) return "#9900ff";
    if (value >= 301 && value <= 450) return "#cc0000";
    return "black";
  };

  const getPressureColor = (value) => {
    if (value >= 0 && value <= 1000) return "#339933";
    if (value >= 1001 && value <= 2000) return "#ffe510";
    if (value >= 2001 && value <= 3000) return "#ffc000";
    if (value >= 3001 && value <= 4000) return "#ff0000";
    if (value >= 4001 && value <= 5000) return "#9900ff";
    return "black";
  };

  const getTemperatureLabel = (value) => {
    if (value >= 0 && value <= 19) return "Cool";
    if (value >= 19.01 && value <= 22) return "Normal";
    if (value >= 22.01 && value <= 27) return "Warm";
    if (value >= 27.01 && value <= 50) return "Hot";
    return "";
  };

  const getHumidityLabel = (value) => {
    if (value >= 30 && value <= 60) return "Good";
    if (value >= 0 && value <= 30) return "Dry";
    if (value >= 60.01 && value <= 100) return "Humid";
    return "";
  };

  const getCarbonMonoxideLabel = (value) => {
    if (value >= 0 && value <= 5) return "Good";
    if (value >= 5.01 && value <= 15) return "Moderate";
    if (value >= 15.01 && value <= 35) return "Unhealthy";
    return "";
  };

  const getOzoneLabel = (value) => {
    if (value >= 0 && value <= 50) return "Good";
    if (value >= 51 && value <= 100) return "Moderate";
    if (value >= 101 && value <= 150) return "Unhealthy(sensitive)";
    if (value >= 151 && value <= 200) return "Unhealthy";
    if (value >= 201 && value <= 300) return "Very Unhealthy";
    if (value >= 301) return "Hazardous";
    return "";
  };

  const getPM1Label = (value) => {
    if (value >= 0 && value <= 54) return "Good";
    if (value >= 55 && value <= 154) return "Moderate";
    if (value >= 155 && value <= 254) return "Unhealthy(sensitive)";
    if (value >= 255 && value <= 354) return "Unhealthy";
    if (value >= 355 && value <= 424) return "Very Unhealthy";
    if (value >= 425 && value <= 604) return "Hazardous";
    return "";
  };

  const getPM25Label = (value) => {
    if (value >= 0 && value <= 12.09) return "Good";
    if (value >= 12.1 && value <= 35.49) return "Moderate";
    if (value >= 35.5 && value <= 55.49) return "Unhealthy(sensitive)";
    if (value >= 55.5 && value <= 150.49) return "Unhealthy";
    if (value >= 150.5 && value <= 250.49) return "Very Unhealthy";
    if (value >= 250.5 && value <= 500.4) return "Hazardous";
    return "";
  };

  const getPressureLabel = (value) => {
    if (value >= 0 && value <= 1000) return "Good";
    if (value >= 1001 && value <= 2000) return "Moderate";
    if (value >= 2001 && value <= 3000) return "Unhealthy(sensitive)";
    if (value >= 3001 && value <= 4000) return "Unhealthy";
    if (value >= 4001 && value <= 5000) return "Very Unhealthy";
    return "";
  };
  const imageSrc =
  themes === "dark"
    ? "../air_quality/psychrometric_chart.png"
    : "../air_quality/psychrometric_chart1.png"; 

  // BarChart component for displaying the bar chart
  const BarChart = ({ value, maxValue, metricType }) => {
    let color, description;

    // Determine the color and description based on the metric type and value
    switch (metricType) {
      case "temperature":
        color = getTemperatureColor(value);
        description = getTemperatureLabel(value);
        break;
      case "humidity":
        color = getHumidityColor(value);
        description = getHumidityLabel(value);
        break;
      case "pm1":
        color = getPM1Color(value);
        description = getPM1Label(value);
        break;
      case "pm25":
        color = getPM25Color(value);
        description = getPM25Label(value);
        break;
      case "co":
        color = getCarbonMonoxideColor(value);
        description = getCarbonMonoxideLabel(value);
        break;
      case "o3":
        color = getOzoneColor(value);
        description = getOzoneLabel(value);
        break;
      case "pressure":
        color = getPressureColor(value);
        description = getPressureLabel(value);
        break;
      case "aqi":
        if (value <= 50) {
          description = "Good";
          color = "#339933";
        } else if (value <= 100) {
          description = "Moderate";
          color = "#ffe510";
        } else if (value <= 150) {
          description = "Unhealthy(sensitive)";
          color = "#ffc000";
        } else if (value <= 200) {
          description = "Unhealthy";
          color = "#ff0000";
        } else if (value <= 300) {
          description = "Very Unhealthy";
          color = "#9900ff";
        } else {
          description = "Hazardous";
          color = "#673301";
        }
        break;
      default:
        color = "black";
        description = "";
    }

    const label = `${value} / ${maxValue}`;

    return (
      <Plot
      className={`plot-container ${
        themes === "light" ? "light-mode1" : ""
      }`}
        data={[
          {
            x: [value],
            y: ["Metric"],
            type: "bar",
            orientation: "h",
            marker: { color },
            hoverinfo: "none", // No hover info for the filled part
          },
          {
            x: [maxValue - value],
            y: ["Metric"],
            type: "bar",
            orientation: "h",
            marker: {                                      color:
              themes === "dark" ? "#2E2E2E" : "#ECEAEA",
},
            hoverinfo: "none", // No hover info for the remaining part
          },
        ]}
        layout={{
          width: plotWidth * 0.2,
          height: 30,
          barmode: "stack",
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
          margin: { t: 10, b: 10, l: 0, r: 20 },
          xaxis: { range: [0, maxValue], visible: false },
          yaxis: { visible: false },
          showlegend: false, // Disable legend
          annotations: [
            {
              x: maxValue, // Position at the end of the bar
              y: "Metric",
              text: description, // The text to display
              xanchor: "right", // Anchor the text to the left
              showarrow: false, // No arrow
              font: {
                size: 14,
                color: color, // Text color
              },
            },
          ],
        }}
        config={{ displayModeBar: false, displaylogo: false }}
      />
    );
  };

  const renderMetrics = () => {
    switch (currentView) {
      case "TEMP_METRICS":
        return (
          <>
            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.temperature || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    °C
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.temperature || 0}
                  maxValue={40}
                  metricType="temperature"
                />
              </MetricCard>
              <MetricCard>
                <div className={`temp-value4 ${
                      themes === "light" ? "light-temp2" : ""
                    }`}>
                  <h3>Temperature</h3>
                </div>
                <img src="../images/temperature.svg" className="tempimg" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.temperature || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    °C
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.temperature || 0}
                  maxValue={40}
                  metricType="temperature"
                />
              </MetricCard>
            </MetricsContainer>
            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.humidity || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    %
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.humidity || 0}
                  maxValue={100}
                  metricType="humidity"
                />
              </MetricCard>
              <MetricCard>
                <div className={`temp-value4 ${
                      themes === "light" ? "light-temp2" : ""
                    }`}>
                  <h3>Humidity</h3>
                </div>
                <img src="../images/humidity.svg" className="tempimg" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.humidity || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    %
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.humidity || 0}
                  maxValue={110}
                  metricType="humidity"
                />
              </MetricCard>
            </MetricsContainer>

            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.pressure || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    kPa
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.pressure || 0}
                  maxValue={5000}
                  metricType="pressure"
                />
              </MetricCard>
              <MetricCard>
                <div className={`temp-value4 ${
                      themes === "light" ? "light-temp2" : ""
                    }`}>
                  <h3>Pressure</h3>
                </div>
                <img src="../images/pressure.svg" className="tempimg" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.pressure || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    kPa
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.pressure || 0}
                  maxValue={5000}
                  metricType="pressure"
                />
              </MetricCard>
            </MetricsContainer>

            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.aqi || "N/A"
                    )}
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.aqi || 0}
                  maxValue={500}
                  metricType="aqi"
                />
              </MetricCard>

              <MetricCard>
                <div className={`temp-value4 ${
                      themes === "light" ? "light-temp2" : ""
                    }`}>
                  <h3>AQI</h3>
                </div>
                <img
                  src="../images/Indoor Air quality.svg"
                  className="tempimg"
                />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.aqi || "N/A"
                    )}
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.aqi || 0}
                  maxValue={500}
                  metricType="aqi"
                />
              </MetricCard>
            </MetricsContainer>
          </>
        );
      case "HUMIDITY_METRICS":
        return (
          <>
            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.pm1 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    µg/m³
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.pm1 || 0}
                  maxValue={604}
                  metricType="pm1"
                />
              </MetricCard>

              <MetricCard>
                <div                     className={`temp-value5 ${
                      themes === "light" ? "light-temp" : ""
                    }`}
>
                  <h3>PM 1 </h3>
                </div>
                <img src="../images/PM.svg" className="tempimg2" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.pm1 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    µg/m³
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.pm1 || 0}
                  maxValue={604}
                  metricType="pm1"
                />
              </MetricCard>
            </MetricsContainer>

            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.pm25 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    µg/m³
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.pm25 || 0}
                  maxValue={500.4}
                  metricType="pm25"
                />
              </MetricCard>

              <MetricCard>
                <div className={`temp-value5 ${
                      themes === "light" ? "light-temp" : ""
                    }`}>
                  <h3>PM 2.5 </h3>
                </div>
                <img src="../images/PM.svg" className="tempimg2" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.pm25 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    µg/m³
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.pm25 || 0}
                  maxValue={500.4}
                  metricType="pm25"
                />
              </MetricCard>
            </MetricsContainer>

            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.co || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    ppb
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.co || 0}
                  maxValue={35}
                  metricType="co"
                />
              </MetricCard>
              <MetricCard>
                <div className={`temp-value6 ${
                      themes === "light" ? "light-temp1" : ""
                    }`}>
                  <h3>Carbon monoxide</h3>
                </div>
                <img src="../images/co.svg" className="tempimg" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.co || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    ppb
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.co || 0}
                  maxValue={35}
                  metricType="co"
                />
              </MetricCard>
            </MetricsContainer>
            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.indoor?.o3 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    ppb
                  </span>
                </div>
                <BarChart
                  value={airQualityData.indoor?.o3 || 0}
                  maxValue={500}
                  metricType="o3"
                />
              </MetricCard>
              <MetricCard>
                <div className={`temp-value5 ${
                      themes === "light" ? "light-temp" : ""
                    }`}>
                  <h3>Ozone</h3>
                </div>
                <img src="../images/ozone.svg" className="tempimg" />
              </MetricCard>
              <MetricCard>
                <div className="metric">
                  <span
                    className={`pm-value ${
                      themes === "light" ? "light-pm" : ""
                    }`}
                  >
                    {loading ? (
                      <Skeleton variant="text" width={50} />
                    ) : (
                      airQualityData.outdoor?.o3 || "N/A"
                    )}
                  </span>
                  <span
                    className={`pm-unit ${
                      themes === "light" ? "light-un" : ""
                    }`}
                  >
                    {" "}
                    ppb
                  </span>
                </div>
                <BarChart
                  value={airQualityData.outdoor?.o3 || 0}
                  maxValue={500}
                  metricType="o3"
                />
              </MetricCard>
            </MetricsContainer>
          </>
        );
      case "PSYCHROMETRIC_CHART":
        const { zone, action } = airQualityData.outdoor;
        return (
          <>
            <MetricsContainer
              className={`mat ${themes === "light" ? "light-mat" : ""}`}
            >
              <MetricCard>
                <div className="metric">
                  {/* Add any additional metrics here if needed */}
                </div>
                <div
                  className="chart-container"
                  style={{ position: "relative" }}
                >
                  <img
                    src={imageSrc}
                    alt="Psychrometric Chart"
                    className="chart"
                  />
                  <div
                    className="overlay-text"
                    style={{
                      position: "absolute",
                      top: "20px", // Adjust as needed
                      left: "20px", // Adjust as needed
                      color: themes === "dark" ? "#949495" : "#000", // Change color as needed
                      backgroundColor: themes === "dark" ? "#282828" : "#FFF", // Background color based on theme
                      padding: "5px", // Optional: padding
                    }}
                  >
                    Psychrometric Chart
                  </div>
                  <div className="description_p">
                    <h5
                      style={{ color: themes === "dark" ? "white" : "black" }}
                    >
                      ZONE : {zone}
                    </h5>
                    <div className="description_p1">
                      <p
                        style={{
                          color: zone === "COMFORT ZONE" ? "green" : "red",
                        }}
                      >
                        {action}
                      </p>
                    </div>
                  </div>
                </div>
              </MetricCard>
            </MetricsContainer>
          </>
        );

      default:
        return null;
    }
  };

  const createGaugePlot = (aqi, label) => {
    let description, textBgColor, bgColor, textColor;

    // Determine the description, colors, and text color based on AQI value
    if (aqi <= 50) {
      description = "Good";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000"; 
    } else if (aqi <= 100) {
      description = "Moderate";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000"; 
    } else if (aqi <= 150) {
      description = "Unhealthy(sensitive)";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000";  // White for Unhealthy(sensitive)
    } else if (aqi <= 200) {
      description = "Unhealthy";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000"; 
    } else if (aqi <= 300) {
      description = "Very Unhealthy";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000"; 
    } else {
      description = "Hazardous";
      bgColor = "#282828";
      textBgColor = themes === "dark" ? "#282828" : "#FFF"; // Dark 
      textColor = themes === "dark" ? "#fff" : "#000"; 
    }

    return (
      <div className="custom-gauge-wrapper">
        <Plot
          data={[
            {
              type: "indicator",
              mode: "gauge+number",
              value: aqi,
              gauge: {
                axis: {
                  range: [0, 500],
                  tickvals: [
                    0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
                  ],
                  ticktext: [
                    "0",
                    "50",
                    "100",
                    "150",
                    "200",
                    "250",
                    "300",
                    "350",
                    "400",
                    "450",
                    "500",
                  ],
                  tickwidth: 1,
                  tickcolor: themes === "dark" ? "white" : "black", // Dynamic tick color
                  tickfont: {
                    color: themes === "dark" ? "white" : "black", // Dynamic tick font color
                  },
                },
                bar: { color: aqi <= 100 ? "white" : "white" },
                steps: [
                  { range: [0, 50], color: "#339933" },
                  { range: [51, 100], color: "#ffe510" },
                  { range: [101, 150], color: "#ffc000" },
                  { range: [151, 200], color: "#ff0000" },
                  { range: [201, 300], color: "#9900ff" },
                  { range: [301, 500], color: "#673301" },
                ],
              },
              number: {
                font: {
                  size: 60,
                  color: themes === "dark" ? "white" : "black",
                }, // Dynamic number font color
              },
            },
          ]}
          layout={{
            title: {
              text: label,
              font: {
                size: 18,
                color: themes === "dark" ? "white" : "black", // Dynamic title font color
                family: "Mulish",
              },
            },
            width: plotWidth * 0.2,
            height: samlltv ? 150 : 220,
            margin: { t: 30, r: 30, l: 20, b: 10 },
            paper_bgcolor: themes === "dark" ? "#282828" : "#FFFFFF",
            plot_bgcolor: themes === "dark" ? "#282828" : "#FFFFFF", // Adjust plot background for light mode
            font: {
              color: themes === "dark" ? "white" : "black", // Default font color for layout
              family: "Mulish",
            },
          }}
          config={{ displayModeBar: false }}
        />
        <div
          className="aqi-description" // Add your desired class name here
          style={{
            backgroundColor: textBgColor, // Background color dynamically set based on AQI level
            color: textColor, // Text color dynamically set based on AQI level
          }}
        >
          {description}
        </div>

        <div className="custom-legend">
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#339933" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Good</div>
          </div>
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#ffe510" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Moderate</div>
          </div>
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#ffc000" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Unhealthy(sensitive)</div>
          </div>
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#ff0000" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Unhealthy</div>
          </div>
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#9900ff" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Very Unhealthy</div>
          </div>
          <div className="legend-item">
            <div
              className="legend-circle"
              style={{ backgroundColor: "#673301" }}
            ></div>
            <div className="legend-label" style={{ color: themes === "dark" ? "white" : "black" }}>Hazardous</div>
          </div>
        </div>
      </div>
    );
  };

  const formatTimeAgo = (date) => {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const remainingSeconds = diffInSeconds % 60;

    if (diffInMinutes === 0) {
      return `${remainingSeconds} sec ago`;
    } else {
      return `${diffInMinutes} min ago`;
    }
  };

  return (
    <>
      {loading && <LoadingSkeleton />}
      <Container className={`vk ${themes === "light" ? "light-back" : ""}`}>
        <div className="mat1 ">
          <TopSection
            className={`gsAVwi ${themes === "light" ? "light-top" : ""}`}
          >
            <div className="iaq">
              <img src="../images/building.svg" />
              <h4>6th Floor, MCloud, Hyderabad</h4>
            </div>
            <img src="../images/dallas-center-v7.png " className="buld" />
          </TopSection>
          <AirQualityContainer
            className={`gsAVwi ${themes === "light" ? "light-top" : ""}`}
          >
            <div className="mat2 ">
              <h3 className="h4">Air Quality Index (AQI)</h3>
              {loading ? (
                <Skeleton variant="rectangular" width="100%" height={220} />
              ) : (
                createGaugePlot(airQualityData.indoor?.aqi || 0, "")
              )}
            </div>
          </AirQualityContainer>
        </div>

        {/* Right Side in Landscape Mode */}
        <MetricsContainer>
          <IndoorOutdoorContainer>
            <MetricCard>
              <div className="title1">
                {currentView !== "PSYCHROMETRIC_CHART" && <b>INDOOR</b>}
              </div>
            </MetricCard>
            <DotsMenu>
              <div
                className={`dot ${
                  currentView === "TEMP_METRICS" ? "active" : ""
                }`}
                onClick={() => setCurrentView("TEMP_METRICS")}
              />
              <div
                className={`dot ${
                  currentView === "HUMIDITY_METRICS" ? "active" : ""
                }`}
                onClick={() => setCurrentView("HUMIDITY_METRICS")}
              />
              <div
                className={`dot ${
                  currentView === "PSYCHROMETRIC_CHART" ? "active" : ""
                }`}
                onClick={() => setCurrentView("PSYCHROMETRIC_CHART")}
              >
                <div className="sync1">
                  <div className="imagesyn" style={{ color: "#949495" }}>
                    <SyncTwoToneIcon className="imagesyn" />
                  </div>
                  <span style={{ color: "#949495" }}>
                    {loading
                      ? "Loading..."
                      : lastUpdated
                      ? `Last Updated: ${formatTimeAgo(lastUpdated)}`
                      : "Loading..."}
                  </span>
                </div>
              </div>
            </DotsMenu>
            <MetricCard>
              <div className="title2">
                {currentView !== "PSYCHROMETRIC_CHART" && <b>OUTDOOR</b>}
              </div>
            </MetricCard>
          </IndoorOutdoorContainer>

          {/* Render Metrics Based on Current View */}
          {renderMetrics()}
        </MetricsContainer>
      </Container>
    </>
  );
};

export default Air;
