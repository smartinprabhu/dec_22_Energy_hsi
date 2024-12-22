import datetime
from datetime import datetime, timedelta

import pandas as pd
import pytz
import pandas as pd
from datetime import datetime, timedelta
import pytz

from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
def cal_met_day(energy_data_all,cost_per_kw):
    
    
    # Get the current date
    current_date = datetime.now().date()

    # Filter the DataFrame for the current day's data
    current_day_data = energy_data_all[energy_data_all['ds'].dt.date == current_date]
    today_total=current_day_data['y'].sum()

    yesterday_date = datetime.now().date() - timedelta(days=1)

    # Filter the DataFrame for yesterday's data
    yesterday_data = energy_data_all[energy_data_all['ds'].dt.date == yesterday_date]
    total_yesterday_consumption=yesterday_data['y'].sum()

    current_datetime = datetime.now()

    current_day_data_so_far = energy_data_all[
        (energy_data_all['ds'].dt.date == current_datetime.date()) &
        (energy_data_all['ds'].dt.hour <= current_datetime.hour)
    ]
    total_today_consumption_so_far= current_day_data_so_far['y'].sum()
    estimated_cost_today = today_total * cost_per_kw 

    emission_factor = 0.87
    emission_hour = (today_total * emission_factor) / 1000


    rate_of_change_hour = (
        (today_total - total_yesterday_consumption) / total_yesterday_consumption
    ) * 100
    if rate_of_change_hour >= 0:
        rate_of_change_hour = (rate_of_change_hour)
    else:
        rate_of_change_hour =(rate_of_change_hour)
    # total_yesterday_consumption = f"{total_yesterday_consumption:.2f} kWh"
    # today_total = f"{today_total:.2f} kWh"
    # emission_hour = f"{emission_hour:.2f} tCO2e"
    # total_today_consumption_so_far = f"{total_today_consumption_so_far:.2f} kWh"

    return     total_yesterday_consumption,total_today_consumption_so_far,today_total,rate_of_change_hour,estimated_cost_today,emission_hour

def cal_met_week(df_daily,tz,cost_per_kw):
    


    # Assuming df_daily is your DataFrame and it has a 'date' column
    # Convert 'date' column to datetime format if it's not already
    df_daily['ds'] = pd.to_datetime(df_daily['ds'])

    # Get the current date with timezone info (Asia/Kolkata)
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Calculate the start of the current week (Monday) with timezone info
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current week (Sunday) with timezone info
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter the DataFrame for the current week's data
    current_week_data = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_week)]
    current_week_total= current_week_data['y'].sum()
    # Assuming df_daily is your DataFrame and it has a 'date' column
    # Convert 'date' column to datetime format if it's not already
    df_daily['ds'] = pd.to_datetime(df_daily['ds'])

    # Get the current date with timezone info (Asia/Kolkata)


    # Calculate the start of the current week (Monday) with timezone info
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # The end date is today with the current time
    end_of_today = current_date

    # Filter the DataFrame for the current week's data up to today
    current_week_data_up_to_today = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_today)]

 

    total_current_week_consumption_so_far =  current_week_data_up_to_today['y'].sum()

    # Calculate the start of the current week (Monday) with timezone info
    start_of_current_week = current_date - timedelta(days=current_date.weekday())
    start_of_current_week = start_of_current_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the start of the previous week (Monday) with timezone info
    start_of_previous_week = start_of_current_week - timedelta(days=7)

    # Calculate the end of the previous week (Sunday) with timezone info
    end_of_previous_week = start_of_current_week - timedelta(seconds=1)

    # Filter the DataFrame for the previous week's data
    previous_week_data = df_daily[(df_daily['ds'] >= start_of_previous_week) & (df_daily['ds'] <= end_of_previous_week)]

    total_previous_week_consumption = previous_week_data['y'].sum()  # Previous week total



    rate_of_change_week = (
        (current_week_total - total_previous_week_consumption)
        / total_previous_week_consumption
    ) * 100

    if rate_of_change_week >= 0:
        rate_of_change_week = (rate_of_change_week) 
    else:
        rate_of_change_week = (rate_of_change_week)
    emission_factor = 0.87
    emission_week = (current_week_total * emission_factor) / 1000
    estimated_cost_current_week = current_week_total * cost_per_kw 
    # emission_week = (emission_week:.2f
    # total_previous_week_consumption = f"{total_previous_week_consumption:.2f} kWh"
    # total_current_week_consumption_so_far = f"{total_current_week_consumption_so_far:.2f} kWh"
    # current_week_total = f"{current_week_total:.2f} kWh"
    return total_previous_week_consumption,total_current_week_consumption_so_far,current_week_total,rate_of_change_week,estimated_cost_current_week,emission_week
def cal_met_month(df_daily,tz,cost_per_kw):
    current_datetime = datetime.now(tz)
    # Calculate the start of the current month

    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current month
    if current_datetime.month == 12:
        end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(seconds=1)
    else:
        end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(seconds=1)

    # Ensure both are timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))
    end_of_month = tz.localize(end_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's datacurrent_datetime
    current_month_data = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= end_of_month)
    ]
    current_month_total=current_month_data['y'].sum() #### 1 curent month total
    # Calculate the start of the previous month
    start_of_previous_month = (current_datetime.replace(day=1) - relativedelta(months=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the previous month
    end_of_previous_month = (current_datetime.replace(day=1) - timedelta(seconds=1)).replace(hour=23, minute=59, second=59)

    # Ensure both are timezone-aware
    start_of_previous_month = tz.localize(start_of_previous_month.replace(tzinfo=None))
    end_of_previous_month = tz.localize(end_of_previous_month.replace(tzinfo=None))

    # Filter the DataFrame for the previous month's data
    previous_month_data = df_daily[
        (df_daily['ds'] >= start_of_previous_month) & (df_daily['ds'] <= end_of_previous_month)
    ]
    total_previous_month_consumption=previous_month_data['y'].sum() #### 2 previous month total
    current_datetime = datetime.now(tz)

    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Ensure the start of the month is timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's data up to today
    current_month_data_up_to_today = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= current_datetime)
    ]
    total_current_month_consumption_so_far=current_month_data_up_to_today['y'].sum() ### 3 so far this  month
    rate_of_change_month = (
        (current_month_total - total_previous_month_consumption)
        / total_previous_month_consumption
    ) * 100
    if rate_of_change_month >= 0:
        rate_of_change_month = (rate_of_change_month)
    else:
        rate_of_change_month = (rate_of_change_month)
    
    estimated_cost_current_month = current_month_total * cost_per_kw 
    # total_current_month_consumption_so_far = f"{total_current_month_consumption_so_far:.2f} kWh"
    # total_previous_month_consumption = f"{total_previous_month_consumption:.2f} kWh"

    emission_factor = 0.87
    emission_month = (current_month_total * emission_factor) / 1000
    # current_month_total = f"{current_month_total:.2f} kWh"
    # emission_month = f"{emission_month:.2f} tCO2e"
    return total_previous_month_consumption,total_current_month_consumption_so_far,current_month_total,rate_of_change_month,estimated_cost_current_month,emission_month
def cal_met_year(df_monthly,cost_per_kw):


    # Get the current year
    current_year = datetime.now().year

    df_current_year = df_monthly[df_monthly['ds'].dt.year == current_year]
    current_year_total=df_current_year['y'].sum() 

    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Filter the dataframe to get data up to the current month
    df_current_year_month = df_current_year[(df_current_year['ds'].dt.year <= current_year) & (df_current_year['ds'].dt.month <= current_month)]
    total_current_year_consumption_so_far=df_current_year_month['y'].sum()


    # Get the current year
    current_year = datetime.now().year

    # Get the previous year
    previous_year = current_year - 1

    # Filter the dataframe to get data for the previous year
    df_previous_year = df_monthly[df_monthly['ds'].dt.year == previous_year]
    total_previous_year_consumption=df_previous_year['y'].sum() #### 3

    # Calculate the rate of change
    rate_of_change_year = (
        (current_year_total - total_previous_year_consumption) / total_previous_year_consumption
    ) * 100
    estimated_cost_current_year=current_year_total*cost_per_kw
    if rate_of_change_year >= 0:
        rate_of_change_year = (rate_of_change_year)
    else:
        rate_of_change_year = (rate_of_change_year)
    emission_factor = 0.87
    emission_current_year = (current_year_total * emission_factor) / 1000
    # emission_current_year = f"{emission_current_year:.2f} tCO2e"
    # total_previous_year_consumption = f"{total_previous_year_consumption:.2f} kWh"
    # total_current_year_consumption_so_far = f"{total_current_year_consumption_so_far:.2f} kWh"
    # current_year_total = f"{current_year_total:.2f} kWh"
    return total_previous_year_consumption,total_current_year_consumption_so_far,current_year_total,rate_of_change_year,estimated_cost_current_year,emission_current_year

def cal_met_workweek(df_workweek,tz,cost_per_kw):

    # Get the current date and time in the specified timezone
    current_datetime = datetime.now(tz)

    # energy_data_alld the start of the week (Sunday) in the specified timezone
    start_of_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # energy_data_alld the end of the week (Saturday) in the specified timezone
    end_of_week = start_of_week + timedelta(days=6)

    # Convert both to timezone-aware datetimes
    start_of_week = tz.localize(start_of_week.replace(tzinfo=None))
    end_of_week = tz.localize(end_of_week.replace(tzinfo=None))

    # Filter the DataFrame for the current week's data
    weekly_data_workweek = df_workweek[
        (df_workweek['ds'] >= start_of_week) & (df_workweek['ds'] <= end_of_week)
    ]
    current_workweek_total=weekly_data_workweek['y'].sum() 

    # energy_data_alld the start of the week (Sunday) in the specified timezone
    start_of_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # Ensure start_of_week is timezone-aware
    start_of_week = tz.localize(start_of_week.replace(tzinfo=None))

    # Filter the DataFrame for the current week's data up to today
    workweek_data_up_to_today = df_workweek[
        (df_workweek['ds'] >= start_of_week) & (df_workweek['ds'] <= current_datetime)]
    total_current_workweek_consumption_so_far=workweek_data_up_to_today['y'].sum()
    start_of_current_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # Calculate the start and end of last week
    start_of_last_week = start_of_current_week - timedelta(days=7)
    end_of_last_week = start_of_current_week - timedelta(seconds=1) 

    # Ensure both are timezone-aware
    start_of_last_week = tz.localize(start_of_last_week.replace(tzinfo=None))
    end_of_last_week = tz.localize(end_of_last_week.replace(tzinfo=None))

    # Filter the DataFrame for last week's data
    last_workweek_data = df_workweek[
        (df_workweek['ds'] >= start_of_last_week) & (df_workweek['ds'] <= end_of_last_week)
        
    ]
    total_previous_workweek_consumption=last_workweek_data['y'].sum()
    rate_of_change_workweek = (
        (current_workweek_total - total_previous_workweek_consumption)
        / total_previous_workweek_consumption
    ) * 100
    emission_factor = 0.87
    emission_workweek = (current_workweek_total * emission_factor) / 1000
    emission_workweek = f"{emission_workweek:.2f} tCO2e"
    # if rate_of_change_workweek >= 0:
    #     rate_of_change_workweek = f"{rate_of_change_workweek:.2f} % ▲   "
    # else:
    #     rate_of_change_workweek = f"{rate_of_change_workweek:.2f} % ▼    "

    estimated_cost_current_workweek=current_workweek_total*cost_per_kw
    # total_previous_workweek_consumption = f"{total_previous_workweek_consumption:.2f} kWh"
    # total_current_workweek_consumption_so_far = f"{total_current_workweek_consumption_so_far:.2f} kWh"
    # current_workweek_total = f"{current_workweek_total:.2f} kWh"
    return total_previous_workweek_consumption,total_current_workweek_consumption_so_far,current_workweek_total,rate_of_change_workweek,estimated_cost_current_workweek,emission_workweek

def cal_met_weekend(forecast_data_weekend_cal, historical_data_daily, df_daily, cost_per_kw):
    current_weekend_total = forecast_data_weekend_cal['y'].sum()
    last_weekend = historical_data_daily[historical_data_daily['ds'].dt.weekday >= 5].iloc[-3:-1]
    total_previous_weekend_consumption = last_weekend['y'].sum()

    # Get the current weekend's data
    today = pd.Timestamp.today().date()
    current_weekend_s = df_daily[(df_daily['ds'].dt.date >= today - pd.Timedelta(days=today.weekday() - 5)) & 
                                 (df_daily['ds'].dt.date <= today)]
    total_current_weekend_consumption_so_far = current_weekend_s['y'].sum()

    rate_of_change_weekend = 0
    if total_previous_weekend_consumption > 0:  # To avoid division by zero
        rate_of_change_weekend = (
            (current_weekend_total - total_previous_weekend_consumption)
            / total_previous_weekend_consumption
        ) * 100

    # if rate_of_change_weekend >= 0:
    #     rate_of_change_weekend = f"{rate_of_change_weekend:.2f}  ▲   "
    # else:
    #     rate_of_change_weekend = f"{rate_of_change_weekend:.2f}  ▼  "


    estimated_cost_current_weekend = current_weekend_total * cost_per_kw

    emission_factor = 0.87
    emission_weekend = (current_weekend_total * emission_factor) / 1000
    # emission_weekend = f"{emission_weekend:.2f} tCO2e"
    # total_previous_weekend_consumption = f"{total_previous_weekend_consumption:.2f} kWh"
    # total_current_weekend_consumption_so_far = f"{total_current_weekend_consumption_so_far:.2f} kWh"
    # current_weekend_total = f"{current_weekend_total:.2f} kWh"
    return (
        total_previous_weekend_consumption,
        total_current_weekend_consumption_so_far,
        current_weekend_total,
        rate_of_change_weekend,
        estimated_cost_current_weekend,
        emission_weekend
    )
