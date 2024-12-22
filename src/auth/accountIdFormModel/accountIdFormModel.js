import { getMaxLenghtForFields } from '../utils/utils';

const maxLengthValues = getMaxLenghtForFields()

export default {
  formId: 'authLogin',
  formFields: {
    accountId: {
      name: 'accountId',
      label: 'Enter Account Code',
      requiredErrorMsg: 'Account Code is required',
      maxLengthError: `AccountId is too long - should be atmost ${maxLengthValues.accountId} characters.`,
    },
  },
};
