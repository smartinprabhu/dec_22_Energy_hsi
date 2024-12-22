import { ChildrenProps } from "./types";
import "./Card.css";
import React from "react";

const Card = ({ children, doubleSize, className }: ChildrenProps) => {
  return (
    <div
      className={
        doubleSize ? `card card-extand ${className} ` : `card ${className}`
      }
    >
      {children}
    </div>
  );
};

export default Card;
