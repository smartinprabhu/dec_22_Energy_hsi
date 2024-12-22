
import React from "react";
import { Box, Typography } from "@mui/material";

import blocksIcon from "./images/blocks.png";
import manIcon from "./images/man.png";

const LoginBackground = () => {

    const LoginHeader = 'GenAI Enabled Insights of your Facility and Assets'

    return (
        <Box sx={{
            width: "50%",
        }}>
            <Typography
                sx={{ position: 'relative', top: '100px', left: '80px', fontFamily:'Suisse Intl',  fontSize:'35px'
            }}
            >
                {LoginHeader}
            </Typography>
            <Box
                sx={{
                    display: "flex",
                }}
            >
                <Box
                    sx={{
                        width: "50%",

                    }}
                >
                    <img
                        src={manIcon}
                        alt="logo"
                        style={{ width: '450px', height: '550px', top: '105px', position: 'relative', zIndex: 10 }}
                    />
                </Box>
                <Box
                    sx={{
                        width: "50%",
                    }}
                >
                    <img
                        src={blocksIcon}
                        alt="logo"
                        style={{ width: '400px', height: '500px', top: '120px', position: 'relative' }}
                    />
                </Box>
            </Box>
        </Box>
    )
}
export default LoginBackground