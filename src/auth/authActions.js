export const LOGIN = "LOGIN";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";

export const LOGOUT_SUCCESS = "LOGOUT_SUCCESS";
export const LOGOUT_FAILURE = "LOGOUT_FAILURE";
export const RESET_LOGIN = "RESET_LOGIN";

export const OKTALOGIN = "OKTALOGIN";
export const OKTALOGIN_SUCCESS = "OKTALOGIN_SUCCESS";
export const OKTALOGIN_FAILURE = "OKTALOGIN_FAILURE";

export const MICROSOFTLOGIN = "MICROSOFTLOGIN";
export const MICROSOFTLOGIN_SUCCESS = "MICROSOFTLOGIN_SUCCESS";
export const MICROSOFTLOGIN_FAILURE = "MICROSOFTLOGIN_FAILURE ";

export const ACCOUNT_ID_LOGIN = "ACCOUNT_ID_LOGIN";
export const ACCOUNT_ID_LOGIN_SUCCESS = "ACCOUNT_ID_LOGIN_SUCCESS";
export const ACCOUNT_ID_LOGIN_FAILURE = "ACCOUNT_ID_LOGIN_FAILURE";

export const GOOGLE_CAPTCHA_VERIFY = "GOOGLE_CAPTCHA_VERIFY";
export const GOOGLE_CAPTCHA_VERIFY_SUCCESS = "GOOGLE_CAPTCHA_VERIFY_SUCCESS";
export const GOOGLE_CAPTCHA_VERIFY_FAILURE = "GOOGLE_CAPTCHA_VERIFY_FAILURE";
export const SAVE_PIN_ENABLE_DATA = "SAVE_PIN_ENABLE_DATA";

export function accountIdLogIn(result) {
  return {
    type: ACCOUNT_ID_LOGIN,
    payload: result,
  };
}

export function accountIdLoginSuccess(result) {
  return {
    type: ACCOUNT_ID_LOGIN_SUCCESS,
    payload: result,
  };
}

export function accountIdLoginFailure(result) {
  return {
    type: ACCOUNT_ID_LOGIN_FAILURE,
    payload: result,
  };
}

export function savePinEnable(data) {
  return {
    type: SAVE_PIN_ENABLE_DATA,
    payload: data,
  };
}

export function logIn(result) {
  return {
    type: LOGIN,
    payload: result,
  };
}

export function loginSuccess(result) {
  return {
    type: LOGIN_SUCCESS,
    payload: result,
  };
}

export function loginFailure(result) {
  return {
    type: LOGIN_FAILURE,
    payload: result,
  };
}

export function logoutSuccess() {
  return {
    type: LOGOUT_SUCCESS,
  };
}

export function logoutFailure(result) {
  return {
    type: LOGOUT_FAILURE,
    payload: result,
  };
}

export function resetLogin() {
  return {
    type: RESET_LOGIN,
  };
}

export function oktaLogIn(result) {
  return {
    type: OKTALOGIN,
    payload: result,
  };
}

export function oktaLoginSuccess(result) {
  return {
    type: OKTALOGIN_SUCCESS,
    payload: result,
  };
}

export function oktaLoginFailure(result) {
  return {
    type: OKTALOGIN_FAILURE,
    payload: result,
  };
}
export function microsoftLogIn(result) {
  return {
    type: MICROSOFTLOGIN,
    payload: result,
  };
}

export function microsoftLoginSuccess(result) {
  return {
    type: MICROSOFTLOGIN_SUCCESS,
    payload: result,
  };
}

export function microsoftLoginFailure(result) {
  return {
    type: "MICROSOFTLOGIN_FAILURE",
    payload: result,
  };
}

export function googleCaptchaVerify(result) {
  return {
    type: GOOGLE_CAPTCHA_VERIFY,
    payload: result,
  };
}

export function googleCaptchaVerifySuccess(result) {
  return {
    type: GOOGLE_CAPTCHA_VERIFY_SUCCESS,
    payload: result,
  };
}

export function googleCaptchaVerifyFailure(result) {
  return {
    type: GOOGLE_CAPTCHA_VERIFY_FAILURE,
    payload: result,
  };
}
