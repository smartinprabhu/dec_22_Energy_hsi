import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "./Air.css";
import CardHeader from "../CardHeader/CardHead";
import ConfigData from '../../auth/config'
import { Lightbulb as LightbulbIcon } from '@mui/icons-material';

const Airindex = ({ handleFilter, activeGroupFilter }) => {
  const [lastUpdated, setLastUpdated] = useState<Date | null>(new Date());
  const handleRefresh = () => {
    setLastUpdated(new Date());
  };

  // Function to calculate how many seconds ago the last update was
  const getSecondsAgo = () => {
    if (!lastUpdated) return null;
    const now = new Date();
    const diff = Math.floor((now.getTime() - lastUpdated.getTime()) / 1000); // Difference in seconds
    return diff === 0 ? "Just now" : `${diff} second(s) ago`;
  };

  // useEffect to set up the interval for auto-refresh
  useEffect(() => {
    const intervalId = setInterval(() => {
      setLastUpdated(new Date());
    }, 30 * 1000); // Refresh every 30 seconds

    // Cleanup interval on component unmount
    return () => {
      clearInterval(intervalId);
    };
  }, []);


  const [airQualityData, setAirQualityData] = useState({
    indoor: {},
    outdoor: {},
    city: "",
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${ConfigData.API_URL}/air/air-quality`);
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

  const createGaugePlot = (aqi, label) => {
    // State to store the width and height of the Plot component
    const [plotDimensions, setPlotDimensions] = useState({ width: 335, height: 250 });

    useEffect(() => {
      // Function to check the screen size and update the plot dimensions
      const updatePlotDimensions = () => {
        if (window.innerWidth === 1920 && window.innerHeight === 1080) {
          setPlotDimensions({ width: 555, height: 335 }); // Adjust dimensions for the specific media query
        } else {
          setPlotDimensions({ width: 335, height: 250 }); // Default dimensions
        }
      };

      // Call updatePlotDimensions when the component mounts
      updatePlotDimensions();

      // Add an event listener to resize
      window.addEventListener('resize', updatePlotDimensions);

      // Clean up the event listener on component unmount
      return () => window.removeEventListener('resize', updatePlotDimensions);
    }, []);

    // Determine the description and background color based on the AQI value
    let description, bgColor, textBgColor;
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
    } else if (aqi <= 250) {
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
                  tickcolor: "transparent", // Remove ticks outline
                  linecolor: "transparent", // Remove axis outline
                  tickmode: "array", // Use array for custom ticks
                  tickvals: [0, 50, 100, 150, 200, 250,500], // Define tick values
                  ticktext: ["0", "50", "100", "150", "200","250", "500"], // Define tick labels
                },
                bar: { color: aqi <= 100 ? "white" : "white" },
                steps: [
                  { range: [0, 50], color: "#339933" },
                  { range: [51, 100], color: "#ffe510" },
                  { range: [101, 150], color: "#ffc000" },
                  { range: [151, 200], color: "#ff0000" },
                  { range: [201, 250], color: "#9900ff" },
                  { range: [251, 500], color: "#673301" },
                  
                ],
                threshold: {
                  line: { color: "transparent", width: 0 },
                },
                bgcolor: "rgba(0,0,0,0)",
              },
              number: {
                suffix: "",
                font: { size: 82, color: "#FFF" },
                valueformat: ".0f",
              },
            },
          ]}
          layout={{
            title: {
              text: label,
              font: {
                color: "#949495",
                size: 23,
                 family: "Mulish, sans-serif"
              },
              y:1.2,
            },
            width: plotDimensions.width,
            height: plotDimensions.height,
            margin: { t: 50, b: 50, l: 10, r: 20 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            font: { color: "#FFF" },
            annotations: [
              {
                text: description,
                x: 0.5,
                y: -0.15,
                showarrow: false,
                font: {
                  size: 25,
                  color: "black",
                },
                bgcolor: textBgColor,
                bordercolor: "transparent",
                borderwidth: 1,
                borderpad: 4,
                opacity: 0.8,
                borderradius: 10,
              },
            ],
          }}
          config={{ displayModeBar: false }}
        />
      </div>
    );
  };
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
        impact: "Significant health risks, particularly if harmful VOCs are present.",
        action: "Identify contamination, maximize ventilation, and limit occupancy.",
      };
    } else {
      return {
        impact: "Severe health effects, including neurotoxicity.",
        action: "Immediate contamination assessment; avoid exposure and maximize ventilation.",
      };
    }
  };
  
  const getOzoneColor = (value) => {
    if (value >= 0 && value <= 50) return "#339933";
    if (value >= 31 && value <= 60) return "#ffe510";
    if (value >= 61 && value <= 90) return "#ffc000";
    if (value >= 91 && value <= 120) return "#ff0000";
    if (value >= 121 && value <= 150) return "#9900ff";
    if (value >= 151 && value <= 450) return "#673301";
    return "black";
  };

  const getCarbonMonoxideColor = (value) => {
    if (value >= 0 && value <= 5) return "#339933";
    if (value >= 5.01 && value <= 15) return "#ffe510";
    if (value >= 15.01 && value <= 35) return "#ff0000";
    return "black";
  };

  const getPM1Color = (value) => {
    if (value >= 0 && value <= 54) return "#339933";
    if (value >= 55 && value <= 154) return "#ffe510";
    if (value >= 155 && value <= 254) return "#ffc000";
    if (value >= 255 && value <= 354) return "#ff0000";
    if (value >= 355 && value <= 424) return "#9900ff";
    if (value >= 425 && value <= 604) return "#673301";
    return "black";
  };

  const getPM25Color = (value) => {
    if (value >= 0 && value <= 12.09) return "#339933";
    if (value >= 12.10 && value <= 35.49) return "#ffe510";
    if (value >= 35.50 && value <= 55.49) return "#ffc000";
    if (value >= 55.50 && value <= 150.49) return "#ff0000";
    if (value >= 150.50 && value <= 250.9) return "#9900ff";
    if (value >= 250.5 && value <= 500.4) return "#673301";
    return "black";
  };

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

  const getDescription = (value, getColor) => {
    const color = getColor(value);
    if (color === "#339933") return "Good";
    if (color === "#ffe510") return "Moderate";
    if (color === "#ffc000") return "Unhealthy";
    if (color === "#ff0000") return "Very Unhealthy";
    if (color === "#9900ff") return "Hazardous";
    if (color === "#673301") return "Extremely Hazardous";
    return "Unknown";
  };

  const createHorizontalBarPlot = (
    label,
    value,
    maxValue,
    defaultColor = 'white',
    width = 342,
    getColor
  ) => {
    const color = getColor ? getColor(value) : defaultColor;
    const description = getDescription(value, getColor);

    // State to store the height of the plot
    const [plotHeight, setPlotHeight] = useState(27);
    useEffect(() => {
      const updatePlotHeight = () => {
        if (window.innerWidth === 1920 && window.innerHeight === 1080) {
          setPlotHeight(30);
        } else {
          setPlotHeight(27);
        }
      };

      updatePlotHeight();
      window.addEventListener('resize', updatePlotHeight);
      return () => window.removeEventListener('resize', updatePlotHeight);
    }, []);

    return (
      <Plot
        data={[
          {
            x: [value],
            y: [label],
            type: "bar",
            orientation: "h",
            marker: {
              color: color,
              width: 1,
            },
            hoverinfo: 'text',
            hovertext: [`${label}: ${value} - ${description}`],
          },
          {
            x: [maxValue - value],
            y: [label],
            type: "bar",
            orientation: "h",
            marker: {
              color: "#2E2E2E",
              width: 1,
            },
            hoverinfo: 'none',
          },
        ]}
        layout={{
          width: width,
          height: plotHeight,
          barmode: "stack",
          // hovermode:'x unified',
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
          margin: { t: 10, b: 10, l: 0, r: 0 },
          xaxis: {
            range: [0, maxValue],
            visible: false,
          },
          yaxis: {
            visible: false,
          },
          font: { color: "#FFF" },
          showlegend: false,
        }}
        config={{ displayModeBar: false }}
      />
    );
  };

  const renderIndoorData = () => (
    <div className="card1">
      <div className="gauge" style={{ color: '#949495', marginTop: '23px' }}>
        <div style={{ color: 'orange', }}>
          {createGaugePlot(airQualityData.indoor.aqi, "<b>Air Quality Index  </b>")}
        </div>
      </div>

      <div className="temp">
        <div>
          <div className="temp-value">
            <h3>Temperature</h3>
          </div>
          <div className="temp-label">
            <img src="../images/temperature.svg" className="img2 icon-color" />
            <h2 className="top1">{airQualityData.indoor.temperature}°C</h2>
          </div>
          {createHorizontalBarPlot(
            "Temperature",
            airQualityData.indoor.temperature,
            50,
            "green",
            322.8,
            getTemperatureColor
          )}
        </div>
        <div>
          <div className="temp-value">
            <h3>Humidity</h3>
          </div>
          <div className="temp-label">
            <img src="../images/humidity.svg" className="img2 icon-color" />
            <h2 className="top1">{airQualityData.indoor.humidity} %</h2>
          </div>
          {createHorizontalBarPlot(
            "Humidity",
            airQualityData.indoor.humidity,
            100,
            "blue",
            322.8,
            getHumidityColor
          )}
        </div>
      </div>
    </div>
  );

  const renderOutdoorData = () => (
    <div className="card1">
      <div className="gauge" style={{ marginTop: '23px' }}>
        {createGaugePlot(airQualityData.outdoor.aqi, "<b>Air Quality Index</b> ")}
      </div>
      <div className="temp">
        <div>
          <div className="temp-value">
            <h3>Temperature</h3>
          </div>
          <div className="temp-label">
            <img src="../images/temperature.svg" className="img2 icon-color" />
            <h2 className="top1">{airQualityData.outdoor.temperature}°C</h2>
          </div>
          {createHorizontalBarPlot(
            "Temperature",
            airQualityData.outdoor.temperature,
            50,
            "green",
            322.8,
            getTemperatureColor
          )}
        </div>
        <div>
          <div className="temp-value">
            <h3>Humidity</h3>
          </div>
          <div className="temp-label">
            <img src="../images/humidity.svg" className="img2 icon-color" />
            <h2 className="top1">{airQualityData.outdoor.humidity} %</h2>
          </div>
          {createHorizontalBarPlot(
            "Humidity",
            airQualityData.outdoor.humidity,
            100,
            "blue",
            322.8,
            getHumidityColor
          )}
        </div>
      </div>
    </div>
  );

  const Card1 = ({ airQualityData, getPM1Color, getPM25Color }) => {
    const [plotWidth1, setPlotWidth1] = useState(329);

    useEffect(() => {
        const updatePlotWidth = () => {
            if (window.innerWidth === 1920 && window.innerHeight === 1080) {
                setPlotWidth1(443);
            } else {
                setPlotWidth1(329);
            }
        };
        updatePlotWidth();
        window.addEventListener('resize', updatePlotWidth);
        return () => window.removeEventListener('resize', updatePlotWidth);
    }, []);

    return (
        <div className="card12">
            <div className="in">
                <div className="temp-value">
                    <h3>Particulate Matter 1 (PM1)</h3>
                </div>
                <div className="temp-label">
                    <img src="../images/Particular matter.svg" className="img2 icon-color" />
                    <h2 className="top1">
                        <span className="pm-value">{airQualityData.indoor.pm1}</span>
                        <span className="pm-unit"> µg/m³</span>
                    </h2>
                </div>
                {createHorizontalBarPlot(
                    "PM1",
                    airQualityData.indoor.pm1,
                    604,
                    "green",
                    plotWidth1,
                    getPM1Color
                )}
            </div>
            <div className="in">
                <div className="temp-value">
                    <h3>Particulate Matter 2.5 (PM 2.5)</h3>
                </div>
                <div className="temp-label">
                    <img src="../images/Particular matter.svg" className="img2 icon-color" />
                    <h2 className="top1">
                        <span className="pm-value">{airQualityData.indoor.pm25}</span>
                        <span className="pm-unit"> µg/m³</span>
                    </h2>
                </div>
                {createHorizontalBarPlot(
                    "PM2.5",
                    airQualityData.indoor.pm25,
                    500.4,
                    "green",
                    plotWidth1,
                    getPM25Color
                )}
            </div>
        </div>
    );
};

const Card2 = ({ airQualityData, getPM1Color, getPM25Color }) => {
  const [plotWidth2, setPlotWidth2] = useState(329);

  useEffect(() => {
      const updatePlotWidth = () => {
          if (window.innerWidth === 1920 && window.innerHeight === 1080) {
              setPlotWidth2(443);
          } else {
              setPlotWidth2(329);
          }
      };
      updatePlotWidth();
      window.addEventListener('resize', updatePlotWidth);
      return () => window.removeEventListener('resize', updatePlotWidth);
  }, []);

  return (
      <div className="card12">
          <div className="in">
              <div className="temp-value">
                  <h3>Particulate Matter 1 (PM1)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/Particular matter.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.outdoor.pm1}</span>
                      <span className="pm-unit"> µg/m³</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "PM1",
                  airQualityData.outdoor.pm1,
                  604,
                  "green",
                  plotWidth2,
                  getPM1Color
              )}
          </div>
          <div className="in">
              <div className="temp-value">
                  <h3>Particulate Matter 2.5 (PM 2.5)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/Particular matter.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.outdoor.pm25}</span>
                      <span className="pm-unit"> µg/m³</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "PM2.5",
                  airQualityData.outdoor.pm25,
                  500.4,
                  "green",
                  plotWidth2,
                  getPM25Color
              )}
          </div>
      </div>
  );
};

const Card3 = ({ airQualityData, getCarbonMonoxideColor, getOzoneColor }) => {
  const [plotWidth3, setPlotWidth3] = useState(329);

  useEffect(() => {
      const updatePlotWidth = () => {
          if (window.innerWidth === 1920 && window.innerHeight === 1080) {
              setPlotWidth3(443);
          } else {
              setPlotWidth3(329);
          }
      };

      updatePlotWidth();
      window.addEventListener('resize', updatePlotWidth);
      return () => window.removeEventListener('resize', updatePlotWidth);
  }, []);

  return (
      <div className="card12">
          <div className="in">
              <div className="temp-value">
                  <h3>Carbon Monoxide (CO)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/Carbon dioxide.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.indoor.co}</span>
                      <span className="pm-unit"> ppb</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "CO",
                  airQualityData.indoor.co,
                  35,
                  "green",
                  plotWidth3,
                  getCarbonMonoxideColor
              )}
          </div>
          <div className="in">
              <div className="temp-value">
                  <h3>Ozone (O3)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/ozone.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.indoor.o3}</span>
                      <span className="pm-unit"> ppb</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "O3",
                  airQualityData.indoor.o3,
                  500,
                  "green",
                  plotWidth3,
                  getOzoneColor
              )}
          </div>
      </div>
  );
};

const Card4 = ({ airQualityData, getCarbonMonoxideColor, getOzoneColor }) => {
  const [plotWidth4, setPlotWidth4] = useState(329);

  useEffect(() => {
      const updatePlotWidth = () => {
          if (window.innerWidth === 1920 && window.innerHeight === 1080) {
              setPlotWidth4(443);
          } else {
              setPlotWidth4(329);
          }
      };

      updatePlotWidth();
      window.addEventListener('resize', updatePlotWidth);
      return () => window.removeEventListener('resize', updatePlotWidth);
  }, []);

  return (
      <div className="card12">
          <div className="in">
              <div className="temp-value">
                  <h3>Carbon Monoxide (CO)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/Carbon dioxide.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.outdoor.co}</span>
                      <span className="pm-unit"> ppb</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "CO",
                  airQualityData.outdoor.co,
                  35,
                  "green",
                  plotWidth4,
                  getCarbonMonoxideColor
              )}
          </div>
          <div className="in">
              <div className="temp-value">
                  <h3>Ozone (O3)</h3>
              </div>
              <div className="temp-label">
                  <img src="../images/ozone.svg" className="img2 icon-color" />
                  <h2 className="top1">
                      <span className="pm-value">{airQualityData.outdoor.o3}</span>
                      <span className="pm-unit"> ppb</span>
                  </h2>
              </div>
              {createHorizontalBarPlot(
                  "O3",
                  airQualityData.outdoor.o3,
                  500,
                  "green",
                  plotWidth4,
                  getOzoneColor
              )}
          </div>
      </div>
  );
};
const ColorIndicatorBar = ({ indoorAQI }) => {
  const [barWidth, setBarWidth] = useState(1433);
  const [barHeight, setBarHeight] = useState(80);

  useEffect(() => {
    const updateWidth = () => {
      if (window.innerWidth === 1920 && window.innerHeight === 1080) {
        setBarWidth(1890);
        setBarHeight(100);
      } else {
        setBarWidth(1433);
        setBarHeight(90);
      }
    };
    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  const { impact, action } = getAQIDescription(indoorAQI);

  return (
    <Plot
      data={[
        {
          x: [50, 50, 50, 50, 50, 250],
          y: [1, 1, 1, 1, 1, 1],
          type: 'bar',
          orientation: 'h',
          marker: {
            color: ['#339933', '#ffe510', '#ffc000', '#ff0000', '#9900ff', '#673301'],
            line: {
              color: '#2e2e2e',
              width: 5,
            },
          },
          hoverinfo: 'none',
        },
      ]}
      layout={{
        barmode: 'stack',
        width: barWidth,
        
        height: barHeight,
        margin: { t: 0, b: 20, l: 100, r: 100 },

        xaxis: {
          showgrid: false,
          zeroline: false,
          range: [0, 500],
          tickvals: [0, 50, 100, 150, 200, 250, 500], // Define tick values
          ticktext: ["0", "50", "100", "150", "200", "250", "500"], // Define tick labels
          tickfont: { color: 'white' },
        },
        yaxis: {
          visible: false,
        },
        showlegend: false,
        paper_bgcolor: '#2e2e2e',
        plot_bgcolor: '#2e2e2e',
        annotations: [
          {
            x: 25,
            y: 1.65,
            text: 'Good',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },
          {
            x: 75, // Position for the "Moderate" label
            y: 1.65,
            text: 'Moderate',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },
          {
            x: 125,
            y: 1.65,
            text: 'Unhealthy(sensitive)',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },
          {
            x: 175,
            y: 1.65,
            text: 'Unhealthy ',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },
          {
            x: 225,
            y: 1.65,
            text: 'Very Unhealthy',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },
          {
            x: 400,
            y: 1.65,
            text: 'Hazardous',
            showarrow: false,
            font: {
              color: '#949495',
            },
          },

          {
            x: 250,
            y: 2.2,
            text: `💡 Impact</b>: ${impact} | Suggested Action: ${action}`,
            showarrow: false,

            font: {
              color: '#949495',

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
  <div className="air-index-container">
    {/* <CardHeader
      handleFilter={handleFilter}
      activeGroupFilter={activeGroupFilter}
    /> */}
    <div className="main-container1">
      <div className="head">
        <h2>INDOOR</h2>
        <h2>OUTDOOR</h2>
      </div>
      <div className="mid">
        <div className="city">
          <img src="../images/building.svg" className="icon-color" />
          <h2>Hotel Chancery Pavilion, Residency Road, Bangalore</h2>
        </div>
        <div className="city city1">
          <img src="../images/building.svg" className="icon-color" />
          <h2>Ashok Nagar, Bengaluru</h2>
        </div>
        <div style={{ marginTop: "14px", textAlign: "right", marginLeft:"87px"}}>
        {lastUpdated && (
          <span style={{ marginLeft: "10px", fontSize: "14px", color: "#888" }}>
            Last updated: {getSecondsAgo()}
          </span>
        )}
        <button onClick={handleRefresh} className="refresh-button">
          <img src="../images/Refresh ccw.svg" alt="Refresh" />
        </button>
      </div>

      </div>
      <div className="container1">
        {renderIndoorData()}
        {renderOutdoorData()}
        <Card1 airQualityData={airQualityData} getPM1Color={getPM1Color} getPM25Color={getPM25Color} />
        <Card2 airQualityData={airQualityData} getPM1Color={getPM1Color} getPM25Color={getPM25Color} />
        <Card3 airQualityData={airQualityData} getCarbonMonoxideColor={getCarbonMonoxideColor} getOzoneColor={getOzoneColor} />
        <Card4 airQualityData={airQualityData} getCarbonMonoxideColor={getCarbonMonoxideColor} getOzoneColor={getOzoneColor} />
        <div className="aqi-bar clas">
          <ColorIndicatorBar indoorAQI={airQualityData.indoor.aqi} />
        </div>
      </div>
    </div>
  </div>
);
};

export default Airindex;
