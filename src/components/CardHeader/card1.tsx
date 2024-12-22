import React, { useState, useEffect, useCallback } from "react";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import "./CardHeader.css";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import { FormControl, RadioGroup, Radio, FormControlLabel } from "@mui/material";
import { styled } from "@mui/material/styles";

const CustomRadio = styled(Radio)({
  color: "white",
  "&.Mui-checked": {
    color: "white",
  },
});

const CustomFormControlLabel = styled(FormControlLabel)(({ theme }) => ({
  color: "white",
  textTransform: "uppercase",
  "& .MuiFormControlLabel-label": {
    color: "white",
    fontFamily: "Mulish",
  },
}));

const CardHeader = (props) => {
  const {
    children,
    headerText,
    subHeader,
    showMiddleBox = false,
    showToggle = false,
    onInputValueChange,
    onLoadUpdate,
    onOptionChange,
    initialSelectedOption, // New prop to initialize the selected option
    staticInputValue, // New prop to store the static input value
    className
  } = props;

  const [selectedOption, setSelectedOption] = useState<"Dynamic" | "Static">(initialSelectedOption);
  const [inputValue, setInputValue] = useState<string>(staticInputValue || "");
  const [isEditing, setIsEditing] = useState(false);
  const [infoDialogOpen, setInfoDialogOpen] = useState(false);
  const [showInfoIcon, setShowInfoIcon] = useState(true);

  useEffect(() => {
    setSelectedOption(initialSelectedOption);
    setInputValue(staticInputValue || "");
  }, [initialSelectedOption, staticInputValue]);

  const handleOptionChange = useCallback((event) => {
    const newOption = event.target.value as "Dynamic" | "Static";
    setSelectedOption(newOption);
    setInputValue(newOption === "Dynamic" ? staticInputValue || "" : "");
    setIsEditing(false);
    onInputValueChange("");
    onOptionChange(newOption);
  }, [onInputValueChange, onOptionChange, staticInputValue]);

  const handleInputChange = useCallback((event) => {
    const value = event.target.value;
    setInputValue(value);
    setIsEditing(true);
    onInputValueChange(value);
  }, [onInputValueChange]);

  const handleLoadData = useCallback(() => {
    if (inputValue.trim() === "") return;
    setIsEditing(false);
    onLoadUpdate(inputValue);
    setShowInfoIcon(false);
  }, [inputValue, onLoadUpdate]);

  const handleInfoIconClick = useCallback(() => {
    setInfoDialogOpen(true);
  }, []);

  return (
    <div className="card-header-box-responsive1">
      <div className="card-header-inner-box-responsive">
        <h1 className="header-box-title-responsive">
          {headerText} <span className="card-value-responsive">{subHeader}</span>
        </h1>
      </div>

      {showMiddleBox && (
        <div className="card-header-middle-box-responsive">
          <span
            className="card-header-middle-text-responsive"
            style={{
              fontFamily: "Mulish, sans-serif",
              fontSize: "17px",
              color: "white",
              marginRight: "1px",
            }}
          >
            Area: 100000 Sq.ft
          </span>
          <span
            className="card-header-middle-text-responsive"
            style={{
              fontFamily: "Mulish, sans-serif",
              fontSize: "17px",
              color: "white",
              marginLeft: "38px",
            }}
          >
            Occupancy: 5000
          </span>
        </div>
      )}

      {showToggle && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "5px",
            marginTop: "10px",
          }}
        >
          <span className="tog1">Target Setting:</span>

          <FormControl component="fieldset">
            <RadioGroup
              row
              aria-label="target-setting"
              name="target-setting"
              value={selectedOption}
              onChange={handleOptionChange}
            >
              <CustomFormControlLabel
                value="Dynamic"
                control={<CustomRadio />}
                label="Dynamic"
              />
              <CustomFormControlLabel
                value="Static"
                control={<CustomRadio />}
                label="Linear"
              />
            </RadioGroup>
          </FormControl>

          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            style={{
              width: "60px",
              padding: "5px",
              border: "1px solid #ccc",
              borderRadius: "4px",
              fontFamily: "Mulish",
            }}
          />
          <span className="tog">{selectedOption === "Static" ? "kWh" : "%"}</span>
          {showInfoIcon && (
            <InfoOutlinedIcon
              onClick={handleInfoIconClick}
              style={{
                marginLeft: "10px",
                cursor: "pointer",
                color: "white",
              }}
            />
          )}
        </div>
      )}

      {isEditing && (
        <div
          style={{
            display: "flex",
            gap: "10px",
          }}
        >
          <Button
            variant="contained"
            color="primary"
            style={{ fontFamily: "Mulish" }}
            onClick={handleLoadData}
          >
            OK
          </Button>
          <Button
            variant="contained"
            color="secondary"
            style={{ fontFamily: "Mulish" }}
            onClick={() => {
              setInputValue("");
              setIsEditing(false);
            }}
          >
            Discard
          </Button>
        </div>
      )}

      <div>{children}</div>

      <Dialog open={infoDialogOpen} onClose={() => setInfoDialogOpen(false)}>
        <DialogTitle className="dailoge">Target</DialogTitle>
        <DialogContent className="dailoge1">
          <p>
            <b>Linear:</b> This target progresses in a straight line, moving steadily toward a defined endpoint. Adjust inputs to maintain a consistent flow and achieve the goal.
          </p>
          <p>
            <b>Dynamic:</b> This target adapts to real-time factors to stay aligned with shifting goals. Factors such as operating hours, temperature, seasonality, etc.
          </p>
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setInfoDialogOpen(false)} color="primary" className="dailoge">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default CardHeader;
