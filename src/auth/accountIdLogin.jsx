import React, { useEffect, useState } from "react";
import { Formik, Form } from "formik";
import { Cookies } from "react-cookie";
import axios from "axios";

import { Box, Button } from "@mui/material";
import InputCustomField from './formfields/inputCustomField.jsx';

import PageLoader from "./pageLoader";

import initialValues from "./accountIdFormModel/accountIdInitialValues";
import validationSchema from "./accountIdFormModel/accountIdValidationSchema";
import formModel from "./accountIdFormModel/accountIdFormModel";
import Login from "./login";
import AppConfig from './config.js';
import LoginBackground from "./loginBackground";
import { getMaxLenghtForFields, convertToUppercase } from './utils/utils';
import { detectMob } from '../utils/appUtils.jsx';

const cookies = new Cookies();

const DynamicLogin = (props) => {
  const { redirectLink } = props;
  const [error, setError] = useState(false);
  const [login, setLogin] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");
  const [accountIdLoginInfo, setAccountIdLoginInfo] = useState({ loading: false, data: null, err: null });

  const { formId, formFields } = formModel;

  const WEBAPPAPIURL =  `${AppConfig.API_URL}/api/`;

  const isMob = detectMob();

  function dynamicLogin(values){
    if (values) {
      setAccountIdLoginInfo({
        loading: true, data: null, count: 0, err: null,
      });
      const URL = `${WEBAPPAPIURL}authProviders/getByAccountId?account_id=${convertToUppercase(values.accountId)}`;
      const config = {
        method: 'get',
        url: URL,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      };
      axios(config)
        .then((response) => setAccountIdLoginInfo({
          loading: false, data: response.data, count: response.data.length, err: null,
        }))
        .catch((error) => {
          setAccountIdLoginInfo({
            loading: false, data: null, count: 0, err: error,
          });
          setErrorMessage("The account code you entered is incorrect. Please try again.");
        });
    }
  }

  const handleSubmit = (values) => {
    setErrorMessage("");  // Clear any previous error messages
    dynamicLogin(values);
  };

  const cornorLogo =
    accountIdLoginInfo &&
    accountIdLoginInfo.data &&
    accountIdLoginInfo.data.data &&
    accountIdLoginInfo.data.data.logo
      ? accountIdLoginInfo.data.data.logo
      : false;

  useEffect(() => {
    if (
      accountIdLoginInfo &&
      accountIdLoginInfo.data &&
      accountIdLoginInfo.data.data &&
      accountIdLoginInfo.data.data.endpoints &&
      accountIdLoginInfo.data.data.endpoints.length
    ) {
      setLogin(true);
      window.localStorage.setItem("company_logo", cornorLogo);
    }
  }, [accountIdLoginInfo]);

  useEffect(() => {
    if (
      accountIdLoginInfo &&
      accountIdLoginInfo.err &&
      accountIdLoginInfo.err.error &&
      accountIdLoginInfo.err.error.message
    ) {
      setError(accountIdLoginInfo.err.error.message);
      setAttempts(attempts + 1);
      window.localStorage.setItem("company_logo", "");
    }
  }, [accountIdLoginInfo]);

  useEffect(() => {
    if (
      cookies.get("client_id") &&
      cookies.get("client_secret") &&
      cookies.get("accountId")
    ) {
      dynamicLogin({ accountId: cookies.get("accountId") });
    }
  }, []);

  const maxLengthValues = getMaxLenghtForFields();

  return login ? (
    <Login redirectLink={redirectLink} accountIdLoginInfo={accountIdLoginInfo} />
  ) : (
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
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            width: isMob ? "100%" : "55%",
            background: '#fff',
            padding: '50px'
          }}
        >
          
          <div>
            <h1 className="login-text pb-0 mb-0 mt-4">Welcome Back!</h1>
            <p className="login-description pt-0 mt-0 mb-4">Please sign in to your account.</p>
          </div>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ values, setFieldValue }) => (
              <Form id={formId}>
                <div className="accountId-text pt-2"> Enter Account Code*</div>
                <InputCustomField
                  name={formFields.accountId.name}
                  label=""
                  labelClassName="m-0"
                  customWrap
                  type="text"
                  className="input"
                  maxLength={maxLengthValues.accountId}
                  placeholder="Enter Account Code"
                />
                <Button
                  type="submit"
                  disabled={(accountIdLoginInfo && accountIdLoginInfo.loading) || (attempts === 3)}
                  sx={{
                    width: "100%",
                    height: "50px",
                    background: "#00A4DC 0% 0% no-repeat padding-box",
                    borderRadius: "4px",
                    color: "#ffffff",
                    textTransform: "capitalize",
                    fontSize: "18px",
                    margin: "8% 0px 0px 0px",
                    "&:hover": {
                      backgroundColor: "#00A4DC",
                    },
                  }}
                >
                  {error ? "Retry" : "Continue"}
                </Button>
                {errorMessage && (
                  <div className="error-msg" style={{ color: "red", marginTop: "10px" }}>
                    {errorMessage}
                  </div>
                )}

              </Form>
            )}
          </Formik>
          {(accountIdLoginInfo && accountIdLoginInfo.loading && (
            <PageLoader />
          ))}
          {error && attempts < 3 && <div className="error-msg">{error}</div>}
          {attempts === 3 && (
            <div className="error-msg">
              Too many failed attempts try again later
            </div>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default DynamicLogin;

