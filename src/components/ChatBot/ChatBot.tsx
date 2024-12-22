import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Grid from "@mui/material/Grid";
import Card from "../Card/CardRes";
import Loader from "../Loader/Loader";
import "../ChatBot/ChatBot.css";
import ConfigData from "../../auth/config";

import Plot from "react-plotly.js";
import html2canvas from "html2canvas";
import { useTheme } from "../ThemeContext";



const PlotlyChart = ({ data }) => {
  const {
    x = [],  // Labels for bar chart
    y = [],  // Values for bar chart
    title = "Chart Title", // Title from the API response
    xAxisTitle = "X Axis", // Default x-axis title
    yAxisTitle = "Y Axis", // Default y-axis title
  } = data || {};
  const { themes } = useTheme();


  const chartType = title.toLowerCase() === "pie chart" ? "pie" : "bar"; // Determine chart type
  const chartRef = useRef(); // Create a ref for the chart

  const handleDownload = () => {
    html2canvas(chartRef.current).then((canvas) => {
      const link = document.createElement("a");
      link.href = canvas.toDataURL("image/png");
      link.download = `${title.replace(/\s+/g, "_")}.png`; // Filename with title
      link.click();
    });
  };

  return (
    <div>
      <div ref={chartRef}>
        <Plot
          className="chart"
          data={[
            {
              x: chartType === "bar" ? x : [],
              y: chartType === "bar" ? y : [],
              labels: chartType === "pie" ? x : [],
              values: chartType === "pie" ? y : [],
              type: chartType,
              marker: {
                colors: chartType === "pie" ? ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"] : undefined,
              },
            },
          ]}
          layout={{
            title: {
              text: title,
              font: {
                family: "Mulish",
                size: 18,
                color: themes === "dark" ? "white" : "black",               },
            },
            showlegend: chartType === "pie",
            paper_bgcolor:themes === "dark" ? "#2D2D2D" : '',
            plot_bgcolor: themes === "dark" ? "#2D2D2D" : '',
            font: {
              family: "Mulish",
              size: 10,
              color: themes === "dark" ? "white" : "black",            },
            xaxis: {
              title: {
                text: xAxisTitle,
                font: {
                  family: "Mulish",
                  size: 14,
                  color: themes === "dark" ? "white" : "black",                },
              },
            },
            yaxis: {
              title: {
                text: yAxisTitle,
                font: {
                  family: "Mulish",
                  size: 14,
                  color: themes === "dark" ? "white" : "black",                },
              },
            },
          }}
          config={{ displayModeBar: false }}
        />
      <button onClick={handleDownload} className="down" >
        Download as Image
      </button>
      </div>
    </div>
  );
};

const GENERAL_QUERY_ENDPOINT = `${ConfigData.API_URL}/aiassist/general_query`;
const CHAT_ENDPOINT = `${ConfigData.API_URL}/aiassist/chat`;
const INSIGHTS_ENDPOINT = `${ConfigData.API_URL}/aiassist/insights`;
const ChatBot = ({ dataLoading }) => {
  const [messageList, setMessageList] = useState([]);
  const [error, setError] = useState("");
  const [topics, setTopics] = useState([]);
  const [featuredPrompts, setFeaturedPrompts] = useState([]);
  const [history, setHistory] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [cancelTokenSource, setCancelTokenSource] = useState(null);
  const [loadingBotMessage, setLoadingBotMessage] = useState(false);
  const [showScrollDownIcon, setShowScrollDownIcon] = useState(false);
  const [copyStatus, setCopyStatus] = useState({});
  const [isMobileView, setIsMobileView] = useState(window.innerWidth <= 768); // Initial mobile view detection
  const [isLeftSideVisible, setIsLeftSideVisible] = useState(
    window.innerWidth > 768
  ); // Initially false if mobile view
  const chatHistoryEndRef = useRef(null);
  const chatHistoryRef = useRef(null);
  const leftSideRef = useRef(null);
  const [isInsightsMode, setIsInsightsMode] = useState(false);
  const { themes } = useTheme();

  const handleResize = () => {
    const mobileView = window.innerWidth <= 768;
    setIsMobileView(mobileView);
    setIsLeftSideVisible(!mobileView); // Hide sidebar on mobile view resize
  };
  const toggleSidebar = () => {
    setIsLeftSideVisible((prev) => !prev);
  };
  useEffect(() => {
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  useEffect(() => {
    const loadInitialScreenData = async () => {
      try {
        const response = await axios.get(
          `${ConfigData.API_URL}/aiassist/initial_screen`
        );
        setTopics(response.data.topics || []);
        setFeaturedPrompts(response.data.featured_prompts || []);
        setHistory(response.data.history || []);
      } catch (error) {
        console.error("Error fetching initial screen data:", error);
      }
    };
    loadInitialScreenData();
  }, []);
  useEffect(() => {
    const handleScroll = () => {
      if (chatHistoryRef.current) {
        const { scrollTop, scrollHeight, clientHeight } =
          chatHistoryRef.current;
        setShowScrollDownIcon(scrollHeight - scrollTop > clientHeight + 5);
      }
    };

    if (chatHistoryRef.current) {
      chatHistoryRef.current.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (chatHistoryRef.current) {
        chatHistoryRef.current.removeEventListener("scroll", handleScroll);
      }
    };
  }, []);
  useEffect(() => {
    if (chatHistoryEndRef.current) {
      chatHistoryEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messageList]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (leftSideRef.current && !leftSideRef.current.contains(event.target)) {
        setIsLeftSideVisible(false);
      }
    };
    // Attach the event listener
    document.addEventListener("mousedown", handleClickOutside);
    // Cleanup the event listener
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);
  const handleRequest = async (message) => {
    if (!message.trim()) return;

    setIsSending(true);
    setLoadingBotMessage(true);

    try {
      // Add the user message to the chat
      addMessage({ text: message, type: "user" });

      const requestBody = {
        message,
        conversation_id: activeConversation,
      };

      const response = await axios.post(GENERAL_QUERY_ENDPOINT, requestBody);


      // Check if response contains the necessary fields
      if (response.data && response.data.response) {
        const responseString = response.data.response;
        const jsonStartIndex = responseString.indexOf("{");
        const jsonEndIndex = responseString.lastIndexOf("}");

        if (jsonStartIndex !== -1 && jsonEndIndex !== -1) {
          const jsonString = responseString.substring(
            jsonStartIndex,
            jsonEndIndex + 1
          );
          const parsedResponse = JSON.parse(jsonString);
          let newChartData1 = { x: [], y: [], title: "", xAxisTitle: "", yAxisTitle: "" };
          if (parsedResponse.chart && parsedResponse.chart.chart_data) {
            const chartData = parsedResponse.chart.chart_data;
            const xAxisLabel = parsedResponse.chart.x_axis_label || "X Axis";
            const yAxisLabel = parsedResponse.chart.y_axis_label || "Y Axis";
          
            if (chartData && chartData.length) {
              // Dynamically determine x and y keys
              const keys = Object.keys(chartData[0]);
              if (keys.length >= 2) {
                const xKey = keys[0]; // Assuming the first key is for x-axis
                const yKey = keys[1]; // Assuming the second key is for y-axis
          
                const x = chartData.map((item) => item[xKey]);
                const y = chartData.map((item) => item[yKey]);
          
                newChartData1 = {
                  x: x || [],
                  y: y || [],
                  title: parsedResponse.chart.title || "Your Chart Title", // Use the chart type as the title
                  xAxisTitle: xAxisLabel || xKey, // Use the JSON label or dynamic key as x-axis title
                  yAxisTitle: yAxisLabel || yKey, // Use the JSON label or dynamic key as y-axis title
                };
              } else {
                console.error("Chart data does not have enough properties to map x and y.");
              }
            } else {
              console.error("No chart data available.");
            }
          }
          const explanation = parsedResponse.explanation;
          if (explanation) {
            addMessage({ text: explanation, chart_data: newChartData1, type: "bot", isHtml: true });
          } else {
            addMessage({
              text: "An error occurred while processing your request. Please try again or try asking a different question.",
              type: "bot",
              isHtml: true,
            });
          }
        } else {
          addMessage({
            text: "An error occurred while processing your request. Please try again or try asking a different question.",
            type: "bot",
            isHtml: true,
          });
        }
      } else {
        addMessage({
          text: "An error occurred while processing your request. Please try again or try asking a different question..",
          type: "bot",
          isHtml: true,
        });
      }

      // Update the active conversation if available
      if (response.data.conversation_id) {
        setActiveConversation(response.data.conversation_id);
      }
      // Update the initial screen data after handling the response
      const loadInitialScreenData = async () => {
        try {
          const response = await axios.get(
            `${ConfigData.API_URL}/aiassist/initial_screen`
          );
          setTopics(response.data.topics || []);
          setFeaturedPrompts(response.data.featured_prompts || []);
          setHistory(response.data.history || []);
        } catch (error) {
          console.error("Error fetching initial screen data:", error);
        }
      };

      // Call loadInitialScreenData after request
      loadInitialScreenData();
      setError("");
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Error fetching data. Please try again.");
    } finally {
      setIsSending(false);
      setLoadingBotMessage(false);
    }
  };
  const handleSubmit = async (messageToSend) => {
  if (messageToSend.trim() === '') return;

    setIsSending(true);
    setLoadingBotMessage(true);
  addMessage({ text: messageToSend, type: 'user' });
  setInputValue('');

    const source = axios.CancelToken.source();
    setCancelTokenSource(source);

    try {
      const requestBody = {
        message: messageToSend,
        conversation_id: activeConversation,
      };

      const endpoint = isInsightsMode ? CHAT_ENDPOINT : GENERAL_QUERY_ENDPOINT;
      const response = await axios.post(endpoint, requestBody, {
        cancelToken: source.token,
      });

      const responseString = response.data.response;

      // Extracting the JSON part of the response
      const jsonStartIndex = responseString.indexOf("{");
      const jsonEndIndex = responseString.lastIndexOf("}");

      let explanation = ""; // Initialize explanation
      let chartData = {
        x: [],
        y: [],
        title: "",
        xAxisTitle: "",
        yAxisTitle: "",
      }; // Initialize chart data

      if (jsonStartIndex !== -1 && jsonEndIndex !== -1) {
        const jsonString = responseString.substring(
          jsonStartIndex,
          jsonEndIndex + 1
        );
        const parsedResponse = JSON.parse(jsonString);

        // Extract the explanation from the parsed response
        explanation = parsedResponse.explanation || "An error occurred while processing your request. Please try again or try asking a different question.";
      let msg = { text: explanation, chart_data: [], type: "bot", isHtml: true };
        // Check for chart data in the parsed response
        if (parsedResponse.chart && parsedResponse.chart.chart_data) {
          const chartDataResponse = parsedResponse.chart.chart_data;

          if (chartDataResponse && chartDataResponse.length) {
            // Dynamically determine x and y keys
            const keys = Object.keys(chartDataResponse[0]);
            if (keys.length >= 2) {
              const xKey = keys[0]; // Assuming the first key is for x-axis
              const yKey = keys[1]; // Assuming the second key is for y-axis

              const x = chartDataResponse.map((item) => item[xKey]);
              const y = chartDataResponse.map((item) => item[yKey]);

              // Set the chart data
              chartData = {
                x: x || [],
                y: y || [],
                title: parsedResponse.chart.title || "Your Chart Title",
                xAxisTitle: xKey, // Use the JSON label or dynamic key as x-axis title
                yAxisTitle: yKey, 
                };
               msg = { text: explanation, chart_data: chartData, type: "bot", isHtml: true };
              // Update the chart state (assuming you have a setChartData function)
            } else {
              console.error(
                "Chart data does not have enough properties to map x and y."
              );
            }
          } else {
            console.error("No chart data available.");
          }
          addMessage(msg);
        }
      } else {
        addMessage({
          text: "An error occurred while processing your request. Please try again or try asking a different question.",
          type: "bot",
          isHtml: true,
          chart_data:[]
        });
      }

      // Update the active conversation if available
      if (response.data.conversation_id) {
        setActiveConversation(response.data.conversation_id);
      }
      

      // Update history with user input and response
      setHistory((prevHistory) => {
        return prevHistory.map((conversation) => {
          if (conversation.Conversation_Id === activeConversation) {
            const updatedLogs = [
              ...(conversation.logs || []),
              {
                Created_By: "user",
                Created_On: new Date().toISOString(),
                Input_Prompt: messageToSend,
                Response: explanation, // Use the explanation variable here
              },
            ];
            return {
              ...conversation,
              logs: updatedLogs,
            };
          }
          return conversation;
        });
      });

      // Scroll down icon logic
      if (
        chatHistoryRef.current.scrollHeight >
        chatHistoryRef.current.clientHeight
      ) {
        setShowScrollDownIcon(true);
      }
    
      if (isInsightsMode) {
        setIsInsightsMode(false); // Exit insights mode after submitting
      }
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log("Request canceled:", error.message);
      } else {
        console.error("Error sending chat message:", error);
        setError("Error sending message. Please try again.");

        setHistory((prevHistory) => {
          return prevHistory.map((conversation) => {
            if (conversation.Conversation_Id === activeConversation) {
              const updatedLogs = [
                ...(conversation.logs || []),
                {
                  Created_By: "user",
                  Created_On: new Date().toISOString(),
                  Input_Prompt: messageToSend,
                  Response:
                    "Sorry, there was an error processing your request.",
                },
              ];
              return {
                ...conversation,
                logs: updatedLogs,
              };
            }
            return conversation;
          });
        });
      }
    } finally {
      setIsSending(false);
      setLoadingBotMessage(false);
      setCancelTokenSource(null);
    }
  };

  const handleStop = () => {
    if (cancelTokenSource) {
      cancelTokenSource.cancel("Operation canceled by the user.");
    }
    setIsSending(false);
    setLoadingBotMessage(false);
    setCancelTokenSource(null);
    setInputValue("");
  };
  const handleConversationClick = async (conversation) => {
    console.log("Conversation clicked:", conversation);
  
    if (!conversation.Conversation_Id) {
      console.log("No conversation Id found.");
      return;
    }
  
    // Clear previous chart data when switching conversations
  
    try {
      // Fetch the conversation logs from the API
      const response = await axios.post(
        `${ConfigData.API_URL}/aiassist/conversation_logs`,
        { Id: conversation.Conversation_Id }
      );
      console.log("Conversation Logs Response:", response.data);
  
      const logs = response.data.conversation_logs || [];
      
      // Initialize chart data and messages array
      const messages = Array.isArray(logs)
        ? logs.map((log) => {
            const jsonStartIndex = log.Response.indexOf("{");
            const jsonEndIndex = log.Response.lastIndexOf("}");
  
            // Initialize explanation and input
            let explanation = "No explanation available."; // Default message
            let newChartData = { x: [], y: [], title: "", xAxisTitle: "", yAxisTitle: "" }; // Default chart data
            let userInput = log.Input_Prompt || "No user input available.";
  
            if (jsonStartIndex !== -1 && jsonEndIndex !== -1) {
              const jsonString = log.Response.substring(jsonStartIndex, jsonEndIndex + 1);
              try {
                const parsedResponse = JSON.parse(jsonString);
  
                explanation = parsedResponse.explanation || "No explanation available.";
  
                // Check if chart data exists
                if (parsedResponse.chart && parsedResponse.chart.chart_data) {
                  const chartDataResponse = parsedResponse.chart.chart_data;
                  const keys = Object.keys(chartDataResponse[0]);
  
                  if (keys.length >= 2) {
                    const xKey = keys[0];
                    const yKey = keys[1];
                    const x = chartDataResponse.map((item) => item[xKey]);
                    const y = chartDataResponse.map((item) => item[yKey]);
  
                    // Accumulate chart data for this conversation
                    newChartData = {
                      x: x || [],
                      y: y || [],
                      title: parsedResponse.chart.title || "Your Chart Title",
                      xAxisTitle: xKey || "X Axis",
                      yAxisTitle: yKey || "Y Axis",
                      };
                  } else {
                     newChartData = { x: [], y: [], title: "", xAxisTitle: "", yAxisTitle: "" }; // Default chart data
                  }
                } else {
                  newChartData = { x: [], y: [], title: "", xAxisTitle: "", yAxisTitle: "" }; // Default chart data
                }
              } catch (error) {
                console.error("Error parsing JSON response:", error);
              }
            }
  
            // Return both user input and bot response
            return [
              { text: userInput, type: "user", isHtml: true },
              { text: explanation, chart_data: newChartData, type: "bot", isHtml: true }
            ];
          })
        : [];
  
      // Flatten messages array since we are returning an array of arrays
      const flattenedMessages = messages.flat();
  
      // Set the messages and chart data
      setMessageList(flattenedMessages);
      setActiveConversation(conversation.Conversation_Id);
      setError("");
  
      // Hide the left sidebar on mobile view
      if (isMobileView) {
        setIsLeftSideVisible(false);
      }
    } catch (error) {
      console.error("Error fetching conversation logs:", error);
      setError("Error fetching conversation logs. Please try again.");
    }
  };
    
    const handleInsightsRequest = async () => {
    setIsLeftSideVisible(false);
    setIsSending(true);
    setLoadingBotMessage(true);
    try {
      setMessageList([]);
      addMessage({
        text: "Requesting Helpdesk Compliance insights...",
        type: "user",
      });
      const response = await axios.post(INSIGHTS_ENDPOINT, {
        message: "Helpdesk Compliance",
      });
      addMessage({
        text: processText(response.data.insights),
        type: "bot",
        isHtml: true,
      });
      setError("");
      setIsInsightsMode(true); // Set insights mode
    } catch (error) {
      console.error("Error fetching insights:", error);
      setError("Error fetching insights. Please try again.");
    } finally {
      setIsSending(false);
      setLoadingBotMessage(false);
    }
  };
  const handleDeleteAllChats = async () => {
    try {
      await axios.delete(`${ConfigData.API_URL}/aiassist/delete_all`);
      setHistory([]);
    } catch (error) {
      console.error("Error deleting all chats:", error);
      setError("Error deleting all chats. Please try again.");
    }
  };
  const addMessage = (message) => {
    setMessageList((prevMessages) => [...prevMessages, message]);
  };
  const handleHomeClick = () => {
    setMessageList([]);
    setActiveConversation(null);
    setIsLeftSideVisible(false);
  };
  const processText = (text) => {
    if (typeof text !== "string") {
      return "Sorry, there was an error processing your request.";
    }
    return text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
  };
  const scrollToBottom = () => {
    if (chatHistoryEndRef.current) {
      chatHistoryEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
    setShowScrollDownIcon(false);
  };
  const copyToClipboard = (text, index) => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        setCopyStatus((prevStatus) => ({
          ...prevStatus,
          [index]: "tick",
        }));
        setTimeout(() => {
          setCopyStatus((prevStatus) => ({
            ...prevStatus,
            [index]: "copy",
          }));
        }, 1000);
      })
      .catch((err) => {
        console.error("Failed to copy text: ", err);
      });
  };
  return (
    <Card className={dataLoading ? "card-loader" : ""}>
      {dataLoading ? (
        <Loader />
      ) : (
        <Grid container spacing={2} className="main-content font">
          {isMobileView && !isLeftSideVisible && (
            <img
              className="toggle-button"
              src="../images/hamburger.png"
              alt="Show Left Side"
              onClick={toggleSidebar}
            />
          )}
          <Grid
            item
            xs={isMobileView ? (isLeftSideVisible ? 8 : 12) : 2}
            className={`left-side ${
              isMobileView && !isLeftSideVisible ? "hidden" : ""
            }`}
            ref={leftSideRef}
          >
            <div className={`chatList ${
                  themes === "light" ? "light-chatls" : ""
                }`}>
              <div className="response">
                <div className="response flex">
                  <div className="image1 title0">
                    <div className="flex1" onClick={handleHomeClick}>
                      <img
                        src="../images/call-center.png"
                        className="log"
                        alt="Help"
                      />
                      {topics.map((topic, index) => (
                        <span key={index}>{topic}</span>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="title11">
                  <p className="lit">Featured Assists</p>
                  {featuredPrompts.map((prompt) => (
                    <p
                      key={prompt.Sequence}
                      onClick={() => handleInsightsRequest(prompt)}
                    >
                      {prompt.Display_Name}
                    </p>
                  ))}
                  <hr />
                </div>
              </div>
              <div className="response recent-chats">
                <div className="recent-chats-header">
                  <span className="title">Recent Chats</span>
                  <div
                    className={`delete-all-icon custom-scroll ${
                      themes === "light" ? "light-del" : ""
                    }`}
                    onClick={handleDeleteAllChats}
                  >
                    <img src="/images/delete (1).png" className="logs" />
                  </div>
                </div>
                <ul className="chat-list custom-scroll">
                  {history.map((conversation, index) => (
                    <li
                      key={index}
                      onClick={() => handleConversationClick(conversation)}
                    >
                      {conversation.Name || "Unnamed Conversation"}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </Grid>
          <div
            className={`overlay ${isLeftSideVisible ? "visible" : ""}`}
            onClick={toggleSidebar}
          ></div>
          <Grid
            item
            xs={isMobileView ? (isLeftSideVisible ? 4 : 12) : 10}
            className={`chat-area ${
              isMobileView && isLeftSideVisible ? "hidden" : ""
            }`}
          >
            <div                 className={`dashboardPage ${
                  themes === "light" ? "light-dash" : ""
                }`}
>
              {messageList.length === 0 && (
                <div className="texts">
                  <div className="logo">
                    <img src="../images/call-center.png" alt="AI" />
                    <span>Chat with your Helpesk data.</span>
                    <span>
                      You may select from the options below to commence your
                      assisted journey
                    </span>
                    <span>with your facility</span>
                  </div>
                  <div                 className={`options font1 wid ${
                  themes === "light" ? "light-dash" : ""
                }`}>
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest("Summary of all open tickets by region")
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="Counselling"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>Summary of all open tickets by region</span>
                    </div>
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest(
                          "Trend of issues by category over last 6 months as a numbered list"
                        )
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="Helpdesk Compliance"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>
                        Trend of issues by category over last 6 months
                      </span>
                    </div>
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest(
                          "How many tickets have breached SLA this year by State?"
                        )
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="CSAT Insights"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>
                        How many tickets have breached SLA this year by State?
                      </span>
                    </div>
                  </div>
                  <div className="options font1 wid">
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest("Sites with highest SLA breaches")
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="Inspections Anomalies"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>Sites with highest SLA breaches</span>
                    </div>
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest(
                          "List of high priority tickets count that are still open by Category"
                        )
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="CSAT Insights"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>
                        List of high priority tickets that are still open
                      </span>
                    </div>
                    <div
                      className="option"
                      onClick={() =>
                        handleRequest(
                          "How do different sites compare in terms of ticket volume and resolution times? "
                        )
                      }
                    >
                      <img
                        src="../images/document.png"
                        alt="Inspections Anomalies"
                        className={`img12 ${
                          themes === "light" ? "light-img" : ""
                        }`}
                      />
                      <span>Ticket Volume and Resolution Time by site</span>
                    </div>
                  </div>
                </div>
              )}
              {Array.isArray(messageList) && messageList.length > 0 && (
                <div
                  className={`chat-history custom-scroll recent-chats1 ${
                    themes === "light" ? "light-chat" : ""
                  }`}
                  ref={chatHistoryRef}
                >
                  {messageList.map((message, index) => (
                    <div
                      key={index}
                      className={`message-wrapper ${
                        message.type === "user" ? "user-message" : "bot-message"
                      }`}
                    >
                      {message.type === "bot" && message.chart_data && (
                        <>
                          {Array.isArray(message.chart_data?.x) && message.chart_data.x.length > 0 &&
                          Array.isArray(message.chart_data?.y) && message.chart_data.y.length > 0 ? (
                            <PlotlyChart data={message.chart_data} />
                          ) : (
                            <div></div>
                          )}
                        </>
                      )}
                      {message.type === "bot" && (
                        <div className="bot-message-content">
                          <img
                            src="../images/AI Icon.svg"
                            alt="Bot"
                            className={`bot-icon ${
                              themes === "light" ? "light-ico" : ""
                            }`}
                          />
                          <pre
                            className={`message bot-message1 ${
                              themes === "light" ? "light-bot" : ""
                            }`}
          
                            dangerouslySetInnerHTML={{ __html: message.text }}
                            style={{
                              whiteSpace: "pre-wrap",
                              wordWrap: "break-word",
                            }}
                          />
                        </div>
                      )}
                      {message.type === "user" && (
                        <pre
                          className={`message user-message1`}
                          dangerouslySetInnerHTML={{ __html: message.text }}
                          style={{
                            whiteSpace: "pre-wrap",
                            wordWrap: "break-word",
                          }}
                        />
                      )}
                      {message.type === "bot" && (
                        <button
                        className={`copy-icon ${
                          themes === "light" ? "light-copy" : ""
                        }`}
                          onClick={() => copyToClipboard(message.text, index)}
                        >
                          <img
                            src={`../images/${
                              copyStatus[index] === "tick"
                                ? "check-mark.png"
                                : "copy.png"
                            }`}
                            alt={
                              copyStatus[index] === "tick" ? "Copied" : "Copy"
                            }
                            className={`img ${
                              themes === "light" ? "light-img" : ""
                            }`}    
                          />
                          <img src="./images/dont-like.png"                         className={`img ${
                          themes === "light" ? "light-img" : ""
                        }`}
 />
                        </button>
                      )}
                    </div>
                  ))}
                  {loadingBotMessage && (
                    <pre className="message bot-message">
                      <span className="blinking"></span>
                    </pre>
                  )}
                  {error && <p className="error-message">{error}</p>}
                  <div ref={chatHistoryEndRef} />
                </div>
              )}
              {showScrollDownIcon && (
                <div className="scroll-down-icon" onClick={scrollToBottom}>
                  <img
                    src="../images/circle-button.png"
                    alt="Scroll Down"
                    className="logs1"
                  />
                </div>
              )}
              <div className="formContainer">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    isSending ? handleStop() : handleSubmit(inputValue);
                  }}
                >
                  <input
                    type="text"
                    placeholder="Ask me anything..."
                    className="font1"
                    value={inputValue}
                    style={{ fontFamily: 'Mulish, sans-serif',fontSize:'16px'
                     }}
                    onChange={(e) => setInputValue(e.target.value)}
                  />
                  {/* <div className="provider-selection">
              <select id="provider-select" value={provider} onChange={handleProviderChange} disabled={loading} className="provider-selection">
                <option value="Groq">Groq</option>
                <option value="AWS">AWS</option>
              </select>
              {loading && <p>Switching provider...</p>}
            </div> */}
                  <button type="submit">
                    <img
                      src={
                        isSending
                          ? "../images/stop-button.png"
                          : "../images/send-button.png"
                      }
                      alt={isSending ? "Pause" : "Send"}
                    />
                  </button>
                </form>
              </div>
              <div className="disc">
                <p>Helix AI Assist can make mistakes. Check Important info</p>
              </div>
            </div>
          </Grid>
        </Grid>
      )}
    </Card>
  );
};
export default ChatBot;


