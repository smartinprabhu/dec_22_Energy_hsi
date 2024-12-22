import React, { useState, useEffect, lazy, Suspense } from 'react';

const PortraitComponent = lazy(() => import('./AirPortrait'));
const LandscapeComponent = lazy(() => import('../AirIndex1/AirLandscape'));

const ResponsiveContainer = () => {
  const [isPortrait, setIsPortrait] = useState(window.matchMedia("(orientation: portrait)").matches);

  useEffect(() => {
    const updateOrientation = (e) => {
      setIsPortrait(e.matches);
    };

    const mediaQuery = window.matchMedia("(orientation: portrait)");
    mediaQuery.addEventListener('change', updateOrientation);

    // Clean up the event listener when the component is unmounted
    return () => {
      mediaQuery.removeEventListener('change', updateOrientation);
    };
  }, []);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      {isPortrait ? <PortraitComponent /> : <LandscapeComponent />}
    </Suspense>
  );
};

export default ResponsiveContainer;
