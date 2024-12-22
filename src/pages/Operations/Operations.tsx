import React, { useEffect, useState } from "react";
import "./Operations.css";
import OperationsFilter from "../../components/OperationsFilter/OperationsFilter";
import DayCalendar from "../../components/DayCalendar/DayCalendar";
import {
  monthFullDates,
  operationsFilterByItems,
  operationsTabs,
  weekFullDates,
} from "../../appData/appData";
import WeekCalendar from "../../components/WeekCalendar/WeekCalendar";
import MonthCalendar from "../../components/MonthCalendar/MonthCalendar";
import OperationsChart from "../../components/OperationsChart/OperationsChart";
import { BiLeftArrow, BiRightArrow } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import useMultipleUrlData from "../../hooks/apiHook";
import { Backdrop, CircularProgress } from "@mui/material";
import {
  capitalizedToSnakeCase,
  convertHelpdeskData,
  convertIncidentData,
  convertInspectionData,
  convertPpmsData,
  dateFormates,
  dayGraph,
  fillMissingDates,
  formatDateFromString,
  getCurrentMonthDates,
  getCurrentWeek,
  getCurrentWeekDates,
  groupDataByDate,
} from "../../utils/utils";
import { ChartDataType } from "../../types/types";
import SnackBar from "../../components/SnackBar/SnackBar";
import AppConfig from "../../auth/config.js";
import axios from "axios";
import { Cookies } from "react-cookie";
import {
  convertHelpdeskTeams,
  convertTeamsData,
  getDateWithSuffix,
  handleLogout,
  removeDuplicates,
} from "../../utils/utils";
import DayOperationsChart from "../../components/OperationsChart/DayOperationChart";
import PpmChart from "../../components/OperationsChart/PpmChart";
import PpmCalendar from "../../components/PpmCalendar/PpmCalendar";
import IncidentChart from "../../components/OperationsChart/IncidentsChart";
import PpmWeekCalendar from "../../components/PpmCalendar/PpmWeekCalendar";
import HelpdeskWeekCalendar from "../../components/HelpdeskCalendar/HelpdeskWeekCalendar";
import HelpdeskMonthCalendar from "../../components/HelpdeskCalendar/HelpdeskMonthCalendar";
import IncidentDayChart from "../../components/OperationsChart/IncidentDayChart";
import HelpdeskMandWChart from "../../components/HelpdeskChart/HelpdeskweekMonthChart";
import HelpdeskDayDayChart from "../../components/HelpdeskChart/HelpdeskDaychart";

const Operations: React.FC = () => {
  const [activeTab, setActiveTab] = useState("Day");
  const [status, setStatus] = useState("");
  const [filterBy, setFilterBy] = useState("");
  const [team, setTeam] = useState("");
  // const [states, setStates] = useState([]);
  const [activeState, setActiveState] = useState("");
  const [companyList, setCompanyList] = useState([]);
  const [activeCompany, setActiveCompany] = useState<any>("");
  const [activeCompanyId, setActiveCompanyId] = useState<number>();
  const [oneHourElapsed, setOneHourElapsed] = useState(false);
  const [elapsed, setElapsed] = useState(false);
  const [tasksData, setTasksData] = useState<any>();
  const [loader, setLoader] = useState<boolean>(false);
  const [err, setErr] = useState<unknown>(null);
  const [errMsg, setErrMsg] = useState("");
  const [opengraphData, setOpenGraphData] = useState<any>([]);
  const [closedgraphData, setClosedGraphData] = useState<any>([]);
  const [upcominggraphData, setUpcomingGraphData] = useState<any>([]);
  const [inProgressgraphData, setInProgressGraphData] = useState<any>([]);
  const [acknowledged, setAcknowledged] = useState<any>([]);
  const [assessed, setAssessed] = useState<any>([]);
  const [recommended, SetRecommended] = useState<any>([]);
  const [resolved, setResolved] = useState<any>([]);
  const [validated, setValidated] = useState<any>([]);
  const [passed, setpassed] = useState<any>([]);
  const [cancelled, setCancelled] = useState<any>([]);
  const [Helpdeskcancelled, setHelpdeskCancelled] = useState<any>([]);
  const [HelpdeskOnHold, setHelpdeskOnHold] = useState<any>([]);
  const [currentTime, setCurrentTime] = useState<any>(
    null
  );
  const [dayData, setDayData] = useState<any>([]);
  const [startDate, setStartDate] = useState(
    new Date().toLocaleDateString("en-CA")
  );
  const [endDate, setEndDate] = useState(
    new Date().toLocaleDateString("en-CA")
  );
  const [startDateOne, setStartDateOne] = useState(dayGraph(new Date()));
  const [endDateOne, setEndDateOne] = useState(dayGraph(new Date()));
  const [dateKey, setDateKey] = useState("");
  const [dateCount, setDateCount] = useState<any>();
  const WEBAPPAPIURL = `${AppConfig.API_URL}/api/`;
  const cookies = new Cookies();
  const accessToken = cookies.get("accessToken");
  const accessTokenOddo16 = cookies.get("accessTokenOddo16");
  const [selectedData, setSelectedData] = useState<any>(null);
  const [selctedDate, setSelectedDate] = useState<any>(null);
  const [latestDate, setlatestDate] = useState(true);
  const [Isvisible, setIsvisible] = useState(true);



  // const getStatesList = () => {
  //   const URL = `${WEBAPPAPIURL}v4/search_read?domain=[["country_id","ilike","India"]]&model=res.country.state&fields=["name"]&limit=100&offset=0`;
  //   const config = {
  //     method: "get",
  //     url: URL,
  //     headers: {
  //       Authorization: `Bearer ${accessToken}`,
  //     },
  //   };

  //   const fetchStatesList = async () => {
  //     setErr(null);
  //     setErrMsg("");
  //     setLoader(true);
  //     try {
  //       const response = await axios(config);
  //       if (response.status === 200) {
  //         const states = response?.data?.data.map((eachState) => {
  //           return {
  //             id: eachState?.id,
  //             displayText: eachState?.name,
  //             value: eachState?.name,
  //           };
  //         });
  //         setStates(states);
  //         setLoader(false);
  //       }
  //     } catch (error: any) {
  //       setErr(true);
  //       setLoader(false);
  //       setErrMsg(error?.response.data.error.message);
  //     }
  //   };

  //   fetchStatesList();
  // };

  const getCompanyLIst = () => {
    const URL = `${WEBAPPAPIURL}v4/search_read?domain=[["state_id","ilike","${activeState}"]]&model=res.company&fields=["name"]`;

    const config = {
      method: "get",
      url: URL,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };

    const fetchCompanyList = async () => {
      setErr(null);
      setErrMsg("");
      setLoader(true);
      try {
        const response = await axios(config);
        if (response.status === 200) {
          const companyList = response?.data?.data?.map((eachCompany) => {
            return {
              id: eachCompany?.id,
              displayText: eachCompany?.name,
              value: eachCompany?.name,
            };
          });
          setCompanyList(companyList);
          setLoader(false);
        }
      } catch (error: any) {
        setErr(true);
        setLoader(false);
        setErrMsg(error?.response.data.error.message);
      }
    };

    fetchCompanyList();
  };

  // useEffect(() => {
  //   getStatesList();
  // }, []);

  useEffect(() => {
    getCompanyLIst();
  }, [activeState]);

  const handleLeftArrowClick = () => {
    if (activeTab === operationsTabs[0].displayText) {
      const prevDate = new Date(startDate);
      prevDate.setDate(prevDate.getDate() - 1);
      setStartDate(prevDate.toLocaleDateString("en-CA"));
      setEndDate(prevDate.toLocaleDateString("en-CA"));

    } else if (activeTab === operationsTabs[1].displayText) {
      setSelectedData(null);
      setSelectedDate(null);
      const prevStartDate = new Date(startDate);
      const prevEndDate = new Date(endDate);
      prevStartDate.setDate(prevStartDate.getDate() - 7);
      prevEndDate.setDate(prevEndDate.getDate() - 7);
      setStartDate(prevStartDate.toLocaleDateString("en-CA"));
      setEndDate(prevEndDate.toLocaleDateString("en-CA"));
      setCurrentTime(new Date().toLocaleDateString("en-CA"));
      setlatestDate(false);

    } else if (activeTab === operationsTabs[2].displayText) {
      setSelectedData(null);
      setSelectedDate(null);
      const prevStartDate = new Date(startDate);
      const prevEndDate = new Date(endDate);
      prevStartDate.setMonth(prevStartDate.getMonth() - 1);
      prevEndDate.setMonth(prevEndDate.getMonth() - 1);
      setStartDate(prevStartDate.toLocaleDateString("en-CA"));
      setEndDate(prevEndDate.toLocaleDateString("en-CA"));
      setCurrentTime(new Date().toLocaleDateString("en-CA"));
      setlatestDate(false);
    }
  };

  const handleRightArrowClick = () => {
    if (activeTab === operationsTabs[0].displayText) {
      const nextDate = new Date(endDate);
      nextDate.setDate(nextDate.getDate() + 1);
      setStartDate(nextDate.toLocaleDateString("en-CA"));
      setEndDate(nextDate.toLocaleDateString("en-CA"));
    } else if (activeTab === operationsTabs[1].displayText) {
      const nextStartDate = new Date(startDate);
      const nextEndDate = new Date(endDate);
      nextStartDate.setDate(nextStartDate.getDate() + 7);
      nextEndDate.setDate(nextEndDate.getDate() + 7);
      setStartDate(nextStartDate.toLocaleDateString("en-CA"));
      setEndDate(nextEndDate.toLocaleDateString("en-CA"));
      setCurrentTime(new Date().toLocaleDateString("en-CA"));

      setSelectedDate(null);
      setSelectedData(null);
      setlatestDate(false);

    } else if (activeTab === operationsTabs[2].displayText) {
      const nextStartDate = new Date(startDate);
      const nextEndDate = new Date(endDate);
      nextStartDate.setMonth(nextStartDate.getMonth() + 1);
      nextEndDate.setMonth(nextEndDate.getMonth() + 1);
      setStartDate(nextStartDate.toLocaleDateString("en-CA"));
      setEndDate(nextEndDate.toLocaleDateString("en-CA"));
      setCurrentTime(new Date().toLocaleDateString("en-CA"));
      setSelectedDate(null);
      setSelectedData(null);
      setlatestDate(false);
    }
  };


  const updateDatesBasedOnTab = () => {
    if (activeTab === operationsTabs[0].displayText) {
      setStartDate(new Date().toLocaleDateString("en-CA"));
      setEndDate(new Date().toLocaleDateString("en-CA"));
    }
    if (activeTab === operationsTabs[1].displayText) {
      setStartDate(new Date(weekFullDates[0]).toLocaleDateString("en-CA"));
      setEndDate(new Date(weekFullDates[weekFullDates?.length - 1]).toLocaleDateString("en-CA"));
      setSelectedData(null);
      setSelectedDate(null);
      setlatestDate(true);

    } else if (activeTab === operationsTabs[2].displayText) {
      setStartDate(new Date(monthFullDates[0]).toLocaleDateString("en-CA"));
      setEndDate(
        new Date(monthFullDates[monthFullDates?.length - 1]).toLocaleDateString(
          "en-CA"
        )
      );
      setSelectedData(null);
      setSelectedDate(null);
      setlatestDate(true);

    }
  };

  const startDate1 = formatDateFromString(startDateOne);
  const endDate1 = formatDateFromString(endDateOne);


  useEffect(() => {
    updateDatesBasedOnTab();
  }, [activeTab]);

  useEffect(() => {
    let URL = ``;
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    }

    const helpDeskURL = `${WEBAPPAPIURL}v2/search_read?model=dw.mvw_helpdesk_tickets&fields=[]&offset=0&limit=0&domain=[["unattended_ppm","!=",true],["maintenance_type","=","bm"],["issue_type","!=","incident"],["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],["company","ilike","${activeCompany}"],["state","ilike","${status}"],["maintenance_team","ilike","${encodeURIComponent(
      team
    )}"]]`;
    const inspectionURL = `${WEBAPPAPIURL}v2/search_read?model=dw.mvw_inspection_checklist&fields=[]&offset=0&limit=0&domain=[["date",">=","${startDate}"],["date","<=","${endDate}"],["company","ilike","${activeCompany}"],["state","ilike","${status}"],["maintenance_team","ilike","${encodeURIComponent(
      team
    )}"]]`;
    const ppmsURL = `${WEBAPPAPIURL}v2/search_read?model=dw.mvw_ppm_scheduler_week&fields=["maintenance_team","starts_on","ends_on","state","equipment_name","company"]&offset=0&limit=0&domain=[["starts_on",">=","${startDate}"],["ends_on","<=","${endDate}"],["company","ilike","${activeCompany}"],["state","ilike","${status}"],["maintenance_team","ilike","${encodeURIComponent(
      team
    )}"]]`;
    const incidentsURL = `${WEBAPPAPIURL}v2/search_read?model=dw.mvw_hx_incident_view&fields=["state","description","incident_on","target_closure_date","state","maintenance_team"]&offset=0&limit=0&domain=[["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],["company","ilike","${activeCompany}"],["state","ilike","${status}"],["maintenance_team","ilike","${encodeURIComponent(
      team
    )}"]]`;

    if (filterBy === operationsFilterByItems[0].value) {
      URL = inspectionURL;
    } else if (filterBy === operationsFilterByItems[1].value) {
      URL = ppmsURL;
    } else if (filterBy === operationsFilterByItems[2].value) {
      URL = helpDeskURL;
    } else if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
    }
    const config = {
      method: "get",
      url: URL,
      headers: {
        Authorization: `Bearer ${accessTokenOddo16}`,
      },
    };

    if (URL) {
      const fetchOperationsData = async () => {
        setTasksData([]);
        setErr(null);
        setErrMsg("");
        setLoader(true);

        try {
          const response = await axios(config);
          if (response.status === 200) {
console.log("response",response.data)
            const convertedData =
              filterBy === operationsFilterByItems[0]?.value
                ? convertInspectionData(response?.data)
                : filterBy === operationsFilterByItems[1]?.value
                  ? convertPpmsData(response?.data)
                  : filterBy === operationsFilterByItems[2]?.value
                    ? convertHelpdeskData(response?.data)
                    : filterBy === operationsFilterByItems[3]?.value
                      ? convertIncidentData(response?.data)
                      : response?.data?.data;
            console.log("sai", convertedData)
            if (response?.data?.length === 0) {
              setErr(true);
              setLoader(false);
              setErrMsg("No data");
            } else {
              const groupedData = groupDataByDate(convertedData);

              setTasksData(fillMissingDates(groupedData, startDate, endDate));
              setDayData(convertedData);

              setLoader(false);
              setErr(null);
              setErrMsg("");
            }
          }
        } catch (error: any) {
          setErr(true);
          setLoader(false);
          setErrMsg(error?.response.data.error.message);
        }
      };
      if (filterBy) {
        fetchOperationsData();
      }
    }
  }, [status, filterBy, team, activeCompany, startDate1, endDate1, startDate, endDate]);
  console.log("sai", dayData)

  const daymissedData = dayData?.filter((item) => item.state === "Missed");
  const daycompletedData = dayData?.filter((item) => item.state === "Completed");
  const dayupcomingData = dayData?.filter((item) => item.state === "Upcoming");
  const helpdeskDayDataOpen = dayData?.filter((item) => item.state === "Open");
  const helpdeskDayDataClosed = dayData?.filter((item) => item.state === "Customer Closed");
  const daySignedOffdData = dayData?.filter((item) => item.state === "signed Off");
  const dayReportedData = dayData?.filter((item) => item.state === "Reported");
  const dayAcknowledgedData = dayData?.filter((item) => item.state === "Acknowledged");
  const dayAssessedData = dayData?.filter((item) => item.state === "Assessed");
  const dayRecommendedData = dayData?.filter((item) => item.state === "Recommended");
  const dayresolveddData = dayData?.filter((item) => item.state === "Resolved");
  const dayValidatedData = dayData?.filter((item) => item.state === "Validated");
  const dayPassedData = dayData?.filter((item) => item.state === "Passed");
  const dayCancelledData = dayData?.filter((item) => item.state === "Cancelled");
  const dayHelpInProgressData = dayData?.filter((item) => item.state === "In Progress");
  const dayHelpCancelledData = dayData?.filter((item) => item.state === "Cancelled");
  const dayHelpOnHoldData = dayData?.filter((item) => item.state === "On Hold");

  const onHandleHourElapsed = (value: boolean) => {
    setOneHourElapsed(value);
  };

  const onHandleElapsed = (value: boolean) => {
    setElapsed(value);
  };

  const onHandleStatus = (value: string) => {
    setStatus(value);
  };

  const onHandleFilterBy = (value: string) => {
    setFilterBy(value);

    if (value === 'dw.mvw_ppm_scheduler_week') {
      setActiveTab('Week');
    }
  };

  const onHandleTeam = (value: string) => {

    setTeam(value);
  }

  const onHandleCompany = (value: string) => {
    setActiveCompany(value);
  };
  const onHandleCompanyId = (value: number) => {
    setActiveCompanyId(value);
  };
  const onHandleState = (value: string) => {
    setActiveState(value);
  };
  const pendingGraphData = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    }
    const helpDeskURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],"%26",["state","=","Open"],["company","=","${activeCompany}"]]&model=dw.mvw_helpdesk_tickets&fields=["create_date"]&groupby=["create_date:day"]`;
    const inspectionURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["date",">=","${startDate}"],["date","<=","${endDate}"],"%26",["state","=","Missed"],["company","=","${activeCompany}"]]&model=dw.mvw_inspection_checklist&fields=["date"]&groupby=["date:day"]`;
    const ppmsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["starts_on",">=","${startDate}"],["ends_on","<=","${endDate}"],"%26",["state","=","Missed"],["company","=","${activeCompany}"]]&model=dw.mvw_ppm_scheduler_week&fields=["starts_on"]&groupby=["starts_on:day"]`;
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Reported"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[0].value) {
      URL = inspectionURL;
      setDateKey("date:day");
      setDateCount("date_count");
    } else if (filterBy === operationsFilterByItems[1].value) {
      URL = ppmsURL;
      setDateKey("starts_on:day");
      setDateCount("starts_on_count");
    } else if (filterBy === operationsFilterByItems[2].value) {
      URL = helpDeskURL;
      setDateKey("create_date:day");
      setDateCount("create_date_count");
    } else if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");
    }
    const config = {
      method: "get",
      url: URL,
      headers: {
        Authorization: `Bearer ${accessTokenOddo16}`,
      },
    };
    const response = await axios(config);
    if (response?.status === 200) {
      setOpenGraphData(response?.data);
    }
  };
  useEffect(() => {
    if (filterBy) {
      pendingGraphData();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const closedGraphData = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    }

    const helpDeskURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],"%26",["state","ilike","Closed"],["company","=","${activeCompany}"]]&model=dw.mvw_helpdesk_tickets&fields=["create_date"]&groupby=["create_date:day"]`;
    const inspectionURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["date",">=","${startDate}"],["date","<=","${endDate}"],"%26",["state","=","Completed"],["company","=","${activeCompany}"]]&model=dw.mvw_inspection_checklist&fields=["date"]&groupby=["date:day"]`;
    const ppmsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["starts_on",">=","${startDate}"],["ends_on","<=","${endDate}"],"%26",["state","=","Completed"],["company","=","${activeCompany}"]]&model=dw.mvw_ppm_scheduler_week&fields=["starts_on"]&groupby=["starts_on:day"]`;
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Signed off"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[0].value) {
      URL = inspectionURL;
      setDateKey("date:day");
      setDateCount("date_count");
    } else if (filterBy === operationsFilterByItems[1].value) {
      URL = ppmsURL;
      setDateKey("starts_on:day");
      setDateCount("starts_on_count");
    } else if (filterBy === operationsFilterByItems[2].value) {
      URL = helpDeskURL;
      setDateKey("create_date:day");
      setDateCount("create_date_count");
    } else if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");
    }
    const config = {
      method: "get",
      url: URL,
      headers: {
        Authorization: `Bearer ${accessTokenOddo16}`,
      },
    };
    const response = await axios(config);
    if (response?.status === 200) {
      setClosedGraphData(response?.data);
    }
  };
  useEffect(() => {
    if (filterBy) {
      closedGraphData();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);
  const upcomingGraphData = async () => {
    try {
      let URL = "";
      let dateKey = "";
      let dateCount = "";

      if (!companyList) {
        return;
      }

      const company = companyList.find((company: any) => company.displayText === activeCompany);



      if (filterBy === operationsFilterByItems[0].value) {
        URL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["date",">=","${startDate}"],["date","<=","${endDate}"],"%26",["state","=","Upcoming"],["company","=","${activeCompany}"]]&model=dw.mvw_inspection_checklist&fields=["date"]&groupby=["date:day"]`;;
        dateKey = "date:day";
        dateCount = "date_count";
      } else if (filterBy === operationsFilterByItems[1].value) {
        URL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["starts_on",">=","${startDate}"],["ends_on","<=","${endDate}"],"%26",["state","=","Upcoming"],["company","=","${activeCompany}"]]&model=dw.mvw_ppm_scheduler_week&fields=["starts_on"]&groupby=["starts_on:day"]`;
        dateKey = "starts_on:day"
        dateCount = "starts_on_count"
      }
      if (!URL) {
        return;
      }

      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };

      const { status, data } = await axios(config);

      if (status === 200) {
        setUpcomingGraphData(data);
      } else {
        console.error('Request failed with status:', status);
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }

  }
  useEffect(() => {
    if (filterBy) {
      upcomingGraphData();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);


  const inProgress = async () => {
    try {
      let URL = "";
      let dateKey = "";
      let dateCount = "";

      if (!companyList) {
        return;
      }

      const company = companyList.find((company: any) => company.displayText === activeCompany);

      if (filterBy === operationsFilterByItems[1].value) {
        URL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["starts_on",">=","${startDate}"],["ends_on","<=","${endDate}"],"%26",["state","=","In Progress"],["company","=","${activeCompany}"]]&model=dw.mvw_ppm_scheduler_week&fields=["starts_on"]&groupby=["starts_on:day"]`;
        dateKey = "starts_on:day";
        dateCount = "starts_on_count";
      } else if (filterBy === operationsFilterByItems[2].value) {
        URL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],"%26",["state","ilike","In Progress"],["company","=","${activeCompany}"]]&model=dw.mvw_helpdesk_tickets&fields=["create_date"]&groupby=["create_date:day"]`;
        dateKey = "create_date:day";
        dateCount = "create_date_count";
      }

      if (!URL) {
        return;
      }

      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };

      const { status, data } = await axios(config);

      if (status === 200) {
        setInProgressGraphData(data);
      } else {
        console.error('Request failed with status:', status);
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };

  useEffect(() => {
    if (filterBy) {
      inProgress();
    }
  }, [filterBy, activeCompany, startDate, endDate]);

  const acknowledgedGraph = async () => {
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    }

    if (filterBy === operationsFilterByItems[3].value && company) {
      const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Acknowledged"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;

      const config = {
        method: "get",
        url: incidentsURL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };

      try {
        const { status, data } = await axios(config);
        if (status === 200) {
          setAcknowledged(data);
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
  };

  useEffect(() => {
    if (filterBy) {
      acknowledgedGraph();
    }
  }, [filterBy, activeCompany, startDate, endDate]);

  const setAssessedGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Assessed"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      try {
        const { status, data } = await axios(config);
        if (status === 200) {
          setAssessed(data);
        }
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      setAssessedGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const SetRecommendedGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Recommended"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        SetRecommended(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      SetRecommendedGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);


  const setResolvedGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Resolved"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setResolved(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      setResolvedGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const setValidatedGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Validated"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setValidated(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      setValidatedGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const setpassedGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Paused"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setpassed(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      setpassedGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const setCancelledGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const incidentsURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["incident_on",">=","${startDate}"],["incident_on","<=","${endDate}"],"%26",["state","=","Cancelled"],["company","=","${activeCompany}"]]&model=dw.mvw_hx_incident_view&fields=["incident_on"]&groupby=["incident_on:day"]`;
    if (filterBy === operationsFilterByItems[3].value) {
      URL = incidentsURL;
      setDateKey("incident_on:day");
      setDateCount("incident_on_count");
      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setCancelled(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      setCancelledGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);


  const HelpdeskCancelledGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const helpdeskURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],"%26",["state","ilike","Cancelled"],["company","=","${activeCompany}"]]&model=dw.mvw_helpdesk_tickets&fields=["create_date"]&groupby=["create_date:day"]`;
    if (filterBy === operationsFilterByItems[2].value) {
      URL = helpdeskURL;
      setDateKey("create_date:day");
      setDateCount("create_date_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setHelpdeskCancelled(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      HelpdeskCancelledGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const HelpdeskOnHoldGraph = async () => {
    let URL = "";
    let company;

    if (companyList) {
      company = companyList?.filter(
        (company: any) => company?.displayText === activeCompany
      );
    };
    const helpdeskURL = `${WEBAPPAPIURL}v2/read_group?domain=["%26","%26",["create_date",">=","${startDate}"],["create_date","<=","${endDate}"],"%26",["state","ilike","On Hold"],["company","=","${activeCompany}"]]&model=dw.mvw_helpdesk_tickets&fields=["create_date"]&groupby=["create_date:day"]`;
    if (filterBy === operationsFilterByItems[2].value) {
      URL = helpdeskURL;
      setDateKey("create_date:day");
      setDateCount("create_date_count");


      const config = {
        method: "get",
        url: URL,
        headers: {
          Authorization: `Bearer ${accessTokenOddo16}`,
        },
      };
      const response = await axios(config);
      if (response?.status === 200) {
        setHelpdeskOnHold(response?.data);
      }
    }
  };
  useEffect(() => {
    if (filterBy) {
      HelpdeskOnHoldGraph();
    }
  }, [filterBy, filterBy, activeCompany, startDate, endDate]);

  const navigate = useNavigate();
  const handleTab = (tab: string) => {
    setActiveTab(tab);
  };
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const dayNames = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];
  const currentDate = new Date();
  const day = dayNames[currentDate.getDay()];
  const month = monthNames[currentDate.getMonth()];
  const year = currentDate.getFullYear();
  const date = currentDate.getDate();
  const currentGraphdate = `${day}, ${month} ${date}, ${year}`;
  const currentYear = new Date().getFullYear();
  const changedDate = new Date(
    `${currentYear} ${selctedDate}`
  ).toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
  return (
    <div className="operations-box">
      <div className="log-out-box" onClick={() => { }}>
        <button className="arrow-btn">
          {/* <AiOutlineLogout size={20} className="arrow-icon" />{" "} */}
        </button>
      </div>
      <OperationsFilter
        // teamsData={data?.data?.teamCount}
        handleLeftArrowClick={handleLeftArrowClick}
        handleRightArrowClick={handleRightArrowClick}
        startDate={startDate}
        endDate={endDate}
        setStartDate={setStartDate}
        setEndDate={setEndDate}
        activeTab={activeTab}
        handleTab={handleTab}
        statusValue={status}
        statusHandle={onHandleStatus}
        filterByValue={filterBy}
        filterByHandle={onHandleFilterBy}
        teamValue={team}
        teamHandle={onHandleTeam}
        elapsed={elapsed}
        elapsedHandle={onHandleElapsed}
        hourElapsed={oneHourElapsed}
        hourElapsedHandle={onHandleHourElapsed}
        companyList={companyList || []}
        activeCompany={activeCompany}
        companyHandle={onHandleCompany}
        activeCompanyId={activeCompanyId}
        companyIdHandle={onHandleCompanyId}
        // stateList={states}
        activeState={activeState}
        stateHandle={onHandleState}
        setSelectedData={setSelectedData}
        setSelectedDate={setSelectedDate}
        startDateOne={startDateOne}
        endDateOne={endDateOne}
      />
      {operationsTabs[0].displayText === activeTab && (
        <DayCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          startDate={startDate}
          endDate={endDate}

        />
      )}
      {operationsTabs[1].displayText === activeTab && ((filterBy !== operationsFilterByItems[2].value)) && ((filterBy !== operationsFilterByItems[3].value)) && (
        <WeekCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
          startDate={startDate}
          selctedDate={selctedDate}
          currentTime={currentTime}

        />
      )}
      {operationsTabs[2].displayText === activeTab && ((filterBy !== operationsFilterByItems[1].value)) && ((filterBy !== operationsFilterByItems[2].value)) && ((filterBy !== operationsFilterByItems[3].value)) && (
        <MonthCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
          startDate={startDate}
          selctedDate={selctedDate}
        />
      )}
      {((operationsTabs[0].displayText !== activeTab) && (filterBy === operationsFilterByItems[1].value)) && (
        <PpmCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
        />
      )}
      {((operationsTabs[1].displayText === activeTab) && (filterBy === operationsFilterByItems[1].value)) && (
        <PpmWeekCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
        />
      )}
      {(((operationsTabs[1].displayText === activeTab) && (filterBy === operationsFilterByItems[2].value)) || ((operationsTabs[1].displayText === activeTab) && (filterBy === operationsFilterByItems[3].value))) && (
        <HelpdeskWeekCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
        />
      )}
      {(((operationsTabs[2].displayText === activeTab) && (filterBy === operationsFilterByItems[2].value)) || ((operationsTabs[2].displayText === activeTab) && (filterBy === operationsFilterByItems[3].value))) && (
        <HelpdeskMonthCalendar
          data={tasksData}
          elapsed={elapsed}
          hourElapsed={oneHourElapsed}
          selectedData={selectedData}
        />
      )}
      {((operationsTabs[0].displayText !== activeTab) && (filterBy !== operationsFilterByItems[1].value) && (filterBy !== operationsFilterByItems[2].value) && (filterBy !== operationsFilterByItems[3].value)) && (
        <OperationsChart
          pendingData={opengraphData}
          dateKey={dateKey}
          countKey={dateCount}
          closedData={closedgraphData}
          upcomingData={upcominggraphData}
          startDate={startDate}
          endDate={endDate}
          setSelectedData={setSelectedData}
          setSelectedDate={setSelectedDate}
          setStartDateOne={setStartDateOne}
          setEndDateOne={setEndDateOne}
          statusValue ={status}

        />
      )}
      {(operationsTabs[0].displayText !== activeTab && filterBy === operationsFilterByItems[2].value) && (
        <HelpdeskMandWChart
          pendingData={opengraphData}
          dateKey={dateKey}
          countKey={dateCount}
          closedData={closedgraphData}
          Helpdeskcancelled={Helpdeskcancelled}
          HelpdeskOnHold={HelpdeskOnHold}
          inprogressData={inProgressgraphData}
          startDate={startDate}
          endDate={endDate}
          setSelectedData={setSelectedData}
          setSelectedDate={setSelectedDate}
          setStartDateOne={setStartDateOne}
          setEndDateOne={setEndDateOne}
          statusValue ={status}
        />
      )}
      {((operationsTabs[0].displayText !== activeTab) && (filterBy === operationsFilterByItems[3].value)) && (
        <IncidentChart
          pendingData={opengraphData}
          dateKey={dateKey}
          countKey={dateCount}
          closedData={closedgraphData}
          // upcomingData={upcominggraphData}
          startDate={startDate}
          endDate={endDate}
          setSelectedData={setSelectedData}
          setSelectedDate={setSelectedDate}
          setStartDateOne={setStartDateOne}
          setEndDateOne={setEndDateOne}
          acknowledged={acknowledged}
          assessed={assessed}
          recommended={recommended}
          resolved={resolved}
          validated={validated}
          passed={passed}
          cancelled={cancelled}
          statusValue ={status}
        />
      )}
      {((operationsTabs[0].displayText !== activeTab) && (filterBy === operationsFilterByItems[1].value)) && (
        <PpmChart
          pendingData={opengraphData}
          dateKey={dateKey}
          countKey={dateCount}
          closedData={closedgraphData}
          upcomingData={upcominggraphData}
          inprogressData={inProgressgraphData}
          dayData={dayData}
          startDate={startDate}
          endDate={endDate}
          setSelectedData={setSelectedData}
          setSelectedDate={setSelectedDate}
          setStartDateOne={setStartDateOne}
          setEndDateOne={setEndDateOne}
          statusValue ={status}
        />
      )}
      {operationsTabs[0].displayText === activeTab && (filterBy === operationsFilterByItems[0].value) && (
        <DayOperationsChart
          pendingData={daymissedData}
          closedData={daycompletedData}
          upcomingData1={dayupcomingData}
          startDate={startDate}
          endDate={endDate}
          statusValue ={status}
        />
      )}
      {operationsTabs[0].displayText === activeTab && (filterBy === operationsFilterByItems[3].value) && (
        <IncidentDayChart
          signedOff={daySignedOffdData}
          reported={dayReportedData}
          acknowledged={dayAcknowledgedData}
          assessed={dayAssessedData}
          recommended={dayRecommendedData}
          resolved={dayresolveddData}
          validated={dayValidatedData}
          passed={dayPassedData}
          cancelled={dayCancelledData}
          startDate={startDate}
          endDate={endDate}
          statusValue ={status}
        />
      )}
      {operationsTabs[0].displayText === activeTab && (filterBy === operationsFilterByItems[2].value) && (
        <HelpdeskDayDayChart
          dayHelpInProgressData={dayHelpInProgressData}
          dayHelpCancelledData={dayHelpCancelledData}
          dayHelpOnHoldData={dayHelpOnHoldData}
          helpdeskDayDataOpen={helpdeskDayDataOpen}
          helpdeskDayDataClosed={helpdeskDayDataClosed}
          startDate={startDate}
          endDate={endDate}
          statusValue ={status}

        />
      )}
      {operationsTabs[0].displayText !== activeTab && (<div style={{ position: "absolute", top: 490 }}><h1 className="o-date currentDate">{selctedDate !== null ? changedDate : latestDate ? currentGraphdate : null}</h1></div>)}
      <div className="arrows-box">
        <button onClick={() => navigate("/dashboard")} className="arrow-btn">
          <BiLeftArrow size={20} className="arrow-icon" />{" "}
        </button>
        <button onClick={() => navigate("/")} className="arrow-btn">
          <BiRightArrow size={20} className="arrow-icon" />{" "}
        </button>
      </div>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loader}
        invisible
      >
        <CircularProgress color="primary" />
      </Backdrop>
      <SnackBar error={err} errorText={errMsg} />
    </div>
  );
};

export default Operations;
