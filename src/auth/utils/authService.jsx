import { Cookies } from 'react-cookie';

const cookies = new Cookies();

const AuthService = (
  // eslint-disable-next-line func-names
  function () {
    function setToken(tokenObj) {
      const accessTokenExp = new Date();
      const refreshTokenExp = new Date();
      accessTokenExp.setTime(accessTokenExp.getTime() + (tokenObj.expires_in * 1000));
      refreshTokenExp.setTime(refreshTokenExp.getTime() + (28800 * 1000));
      cookies.set('accessToken', tokenObj.access_token, {
        path: '/', secure: true, sameSite: 'strict', expires: accessTokenExp,
      });
      cookies.set('refresh_token', tokenObj.refresh_token, {
        path: '/', secure: true, sameSite: 'strict', expires: refreshTokenExp,
      });
    }
    function setUid(userObj) {
      const uidExp = new Date();
      uidExp.setTime(uidExp.getTime() + (28800 * 1000));
      cookies.set('uid', userObj.refresh_token, { path: '/', expires: uidExp });
    }
    function getAccessToken() {
      return cookies.get('accessToken');
    }
    function getRefreshToken() {
      return cookies.get('refresh_token');
    }
    function getSessionExpiry() {
      return cookies.get('sessionExpiry');
    }
    function getGatewaySession() {
      return cookies.get('Session') !== 'undefined' ? cookies.get('Session') : false;
    }
    function clearToken() {
      cookies.remove('accessToken', { path: '/' });
      cookies.remove('refresh_token', { path: '/' });
      cookies.remove('server_error_count');
      cookies.remove('uid');
      cookies.remove('microsoft_uid');
      cookies.remove('session_id');
      cookies.remove('Session');
      cookies.remove('sessionExpiry', { path: '/' });
      cookies.remove('microsoft_client_id');
      window.localStorage.removeItem('issuer');
      window.localStorage.removeItem('redirect_uri');
      window.localStorage.removeItem('okta_client_id');
      window.localStorage.removeItem("TimeZone")
      window.sessionStorage.clear();
    }
    function setServerError() {
      return cookies.set('server_error', 'true');
    }
    function getServerError() {
      return cookies.get('server_error');
    }
    function clearServerError() {
      cookies.remove('server_error');
    }
    function setServerErrorCount(count) {
      return cookies.set('server_error_count', count);
    }
    function getServerErrorCount() {
      return cookies.get('server_error_count');
    }
    function getUid() {
      return cookies.get('uid');
    }
    function setMicrosoftUid(userObj) {
      const microsoftUidExp = new Date();
      microsoftUidExp.setTime(microsoftUidExp.getTime() + (28800 * 1000));
      cookies.set('microsoft_uid', userObj.refresh_token, { path: '/', expires: microsoftUidExp });
    }
    function getMicrosoftUid() {
      return cookies.get('microsoft_uid');
    }
    function setMicrosoftCredentials(data) {
      cookies.set('microsoft_client_id', data.client_id);
    }
    function getMicrosoftCredentials() {
      return cookies.get('microsoft_client_id');
    }
    function setOktaCredentials(data) {
      window.localStorage.setItem('okta_client_id', data.client_id);
      window.localStorage.setItem('issuer', data.web_discovery_uri);
      window.localStorage.setItem('redirect_uri', data.web_redirect_uri);
    }
    function getOktaCredentials() {
      return window.localStorage.getItem('okta_client_id');
    }
    function setCredentials(data) {
        cookies.set('client_id', data.client_key, { secure: true, sameSite: 'strict' });
        cookies.set('client_secret', data.client_secret, { secure: true, sameSite: 'strict' });
        cookies.set('accountId', data.account_id, { secure: true, sameSite: 'strict' });
    }
    function clearCredentials() {
        window.localStorage.removeItem('api-url');
        cookies.remove('client_id');
        cookies.remove('client_secret');
        cookies.remove('accountId');
    }
    function getCredentials() {
      let credentials = {
        client_id: cookies.get('client_id'),
        client_secret: cookies.get('client_secret'),
        account_id: cookies.get('accountId'),
      };
      return credentials;
    }
    function setGlobalTower(data) {
      cookies.set('global_tower', data.code);
    }
    function getGlobalTower() {
      cookies.get('global_tower');
    }
    function removeGlobalTower() {
      cookies.remove('global_tower');
    }
    return {
      setToken,
      setGlobalTower,
      getGlobalTower,
      removeGlobalTower,
      getAccessToken,
      getRefreshToken,
      getSessionExpiry,
      getGatewaySession,
      clearToken,
      setServerError,
      getServerError,
      clearServerError,
      setServerErrorCount,
      getServerErrorCount,
      setUid,
      getUid,
      setMicrosoftUid,
      getMicrosoftUid,
      getMicrosoftCredentials,
      setMicrosoftCredentials,
      setOktaCredentials,
      getOktaCredentials,
      setCredentials,
      getCredentials,
      clearCredentials,
    };
  }
);

export default AuthService;
