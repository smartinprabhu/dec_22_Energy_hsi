import { Cookies } from 'react-cookie';

import AuthService from './utils/authService';
import {
  loginSuccess, loginFailure, logoutSuccess, logIn,
 accountIdLogIn, accountIdLoginSuccess, accountIdLoginFailure,
} from './authActions';
import { convertToUppercase } from './utils/utils';

const axios = require('axios');
const FormData = require('form-data');

const authService = AuthService();
const cookies = new Cookies();
const WEBAPPAPIURL = `${appConfig.WEBAPIURL}/api/`;


export const login = (credentials, redirectLink) => (dispatch) => {
    const data = new FormData();
    const authData = authService.getCredentials();

    dispatch(logIn());
    data.append('grant_type', 'password');
    data.append('client_id', authData.client_id);
    data.append('client_secret', authData.client_secret);
    data.append('username', credentials.userName);
    data.append('password', credentials.password);

    const config = {
      method: 'post',
      url: `${WEBAPPAPIURL}authentication/oauth2/token`,
      data,
      withCredentials: true,
      headers: { endpoint: window.localStorage.getItem('api-url') },
    };

    axios(config)
      .then((response) => {
        authService.setToken(response.data);
        dispatch(loginSuccess(response));
        /* if (!redirectLink) {
          window.location.href = '/';
        } else {
          window.location.href = redirectLink;
        } */
      })
      .catch((error) => {
        dispatch(loginFailure(error));
      });
};

export const logout = () => (dispatch) => {
    authService.clearToken();
    dispatch(logoutSuccess());
    if (!authService.getAccessToken()) {
      window.location.reload();
    }
};

export const dynamicLogin = (values) => (dispatch) => {
  const URL = `${WEBAPPAPIURL}authProviders/getByAccountId?account_id=${convertToUppercase(values.accountId)}`;
  const config = {
    method: 'get',
    url: URL,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  };
  dispatch(accountIdLogIn());
  axios(config)
    .then((response) => {
      dispatch(accountIdLoginSuccess(response));
    }).catch((error) => {
      dispatch(accountIdLoginFailure(error));
    });
};
