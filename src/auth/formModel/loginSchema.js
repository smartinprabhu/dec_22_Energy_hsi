import * as Yup from 'yup';
import loginModel from './loginFormModel';

import { getMaxLenghtForFields } from '../utils/utils';

const {
  formField: {
    username,
    password,
  },
} = loginModel;
const maxLengthValues = getMaxLenghtForFields()
const loginSchema = Yup.object({
  [username.name]: Yup.string()
    .required(`${username.requiredErrorMsg}`)
    .max(maxLengthValues.username, username.maxLengthError),
  // .matches(username.regEx, username.invalidErrorMsg),
  [password.name]: Yup.string()
    .required(`${password.requiredErrorMsg}`)
    .max(maxLengthValues.password, password.maxLengthError),
});

export default loginSchema;
