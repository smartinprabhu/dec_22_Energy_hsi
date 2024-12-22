/* eslint-disable max-len */
/* eslint-disable prefer-destructuring */
/* eslint-disable radix */
import React from 'react';


export function detectMob() {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    return (((window.innerWidth <= 800) && (window.innerHeight <= 600)) || (isMobile));
}

export function convertPXToVW(px, ph, deValue) {
    console.log(px);
    console.log(ph);
  const w = (px / document.documentElement.clientWidth) * 100;
  const h = (ph / document.documentElement.clientHeight) * 100;
  let vw = w * (100 / document.documentElement.clientWidth);
  const vh = h * (100 / document.documentElement.clientHeight);
  let respMobPx = 3.3;
  if (deValue) {
    respMobPx -= (deValue + 2.4);
    if (vw > deValue) {
      vw -= deValue;
    }
  }
  const isMob = detectMob();
  return isMob ? `calc(${deValue ? '13' : '14'}px + ${respMobPx}vw)` : `${vw}vw`;// `calc(${vw}vw + ${vh}vh)`;
}
