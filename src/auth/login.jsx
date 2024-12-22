import React, { useState, useEffect } from 'react';
import { Formik, Form } from 'formik';
import * as PropTypes from 'prop-types';
import { Cookies } from 'react-cookie';
import { Box, Button } from '@mui/material';
import axios from "axios";

import LoginInputField from './formfields/loginInputField.jsx';
import PageLoader from "./pageLoader";

import mailIcon from './images/mailIcon.svg';
import passwordIcon from './images/passwordIcon.svg';
import companyLoginLogo from './images/companyLoginLogo.png';

import loginModel from './formModel/loginFormModel';
import loginSchema from './formModel/loginSchema';
import initialValues from './formModel/loginInitialValue';
import AuthService from './utils/authService';
import AppConfig from './config.js';
import { getMaxLenghtForFields } from './utils/utils';
import LoginBackground from "./loginBackground";
import { detectMob } from '../utils/appUtils.jsx';

const authService = AuthService();

const Login = (props) => {
  const {
    redirectLink,
    accountIdLoginInfo,
  } = props;
  const { formId, formField } = loginModel;

  // const [username, setUsername] = useState('');
  // const [password, setPassword] = useState('');
  const [endpoints, setEndpoints] = useState(false);
  const [traditionalLoginTrue, setTraditionalLogin] = useState(false);
  const [loginData, setLoginData] = useState({ loading: false, data: null, err: null });

  const WEBAPPAPIURL =  `${AppConfig.API_URL}/api/`;

  const cookies = new Cookies();

  const isMob = detectMob();


  function login(credentials, redirectLink) {
    const data = new FormData();
    const authData = authService.getCredentials();
  
    setLoginData({
      loading: true, data: null, err: null,
    });
  
    data.append('grant_type', 'password');
    data.append('client_id', authData.client_id);
    data.append('client_secret', authData.client_secret);
    data.append('username', credentials.userName);
    data.append('password', credentials.password);
  
    const config = {
      method: 'post',
      url: `${WEBAPPAPIURL}authentication/oauth2/token`,
      data,
      withCredentials: false,
      headers: { endpoint: window.localStorage.getItem('api-url') },
    };
  
    axios(config)
      .then((response) => {
        authService.setToken(response.data);
        setLoginData({
          loading: false, data: response.data, err: null,
        });
      })
      .catch((error) => {
        let errorMessage = 'Something went wrong..';
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = 'Wrong username or password';
          } else if (error.response.data && error.response.data.message) {
            errorMessage = error.response.data.message;
          }
        }
        setLoginData({
          loading: false, data: null, err: { message: errorMessage },
        });
      });
  }
  


  // const history = useHistory();
  const errTxt = 'Something went wrong..';
  const maxLengthValues = getMaxLenghtForFields();
  // Un comment this while using registration process

  // const handleSignUp = () => {
  //   dispatch(resetRegistration());
  //   history.push('/registration');
  //   window.location.reload();
  // };

  useEffect(() => {
    if (!authService.getAccessToken()) {
      cookies.set('sessionExpiry', '0', {
        path: '/', secure: true, sameSite: 'strict',
      });
    }
  }, []);

  useEffect(() => {
    if (loginData && loginData.data) {
      cookies.set('sessionExpiry', '1', {
        path: '/', secure: true, sameSite: 'strict',
      });
      window.location.href = redirectLink || '/';
    }
  }, [loginData]);

 
  const handleLoginCredentialsChange = (event) => {
    loginData.err = {};
    /* if (event.target.name === 'username') {
      setUsername(event.target.value);
    } else {
      setPassword(event.target.value);
    } */
  };

  const redirectToResetPassword = () => {
   // history.push({ pathname: '/forgot-password' });
    // window.location.reload();
  };

  const handleSwitchAccount = () => {
    authService.clearCredentials();
    window.location.pathname = '/';
  };

  const handleSubmit = (values, endpoint) => {
    let data = {
      userName: values.username,
      password: values.password,
      accountId: cookies.get('accountId'),
      client_id: endpoint.client_id,
      client_secret: endpoint.client_secret,
    };
   login(data, redirectLink);
  };


  useEffect(() => {
    if (accountIdLoginInfo && accountIdLoginInfo.data && accountIdLoginInfo.data.data && accountIdLoginInfo.data.data.endpoints && accountIdLoginInfo.data.data.endpoints.length) {
      setEndpoints(accountIdLoginInfo.data.data.endpoints);
    }
  }, [accountIdLoginInfo]);

  useEffect(() => {
    if (accountIdLoginInfo && accountIdLoginInfo.data && accountIdLoginInfo.data.data) {
      window.localStorage.setItem('api-url', accountIdLoginInfo.data.data.endpoint || accountIdLoginInfo.data.data.domain);
      authService.setCredentials(accountIdLoginInfo.data.data);
    }
  }, [accountIdLoginInfo, traditionalLoginTrue]);

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        color: '#0789B5',
        backgroundColor: '#B9EAFE',
        top: '0px',
        left: '0px',
      }}
    >
      {!isMob && (
      <LoginBackground />
      )}
      <Box
        sx={{
          width: isMob ? "100%" : "50%",
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Box
          sx={{
            width: isMob ? "100%" : "55%",
            background: '#fff',
            padding: '50px'
          }}
        >
          <img
            src={companyLoginLogo}
            alt="logo"
            className="company-login-logo"
          />
          <div>
            <h1 className="login-text pb-0 mb-0 mt-4">Welcome Back!</h1>
            <p className="login-description pt-0 mt-0 mb-3">Please sign in to your account.</p>
          </div>
          {endpoints && endpoints.length && endpoints.map((endpoint) => (
            <>
              {endpoint.type === 'Traditional' ? (
                <>
                  <Formik
                    initialValues={initialValues}
                    validationSchema={loginSchema}
                    onSubmit={(values) => handleSubmit(values, endpoint)}
                    validateOnBlur={false}
                    validateOnChange={false}
                  >
                    {(props) => (
                      <Form onSubmit={props.handleSubmit} onChange={handleLoginCredentialsChange} id={formId} className="pt-2">
                        <LoginInputField
                          name={formField.username.name}
                          type="text"
                          label={formField.username.label}
                          maxLength={maxLengthValues.username}
                          placeholder="Enter Username or Email"
                          fieldIcon={mailIcon}
                          labelClassName="text-black"
                        />
                        <LoginInputField
                          name={formField.password.name}
                          autoComplete="new-password"
                          type="password"
                          label={formField.password.label}
                          maxLength={maxLengthValues.password}
                          placeholder="Enter Password"
                          fieldIcon={passwordIcon}
                          labelClassName="text-black"
                        />
                        <Box
                          sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            width: '100%',
                          }}
                        >
                          <p aria-hidden onClick={redirectToResetPassword} className="switch-text mt-2">
                            Forgot password?
                          </p>
                          <p aria-hidden onClick={handleSwitchAccount} className="switch-text mt-2">
                            Switch Account
                          </p>
                        </Box>
                        <Button
                          type="submit"
                          onClick={() => setTraditionalLogin(true)}
                          disabled={(loginData && loginData.loading)}
                          sx={{
                            width: '100%',
                            height: '50px',
                            background: '#00A4DC 0% 0% no-repeat padding-box',
                            borderRadius: '4px',
                            color: '#ffffff',
                            textTransform: 'capitalize',
                            fontSize: '18px',
                            '&:hover': {
                              backgroundColor: '#00A4DC',
                            },
                            fontFamily: 'Suisse Intl'
                          }}
                        >
                          Login
                        </Button>
                      </Form>
                    )}
                  </Formik>
                  {loginData && loginData.err && loginData.err.message && (
            <div className="error-msg text-center">
              {loginData.err.message}
            </div>
          )}
                </>
              ) : ''}
              
            </>
          ))}
          {loginData && loginData.err && loginData.err.data && loginData.err.data.message && loginData.err.data.message === "'NoneType' object has no attribute 'strip'" && (
            <div className="error-msg text-center">
              Your AccountId does not have valid credentials to Login, please try with other AccountId.
            </div>
          )}
          {loginData && loginData.err && loginData.err.data && loginData.err.data.message && (
            <div className="error-msg text-center">
              {loginData.err.data.message}
            </div>
          )}
          {loginData && loginData.err && loginData.err.data && !loginData.err.data.message && (
            <div className="error-msg text-center">
              {errTxt}
            </div>
          )}
          {(loginData && loginData.loading && (
            <PageLoader />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

Login.defaultProps = {
  redirectLink: false,
};

Login.propTypes = {
  redirectLink: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
};

export default Login;

