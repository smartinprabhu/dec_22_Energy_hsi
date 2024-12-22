import React from 'react';
import { Box, BoxProps } from '@mui/material';

interface CustomCardContentProps extends BoxProps {
  children: React.ReactNode;
}

const CustomCardContent: React.FC<CustomCardContentProps> = ({ children, ...props }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
      }}
      {...props}
    >
      {children}
    </Box>
  );
};

export default CustomCardContent;
