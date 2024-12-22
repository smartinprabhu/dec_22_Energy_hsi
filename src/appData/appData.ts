export const screenLayout = [
  {
    w: 1,
    h: 1.5,
    x: 0,
    y: 0,
    i: "a",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 1,
    y: 0,
    i: "b",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 2,
    y: 0,
    i: "c",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 0,
    y: 4,
    i: "d",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 1,
    y: 4,
    i: "e",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 3,
    x: 2,
    y: 4,
    i: "f",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 0,
    y: 8,
    i: "g",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 1,
    y: 8,
    i: "h",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 0,
    y: 12,
    i: "i",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 1,
    y: 12,
    i: "j",
    moved: false,
    static: false,
    isResizable: false,
  },
  {
    w: 1,
    h: 1.5,
    x: 2,
    y: 12,
    i: "k",
    moved: false,
    static: false,
    isResizable: false,
  },
];

export const headerGroupFilterOptions = [
  {
    id: 1,
    displayText: "7 days",
  },
  {
    id: 2,
    displayText: "1 month",
  },
  {
    id: 3,
    displayText: "3 months",
  },
];

export const operationsTabs = [
  {
    id: 1,
    displayText: "Day",
  },
  {
    id: 2,
    displayText: "Week",
  },
  {
    id: 3,
    displayText: "Month",
  },
];

export const dayCalendarData = [
  {
    displayText: "12 AM",
  },
  {
    displayText: "1 AM",
  },
  {
    displayText: "2 AM",
  },
  {
    displayText: "3 AM",
  },
  {
    displayText: "4 AM",
  },
  {
    displayText: "5 AM",
  },
  {
    displayText: "6 AM",
  },
  {
    displayText: "7 AM",
  },
  {
    displayText: "8 AM",
  },
  {
    displayText: "9 AM",
  },
  {
    displayText: "10 AM",
  },
  {
    displayText: "11 AM",
  },
  {
    displayText: "12 PM",
  },
  {
    displayText: "1 PM",
  },
  {
    displayText: "2 PM",
  },
  {
    displayText: "3 PM",
  },
  {
    displayText: "4 PM",
  },
  {
    displayText: "5 PM",
  },
  {
    displayText: "6 PM",
  },
  {
    displayText: "7 PM",
  },
  {
    displayText: "8 PM",
  },
  {
    displayText: "9 PM",
  },
  {
    displayText: "10 PM",
  },
  {
    displayText: "11 PM",
  },
];

// const currentDate: Date = new Date();

// const currentDayOfWeek: number = currentDate.getDay();

// const weekDays: string[] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun"];

// const startDate: Date = new Date(
//   currentDate.setDate(currentDate.getDate() - currentDayOfWeek)
// );

// export const weekDates: number[] = [];
// export const weekFullDates: Date[] = [];
// export const weekDaysArray: string[] = [];

// for (let i: number = 0; i < 7; i++) {
//   const date: Date = new Date(startDate);
//   date.setDate(startDate.getDate() + i);
//   weekDates.push(date.getDate());
//   weekFullDates.push(date);
//   weekDaysArray.push(weekDays[date.getDay()]);
// }

// const currentYear: number = currentDate.getFullYear();
// const currentMonth: number = currentDate.getMonth();

// const numDaysInMonth: number = new Date(
//   currentYear,
//   currentMonth + 1,
//   0
// ).getDate();
const currentDate = new Date();

const currentDayOfWeek = currentDate.getDay();

const weekDays = ["Sun","Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const startDate = new Date(currentDate);

startDate.setDate(currentDate.getDate() - currentDayOfWeek + 1);

export const weekDates: number[] = [];
export const weekFullDates: Date[] = [];
export const weekDaysArray: string[] = [];

for (let i = 0; i < 7; i++) {
  const date = new Date(startDate);
  date.setDate(startDate.getDate() + i);
  weekDates.push(date.getDate());
  weekFullDates.push(date);
  weekDaysArray.push(weekDays[date.getDay()]);
}

const currentYear = currentDate.getFullYear();
const currentMonth = currentDate.getMonth();

const numDaysInMonth = new Date(
  currentYear,
  currentMonth + 1,
  0
).getDate();


export const monthDates: number[] = [];
export const monthFullDates: Date[] = [];
export const monthDaysArray: string[] = [];

for (let i: number = 1; i <= numDaysInMonth; i++) {
  const date: Date = new Date(currentYear, currentMonth, i);
  monthDates.push(date.getDate());
  monthFullDates.push(date);
  monthDaysArray.push(date.toLocaleDateString("en-US", { weekday: "short" }));
}

export const operationsFilterByItems = [
  {
    id: 1,
    displayText: "Inspections",
    value: "dw.mvw_inspection_checklist",
  },
  {
    id: 2,
    displayText: "PPMs",
    value: "dw.mvw_ppm_scheduler_week",
  },
  {
    id: 3,
    displayText: "Helpdesk",
    value: "dw.mvw_helpdesk_tickets",
  },
  {
    id: 4,
    displayText: "Incidents",
    value: "dw.mvw_hx_incident_view",
  },
];

export const incidentsItems = [
  {
    id: 10,
    displayText: "Show all",
    value: "",
  },
  {
    id: 1,
    value: "Reported",
    displayText: "Reported",
  },
  {
    id: 2,
    value: "Acknowledged",
    displayText: "Acknowledged",
  },
  {
    id: 3,
    value: "Analyzed",
    displayText: "Assessed",
  },
  {
    id: 4,
    value: "Remediated",
    displayText: "Recommended",
  },
  {
    id: 5,
    value: "Resolved",
    displayText: "Resolved",
  },
  {
    id: 6,
    value: "Validated",
    displayText: "Validated",
  },
  {
    id: 7,
    value: "Signed off",
    displayText: "Signed off",
  },
  {
    id: 8,
    value: "Paused",
    displayText: "Paused",
  },
  {
    id: 9,
    value: "Cancelled",
    displayText: "Cancelled",
  },
];

export const ppmsItems = [{
  id: 5,
  displayText: "Show all",
  value: "",
},
{ id: 1, displayText: "Missed", value: "Missed" },
{ id: 2, displayText: "Upcoming", value: "Upcoming" },
{ id: 3, displayText: "Completed", value: "Completed" },
{id: 4,displayText: "In Progress",value: "In Progress"},]

export const maintenanceItems = [
  {
    id: 9,
    displayText: "Show all",
    value: "",
  },
  { id: 1, value: "draft", displayText: "Draft" },
  { id: 2, value: "released", displayText: "Waiting Parts" },
  { id: 3, value: "ready", displayText: "Ready to maintenance" },
  { id: 4, value: "assigned", displayText: "Assigned" },
  { id: 5, value: "in_progress", displayText: "In Progress" },
  { id: 6, value: "pause", displayText: "Pause" },
  { id: 7, value: "done", displayText: "Done" },
  { id: 8, value: "cancel", displayText: "Cancelled" },
];

export const helpdeskItems = [
  {
    id: 6,
    displayText: "Show all",
    value: "",
  },
  {
    id: 1,
    displayText: "Open",
    value: "Open",
  },
  {
    id: 2,
    displayText: "Customer Closed",
    value: "Customer Closed",
  },
  {
    id: 3,
    displayText: "In Progress",
    value: "In Progress",
  },
  {
    id: 4,
    displayText: "Cancelled",
    value: "Cancelled",
  },
  {
    id: 5,
    displayText: "On Hold",
    value: "On Hold",
  },
];

export const inspectionItems = [
  {
    id: 4,
    displayText: "Show all",
    value: "",
  },
  { id: 1, displayText: "Missed", value: "Missed" },
  { id: 2, displayText: "Upcoming", value: "Upcoming" },
  { id: 3, displayText: "Completed", value: "Completed" },
];

export const operationsTeamItems = [
  {
    id: 4,
    displayText: "Show all",
  },
  {
    id: 1,
    displayText: "Pm Team",
  },
  {
    id: 2,
    displayText: "M&E Team",
  },
  {
    id: 3,
    displayText: "Soft Service Team",
  },
];

export const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];
