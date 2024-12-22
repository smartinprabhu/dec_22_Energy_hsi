import React from "react";
import { Handle } from "react-flow-renderer";
import { Link } from "react-router-dom";
import { useTheme } from "../ThemeContext";
import { transition } from "d3";

const CustomNode = ({ data }) => {
  const path = window.location.pathname.split("?")[1];
  const curModule = window.location.hash.split("#")[1];
  const { themes } = useTheme();

  // Combined styles with display: flex
  const combinedStyles = {
    display: "flex",
    flexDirection: "column", // Corrected property name
    alignItems: "center",
    backgroundColor: themes === "dark" ? "#2E2E2E" : "",
    border: themes === "dark" ? "1px solid black" : "1px solid #707070",
    ...data.style, // Assuming data.style is an object
  };

  return (
    <div style={combinedStyles}>
{data.status && (
  <div
    className={`blinking-dot ${
      data.status === "active" ? "green" :
      data.status === "inactive" ? "red" :
      "gray"  // Default to gray when status is not "active" or "inactive"
    }`}
  ></div>
)}
      {/* Render the main energy meter if available */}
      {data.mainEnergyMeter && (
        <div className="flow-in-box1">
          <p>{data.text}</p>
          <div className="in-flow-box">
            <p className="react-flow-description">
              {data.mainEnergyMeter.text}
            </p>
            <img
              className="flow-in-img"
              src={data.mainEnergyMeter.imageUrl}
              alt={data.mainEnergyMeter.text}
            />
          </div>
        </div>
      )}
      {!data.mainEnergyMeter && data.description && (
        <div className="flow-in-box2">
          <p className="font-weight-800">{data.text}</p>
        </div>
      )}

      {/* Render the energy meters if available */}
      {data.energyMeters && data.energyMeters.length > 0 ? (
        <div className="flow-in-box-group">
          {data.energyMeters.map((item) => (
            <div
              key={item.id}
              style={{
                width: "calc(22% - 5px)",
                margin: "5px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textAlign: "center",
                backgroundColor: themes === "dark" ? "#2E2E2E" : "",
                border:
                  themes === "dark" ? "1px solid black" : "1px solid #707070",
                borderRadius: "8px",
                padding: "10px",
                wordBreak: "break-word",
                position: "relative", // For blinking dot positioning
              }}
            >
              <img
                src={item.imageUrl}
                alt={`${item.text} node`}
                style={{ width: "35px", height: "35px" }}
              />
              <div style={{ color: themes === "dark" ? "white" : "black" }}>
                {item.text}
              </div>
              {/* Add blinking dot */}
              {item.status && (
  <div
    className={`blinking-dot ${
      item.status === "active" ? "green" :
      item.status === "inactive" ? "red" :
      "gray"  // Default to gray when status is neither "active" nor "inactive"
    }`}
    style={{
      width: "15px",
      height: "15px",
      position: "absolute",
      top: "-10px",
      left: "50%",
      transform: "translateX(-50%)",
      animation: "blink-animation 1s infinite",
    }}
  ></div>
)}
            </div>
          ))}
        </div>
      ) : data.imageUrl ? (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {data.energyMeter && data.energyMeter.id ? (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textDecoration: "none",
                color: "inherit",
              }}
            >
              <img
                src={data.imageUrl}
                alt={data.text}
                style={{ width: "40px", height: "40px" }}
              />
              <div style={{ color: themes === "dark" ? "white" : "black" }}>
                {data.text}
              </div>
            </div>
          ) : (
            <>
              <img
                src={data.imageUrl}
                alt={data.text}
                style={{ width: "40px", height: "40px" }}
              />
              <div style={{ color: themes === "dark" ? "white" : "black" }}>
                {data.text}
              </div>
            </>
          )}
        </div>
      ) : null}

      {/* Render handles */}
      {data.handlers &&
        data.handlers.map((handler) => (
          <Handle
            key={handler.handle.handleId}
            type={handler.handle.type}
            position={handler.handle.position}
            id={handler.handle.handleId}
            className={handler.handle.className}
          />
        ))}
    </div>
  );
};

export default CustomNode;
