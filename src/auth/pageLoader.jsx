import React from "react";
import * as PropTypes from "prop-types";
import Backdrop from "@mui/material/Backdrop";
// import { Circles } from "react-loader-spinner";
import CircularProgress from "@mui/material/CircularProgress";

const PageLoader = (props) => {
  const { type } = props;
  return (
    <>
      <Backdrop
        sx={{
          color: "#fff",
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
        open={true}
        invisible
      >
        {type === "max" && (
          <div className="home-box">
            <div className="content-inner-box">
              <CircularProgress color="primary" />
            </div>
          </div>
        )}
        {type === "mini" && <CircularProgress color="primary" />}
        {type === "chart" && (
          <div className="data-center">
            <CircularProgress color="primary" />
          </div>
        )}
      </Backdrop>
    </>
  );
};

PageLoader.defaultProps = {
  type: "",
};

PageLoader.propTypes = {
  type: PropTypes.string,
};

export default PageLoader;
