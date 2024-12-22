import React from 'react';
import { at } from 'lodash';
import PropTypes from 'prop-types';
import { useField } from 'formik';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  input: {
    '&::placeholder': {
      textOverflow: 'ellipsis !important',
      color: '#b4b8bc',
    },
    height: 30,
  },
}));

const LoginInputField = (props) => {
  const {
    name, label, type, customClassName, labelClassName, fieldIcon, formGroupClassName, isRequired, customWrap, customError, hideError, ...rest
  } = props;
  const [field, meta] = useField(props);
  const classes = useStyles();

  function renderHelperText() {
    const [touched, error] = at(meta, 'touched', 'error');
    let errorValue = '';
    if (touched && error) {
      errorValue = error;
    }
    return errorValue;
  }

  return (
    <>

      <label className={`${labelClassName} mt-2 mb-0 accountId-text` || ''} htmlFor={name}>
        {label}
        {isRequired && (<span className="ml-1 text-danger">*</span>)}
      </label>
      <div className="input-box mt-1">
        <img src={fieldIcon} alt="mailIcon" className="fieled-icon" />
        <input
          type={type}
          className="input"
          name={name}
          {...field}
          {...rest}
          style={{ fontFamily: 'Suisse Intl' }}
        />
      </div>
      {meta.touched && meta.error && !customError && !hideError && (
        <p className="error-msg">{renderHelperText()}</p>
      )}
      {customError && (
        <p className="error-msg">{customError}</p>
      )}
    </>
  );
};

LoginInputField.defaultProps = {
  customClassName: false,
  labelClassName: false,
  formGroupClassName: false,
  isRequired: false,
  customError: false,
  hideError: false,
  customWrap: false,
};

LoginInputField.propTypes = {
  label: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  customWrap: PropTypes.bool,
  labelClassName: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
  formGroupClassName: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
  customClassName: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
  isRequired: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
  customError: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
  hideError: PropTypes.oneOfType([
    PropTypes.bool,
    PropTypes.string,
  ]),
};

export default LoginInputField;
