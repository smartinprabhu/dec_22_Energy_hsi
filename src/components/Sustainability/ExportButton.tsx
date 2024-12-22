import React from 'react';
import { Button } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

const ExportButton = ({ data, filename }) => {
  const handleExportToCSV = () => {
    const csvContent = data
      .map(row => {
        if (Array.isArray(row)) {
          return row.join(",");
        } else if (typeof row === 'object') {
          return Object.values(row).join(",");
        } else {
          return row;
        }
      })
      .join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${filename}.csv`;
    link.click();
  };

  return (
    <Button
      variant="contained"
      color="primary"
      startIcon={<DownloadIcon />}
      onClick={handleExportToCSV}
      sx={{
        margin: '10px 0',
        backgroundColor: '#ff8200',
        color: '#FFFFFF',
        '&:hover': {
          backgroundColor: '#cc6600',
        },
        fontSize: '12px'
      }}
    >
      Export to CSV
    </Button>
  );
};

export default ExportButton;
