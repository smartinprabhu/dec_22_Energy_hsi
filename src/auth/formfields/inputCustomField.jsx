/* eslint-disable react/jsx-props-no-spreading */
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

const InputCustomField = (props) => {
  const {
    name, label, type, customClassName, labelClassName, formGroupClassName, isRequired, customWrap, customError, hideError, ...rest
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

      {!customWrap && (
      <label className={labelClassName || ''} htmlFor={name}>
        {label}
        {isRequired && (<span className="ml-1 text-danger">*</span>)}
      </label>
      )}
      {!customWrap && (
      <input
        type={type}
        className={customClassName || classes.input}
        name={name}
        {...field}
        {...rest}
      />
      )}
      {customWrap && (
        <div className="welcome-input-box">
          <input
            type={type}
            className={customClassName || classes.input}
            name={name}
            {...field}
            {...rest}
          />
        </div>
      )}
      {meta.touched && meta.error && !customError && !hideError && (
      <p className="display-block error-msg">{renderHelperText()}</p>
      )}
      {customError && (
        <p className="display-block error-msg">{customError}</p>
      )}
    </>
  );
};

InputCustomField.defaultProps = {
  customClassName: false,
  labelClassName: false,
  formGroupClassName: false,
  isRequired: false,
  customError: false,
  hideError: false,
  customWrap: false,
};

InputCustomField.propTypes = {
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

export default InputCustomField;
