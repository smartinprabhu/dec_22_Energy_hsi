import React from "react";
import { FormControl, FormControlLabel, RadioGroup, Radio, Select, MenuItem } from "@mui/material";
import { styled } from "@mui/material/styles";

interface PlotTypeSelectorProps {
  plotType: string;
  handlePlotTypeChange: (event: React.ChangeEvent<{ value: unknown }>) => void;
  isDropdown: boolean;
}

// Custom styled radio button
const CustomRadio = styled(Radio)({
  color: "white",
  "&.Mui-checked": {
    color: "white",
  },
});

// Custom styled FormControlLabel
const CustomFormControlLabel = styled(FormControlLabel)(({ theme }) => ({
  color: "white",
  textTransform: "uppercase",
  // fontSize: "17px",
  "& .MuiFormControlLabel-label": {
    color: "white",
    fontFamily: "Mulish",
  },
}));

const PlotSelector: React.FC<PlotTypeSelectorProps> = ({ plotType, handlePlotTypeChange, isDropdown }) => {
  const plotTypes = ["Today", "Week", "Month", "Year"];

  return isDropdown ? (
    <FormControl variant="outlined" size="small">
      <Select
        value={plotType}
        onChange={handlePlotTypeChange}
        displayEmpty
        inputProps={{ "aria-label": "Plot Type" }}
        style={{ color: "white" }} // Add this to change the Select text color
      >
        {plotTypes.map((type) => (
          <MenuItem key={type} value={type}>
            {type}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  ) : (
    <FormControl component="fieldset">
      <RadioGroup
        row
        aria-label="plot-type"
        name="plot-type"
        value={plotType}
        onChange={handlePlotTypeChange}
      >
        {plotTypes.map((type) => (
          <CustomFormControlLabel
            key={type}
            value={type}
            control={<CustomRadio />}
            label={type}
          />
        ))}
      </RadioGroup>
    </FormControl>
  );
};

export default PlotSelector;
