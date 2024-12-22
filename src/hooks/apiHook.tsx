import axios from "axios";
import Cookies from "js-cookie";

import { useState, useEffect, useRef } from "react";
import {
  getCurrentMonth,
  getCurrentWeek,
  getLastThreeMonths,
  getThismonth,
} from "../utils/utils";
import AppConfig from '../auth/config.js';

const accessToken = Cookies.get("accessToken");

const useMultipleUrlData = (
  type: any,
  swapeDates: boolean = false,
  filter: string = "7 days",
  groupBy: string = "",
  filterBy: string = ""
) => {
  const date = new Date();
  const currentDate =
    filter === "7 days"
      ? date.toISOString().slice(0, 10)
      : filter === "1 month"
      ? getThismonth()[1]
      : filter === "3 months"
      ? getLastThreeMonths()[1]
      : filter === "Week"
      ? getCurrentWeek()[1]
      : filter === "Month"
      ? getCurrentMonth()[1]
      : date.toISOString().slice(0, 10);
  let oldDate: Date | string = new Date();

  if (filter === "7 days") {
    oldDate.setTime(oldDate.getTime() - 24 * 60 * 60 * 1000 * 7);
  } else if (filter === "1 month") {
    oldDate = getThismonth()[0];
  } else if (filter === "3 months") {
    oldDate = getLastThreeMonths()[0];
  } else if (filter === "Week") {
    oldDate = getCurrentWeek()[0];
  } else if (filter === "Month") {
    oldDate = getCurrentMonth()[0];
  }

  const sevenDaysOff = new Date(oldDate).toISOString().slice(0, 10);

  const WEBAPPAPIURL =  `${AppConfig.API_URL}/api/`;

  const urls = `${WEBAPPAPIURL}sensor_data/dmrData?type=${type}&endDate=${
    swapeDates ? currentDate : sevenDaysOff
  }&startDate=${swapeDates ? sevenDaysOff : currentDate}&groupBy=${
    filter === "7 days"
      ? "day"
      : filter === "1 month"
      ? "week"
      : filter === "3 months"
      ? "month"
      : groupBy === "Open"
      ? "open"
      : groupBy === "Closed"
      ? "closed"
      : groupBy === "In progress"
      ? "inProgress"
      : ""
  }${filterBy ? `&filter=${filterBy.toLocaleLowerCase()}` : ""}`;
  const [data, setData] = useState<any>();

  const [isLoading, setIsLoading] = useState(true);

  const [error, setError] = useState<any>(null);

  const dataFetched = useRef<any>(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const responseArray = await axios.get(urls, {
          headers: {
            Authorization: `Bearer ${accessToken}`,

            "Content-Type": "application/json",
          },
        });

        setData(responseArray);

        setIsLoading(false);
      } catch (error) {
        setError(error);

        setIsLoading(false);
      }
    };

    if (!dataFetched.current) {
      fetchData();
      dataFetched.current = true;
    }
  }, [filter, groupBy, filterBy]);
  dataFetched.current = false;
  return { data, isLoading, error };
};

export default useMultipleUrlData;
