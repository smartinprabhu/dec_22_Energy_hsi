/* eslint-disable max-len */
/* eslint-disable react/jsx-max-props-per-line */
/* eslint-disable no-undef */
/* eslint-disable react/jsx-no-bind */
/* eslint-disable import/no-unresolved */
import {
  Card,
  CardBody,
  Col, Row,
} from 'reactstrap';
import policyJson from './policy.json';
import React from 'react';
import appConfig from '../config/appConfig';

const TermsOfCondition = () => (
  <Card className="border-0 text-line-height-1">
    <CardBody className="text-justify pt-0">
    <Row dangerouslySetInnerHTML={{ __html:(policyJson[appConfig.CLIENTNAME])}}/>
    </CardBody>
  </Card>
);

export default TermsOfCondition;
