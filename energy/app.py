"""Energy-Analyzer Flask API"""
import json
import pandas as pd
import pytz
from datetime import datetime, time, timedelta
from flask import Flask, Response
from flask_cors import CORS
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fig_day import fig_day
from load_data import load_and_process_data
from fig_week import fig_week
from datetime import timedelta
import pandas as pd
from fig_month import fig_month
from fig_workweek import fig_workweek
from fig_weekend import fig_weekend
from fig_year import fig_yearly
from metric import cal_met_day,cal_met_week,cal_met_month,cal_met_year,cal_met_workweek,cal_met_weekend
from process  import synthetic_algol,model_energy,model_weather,model_weather_day,weather_present,weather_present_day,model_energy_day
app = Flask(__name__)
CORS(app)


cost_per_kw = 6.09
num_days = 120

df_energy,dz_hour=load_and_process_data()
dz_hour['date'] = pd.to_datetime(dz_hour['date'])
# Assuming dz_hour is your DataFrame
# Ensure "date" column is in datetime format
dz_hour['date'] = pd.to_datetime(dz_hour['date'])

# Set the "date" column as the index
dz_hour = dz_hour.set_index('date')

# Now you can resample
dz_day = dz_hour.resample('D').mean().reset_index()
dz_hour=dz_hour.reset_index()
df_energy["Timestamp_UTC"] = pd.to_datetime(df_energy["Timestamp_UTC"], errors="coerce")

df_hour=synthetic_algol(df_energy)

energy_data_all=model_energy(df_hour)

df_daily=model_energy_day(energy_data_all)

weather_data_hour=model_weather(dz_hour)

dz_hour=weather_present(weather_data_hour)
weather_data_day=model_weather_day (dz_day)
dz_day=weather_present_day(weather_data_day)

@app.route("/forecast", methods=["POST"])
def get_energy_data():

    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    current_time_dt641=current_time_dt64+ pd.Timedelta(hours=1)
    energy_data_all["ds"] = pd.to_datetime(energy_data_all["ds"])
    if energy_data_all["ds"].dt.tz is None:
        energy_data_all["ds"] = energy_data_all["ds"].dt.tz_localize(tz)
    else:
        energy_data_all["ds"] = energy_data_all["ds"].dt.tz_convert(tz)

    dz_hour["ds"] = pd.to_datetime(dz_hour["ds"])
    if dz_hour["ds"].dt.tz is None:
        dz_hour["ds"] = dz_hour["ds"].dt.tz_localize(tz)
    else:
        dz_hour["ds"] = dz_hour["ds"].dt.tz_convert(tz)

    # Split the data into historical and forecasted
    historical_data = energy_data_all[energy_data_all["ds"] <= current_time_dt641]
    forecasted_data = energy_data_all[energy_data_all["ds"] > current_time_dt641]
    historical_data = historical_data[historical_data["ds"] >= current_time_dt641 - pd.Timedelta(days=2)]

    # Get the end of the next 24 hours
    next_24_hours_end = current_time_dt641 + timedelta(days=1)
    next_24_hours_end = pd.Timestamp(next_24_hours_end.replace(hour=23, minute=59, second=59, microsecond=999999)).tz_convert(tz)

    forecasted_bar_data = energy_data_all[
        (energy_data_all["ds"] > current_time_dt641) & (energy_data_all["ds"] <= next_24_hours_end)
    ]
    # For annotation calculation
    current_day_end = datetime.combine(current_time_dt641.date(), time(23, 59, 59, 999999)).astimezone(tz)
    forecasted_data_today = energy_data_all[
        (energy_data_all["ds"] > current_time_dt641) & (energy_data_all["ds"] <= current_day_end)
    ]

    day_plot=fig_day(historical_data,forecasted_data_today,forecasted_bar_data,dz_hour,current_time,current_time_dt641,cost_per_kw)
    
    df_daily["ds"] = pd.to_datetime(df_daily["ds"])
    if df_daily["ds"].dt.tz is None:
        df_daily["ds"] = df_daily["ds"].dt.tz_localize(tz)
    else:
        df_daily["ds"] = df_daily["ds"].dt.tz_convert(tz)

    historical_data_daily = df_daily[
        (df_daily["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (df_daily["ds"].dt.date <= current_time.date())
    ]

    next_7_days_end = current_time + timedelta(days=7)
    next_7_days_end = pd.Timestamp(next_7_days_end.replace(hour=23, minute=59, second=59, microsecond=999999)).tz_convert(tz)
    forecasted_bar_data_daily = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= next_7_days_end)
    ]

        
    end_of_week = current_time + timedelta(days=(6 - current_time.weekday()))


    next_7_days_end = end_of_week + timedelta(days=7)

    forecasted_bar_data_daily = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= next_7_days_end)
    ]

    forecasted_data_week_end = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= end_of_week)]
    week_plot=fig_week(tz, historical_data_daily,cost_per_kw, forecasted_data_week_end,next_7_days_end, forecasted_bar_data_daily, dz_day)
    
    historical_data_month = df_daily[
        (df_daily["ds"].dt.date >= (current_time - pd.Timedelta(days=59)).date())
        & (df_daily["ds"].dt.date <= current_time.date())
    ]
    # Get the current date
    current_date = pd.Timestamp.now(tz=tz)

    # Get the end of the current month
    current_month_end = pd.Timestamp(current_date.year, current_date.month + 1, 1) - pd.Timedelta(days=1)
    current_month_end = current_month_end.tz_localize(tz)
    # Get the end of the next month
    current_date = pd.Timestamp.now()  # Example current date
    next_month = (current_date.month + 1) % 12 + 1
    next_year = current_date.year + (current_date.month + 1) // 12 
    next_month_end = pd.Timestamp(next_year, next_month, 1) - pd.Timedelta(days=1)

    # Convert next_month_end to the same timezone as df_daily["ds"]
    next_month_end = next_month_end.tz_localize(tz)

    # Filter the dataframe
    forecasted_bar_data_monthly = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= next_month_end)
    ]


    forecasted_data_month_end = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= current_month_end)]

    month_plot=fig_month(tz, historical_data_month,cost_per_kw, forecasted_data_month_end,next_month_end, forecasted_bar_data_monthly, dz_day)

    # Filter dataframes for weekdays
    df_workweek = df_daily[
        df_daily["ds"]
        .dt.day_name()
        .isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    ]


    # Calculate the start date of the last two work weeks
    start_date = (current_time - pd.Timedelta(days=14)).date()

    # Select the data for the last two work weeks
    historical_data_workweek = df_workweek[
        (df_workweek["ds"].dt.date >= start_date)
        & (df_workweek["ds"].dt.date <= current_time.date())
    ]

    current_week_start = current_time - pd.Timedelta(days=current_time.weekday())
    current_week_end = current_week_start + pd.Timedelta(days=6)

    # Calculate the start and end dates of the next work week
    next_week_start = current_week_end + pd.Timedelta(days=1)
    next_week_end = next_week_start + pd.Timedelta(days=6)

    # Create a new variable that includes the current work week (after today) and the next one
    forecast_data_bar_workweek = df_workweek[
        (df_workweek["ds"].dt.date >max(current_time.date(), current_week_start.date()))
        & (df_workweek["ds"].dt.date <= next_week_end.date())
    ]

    # Create a new variable that includes the current work week (after today)
    forecast_data_workweek_cal = df_workweek[
        (df_workweek["ds"].dt.date > max(current_time.date(), current_week_start.date()))
        & (df_workweek["ds"].dt.date <= current_week_end.date())
    ]
    
    workweek_plot= fig_workweek(tz,next_week_end, forecast_data_workweek_cal,cost_per_kw, forecast_data_bar_workweek,historical_data_workweek, current_time, dz_day)


    # Calculate the start and end of the current weekend
    current_weekend_start = current_time + timedelta(days=(5 - current_time.weekday()))  # Saturday
    current_weekend_end = current_weekend_start + timedelta(days=1)  # Sunday

    # Filter the data for the current weekend
    forecast_data_weekend_1 = df_daily[
        (df_daily["ds"].dt.date >= current_weekend_start.date()) & 
        (df_daily["ds"].dt.date <= current_weekend_end.date())
    ]

    # Calculate the start and end of the next weekend
    next_weekend_start = current_weekend_start + timedelta(days=7)  # Next Saturday
    next_weekend_end = next_weekend_start + timedelta(days=1)  # Next Sunday

    # Filter the data for the next weekend
    forecast_data_weekend_cal = df_daily[
        (df_daily["ds"].dt.date >= next_weekend_start.date()) & 
        (df_daily["ds"].dt.date <= next_weekend_end.date())
    ]

    # Combine the forecast data for the current and next weekends
    forecast_data_bar_weekend = pd.concat([forecast_data_weekend_1, forecast_data_weekend_cal])

    # For historical data, filter for weekends (Saturday and Sunday)
    historical_data_weekend = historical_data_daily[historical_data_daily['ds'].dt.weekday >= 5]
    weekend_plot=fig_weekend(tz,next_weekend_end, historical_data_weekend,cost_per_kw, forecast_data_weekend_cal,forecast_data_bar_weekend, current_time, dz_day)
 
    df_monthly=energy_data_all.set_index("ds").resample('M').sum().reset_index()
    dz_month=dz_hour.set_index("ds").resample("M").mean().reset_index()
    dz_month['ds'] = pd.to_datetime(dz_month['ds'])


    # Define the end of the current month
    end_of_current_month = (current_time + relativedelta(day=31)).date()

    # Filter data up to the end of the current month
    historical_data_monthly = df_monthly[
        (df_monthly["ds"].dt.date >= (current_time - relativedelta(years=2)).date()) &
        (df_monthly["ds"].dt.date <= end_of_current_month)
    ]

    before_current_time1 = dz_month[
        (dz_month["ds"].dt.date >= (current_time - relativedelta(years=2)).date()) &
        (dz_month["ds"].dt.date <= end_of_current_month)
    ]

    # Define the start of the month after the current month
    start_of_next_month = (current_time + relativedelta(day=1, months=1)).date()

    # Define the end of the next year
    end_of_next_year = (current_time + relativedelta(years=2, day=31, month=12)).date()

    # Filter the data for the period after the current month up to the end of next year
    forecast_data_monthly = df_monthly[
        (df_monthly["ds"].dt.date >= start_of_next_month) &
        (df_monthly["ds"].dt.date <= end_of_next_year)
    ]

    after_current_time = dz_month[
        (dz_month["ds"].dt.date >= start_of_next_month) &
        (dz_month["ds"].dt.date <= end_of_next_year)
    ]

    # Define the end of the current year
    end_of_current_year = (current_time + relativedelta(day=31, month=12)).date()

    # Filter the data for the period from the start of the next month to the end of the current year
    forecast_data_until_end_of_year_cal = df_monthly[
        (df_monthly["ds"].dt.date >= start_of_next_month) &
        (df_monthly["ds"].dt.date <= end_of_current_year)
    ]
    year_plot=fig_yearly(tz,after_current_time,before_current_time1,forecast_data_until_end_of_year_cal,historical_data_monthly, forecast_data_monthly,cost_per_kw)
    
    total_yesterday_consumption,total_today_consumption_so_far,today_total,rate_of_change_hour,estimated_cost_today,emission_hour=cal_met_day(energy_data_all,cost_per_kw)
    total_previous_week_consumption,total_current_week_consumption_so_far,current_week_total,rate_of_change_week,estimated_cost_current_week,emission_week=cal_met_week(df_daily,tz,cost_per_kw)
    total_previous_month_consumption,total_current_month_consumption_so_far,current_month_total,rate_of_change_month,estimated_cost_current_month,emission_month=cal_met_month(df_daily,tz,cost_per_kw)
    total_previous_year_consumption,total_current_year_consumption_so_far,current_year_total,rate_of_change_year,estimated_cost_current_year,emission_current_year= cal_met_year(df_monthly,cost_per_kw)
    total_previous_workweek_consumption,total_current_workweek_consumption_so_far,current_workweek_total,rate_of_change_workweek,estimated_cost_current_workweek,emission_workweek=cal_met_workweek(df_workweek,tz,cost_per_kw)
    total_previous_weekend_consumption,total_current_weekend_consumption_so_far,current_weekend_total,rate_of_change_weekend,estimated_cost_current_weekend,emission_weekend=cal_met_weekend(forecast_data_weekend_cal,historical_data_daily,df_daily,cost_per_kw)

    response = ([
                        ('week', {
                    'Previous_Week': total_previous_week_consumption,
                    'Current_Week_so_far': total_current_week_consumption_so_far,
                    'Predicted_this_Week': current_week_total,
                    'Change_in_Consumption': rate_of_change_week,
                    'Estimated_Cost': estimated_cost_current_week,
                    'Predicted_Emissions': emission_week,
                    'week_plot':week_plot

                }),
                                ('Month', {
                    'Previous_Month': total_previous_month_consumption,
                    'Current_Month_so_far': total_current_month_consumption_so_far,
                    'Predicted_this_Month': current_month_total,
                    'Change_in_Consumption': rate_of_change_month,
                    'Estimated_Cost': estimated_cost_current_month,
                    'Predicted_Emissions': emission_month,
                    'month_plot':month_plot

                }),
                                
                ('Year', {
                    'Previous_Year': total_previous_year_consumption,
                    'Current_Year_so_far': total_current_year_consumption_so_far,
                    'Predicted_this_Year': current_year_total,
                    'Change_in_Consumption': rate_of_change_year,
                    'Estimated_Cost': estimated_cost_current_year,
                    'Predicted_Emissions': emission_current_year,
                    'year_plot':year_plot

                }),
        ('workweek', {
            'Previous_Workweek': total_previous_workweek_consumption,
            'Current_Workweek_so_far': total_current_workweek_consumption_so_far,
            'Predicted_this_Workweek': current_workweek_total,
            'Change_in_Consumption': rate_of_change_workweek,
            'Estimated_Cost': estimated_cost_current_workweek,
            'Predicted_Emissions': emission_workweek,
            'workweek_plot': workweek_plot
        }),
        ('weekend', {
            'Previous_Weekend': total_previous_weekend_consumption,
            'Current_Week_so_far': total_current_weekend_consumption_so_far,
            'Predicted_this_Weekend': current_weekend_total,
            'Change_in_Consumption': rate_of_change_weekend,
            'Estimated_Cost': estimated_cost_current_weekend,
            'Predicted_Emissions': emission_weekend,
            'weekend_plot': weekend_plot
        }),

                ('Day', {
                    'Yesterday': total_yesterday_consumption,
                    'So_far_Today': total_today_consumption_so_far,
                    'Predicted_Today': today_total,
                    'Change_in_Consumption': rate_of_change_hour,
                    'Estimated_Cost': estimated_cost_today,
                    'Predicted_Emissions': emission_hour,
                    'day_plot': day_plot
                })
            ])
    response_json = json.dumps(response)
    return Response(response_json, content_type='application/json')
if __name__ == "__main__":
    app.run(debug=True)
