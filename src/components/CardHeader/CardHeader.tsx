import {
  MdDragIndicator,
  MdDateRange,
  MdOutlineOpenInFull,
  MdOutlineClose,
} from "react-icons/md";
import "./CardHeader.css";
import { ChildrenProps } from "./types";
import { Menu, MenuItem } from "@mui/material";
import { useState } from "react";
import { headerGroupFilterOptions } from "../../appData/appData";
import customData from './customData.json';
import React from "react";

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
  } = props;

  // const [activeGroupFilter, setActiveGroupFilter] = useState<string>(
  //   filter ? (filterText ? filterText : "7 Days") : ""
  // );

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  // const handleFilter = (filter: string) => {
  //   setActiveGroupFilter(filter);
  // };


  return (
    <div className={`${expand ? "card-header-box-expand" : "card-header-box"}`}>
      <div className="card-header-inner-box">
        {!expand && (
          <MdDragIndicator color="#FFFFFF" cursor="pointer" size={20} />
        )}
        <h1
          className={`${
            expand ? "header-box-title-expand" : "header-box-title"
          }`}
        >
          {headerText}{" "}
          <span className={expand ? "card-value-expand" : "legend-value"}>
            {subHeader}
          </span>{" "}
        </h1>
      </div>
      <div>{children}</div>
      <div className="card-header-inner-box">
        <p
          className={`${expand ? "card-value-date-expand" : "card-value-date"}`}
        >
          {/* {filter ? (filterText ? filterText : "7 Days") : null} */}
          {customData && customData.dateFiltersText && activeGroupFilter && customData.dateFiltersText[activeGroupFilter] ? customData.dateFiltersText[activeGroupFilter] : ''}
        </p>

        <MdDateRange
          onClick={handleClick}
          color="#FFFFFF"
          cursor="pointer"
          size={expand ? 30 : 15}
        />
        <Menu
          id="basic-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          MenuListProps={{
            "aria-labelledby": "basic-button",
          }}
          sx={{
            "& .MuiPaper-root": {
              backgroundColor: "#3E3E3E",
            },
          }}
        >
          {headerGroupFilterOptions.map((eachOption) => (
            <MenuItem
              sx={{
                font: "normal normal normal 12px Mulish",
                color: "#ffffff",
              }}
              key={eachOption.id}
              onClick={() => {
                handleFilter?.(eachOption.displayText);
                handleClose();
              }}
            >
              {eachOption.displayText}
            </MenuItem>
          ))}
        </Menu>

        {expand ? (
          <MdOutlineClose
            onClick={() => {
              setDialog?.(false);
            }}
            color="#FFFFFFAB"
            cursor="pointer"
            size={expand ? 30 : 15}
          />
        ) : (
          <MdOutlineOpenInFull
            onClick={() => {
              setDialog?.(true);
            }}
            color="#FFFFFFAB"
            cursor="pointer"
            size={15}
          />
        )}
      </div>
    </div>
  );
};

export default CardHeader;
