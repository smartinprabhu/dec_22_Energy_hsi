import moment from "moment";
import { Cookies } from "react-cookie";

const cookies = new Cookies();

export const getMonth = (date: any) => {
  const month = new Intl.DateTimeFormat("en-US", { month: "long" }).format(
    date
  );
  return month;
};

export const dateFormates = (dateString: string | number | Date) => {
  const date = dateString ? new Date(dateString) : new Date();

  const day = date.getDate();

  let suffix = "th";

  if (day === 1 || day === 21 || day === 31) {
    suffix = "st";
  } else if (day === 2 || day === 22) {
    suffix = "nd";
  } else if (day === 3 || day === 23) {
    suffix = "rd";
  }

  return `${getMonth(date)} ${day}${suffix}`;
};

export const tower1ConsumptionDataFormate = (
  data: any,
  key: any,
  convert = false
) => {
  const resultData = data?.map((eachItem: any) => {
    if (convert) {
      return dateFormates(eachItem[key]);
    } else {
      return eachItem[key].toFixed(1);
    }
  });

  return resultData;
};

export const getLastThreeMonths = () => {
  const now = new Date();

  const currentYear = now.getFullYear();

  const currentMonth = now.getMonth() + 1;

  const lastThreeMonthsStart = new Date(currentYear, currentMonth - 3, 1);

  const lastThreeMonthsEnd = new Date(currentYear, currentMonth - 0, 0);

  const lastThreeMonthsStartDate = lastThreeMonthsStart
    .toISOString()
    .slice(0, 10);

  const lastThreeMonthsEndDate = lastThreeMonthsEnd.toISOString().slice(0, 10);

  return [lastThreeMonthsStartDate, lastThreeMonthsEndDate];
};

export const getThismonth = () => {
  const now = new Date();

  const currentYear = now.getFullYear();

  const currentMonth = now.getMonth() + 1;

  const thisMonthStart = new Date(currentYear, currentMonth - 1, 1);

  const thisMonthEnd = new Date(currentYear, currentMonth, 0);

  const thisMonthStartDate = thisMonthStart.toISOString().slice(0, 10);

  const thisMonthEndDate = thisMonthEnd.toISOString().slice(0, 10);

  return [thisMonthStartDate, thisMonthEndDate];
};

export function formatDate(date: Date): string {
  const year = String(date.getFullYear());
  const month: string = String(date.getMonth() + 1).padStart(2, "0");
  const day: string = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

export const getCurrentWeek = () => {
  const currentDate: Date = new Date();
  const currentDayOfWeek: number = currentDate.getDay();

  const startDate: Date = new Date(
    currentDate.setDate(currentDate.getDate() - currentDayOfWeek)
  );

  const endDate: Date = new Date(startDate);
  endDate.setDate(startDate.getDate() + 6);
  return [
    startDate.toISOString().slice(0, 10),
    endDate.toISOString().slice(0, 10),
  ];
};


export const countSameDates = (data) => {
  const dateCounts = {};

  data.forEach((item) => {
    const datePair = item.startDate + '-' + item.endDate;
    if (dateCounts[datePair]) {
      dateCounts[datePair]++;
    } else {
      dateCounts[datePair] = 1;
    }
  });

  return Object.values(dateCounts);
};

 export const findUniqueDatePairs = (data: any) => {
  const datePairs: Set<string> = new Set();

  const formatter: Intl.DateTimeFormat = new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
  });

  data?.forEach((item: any) => {
    if (item?.startDate && item?.endDate) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);

      if (!isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) {
        const formattedStartDate: string = formatter?.format(startDate);
        const formattedEndDate: string = formatter?.format(endDate);

        const datePair = `${formattedStartDate}-${formattedEndDate}`;
        datePairs.add(datePair);
      }
    }
  });

  const sortedPairs = Array.from(datePairs).sort((a: string, b: string) => {
    const dateA:any = new Date(a.split('-')[0]);
    const dateB:any = new Date(b.split('-')[0]);
    return dateA - dateB;
  });

  return sortedPairs;
};

export const getCurrentWeekDates = () => {
  const currentDate: Date = new Date();
  const currentDayOfWeek: number = currentDate.getDay();
  const startDate: Date = new Date(currentDate);
  startDate.setDate(currentDate.getDate() - currentDayOfWeek);
  const endDate: Date = new Date(startDate);
  endDate.setDate(startDate.getDate() + 6);
  const weekDates: string[] = [];
  const monthOptions: Intl.DateTimeFormatOptions = { month: 'short' };
  const dayOptions: Intl.DateTimeFormatOptions = { day: 'numeric' };
  const yearOptions: Intl.DateTimeFormatOptions = { year: 'numeric' };

  for (let i = 0; i <= 6; i++) {
    const currentDate: Date = new Date(startDate);
    currentDate.setDate(startDate.getDate() + i);

    const monthPart: string = currentDate.toLocaleDateString(undefined, monthOptions);
    const dayPart: string = currentDate.toLocaleDateString(undefined, dayOptions);
    const yearPart: string = currentDate.toLocaleDateString(undefined, yearOptions);

    const formattedDate: string = `${monthPart} ${dayPart} ${yearPart}`;
    weekDates.push(formattedDate);
  }

  return weekDates;
};

export function dayGraph(date) {
  const options = { month: 'short', day: 'numeric' };
  return date.toLocaleDateString("en-CA", options);
}

export  function formatDateFromString(inputDate) {
  const [month, day] = inputDate?.match(/\b\w+\b/g) || [];
  if (!month || !day) return 'Invalid Date';
  const monthNumber = new Date(`${month} 1, 2023`).getMonth() + 1;
  if (isNaN(monthNumber)) return 'Invalid Date';
  const formattedDate = `2023-${String(monthNumber).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  return formattedDate;
}



export const graphDates =  (startDate: any, endDate: any):any => {
  const dateList: any = [];
  let currentDate: Date = new Date(startDate);
  const lastDate: Date = new Date(endDate);

  while (currentDate <= lastDate) {
    dateList.push(currentDate.toISOString().split('T')[0]);
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return dateList;
};




export const  mergeDataWithCurrentWeek22 = (apiData, currentWeekDates, dateKey, countKey) => {
  const mergedData = currentWeekDates
    ?.map((date) => {
      let totalValue = 0;

      apiData?.forEach((item) => {
        const formattedApiDate = new Date(item[dateKey]).toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        });

        const formattedCurrentWeekDate = new Date(date).toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        });

        if (formattedApiDate === formattedCurrentWeekDate) {
          totalValue += item[countKey];
        }
      });

      if (totalValue > 0) {
        return { date: date, totalValue: totalValue };
      }
      return null; // Return null for dates with no match
    })
    .filter((result) => result !== null); // Filter out null results

  return mergedData;

  }

export const getCurrentMonthDates = (): string[] => {
  const currentDate: Date = new Date();
  const currentYear: number = currentDate.getFullYear();
  const currentMonth: number = currentDate.getMonth();

  const firstDayOfMonth: Date = new Date(currentYear, currentMonth, 1);
  const lastDayOfMonth: Date = new Date(currentYear, currentMonth + 1, 0);

  const monthDates: string[] = [];
  const monthOptions: Intl.DateTimeFormatOptions = { month: 'short' };
  const dayOptions: Intl.DateTimeFormatOptions = { day: 'numeric' };
  const yearOptions: Intl.DateTimeFormatOptions = { year: 'numeric' };

  for (let date: Date = firstDayOfMonth; date <= lastDayOfMonth; date.setDate(date.getDate() + 1)) {
    const monthPart: string = date.toLocaleDateString(undefined, monthOptions);
    const dayPart: string = date.toLocaleDateString(undefined, dayOptions);
    const yearPart: string = date.toLocaleDateString(undefined, yearOptions);

    const formattedDate: string = `${monthPart} ${dayPart} ${yearPart}`;
    monthDates.push(formattedDate);
  }

  return monthDates;
};

export   const  formatDateRange = (startDateStr, endDateStr) => {
  const startDate = new Date(startDateStr);
  const endDate = new Date(endDateStr);

  const startMonthShort = startDate.toLocaleString('default', { month: 'short' });
  const startMonthFull = startDate.toLocaleString('default', { month: 'long' });
  const startWeekday = startDate.toLocaleString('default', { weekday: 'short' });
  const startDay = startDate.getDate();
  const endDay = endDate.getDate();
  const year = startDate.getFullYear();
  const day = `${startMonthFull}, ${startWeekday} ${getDateWithSuffix(startDay)}`;
  const week = `${startMonthShort} ${getDateWithSuffix(startDay)} - ${getDateWithSuffix(endDay)}`;
  const month = `${startMonthFull}, ${year}`;
  

  return { day, week , month };
}


interface Item {
  startDate: any;
  endDate?: string | null;
  // Add other properties as needed
}

export function roundOffEndTimes(data: any) {
  const roundedEndTimes: any= data?.map((item: Item | null) => {
    const endDate: any = item?.endDate;
    if (endDate && typeof endDate === 'string') {
      const timePart: string[] = endDate.split(" ")[1]?.slice(0, -3)?.split(":") || [];
      if (timePart.length === 2) {
        const [hours, minutes]: string[] = timePart;
        const roundedHours: number = parseInt(hours);
        return `${roundedHours.toString().padStart(2, '0')}:00`;
      }
    }
    return null;
  });

  return roundedEndTimes;
}

export function roundOffStartTimes1(data: any)  {
  const roundedStartTimes: any = data?.map((item: Item) => {
    const startDate: any = item?.startDate;
    if (startDate && typeof startDate === 'string') {
      const timePart: string[] = startDate.split(" ")[1]?.slice(0, -3)?.split(":") || [];
      if (timePart.length === 2) {
        const [hours, minutes]: string[] = timePart;
        const roundedHours: number = parseInt(hours);
        return `${roundedHours.toString().padStart(2, '0')}:00`;
      }
    }
    return null;
  });

  return roundedStartTimes;
}



export function hoursData(currenttime, compareStrings) {
  return currenttime.map(time =>
    compareStrings?.includes(time) ? compareStrings.filter(t => t === time).length : 0
  );
}




export const mergeDataWithCurrentWeek = (apiData, currentWeekDates, dateKey, countKey) => {
  const mergedData = currentWeekDates?.map((date) => {
    let totalValue = 0; 
    apiData?.forEach((item) => {
      
      const formattedApiDate = new Date(item[dateKey]).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });

      
      const formattedCurrentWeekDate = new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });

    
      if (formattedApiDate === formattedCurrentWeekDate) {
        totalValue += item[countKey];
      }
    });

    return totalValue;
  });

  return mergedData;
};




export const mergeDataWithCurrentWeek11 = (apiData, currentWeekDates, dateKey, countKey) => {
  const mergedData = currentWeekDates?.map((date) => {
    let totalValue = 0;

    apiData?.forEach((item) => {
      const formattedApiDate = new Date(item[dateKey]).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });

      const formattedCurrentWeekDate = new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });

      if (formattedApiDate === formattedCurrentWeekDate) {
        totalValue += item[countKey];
      }
    });

    // Only return a total value if it's greater than 0
    if (totalValue > 0) {
      return totalValue;
    } else {
      return null; // Return null for dates with no matching data
    }
  }).filter((totalValue) => totalValue !== null); // Filter out null values

  return mergedData;
};



export const getCurrentMonth = () => {
  const currentDate: Date = new Date();

  // return [startDate.toISOString().slice(0, 10), endDate.toISOString().slice(0, 10)]
  const currentYear: number = currentDate.getFullYear();
  const currentMonth: number = currentDate.getMonth();

  const numDaysInMonth: number = new Date(
    currentYear,
    currentMonth + 1,
    0
  ).getDate();

  const startDate: Date = new Date(currentYear, currentMonth, 1);
  const endDate: Date = new Date(currentYear, currentMonth, numDaysInMonth);

  return [formatDate(startDate), formatDate(endDate)];
};

export const weekMonthFormat = (data: any, format: string) => {
  let resultData;
  if (format === "week") {
    resultData = data?.map((e: any) => {
      return `${dateFormates(e?.startDate)}`;
    });
  } else {
    resultData = data?.map((eachWeek: any) => {
      return `${getMonth(
        eachWeek?.startDate ? new Date(eachWeek?.startDate) : new Date()
      )}`;
    });
  }
  return resultData;
};


export function getCurrentTimeSlot() {
  const now = new Date();
  const currentHour = now.getHours();
  return currentHour
}



export function subtractDates(
  date1: Date,
  date2: Date
): { days: number; hours: number; minutes: number; seconds: number } {
  const timeDifference = date1.getTime() - date2.getTime();
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  const hours = Math.floor((timeDifference / (1000 * 60 * 60) % 24));
  const minutes = Math.floor((timeDifference / (1000 * 60) % 60));
  const seconds = Math.floor((timeDifference / 1000) % 60);

  return { days, hours, minutes, seconds };
}


export const getHourMinute = (datetimeString: string) => {
  const timeComponent: string = datetimeString.split(" ")[1];
  const [hour, minute]: number[] = timeComponent.split(":").map(Number);
  return {
    hour,
    minute,
  };
};

export const getLeftAndWidth = (startDate = "", endDate = "") => {
  let calculateLeft;
  let calculateWidth;

  // Check if endDate is "Not Closed"
  if (endDate === "Not Closed") {
    // Ticket is not complete, set the width to cover from the startTime to 11:59 PM
    const date2: Date = new Date(startDate);
    const endOfDay = new Date(date2);
    endOfDay.setHours(23, 59, 59, 999); // Set to 11:59:59.999 PM
    const timeDifference = endOfDay.getTime() - date2.getTime();
    const hours = Math.floor(timeDifference / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference / (1000 * 60)) % 60);

    const timeComponent: string = startDate?.split(" ")?.[1];
    if (timeComponent) {
      const [hour, minute]: number[] = timeComponent?.split(":")?.map(Number);
      calculateLeft = hour + minute / 60;
      calculateWidth = hours + minutes / 60;
    }
  } else {
    // Ticket is complete, use the provided endDate but limit it to 11:59 PM
    const date1: Date = new Date(endDate);
    const date2: Date = new Date(startDate);
    const endOfDay = new Date(date2);
    endOfDay.setHours(23, 59, 59, 999); // Set to 11:59:59.999 PM

    if (date1 > endOfDay) {
      // If endDate is after 11:59 PM, limit it to 11:59 PM
      date1.setTime(endOfDay.getTime());
    }

    const timeDifference = date1.getTime() - date2.getTime();
    const hours = Math.floor(timeDifference / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference / (1000 * 60)) % 60);

    const timeComponent: string = startDate?.split(" ")?.[1];
    if (timeComponent) {
      const [hour, minute]: number[] = timeComponent?.split(":")?.map(Number);
      calculateLeft = hour + minute / 60;
      calculateWidth = hours + minutes / 60;
    }
  }

  return {
    left: calculateLeft * 62.5, // 1 hour corresponds to 62px
    width: calculateWidth * 62.5, // 1 hour corresponds to 62px
  };
};



export const getLeftAndWidth1 = (startDate = "", endDate = "") => {
  const date1: Date = new Date(endDate);
  const date2: Date = new Date(startDate);
  let calculateLeft;
  let calculateWidth;
  const timeDifference = date1.getTime() - date2.getTime();

  const hours = Math.floor(timeDifference / (1000 * 60 * 60));
  const minutes = Math.floor((timeDifference / (1000 * 60)) % 60);

  // Calculate left and width using only the date part
  calculateLeft = date2.getDate();
  calculateWidth = hours / 24 + minutes / (60 * 24);

  return {
    left: calculateLeft,
    width: calculateWidth*249 ,
  };
};

export const getLeftAndWidth3 = (startDate, endDate, slaHours) => {
  let calculateLeft = 0;
  let calculateWidth = 0;

  const date1:any = new Date(startDate);
  const dayOfWeek = date1.getDay();
  const daysUntilStartOfWeek = (dayOfWeek + 7 - 1) % 7;
  const lastDayOfWeek:any = new Date(date1);
  lastDayOfWeek.setDate(date1.getDate() + (6 - daysUntilStartOfWeek));

  if (endDate === "Not Closed" && slaHours) {
    // Extract hours from the SLA time in "hh:mm" format and parse it as an integer
    const slaHoursValue = parseInt(slaHours.split(":")[0], 10);

    // Calculate the total width as the sum of the start date and SLA hours
    const totalWidth = (slaHoursValue / 24) * 214;

    // Ensure that the total width doesn't exceed the width of the current week
    calculateWidth = Math.min(totalWidth, (7 - daysUntilStartOfWeek) * 214);
  } else {
    const date2:any = endDate === "Not Closed" ? null : new Date(endDate);

    if (date2 && date2 >= date1 && date2 <= lastDayOfWeek) {
      const daysDifference = Math.ceil((date2 - date1) / (24 * 60 * 60 * 1000));
      calculateWidth = (daysDifference + 1) * 214;
    } else {
      const daysDifference = Math.ceil((lastDayOfWeek - date1) / (24 * 60 * 60 * 1000));
      calculateWidth = (daysDifference + 1) * 214;
    }
  }

  calculateLeft = daysUntilStartOfWeek * 214;

  return {
    left: calculateLeft,
    width: calculateWidth,
  };
};



export const getLeftAndWidth4 = (startDate, endDate, slaHours) => {
  let calculateLeft = 0;
  let calculateWidth = 0;

  const date1:any = new Date(startDate);
  const date2:any = new Date(endDate);

  const startOfMonth:any = new Date(date1.getFullYear(), date1.getMonth(), 1);
  const endOfMonth:any = new Date(date1.getFullYear(), date1.getMonth() + 1, 0);

  const isSameMonth = date1.getMonth() === date2.getMonth() && date1.getFullYear() === date2.getFullYear();

  if (slaHours) {
    // Parse SLA hours as an integer
    const slaHoursValue = parseInt(slaHours, 10);

    if (isSameMonth) {
      // Calculate the number of days between startDate and endDate
      const daysDifference = Math.ceil((date2 - date1) / (24 * 60 * 60 * 1000));

      // Calculate width for the same month, limited by SLA hours if it's less than the full month
      calculateWidth = Math.min((daysDifference + 1) * 45, (slaHoursValue / 24) * 45);
    } else {
      // Calculate the number of days in the entire month for the startDate
      const daysInMonth = Math.ceil((endOfMonth - startOfMonth) / (24 * 60 * 60 * 1000));

      // Calculate width for the current month, limited by SLA hours if it's less than the full month
      calculateWidth = Math.min((daysInMonth) * 45, (slaHoursValue / 24) *45 );
    }
  } else {
    if (isSameMonth) {
      const daysDifference = Math.ceil((date2 - date1) / (24 * 60 * 60 * 1000));
      calculateWidth = (daysDifference + 1) * 45;
    } else {
      const daysInMonth = Math.ceil((endOfMonth - startOfMonth) / (24 * 60 * 60 * 1000));
      calculateWidth = (daysInMonth) * 45;
    }
  }

  calculateLeft = (date1.getDate() - 1) * 48.5;

  return {
    left: calculateLeft,
    width: calculateWidth,
  };
};

export const calculateLeftValue = (startDate, endDate) =>  {
  const startDateObj:any = new Date(startDate);
  const endDateObj:any = new Date(endDate);
  
  const timeDifferenceInDays = (endDateObj - startDateObj) / (1000 * 60 * 60 * 24);
  
  const leftValue = timeDifferenceInDays * 100; 
  
  return leftValue;
}

export function getDateWithSuffix(date:any) {
  if (date >= 11 && date <= 13) {
    return date + "<sup>th</sup>";
  } else {
    const lastDigit = date % 10;
    switch (lastDigit) {
      case 1:
        return date + "<sup>st</sup>";
      case 2:
        return date + "<sup>nd</sup>";
      case 3:
        return date + "<sup>rd</sup>";
      default:
        return date + "<sup>th</sup>";
    }
  }
}


const snakeCaseToCapitalizedText = (inputString: string) => {
  const words = inputString
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase());
  return words.join(" ");
};

export const capitalizedToSnakeCase = (input: string): string => {
  return input.replace(/([a-z])([A-Z])/g, "$1_$2").toLowerCase();
};

export const convertHelpdeskData = (data: any) => {
  const resultData = data?.map((each) => {
    const startDate = each?.create_date;
    let endDate;

    if (each?.closed_time === false) {
      endDate = "Not Closed";
    } else {
      endDate = each?.closed_time; 
    }

    return {
      id: each?.id,
      startDate: startDate,
      endDate: endDate,
      state: each?.state,
      subject: each?.subject,
      maintenanceTeam: each?.maintenance_team,
      plannedSla : each?.planned_sla

    };
  });
  return resultData;
};


export const convertInspectionData = (data: any) => {
  const resultData = data?.map((each) => {
    return {
      id: each?.id,
      startDate: each?.start_datetime,
      endDate: each?.end_datetime,
      state: snakeCaseToCapitalizedText(each?.state),
      subject: each?.check_list_name,
      maintenanceTeam: each?.maintenance_team,
      equipment_name: each?.equipment_name,
      space_name: each?.space_name ,
      date_execution: each?.date_execution,
      checklist_json_data: each?.checklist_json_data
    };
  });
  return resultData;
};



export function formatTimeWithAMPM(dateTimeString) {
  const inputDate = new Date(dateTimeString);
  const options: any = { hour: 'numeric', minute: 'numeric', hour12: true };
  return inputDate.toLocaleString('en-US', options);
}

export const convertIncidentData = (data: any) => {
  const resultData = data?.map((each) => {
    return {
      id: each?.id,
      startDate: each?.incident_on,
      endDate: each?.target_closure_date,
      state: snakeCaseToCapitalizedText(each?.state),
      subject: each?.description,
      maintenanceTeam: each?.maintenance_team || "No team",
    };
  });
  return resultData;
};

export const convertPpmsData = (data: any) => {
  const resultData = data?.map((each) => {
    return {
      id: each?.id,
      startDate: each?.starts_on,
      endDate: each?.ends_on,
      state: snakeCaseToCapitalizedText(each?.state),
      subject: each?.equipment_name,
      maintenanceTeam: each?.maintenance_team,
    };
  });
  return resultData;
};

export const convertHelpdeskTeams = (data: any) => {
  const resultData = data?.map((each, index) => {
    return {
      id: index,
      displayText: each?.state,
      value: each?.state,
    };
  });
  return resultData;
};

export const removeDuplicates = (data) => {
  const uniqueData = data.reduce((accumulator, current) => {
    const existingTeamIds = accumulator.map(
      (item) => item.maintenance_team_id[1]
    );

    if (!existingTeamIds.includes(current.maintenance_team_id[1])) {
      accumulator.push(current);
    }

    return accumulator;
  }, []);
  return uniqueData;
};

export const convertTeamsData = (data) => {
  const resultData = data?.map((each, index) => {
    return {
      id: index,
      displayText: each?.maintenance_team,
      value: each?.maintenance_team,
    };
  });
  return resultData;
};

export const groupDataByDate = (rawData) => {
  const data = rawData.sort(
    (a, b) => moment(a.date).valueOf() - moment(b.date).valueOf()
  );
  const groupedData = data.reduce((acc, cur) => {
    let date = cur.startDate; // extract the date from the date string
    if (!acc[moment(date).format("YYYY-MM-DD")]) {
      acc[moment(date).format("YYYY-MM-DD")] = [];
    }
    acc[moment(date).format("YYYY-MM-DD")].push(cur);
    return acc;
  }, {});

  return groupedData;
};

export const fillMissingDates = (data, startDate, endDate) => {
  const result = {};

  let currentDate = new Date(startDate);
  let lastDate = new Date(endDate);

  while (currentDate <= lastDate) {
    const dateString = moment(currentDate).format("YYYY-MM-DD");

    if (data[dateString]) {
      result[dateString] = data[dateString];
    } else {
      result[dateString] = [];
    }

    currentDate.setDate(currentDate.getDate() + 1);
  }

  return result;
};

export const handleLogout = () => {
  cookies.remove("accessToken");

  cookies.remove("accessTokenOddo16");

  // cookies.remove("client_id");
  // cookies.remove("client_secret");
  // cookies.remove("accountId");

  cookies.remove("access_token");
  cookies.remove("refresh_token");
  cookies.remove("global_tower");

  window.location.reload();
};
