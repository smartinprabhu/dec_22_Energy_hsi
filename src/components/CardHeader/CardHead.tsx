import React, { useState, useEffect } from "react";
import "./CardHeader.css";
import { ChildrenProps } from "./types";

const CardHeader = (props: ChildrenProps) => {
  const {
    children,
    headerText,
    filter = true,
    subHeader,
    expand = false,
    setDialog,
    filterText,
    handleFilter,
    activeGroupFilter,
    height, 
    width,
    showMiddleBox = false,
    imageSrc,
    imageAlt = "Card header image"
  } = props;

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(new Date()); // Initialize with current date and time
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  // Function to handle refresh manually
  const handleRefresh = () => {
    setLastUpdated(new Date());
  };

  // Function to calculate how many minutes ago the last update was
  const getMinutesAgo = () => {
    if (!lastUpdated) return null;
    const now = new Date();
    const diff = Math.floor((now.getTime() - lastUpdated.getTime()) / 1000 / 60); // Difference in minutes
    return diff === 0 ? "Just now" : `${diff} minute(s) ago`;
  };

  // useEffect to set up the interval for auto-refresh
  useEffect(() => {
    const intervalId = setInterval(() => {
      setLastUpdated(new Date());
    }, 5 * 60 * 1000); // Refresh every 5 minutes

    // Cleanup interval on component unmount
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  return (
    <div className="card-header-box-responsive">
      <div className="card-header-inner-box-responsive">
        {/* Add image */}
        {imageSrc && (
          <img
            src={imageSrc}
            alt={imageAlt}
            className="card-header-image"
            style={{ width: "40px", height: "100px", marginRight: "10px" }}
          />
        )}
        <h1 className="header-box-title-responsive">
          {headerText}
          <span className="card-value-responsive">{subHeader}</span>
        </h1>
      </div>
      <div>{children}</div>

      {/* Refresh button and last updated time */}
      <div style={{ marginTop: "0px", textAlign: "right" }}>
        {lastUpdated && (
          <span style={{ marginLeft: "10px", fontSize: "14px", color: "#888" }}>
            Last updated: {getMinutesAgo()}
          </span>
        )}
        <button onClick={handleRefresh} className="refresh-button">
          <img src="../images/Refresh ccw.svg" alt="Refresh" />
        </button>
      </div>
    </div>
  );
};

export default CardHeader;
