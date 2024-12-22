/* eslint-disable import/no-unresolved */
/* eslint-disable react/prop-types */
import React from 'react';
import Carousel from 'react-material-ui-carousel';
import HorizontalRuleRoundedIcon from '@mui/icons-material/HorizontalRuleRounded';
import { Paper } from '@mui/material';

import firstImage from '@images/carousel/firstImage.png';
import secondImage from '@images/carousel/secondImage.png';

const Item = (props) => {
  const { src, description } = props;
  return (
    <Paper sx={{ backgroundColor: '#000000', position: 'relative' }}>
      <img src={src} className="login-form-carousel-image-size" alt="" />
      <div className="carousel-text">
        <p
          style={{
            color: 'white',
            fontFamily: 'Suisse Intl',
            fontSize: '28px',
            width: '82%',
          }}
        >
          {description}
        </p>
      </div>
    </Paper>
  );
};

const FormCarousel = () => (
  <Carousel
    sx={{
      height: '100vh',
      position: 'relative',
    }}
    IndicatorIcon={(
      <HorizontalRuleRoundedIcon
        sx={{
          width: '40px',
          height: '60px',
        }}
      />
      )}
    indicatorIconButtonProps={{
      style: {
        fontSize: '50px',
        fontWeight: 'bold',
        color: '#808080',
      },
    }}
    activeIndicatorIconButtonProps={{
      style: {
        color: '#00A4DC',
        width: '60px',
      },
    }}
    indicatorContainerProps={{
      style: {
        textAlign: 'left',
        marginLeft: '30px',
        position: 'absolute',
        top: '90%',
        zIndex: 999,
      },
    }}
  >
    <Item src={firstImage} description="Digital transformation of facilities and property management" />
    <Item src={secondImage} description="Sensor-based smart solutions for Greater facility solutions" />
  </Carousel>
);

export default FormCarousel;
