export type DropDownProps = {
  items?: {
    id: number;
    displayText: string;
    value?: string;
  }[];
  placeHolder?: string;
  isDisabled?: boolean;
  onHandleStatus?: (value: string) => void;
  handleGlobalItemClick?: (value: object) => void;
  value?: string;
  onHandleCompanyId?: (value: number) => void;
 shouldShowPlaceholder?: boolean;
 floatingLabel?:any;
 

  
};

export type CompanyType = {
  id: number;
  displayText: string;
  value: string;
};

export type StateType = {
  id: number;
  displayText: string;
  value: string;
};

export type OperationsFilterProps = {
  handleLeftArrowClick: any;
  handleRightArrowClick: any;
  startDate: any;
  endDate: any;
  setStartDate: any;
  setEndDate: any;
  activeTab: string;
  handleTab: (tab: string) => void;
  teamsData?: any;
  statusValue?: string;
  statusHandle?: (value: string) => void;
  filterByValue?: string;
  filterByHandle?: (value: string) => void;
  teamValue?: string;
  teamHandle?: (value: string) => void;
  companyList: CompanyType[];
  activeCompany?: string;
  companyHandle?: (value: string) => void;
  elapsed?: boolean;
  elapsedHandle?: (value: boolean) => void;
  hourElapsed?: boolean;
  hourElapsedHandle?: (value: boolean) => void;
  activeCompanyId?: number | undefined;
  companyIdHandle?: (value: number) => void;
  stateList?: StateType[];
  activeState?: string;
  stateHandle?: (value: string) => void;
  setSelectedData?: any;
  setStartDateOne?: any;
  setendDateOne?: any;
  startDateOne?: any;
  endDateOne?: any;
  setSelectedDate?: any;
 
};

type TicketCardType = {
  check_list_id: (string | number)[];
  company_id: (string | number)[];
  end_datetime: string;
  hx_inspection_list: (string | number)[];
  id: number;
  maintenance_team_id: (string | number)[];
  order_id: boolean;
  order_state: boolean;
  date: string;
  status: string;
  subject: string;
};

export type DayCalendarProps = {
  data?: any;
  elapsed?: boolean;
  hourElapsed?: boolean;
  startDate?:any;
  setCurrentTimeSlot?: any;
  currentTimeSlot?: any;
  endDate?: any;
  
};

export type WeekCalendarProps = {
  data?: TicketCardType[];
  elapsed?: boolean;
  hourElapsed?: boolean;
  selectedData?: any;
  setselectedData?: any;
  startDate?: any;
  selctedDate?: any;
  currentTime?: any;
};

export type MonthCalendarProps = {
  data?: TicketCardType[];
  elapsed?: boolean;
  hourElapsed?: boolean;
  selectedData?: any;
  startDate?: any;
  selctedDate?: any;
};

export type TicketCardProps = {
  styles?: {
    left: number | string;
    top: number | string;
    height: number | string;
    width?: number | string;
  };
  data?: {
    id: number;
    startDate: string;
    endDate: string;
    state: string;
    subject: string;
    maintenanceTeam: (string | number)[];
    plannedSla?: string;
    space_name?: any;
    equipment_name?: any;
    date_execution?:any;
    checklist_json_data?: any;

  };
  isInspection ?: boolean;
};

export type PillProps = {
  status?: string;
};

export type ChartDataType = {
  dates: string[];
  pending?: any;
  closed?: any;
  state?: any
};



export type ChartDataProps = {
  pendingData?: ChartDataType;
  closedData?: ChartDataType;
  upcomingData?: ChartDataType;
  Helpdeskcancelled?: ChartDataType;
  HelpdeskOnHold?: ChartDataType;
  inprogressData?: ChartDataType;
  startDate?: string;
  endDate?: string;
  dateKey?: string;
  countKey?: number;
  setSelectedData?: any;
  setSelectedDate?: any;
  upcomingData1?: any;
  setStartDateOne?: any;
  setEndDateOne?: any;
  dayData?:any;
  signedOff?: any;
  reported?: any;
  acknowledged?: any ,
    assessed?: any ,
    recommended?: any ,
    resolved?: any ,
    validated?: any,
    passed?: any ,
    cancelled?: any 
    dayHelpInProgressData?: any,
        dayHelpCancelledData?: any,
        dayHelpOnHoldData?: any,
        daymissedData?: any,
        daycompletedData?: any,
        helpdeskDayDataOpen?: any,
          helpdeskDayDataClosed?: any,
          statusValue?: any
        
};

export type SnackbarType = {
  error?: any;
  errorText?: string;
};
