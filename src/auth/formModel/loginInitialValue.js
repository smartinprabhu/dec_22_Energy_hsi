import loginModel from './loginFormModel';

const {
  formField: {
    username,
    password,
  },
} = loginModel;

export default {
  [username.name]: '',
  [password.name]: '',
};
