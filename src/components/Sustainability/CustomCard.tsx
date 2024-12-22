import React from 'react';
import { Box, BoxProps } from '@mui/material';
import { useTheme } from "../ThemeContext";

interface CustomCardProps extends BoxProps {
  children: React.ReactNode;
}

  const CustomCard = ({ children, sx }) => {
    const { themes } = useTheme();

    return (
      <Box  sx={{ backgroundColor: themes === "dark" ? '#2E2E2E' :"white", color: themes === "dark" ? 'white' : 'black', borderRadius: '8px', padding: '10px', boxSizing: 'border-box', boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', height: '100%', width: '100%', '@media (max-width: 576px)': { width: '96%', marginLeft: '5px', marginBottom: '-26px', }, }}>
        {children}
      </Box>
    );
  };

export default CustomCard;
