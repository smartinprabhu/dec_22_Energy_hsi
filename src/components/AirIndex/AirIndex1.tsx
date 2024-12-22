import React, { useEffect, useState } from "react";
import { Grid } from "@mui/material";
import Plot from "react-plotly.js";
import axios from "axios"; // Make sure to import axios
import "./Air1.css";
import ConfigData from "../../auth/config";

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

// Bar Chart Components
const TemperatureBarChart = ({ value, maxValue }) => {
  const color = getTemperatureColor(value);
  const label = getTemperatureLabel(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Temperature"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Temperature"],
        },
        {
          x: [maxValue - value],
          y: ["Temperature"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Temperature",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
            x:46,
            yanchor: "middle",

          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

const HumidityBarChart = ({ value, maxValue }) => {
  const color = getHumidityColor(value);
  const label = getHumidityLabel(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Humidity"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Humidity"],
        },
        {
          x: [maxValue - value],
          y: ["Humidity"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Humidity",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
            x:92,
            yanchor: "middle",
          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

const PM1BarChart = ({ value, maxValue }) => {
  const color = getPM1Color(value);
  const label = getPM1Label(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Particulate Matter 1 (PM1)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Particulate Matter 1 (PM1)"],
        },
        {
          x: [maxValue - value],
          y: ["Particulate Matter 1 (PM1)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Particulate Matter 1 (PM1)",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
            x:520,
            yanchor: "middle",
          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

const PM25BarChart = ({ value, maxValue }) => {
  const color = getPM25Color(value);
  const label = getPM25Label(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Particulate Matter 2.5 (PM2.5)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Particulate Matter 2.5 (PM2.5)"],
        },
        {
          x: [maxValue - value],
          y: ["Particulate Matter 2.5 (PM2.5)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Particulate Matter 2.5 (PM2.5)",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
            x:420,
            yanchor: "middle",
          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

const COBarChart = ({ value, maxValue }) => {
  const color = getCarbonMonoxideColor(value);
  const label = getCarbonMonoxideLabel(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Carbon Monoxide (CO)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Carbon Monoxide (CO)"],
        },
        {
          x: [maxValue - value],
          y: ["Carbon Monoxide (CO)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Carbon Monoxide (CO)",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
              x:30,
            yanchor: "middle",
          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

const O3BarChart = ({ value, maxValue }) => {
  const color = getOzoneColor(value);
  const label = getOzoneLabel(value);

  return (
    <Plot
      data={[
        {
          x: [value],
          y: ["Ozone (O3)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: color,
            width: 1,
          },

          textfont: {
            color: "white",
          },
          hoverinfo: "none",
          hovertext: ["Ozone (O3)"],
        },
        {
          x: [maxValue - value],
          y: ["Ozone (O3)"],
          type: "bar",
          orientation: "h",
          marker: {
            color: "#2E2E2E",
            width: 1,
          },
          hoverinfo: "text",
          hovertext: [""],
        },
      ]}
      layout={{
        width: 325,
        height: 30,
        barmode: "stack",
        paper_bgcolor: "transparent",
        plot_bgcolor: "transparent",
        margin: { t: 10, b: 10, l: 0, r: 20 },
        xaxis: {
          range: [0, maxValue],
          visible: false,
        },
        yaxis: {
          visible: false,
        },
        font: { color: "#FFF" },
        showlegend: false,
        annotations: [
          {
            x: value + (maxValue - value) / 2,
            y: "Ozone (O3)",
            text: `${label}`,
            showarrow: false,
            font: {
              color: "white",
            },
            xanchor: "left",
            x:450,
            yanchor: "middle",
          },
        ],
      }}
      config={{ displayModeBar: false }}
    />
  );
};

// Main Component
const AirIndex1 = () => {
  const [lastUpdated, setLastUpdated] = useState<Date | null>(new Date());
  const handleRefresh = () => {
    setLastUpdated(new Date());
  };

  const getSecondsAgo = () => {
    if (!lastUpdated) return null;
    const now = new Date();
    const diff = Math.floor((now.getTime() - lastUpdated.getTime()) / 1000);
    return diff === 0 ? "Just now" : `${diff} second(s) ago`;
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      setLastUpdated(new Date());
    }, 30 * 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const [airQualityData, setAirQualityData] = useState({
    indoor: { aqi: 0 },
    outdoor: { aqi: 0 },
    city: "",
  });

  const createGaugePlot = (aqi, label) => {
    let description, textBgColor,bgColor;
    if (aqi <= 50) {
        description = "Good";
        bgColor = "#339933";
        textBgColor = "#339933"; // Darker green with opacity
      } else if (aqi <= 100) {
        description = "Moderate";
        bgColor = "#ffe510";
        textBgColor = "#ffe510"; // Darker yellow with opacity
      } else if (aqi <= 150) {
        description = "Unhealthy(sensitive)";
        bgColor = "#ffc000";
        textBgColor = "#ffc000"; // Darker orange with opacity
      } else if (aqi <= 200) {
        description = " Unhealthy";
        bgColor = "#ff0000";
        textBgColor = "#ff0000"; // Darker red with opacity
      } else if (aqi <= 300) {
        description = "Very Unhealthy";
        bgColor = "#9900ff";
        textBgColor = "#9900ff"; // Darker red with opacity
      } else {
        description = "Hazardous";
        bgColor = "#673301";
        textBgColor = "#673301"; // Darker purple with opacity
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
                  tickwidth: 1,
                  tickcolor: "transparent",
                  linecolor: "transparent",
                  tickmode: "array",
                  tickvals: [0, 50, 100, 150, 200,250, 300,350,400,450,500], // Define tick values
                  ticktext: ["0", "50", "100", "150", "200","250","300","350","400","450", "500"], // Define tick labels
                },
                bar: { color: aqi <= 100 ? "white" : "white" },
                steps: [
                    { range: [0, 50], color: "#339933" },
                    { range: [51, 100], color: "#ffe510" },
                    { range: [101, 150], color: "#ffc000" },
                    { range: [151, 200], color: "#ff0000" },
                    { range: [201, 300], color: "#9900ff" },
                    { range: [301, 500], color: "#673301" },                ],
                threshold: {
                  line: { color: "transparent", width: 0 },
                },
                bgcolor: "rgba(0,0,0,0)",
              },
              number: {
                suffix: "",
                font: { size: 42, color: "#FFF" },
                valueformat: ".0f",
              },
            },
          ]}
          layout={{
            title: {
              text: label,
              font: {
                color: "#949495",
                size: 14,
                
                family: "mulish",
              },
              y: 1.3,
            },
            width: 350,
            height: 300,
            margin: { t: 70, b: 35, l: 20, r: 40 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            font: { color: "#FFF" },
            annotations: [
              {
                text: description,
                x: 0.5,
                y: -0.05,
                showarrow: false,
                font: {
                  size: 14,
                  color: "black",
                  family: "mulish",
                },
                bgcolor: textBgColor,
                bordercolor: "transparent",
                borderwidth: 1,
                borderpad: 4,
                opacity: 1,
                borderradius: 10,
              },
            ],
          }}
          config={{ displayModeBar: false }}
        />
      </div>
    );
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `${ConfigData.API_URL}/air/air-quality`
        );
        const data = response.data;
        setAirQualityData({
          indoor: data[0][1],
          outdoor: data[1][1],
          city: data[0][1].city,
        });
      } catch (error) {
        console.error("Error fetching air quality data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getAQIDescription = (aqi) => {
    if (aqi <= 50) {
      return {
        impact: "Optimal air quality; ideal for health and well-being.",
        action: "No action required.",
      };
    } else if (aqi <= 100) {
      return {
        impact: "No significant impact on health.",
        action: "No action required.",
      };
    } else if (aqi <= 150) {
      return {
        impact: "Potential reduction in comfort or well-being.",
        action: "Improve ventilation.",
      };
    } else if (aqi <= 200) {
      return {
        impact: "Increased irritation or discomfort.",
        action: "Enhance ventilation with clean air.",
      };
    } else if (aqi <= 250) {
      return {
        impact: "Risk of headaches and other symptoms due to certain VOCs.",
        action: "Optimize ventilation.",
      };
    } else if (aqi <= 350) {
      return {
        impact:
          "Significant health risks, particularly if harmful VOCs are present.",
        action:
          "Identify contamination, maximize ventilation, and limit occupancy.",
      };
    } else {
      return {
        impact: "Severe health effects, including neurotoxicity.",
        action:
          "Immediate contamination assessment; avoid exposure and maximize ventilation.",
      };
    }
  };

  const ColorIndicatorBar = ({ indoorAQI }) => {
    const { impact, action } = getAQIDescription(indoorAQI);
    return (
      <Plot
        data={[
          {
            x: [50, 50, 50, 50, 100, 200],
            y: [1, 1, 1, 1, 1, 1],
            type: "bar",
            orientation: "h",
            marker: {
              color: [
                "#339933",
                "#ffe510",
                "#ffc000",
                "#ff0000",
                "#9900ff",
                "#673301",
              ],
              line: {
                color: "#2e2e2e",
                width: 5,
              },
            },
            hoverinfo: "none",
          },
        ]}
        layout={{
          barmode: "stack",
          width: 1420,
          height: 80,
          margin: { t: 0, b: 20, l: 100, r: 100 },
          xaxis: {
            showgrid: false,
            zeroline: false,
            range: [0, 500],
            tickvals: [0, 50, 100, 150, 200, 300, 500],
            ticktext: ["0", "50", "100", "150", "200", "300", "500"],
            tickfont: { color: "white" },
          },
          yaxis: {
            visible: false,
          },
          showlegend: false,
          paper_bgcolor: "#2e2e2e",
          plot_bgcolor: "#2e2e2e",
          annotations: [
            {
              x: 25,
              y: 1.65,
              text: "Good",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 75,
              y: 1.65,
              text: "Moderate",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 125,
              y: 1.65,
              text: "Unhealthy(sensitive)",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 175,
              y: 1.65,
              text: "Unhealthy ",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 250,
              y: 1.65,
              text: "Very Unhealthy",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 400,
              y: 1.65,
              text: "Hazardous",
              showarrow: false,
              font: {
                color: "#949495",
              },
            },
            {
              x: 260,
              y: 2.9,
              text: `💡Impact</b>: ${impact} | Suggested Action: ${action}`,
              showarrow: false,
              font: {
                color: "#949495",
                size: 16,
              },
            },
          ],
        }}
        config={{ displayModeBar: false }}
      />
    );
  };

  return (
    <Grid
      container
      spacing={2}
      columns={{ xs: 4, sm: 8, md: 12, lg: 12 }}
      className="main-content"
    >
      {/* Indoor Section */}
      <Grid item xs={12} sm={12} md={6} lg={6} className="indoor-section">
        <h3 className="name">INDOOR</h3>
        <div className="city">
          <img src="../images/building.svg" className="icon-color" />
          <h2>Hotel Chancery Pavilion, Residency Road, Bangalore</h2>
        </div>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <div className="cardgrid dis">
              <div>
                {createGaugePlot(
                  airQualityData.indoor.aqi,
                  "<b>Air Quality Index</b> "
                )}
              </div>
              <div>
                <div className="temp-value">
                  <h3>Temperature</h3>
                  <div className="temp-label">
                    <img
                      src="../images/temperature.svg"
                      className="img2 icon-color"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                      {airQualityData.indoor.temperature}
                      </span>
                      <span className="pm-unit"> °C</span>
                    </h2>
                  </div>
                  <TemperatureBarChart
                    value={airQualityData.indoor.temperature}
                    maxValue={50}
                  />
                </div>
                <div>
                  <div className="temp-value">
                    <h3>Humidity</h3>
                  </div>
                  <div className="temp-label">
                    <img
                      src="../images/humidity.svg"
                      className="img2 icon-color"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                      {airQualityData.indoor.humidity}
                      </span>
                      <span className="pm-unit"> %</span>
                    </h2>
                  </div>
                  <HumidityBarChart
                    value={airQualityData.indoor.humidity}
                    maxValue={100}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Particulate Matter 1 (PM1)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Particular matter.svg"
                      className="img2 icon-color"
                      alt="Particulate Matter Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.indoor.pm1}
                      </span>
                      <span className="pm-unit"> µg/m³</span>
                    </h2>
                  </div>
                  <PM1BarChart
                    value={airQualityData.indoor.pm1}
                    maxValue={604}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Particulate Matter 2.5 (PM2.5)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Particular matter.svg"
                      className="img2 icon-color"
                      alt="Particulate Matter Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.indoor.pm25}
                      </span>
                      <span className="pm-unit"> µg/m³</span>
                    </h2>
                  </div>
                  <PM25BarChart
                    value={airQualityData.indoor.pm25}
                    maxValue={500.4}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Carbon Monoxide (CO)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Carbon dioxide.svg"
                      className="img2 icon-color"
                      alt="Carbon Monoxide Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.indoor.co}
                      </span>
                      <span className="pm-unit"> ppm</span>
                    </h2>
                  </div>
                  <COBarChart
                    value={airQualityData.indoor.co}
                    maxValue={35}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Ozone (O3)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/ozone.svg"
                      className="img2 icon-color"
                      alt="Ozone Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">{airQualityData.indoor.o3}</span>
                      <span className="pm-unit"> ppb</span>
                    </h2>
                  </div>
                  <O3BarChart
                    value={airQualityData.indoor.o3}
                    maxValue={500}
                  />
                </div>
              </div>
            </div>
          </Grid>
        </Grid>
      </Grid>

      {/* Outdoor Section */}
      <Grid item xs={12} sm={12} md={6} lg={6} className="outdoor-section">
        <h3 className="name">OUTDOOR</h3>
        <div className="city">
          <img src="../images/building.svg" className="icon-color" />
          <h2>Ashok Nagar, Bengaluru</h2>
          <div
            style={{
              marginTop: "-106px",
              marginRight: "-230px",
            }}
          >
            {lastUpdated && (
              <span
                style={{ marginLeft: "10px", fontSize: "14px", color: "#888" }}
              >
                Last updated: {getSecondsAgo()}
              </span>
            )}
            <button onClick={handleRefresh} className="refresh-button">
              <img src="../images/Refresh ccw.svg" alt="Refresh"className="refr" />
            </button>
          </div>
        </div>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <div className="cardgrid dis">
              <div>
                {createGaugePlot(
                  airQualityData.outdoor.aqi,

                  "<b>Air Quality Index</b> "

                )}
              </div>
              <div>
                <div className="temp-value">
                  <h3>Temperature</h3>
                  <div className="temp-label">
                    <img
                      src="../images/temperature.svg"
                      className="img2 icon-color"
                    />

                    <h2 className="top1">
                      <span className="pm-value">
                      {airQualityData.outdoor.temperature}
                      </span>
                      <span className="pm-unit"> °C</span>
                    </h2>
                  </div>
                  <TemperatureBarChart
                    value={airQualityData.outdoor.temperature}
                    maxValue={50}
                  />
                </div>
                <div>
                  <div className="temp-value">
                    <h3>Humidity</h3>
                  </div>
                  <div className="temp-label">
                    <img
                      src="../images/humidity.svg"
                      className="img2 icon-color"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                      {airQualityData.outdoor.humidity}
                      </span>
                      <span className="pm-unit"> %</span>
                    </h2>
                  </div>
                  <HumidityBarChart
                    value={airQualityData.outdoor.humidity}
                    maxValue={100}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={5.95}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Particulate Matter 1 (PM1)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Particular matter.svg"
                      className="img2 icon-color"
                      alt="Particulate Matter Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.outdoor.pm1}
                      </span>
                      <span className="pm-unit"> µg/m³</span>
                    </h2>
                  </div>
                  <PM1BarChart
                    value={airQualityData.outdoor.pm1}
                    maxValue={604}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={6}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Particulate Matter 2.5 (PM2.5)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Particular matter.svg"
                      className="img2 icon-color"
                      alt="Particulate Matter Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.outdoor.pm25}
                      </span>
                      <span className="pm-unit"> µg/m³</span>
                    </h2>
                  </div>
                  <PM25BarChart
                    value={airQualityData.outdoor.pm25}
                    maxValue={500.4}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={5.95}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Carbon Monoxide (CO)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/Carbon dioxide.svg"
                      className="img2 icon-color"
                      alt="Carbon Monoxide Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">
                        {airQualityData.outdoor.co}
                      </span>
                      <span className="pm-unit"> ppm</span>
                    </h2>
                  </div>
                  <COBarChart
                    value={airQualityData.outdoor.co}
                    maxValue={35}
                  />
                </div>
              </div>
            </div>
          </Grid>
          <Grid item xs={5.95}>
            <div className="card12">
              <div className="in">
                <div className="temp-value1">
                  <h3>Ozone (O3)</h3>
                  <div className="temp-label">
                    <img
                      src="../images/ozone.svg"
                      className="img2 icon-color"
                      alt="Ozone Icon"
                    />
                    <h2 className="top1">
                      <span className="pm-value">{airQualityData.outdoor.o3}</span>
                      <span className="pm-unit"> ppb</span>
                    </h2>
                  </div>
                  <O3BarChart
                    value={airQualityData.outdoor.o3}
                    maxValue={500}
                  />
                </div>
              </div>
            </div>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6} className="outdoor-section">
        <Grid xs={12}>
          <ColorIndicatorBar indoorAQI={airQualityData.indoor.aqi} />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default AirIndex1;
