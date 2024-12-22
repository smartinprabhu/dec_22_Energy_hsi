import React, {
  useEffect,
  useState,
  useRef,
  useCallback,
  useMemo,
} from "react";
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

const Energy = ({
  defaultDate,
  headerText,
  showBackButton,
  onBackButtonClick,
  fontSize
}) => {
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
  const [increaseValue, setIncreaseValue] = useState("0");
  const [selectedOption, setSelectedOption] = useState("Dynamic"); // Default is Static
  const [staticResults, setStaticResults] = useState(null);
  const [dynamicResults, setDynamicResults] = useState(null);
  const [staticInputValue, setStaticInputValue] = useState("0"); // Store the static input value
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

  const handleResize = useCallback(() => {
    setPlotDimensions({
      width: window.innerWidth,
      height: window.innerHeight * 0.7, // Adjusted to 70% of the viewport height
    });
  }, []);

  const handlePlotTypeChange = useCallback((event) => {
    setPlotType(event.target.value);
  }, []);

  const fetchPlotData = useCallback(
    async (option = selectedOption) => {
      setIsLoading(true);
      setPlotData({}); // Clear plot data on option change
      try {
        const url =
          option === "Dynamic"
            ? `${ConfigData.API_URL}/energy/forecast/dynamic`
            : `${ConfigData.API_URL}/energy/forecast/static`;

        const body =
          option === "Static"
            ? { increase_value: increaseValue }
            : { increase_percent: increaseValue };

        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });
        const data = await response.json();
        const structuredData = structureData(data);

        if (option === "Dynamic") {
          setDynamicResults(structuredData);
          setStaticInputValue(increaseValue);
        } else {
          setStaticResults(structuredData);
          setStaticInputValue(increaseValue);
        }

        setPlotData(structuredData);
        setError("");
      } catch (error) {
        setError(
          error.message || "An error occurred while fetching the plot data."
        );
        setPlotData({});
      } finally {
        setIsLoading(false);
      }
    },
    [increaseValue]
  );

  const structureData = useCallback((data) => {
    // Assuming the data format is an array of arrays
    const structured = {};
    data.forEach((entry) => {
      // Assuming each entry is an array of two items: [key, value]
      const [key, value] = entry;
      structured[key] = value;
    });
    return structured;
  }, []);

  const theme = useMemo(
    () =>
      createTheme({
        components: {
          MuiRadio: {
            styleOverrides: {
              root: {
                color: "#ffffff",
              },
            },
          },
        },
      }),
    []
  );

  const currentData = useMemo(
    () => plotData[plotType] || {},
    [plotData, plotType]
  );

  const customLayout = useMemo(
    () => ({
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
    }),
    []
  );

  const handleOptionChange = useCallback(
    (option) => {
      setSelectedOption(option);
      fetchPlotData(option); // Pass the new option directly
      if (option === "Static") setDynamicResults(null);
      else setStaticResults(null);
    },
    [fetchPlotData]
  );

  const handleLoadUpdate = useCallback(
    (value) => {
      setIncreaseValue("0");
      fetchPlotData(selectedOption); // Trigger data load and update based on the current option
    },
    [selectedOption, fetchPlotData]
  );
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
            headerText={headerText || "Energy"}
            showToggle={true}
            onInputValueChange={setIncreaseValue}
            onLoadUpdate={handleLoadUpdate}
            onOptionChange={handleOptionChange}
            initialSelectedOption={selectedOption} // Pass the selected option as a prop
            staticInputValue={staticInputValue}
            showBackButton={showBackButton}
            onBackButtonClick={onBackButtonClick}
            fontSize={fontSize} // Pass the static input value as a prop
          >
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
                  {Object.entries(currentData).map(([key, value], index) => {
                    // Skip the 'week_plot' section
                    if (key === "week_plot") {
                      return null;
                    }

                    // Render the fourth response fully with separate styling
                    if (index === 3) {
                      return (
                        <div
                          key={key}
                          className={`energybox fourth-card ${
                            themes === "light" ? "lighteng" : ""
                          }`}
                        >
                          <div className="par1">
                            <p
                              className={`tit1${
                                themes === "light" ? "light-mode" : "dark-mode"
                              }`}
                            >
                              {key.replace(/_/g, " ")}
                            </p>
                            {/* Render the entire fourth response fully */}
                            {typeof value === "object" &&
                            !Array.isArray(value) ? (
                              <div className="parent-container">
                                {Object.entries(value).map(
                                  ([subKey, subValue]) => (
                                    <div className="subKey" key={subKey}>
                                      <React.Fragment>
                                        <p className="p1 chart-title-responsive font">
                                          {subKey.replace(/_/g, " ")}
                                        </p>
                                        <p className="p2 chart-title-responsive font">
                                          {typeof subValue === "string" &&
                                          (subValue.includes("▼") ||
                                            subValue.includes("▲"))
                                            ? (() => {
                                                const isNegative =
                                                  subValue.includes("▼");
                                                const colorClass = isNegative
                                                  ? "green-text"
                                                  : "red-text"; // Add class based on value
                                                return (
                                                  <span className={colorClass}>
                                                    {subValue}
                                                  </span>
                                                );
                                              })()
                                            : typeof subValue === "number"
                                            ? subValue.toFixed(2) // Ensure two decimal places for numbers
                                            : String(subValue)}
                                        </p>
                                      </React.Fragment>
                                    </div>
                                  )
                                )}
                              </div>
                            ) : null}
                          </div>
                        </div>
                      );
                    }

                    // Skip the second subkey-subvalue pairs for all other responses
                    if (key !== `${plotType.toLowerCase()}_plot`) {
                      return (
                        <div
                          key={key}
                          className={`energybox ${
                            themes === "light" ? "lighteng" : ""
                          }`}
                        >
                          <div className="par">
                            <p
                              className={`tit${
                                themes === "light" ? "light-mode" : "dark-mode"
                              }`}
                            >
                              {key.replace(/_/g, " ")}
                              <p className="subtit">
                                {typeof value === "object" &&
                                !Array.isArray(value)
                                  ? (() => {
                                      const entries = Object.entries(value);
                                      const secondEntry = entries.find(
                                        ([key]) =>
                                          key === "So_far_Today" ||
                                          key === "Current_Weekend_so_far" ||
                                          key === "Current_Workweek_so_far" ||
                                          key === "Current_Year_so_far" ||
                                          key === "Current_Month_so_far" ||
                                          key === "Current_Week_so_far"
                                      );
                                      return secondEntry
                                        ? (() => {
                                            const match =
                                              secondEntry[1].match(
                                                /([\d.]+)\s*(.+)/
                                              ); // Separate number and unit
                                            if (match) {
                                              const [_, numericValue, unit] =
                                                match; // Extract matched groups
                                              return (
                                                <>
                                                  {numericValue}
                                                  <span className="unit">
                                                    {" "}
                                                    {unit}
                                                  </span>
                                                </>
                                              );
                                            }
                                            return secondEntry[1];
                                          })()
                                        : null;
                                    })()
                                  : null}
                              </p>
                              {/* Add image based on the key */}
                            </p>
                            <div
                              className={`imgg${
                                themes === "light" ? "light-mode" : ""
                              }`}
                            >
                              {key.toLowerCase().includes("consumption") && (
                                <img
                                  src="../images/power.svg"
                                  alt="Consumption"
                                  className="data-image"
                                />
                              )}
                              {key.toLowerCase().includes("cost") && (
                                <img
                                  src="../images/DOLLAR.svg"
                                  alt="Estimated Cost"
                                  className="data-image"
                                />
                              )}
                              {key.toLowerCase().includes("emissions") && (
                                <img
                                  src="../images/LEAF.svg"
                                  alt="Emissions"
                                  className="data-image im"
                                />
                              )}
                            </div>
                          </div>
                          {/* Render other subkeys and subvalues */}
                          {typeof value === "object" &&
                          !Array.isArray(value) ? (
                            <div className="parent-container">
                              {/* Skip the second subkey-subvalue pair */}
                              {Object.entries(value)
                                .filter((_, index) => index !== 1) // Skip the second subkey-subvalue pair
                                .map(([subKey, subValue]) => (
                                  <div className="subKey" key={subKey}>
                                    <React.Fragment>
                                      <p className="p1 chart-title-responsive font">
                                        {subKey.replace(/_/g, " ")}
                                      </p>
                                      <p className="p2 chart-title-responsive font">
                                        {typeof subValue === "string" &&
                                        (subValue.includes("▼") ||
                                          subValue.includes("▲"))
                                          ? (() => {
                                              const isNegative =
                                                subValue.includes("▼");
                                              const colorClass = isNegative
                                                ? "green-text"
                                                : "red-text"; // Add class based on value
                                              return (
                                                <span className={colorClass}>
                                                  {subValue}
                                                </span>
                                              );
                                            })()
                                          : typeof subValue === "number"
                                          ? subValue.toFixed(2) // Ensure two decimal places for numbers
                                          : String(subValue)}
                                      </p>
                                    </React.Fragment>
                                  </div>
                                ))}
                            </div>
                          ) : null}
                        </div>
                      );
                    }
                  })}
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
                      ...customLayout,
                      ...currentData[`${plotType.toLowerCase()}_plot`]?.layout,
                      title: {
                        text: "Predicted Energy Consumption vs. Target",
                        font: {
                          family: "Mulish",
                          size: 17,
                          color: themes === "dark" ? "white" : "black",
                        },
                        y: 0.95,
                        x: 0.02,
                        align: "left",
                      },
                      font: {
                        color: themes === "dark" ? "white" : "black",
                      },
                    }}
                    style={{
                      width: plotDimensions.width,
                      height: 620,
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

export default Energy;
