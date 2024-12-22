/* eslint-disable no-console */
/* eslint-disable react/prop-types */
import React, { useEffect } from 'react';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { Cookies } from 'react-cookie';

import AuthService from '../util/authService';
import {
  loginSuccess,
} from './authActions';

const appConfig = require('../config/appConfig').default;

const authService = AuthService();

const JumpLogin = () => {
  const dispatch = useDispatch();
  const cookies = new Cookies();

  const WEBAPPAPIURL = `${appConfig.WEBAPIURL}/`;

  const clearData = () => {
    const config = {
      method: 'get',
      url: `${WEBAPPAPIURL}clearjumpresult`,
    };

    axios(config)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const clearData1 = () => {
    const config = {
      method: 'get',
      url: `${WEBAPPAPIURL}clearsessionresult`,
    };

    axios(config)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const viewData = () => {
    const config = {
      method: 'get',
      url: `${WEBAPPAPIURL}getjumpresult`,
    };

    axios(config)
      .then((response) => {
        if (response.data && response.data && response.data.access_token) {
          clearData();
          authService.setToken(response.data);
          cookies.remove('sessionExpiry', { path: '/' });
          cookies.set('sessionExpiry', '1', {
            path: '/', secure: true, sameSite: 'strict',
          });
          dispatch(loginSuccess(response));
          window.location.pathname = '/';
        } else {
          window.location.pathname = '/';
        }
      })
      .catch((error) => {
        console.log(error);
        window.location.pathname = '/';
      });
  };

  const sessionData = () => {
    const config = {
      method: 'get',
      url: `${WEBAPPAPIURL}getsessionresult`,
    };

    axios(config)
      .then((response) => {
        if (response.data && response.data && response.data.session_value) {
          clearData1();
          const myArray = response.data.session_value.split('=');
          const wordSession = myArray[1];
          const myArray1 = wordSession.split(' ');
          const wordSession1 = myArray1[0];
          const fsees = wordSession1.slice(0, wordSession1.length - 1);
          cookies.set('Session', fsees, { path: '/', secure: true, sameSite: 'strict' });
          // dispatch(loginSuccess(response));
          // window.location.pathname = '/';
        } else {
          // window.location.pathname = '/';
        }
      })
      .catch((error) => {
        console.log(error);
        // window.location.pathname = '/';
      });
  };

  useEffect(() => {
    viewData();
    sessionData();
  }, []);

  return (
    <div role="alert" className="p-3 text-center">
      <p>Loading ...</p>
    </div>
  );
};

export default JumpLogin;
