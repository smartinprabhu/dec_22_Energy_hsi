import { getMaxLenghtForFields } from '../utils/utils';

const maxLengthValues = getMaxLenghtForFields()

export default {
  formId: 'loginForm',
  formField: {
    username: {
      name: 'username',
      label: 'Username or Email*',
      requiredErrorMsg: 'Username is required',
      maxLengthError: `Username is too long - should be atmost ${maxLengthValues.username} characters.`,
      invalidErrorMsg: 'Invalid username (e.g. abc@gmail.com)',
      regEx: /^[^\s@]+@[^\s@]+\.[^\s@]{2,50}$/,
    },
    password: {
      name: 'password',
      label: 'Password*',
      requiredErrorMsg: 'Password is required',
      maxLengthError: `Password is too long - should be atmost ${maxLengthValues.password} characters.`,
    },
  },
};
