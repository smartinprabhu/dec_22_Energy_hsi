import React from 'react';
import { Typography } from '@mui/material';
import { useTheme } from "../ThemeContext";

interface EnergyCardHeaderProps {
  title: string;
}

const EnergyCardHeader: React.FC<EnergyCardHeaderProps> = ({ title }) => {
  const { themes } = useTheme();
  return (
    <Typography
      variant="h5"
      sx={{
        fontFamily: "Mulish",
        fontSize: '17px',
        color: themes === "dark" ? "white" : "black", // Corrected color logic
        paddingTop: '-10px',
      }}
    >
      {title}
    </Typography>
  );
};

export default EnergyCardHeader;
