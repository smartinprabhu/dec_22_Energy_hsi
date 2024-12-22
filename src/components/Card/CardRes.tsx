import { ChildrenProps } from "./types";
import "./Card.css";

const Card = ({ children, doubleSize, className }: ChildrenProps) => {
  return (
    <div
      className={
        doubleSize ? `card-responsive card-extand-responsive ${className} ` : `card-responsive ${className}`
      }
    >
      {children}
    </div>
  );
};

export default Card;