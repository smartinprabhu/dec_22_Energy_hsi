import React from "react";
import Skeleton from "@mui/material/Skeleton";
import CircularProgress from "@mui/material/CircularProgress";
import styled from "styled-components";

const FullPageSkeleton = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const SkeletonContainer = styled.div`
  position: relative;
  width: 100%;
  height: 100%;
`;

const OverlayProgress = styled.div`
  position: absolute;

  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1001;
`;

const LoadingSkeleton = () => (
  <FullPageSkeleton>
    <SkeletonContainer>
      <Skeleton variant="rectangular" width="100%" height="100%" style={{ opacity: 0.5 }} />
      <OverlayProgress>
        <CircularProgress style={{ color: "#2275e0" }} />
      </OverlayProgress>
    </SkeletonContainer>
  </FullPageSkeleton>
);

export default LoadingSkeleton;
