import json
from datetime import datetime, time, timedelta

import numpy as np
import pandas as pd
import plotly
import pytz
from dateutil.relativedelta import relativedelta
from flask import Flask, Response
from flask_cors import CORS
from prophet import Prophet

from fig_day import fig_day
from fig_month import fig_month
from fig_week import fig_week
from fig_weekend import weekend_fig
from fig_workweek import workweek_fig
from fig_year import fig_year
from load_data import load_and_process_data
from m import (tot_con_month, tot_con_week, tot_con_weekend, tot_con_workweek,
               tot_con_year, total_consumption)
from man_hours import (man_hours, man_hours1, man_hours2, man_hours3,
                       man_hours4, man_hours5)
from model import modeling_day, modeling_hour_count, modeling_hour_iaqz
from synthetic_data import synthetic_process_algol
from waste import (waste_day, waste_month, waste_week, waste_workweek,
                   waste_year)

app = Flask(__name__)
CORS(app)

# Initialize and return parameters for the API
cost_per_hr = 0
num_days = 120

pplin, iaqz = load_and_process_data()
energy_with_synthetic, replaced_data, r_cost = synthetic_process_algol(
    pplin, cost_per_hr
)
energy_with_synthetic = energy_with_synthetic[
    energy_with_synthetic["answer_value"] <= 150
]
energy_with_synthetic = energy_with_synthetic.reset_index()

energy_with_synthetic = energy_with_synthetic.rename(
    columns={"measured_ts": "ds", "answer_value": "y"}
)
iaqz = iaqz.rename(columns={"measured_ts": "ds", "answer_value": "y"})

iaqz["ds"] = pd.to_datetime(iaqz["ds"], format="mixed", errors="coerce")
fin, future_forecast = modeling_hour_count(energy_with_synthetic)
fin1, future_forecast1 = modeling_hour_iaqz(iaqz)
df_daily = modeling_day(energy_with_synthetic)

energy_data = energy_with_synthetic.set_index("ds").resample("D").sum().reset_index()

# Initialize the Prophet model
model = Prophet()

# Fit the Prophet model to the dataset
model.fit(energy_data)

# Calculate future start date
future_start_date = energy_data["ds"].max() + pd.Timedelta(days=1)

# Set future end date to the current day plus one month
future_end_date = pd.Timestamp.now() + pd.DateOffset(months=2)

# Create a DataFrame for future dates for forecasting
future = pd.DataFrame(
    {"ds": pd.date_range(start=future_start_date, end=future_end_date, freq="D")}
)

# Make predictions for the future period
future_forecast = model.predict(future)
future_forecast["yhat"] = future_forecast["yhat"].apply(
    lambda x: np.exp(x) if x < 0 else x
)
future_forecast = future_forecast.rename(columns={"yhat": "y"})
df_daily = pd.concat([energy_data, future_forecast], ignore_index=True)
df_daily["ds"] = pd.to_datetime(df_daily["ds"])
fin["ds"] = pd.to_datetime(fin["ds"])
fin1["ds"] = pd.to_datetime(fin1["ds"])


@app.route("/forecast", methods=["POST"])
def get_energy_data():
    
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    future_forecast["ds"] = pd.to_datetime(future_forecast["ds"])
    if future_forecast["ds"].dt.tz is None:
        future_forecast["ds"] = future_forecast["ds"].dt.tz_localize(tz)
    else:
        future_forecast["ds"] = future_forecast["ds"].dt.tz_convert(tz)

    fin["ds"] = pd.to_datetime(fin["ds"])
    if fin["ds"].dt.tz is None:
        fin["ds"] = fin["ds"].dt.tz_localize(tz)
    else:
        fin["ds"] = fin["ds"].dt.tz_convert(tz)

    fin1["ds"] = pd.to_datetime(fin1["ds"])
    if fin1["ds"].dt.tz is None:
        fin1["ds"] = fin1["ds"].dt.tz_localize(tz)
    else:
        fin1["ds"] = fin1["ds"].dt.tz_convert(tz)

    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    current_time_dt641 = pd.Timestamp(current_time).tz_convert(tz)+ pd.Timedelta(hours=1)

    # Get the date for the previous day
    previous_day = current_time_dt64.date() - timedelta(days=1)

    # Create the start and end timestamps for the previous day
    start_time = pd.Timestamp(previous_day, tz=tz)

    # Split the data into historical and forecasted
    forecasted_data = fin[fin["ds"] > current_time_dt64]
    historical_data = fin[(fin["ds"] >= start_time) & (fin["ds"] <= current_time_dt641)]

    # Get the end of the next 24 hours
    next_24_hours_end = current_time + timedelta(days=1)
    next_24_hours_end = pd.Timestamp(
        next_24_hours_end.replace(hour=23, minute=59, second=59, microsecond=999999)
    ).tz_convert(tz)

    forecasted_bar_data = fin[
        (fin["ds"] > current_time_dt641) & (fin["ds"] <= next_24_hours_end)
    ]

    # For annotation calculation
    current_day_end = datetime.combine(
        current_time.date(), time(23, 59, 59, 999999)
    ).astimezone(tz)
    forecasted_data_today = fin[
        (fin["ds"] > current_time_dt641) & (fin["ds"] <= current_day_end)
    ]
    forecasted_bar_data["y"] = forecasted_bar_data["y"].round().astype(int)
    historical_data["y"] = historical_data["y"].round().astype(int)
    forecasted_data_today = forecasted_data_today["y"].round().astype(int)

    day_plot, total_today_work_orders, so_far_work_orders = fig_day(
        fin,
        current_time,
        fin1,
        tz,
        historical_data,
        cost_per_hr,
        forecasted_data_today,
        current_time_dt641,
        next_24_hours_end,
        forecasted_bar_data,
    )

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
    next_7_days_end = pd.Timestamp(
        next_7_days_end.replace(hour=23, minute=59, second=59, microsecond=999999)
    ).tz_convert(tz)
    forecasted_bar_data_daily = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= next_7_days_end)
    ]

    end_of_week = current_time + timedelta(days=(6 - current_time.weekday()))

    next_7_days_end = end_of_week + timedelta(days=7)

    forecasted_bar_data_daily = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= next_7_days_end)
    ]

    forecasted_data_week_end = df_daily[
        (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= end_of_week)
    ]

    dz_day, week_plot, tot_this_week_work, so_far_week_work_orders = fig_week(
        tz,
        fin1,
        fin,
        current_time,
        next_7_days_end,
        current_time_dt64,
        forecasted_data_week_end,
        cost_per_hr,
        forecasted_bar_data_daily,
        historical_data_daily,
    )

    historical_data_month = df_daily[
        (df_daily["ds"].dt.date >= (current_time - pd.Timedelta(days=59)).date())
        & (df_daily["ds"].dt.date <= current_time.date())
    ]

    # Get the current date
    current_date = pd.Timestamp.now(tz=tz)

    # Get the end of the current month
    # current_month_end = pd.Timestamp(
    #     current_date.year, current_date.month + 1, 1
    # ) - pd.Timedelta(days=1)
    # current_month_end = current_month_end.tz_localize(tz)
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

    # forecasted_data_month_end = df_daily[
    #     (df_daily["ds"] > current_time_dt64) & (df_daily["ds"] <= current_month_end)
    # ]

    historical_data_month["y"] = historical_data_month["y"].round().astype(int)
    forecasted_bar_data_monthly["y"] = (
        forecasted_bar_data_monthly["y"].round().astype(int)
    )

    month_plot,tot_this_month_work,so_far_month_work_orders= fig_month(
        tz,
        fin,
        historical_data_month,
        forecasted_bar_data_monthly,
        dz_day,
        current_time_dt64,
        next_month_end,
        current_time,
        cost_per_hr,
    )

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
        (
            df_workweek["ds"].dt.date
            > max(current_time.date(), current_week_start.date())
        )
        & (df_workweek["ds"].dt.date <= next_week_end.date())
    ]

    # Create a new variable that includes the current work week (after today)
    forecast_data_workweek_cal = df_workweek[
        (
            df_workweek["ds"].dt.date
            > max(current_time.date(), current_week_start.date())
        )
        & (df_workweek["ds"].dt.date <= current_week_end.date())
    ]

    historical_data_workweek["y"] = historical_data_workweek["y"].round().astype(int)
    forecast_data_bar_workweek["y"] = (
        forecast_data_bar_workweek["y"].round().astype(int)
    )

    workweek_plot,so_far_workweek_work_orders,tot_this_workweek_work = workweek_fig(
        next_week_end,
        fin,
        dz_day,
        historical_data_workweek,
        forecast_data_bar_workweek,
        forecast_data_workweek_cal,
        start_date,
        current_week_start,
        cost_per_hr,
        current_time,
        tz,
    )

    # Calculate the start and end of the current weekend
    current_weekend_start = current_time + timedelta(
        days=(5 - current_time.weekday())
    )  # Saturday
    current_weekend_end = current_weekend_start + timedelta(days=1)  # Sunday

    # Filter the data for the current weekend
    forecast_data_weekend_1 = df_daily[
        (df_daily["ds"].dt.date >= current_weekend_start.date())
        & (df_daily["ds"].dt.date <= current_weekend_end.date())
    ]

    # Calculate the start and end of the next weekend
    next_weekend_start = current_weekend_start + timedelta(days=7)  # Next Saturday
    next_weekend_end = next_weekend_start + timedelta(days=1)  # Next Sunday

    # Filter the data for the next weekend
    forecast_data_weekend_cal = df_daily[
        (df_daily["ds"].dt.date >= next_weekend_start.date())
        & (df_daily["ds"].dt.date <= next_weekend_end.date())
    ]

    # Combine the forecast data for the current and next weekends
    forecast_data_bar_weekend = pd.concat(
        [forecast_data_weekend_1, forecast_data_weekend_cal]
    )

    # For historical data, filter for weekends (Saturday and Sunday)
    historical_data_weekend = historical_data_daily[
        historical_data_daily["ds"].dt.weekday >= 5
    ]

    weekend_plot,so_far_weekend_work_orders,tot_this_weekend_work = weekend_fig(
        fin,
        current_weekend_start,
        forecast_data_bar_weekend,
        historical_data_weekend,
        dz_day,
        next_weekend_start,
        next_weekend_end,
        forecast_data_weekend_cal,
        current_weekend_end,
        current_time,
        cost_per_hr,
        tz,
    )

    df_monthly = df_daily[["ds", "y"]].set_index("ds").resample("M").sum().reset_index()
    dz_month = dz_day[["ds", "y"]].set_index("ds").resample("M").mean().reset_index()

    # Define the end of the current month
    end_of_current_month = (current_time + relativedelta(day=31)).date()

    # Filter data up to the end of the current month
    historical_data_monthly = df_monthly[
        (df_monthly["ds"].dt.date >= (current_time - relativedelta(years=2)).date())
        & (df_monthly["ds"].dt.date <= end_of_current_month)
    ]

    before_current_time1 = dz_month[
        (dz_month["ds"].dt.date >= (current_time - relativedelta(years=2)).date())
        & (dz_month["ds"].dt.date <= end_of_current_month)
    ]

    # Define the start of the month after the current month
    start_of_next_month = (current_time + relativedelta(day=1, months=1)).date()

    # Define the end of the next year
    end_of_next_year = (current_time + relativedelta(years=2, day=31, month=12)).date()

    # Filter the data for the period after the current month up to the end of next year
    forecast_data_monthly = df_monthly[
        (df_monthly["ds"].dt.date >= start_of_next_month)
        & (df_monthly["ds"].dt.date <= end_of_next_year)
    ]

    after_current_time = dz_month[
        (dz_month["ds"].dt.date >= start_of_next_month)
        & (dz_month["ds"].dt.date <= end_of_next_year)
    ]

    # Define the end of the current year
    end_of_current_year = (current_time + relativedelta(day=31, month=12)).date()

    # Filter the data for the period from the start of the next month to the end of the current year
    forecast_data_until_end_of_year_cal = df_monthly[
        (df_monthly["ds"].dt.date >= start_of_next_month)
        & (df_monthly["ds"].dt.date <= end_of_current_year)
    ]
    forecast_data_monthly["y"] = round(forecast_data_monthly["y"])

    year_plot,so_far_year_work_orders,tot_this_year_work = fig_year(
        fin,
        start_of_next_month,
        dz_day,
        end_of_next_year,
        current_time,
        end_of_current_month,
        forecast_data_monthly,
        historical_data_monthly,
        before_current_time1,
        forecast_data_until_end_of_year_cal,
        after_current_time,
        cost_per_hr,
    )

    consumption_plot = total_consumption(fin, tz)
    consumption_plot_week = tot_con_week(df_daily)
    consumption_plot_month = tot_con_month(df_daily, current_time)
    consumption_plot_year = tot_con_year(df_daily, current_time)
    consumption_plot_workweek = tot_con_workweek(df_daily)
    consumption_plot_weekend = tot_con_weekend(df_daily)

    man_plot = man_hours(fin)
    man_plot1 = man_hours1(fin)
    man_plot2 = man_hours2(fin)
    man_plot3 = man_hours3(fin)
    man_plot4 = man_hours4(fin)
    man_plot5 = man_hours5(fin)

    waste_plot = waste_day(fin)
    waste_plot1 = waste_week(fin)
    waste_plot2 = waste_workweek(fin)
    waste_plot3 = waste_month(fin)
    waste_plot4 = waste_year(fin)

    response = [
        (
            "week",
            {
                "Footfalls Prediction": consumption_plot_week,
                "Estimated_Resources": man_plot1,
                "so_far": {
                    "so_far_work_orders": int(so_far_week_work_orders),
                    "total_today_work_orders": int(tot_this_week_work),
                },
                "Footfall_Usage": waste_plot1,
                "day_plot": week_plot,
            },
        ),
        (
            "Month",
            {
                "Footfalls Prediction": consumption_plot_month,
                "Estimated_Resources": man_plot2,
                "so_far": {
                    "so_far_work_orders": int(so_far_month_work_orders),
                    "total_today_work_orders": int(tot_this_month_work),
                },
                "Footfall_Usage": waste_plot3,
                "day_plot": month_plot,
            },
        ),
        (
            "Year",
            {
                "Footfalls Prediction": consumption_plot_year,
                "Estimated_Resources": man_plot5,
                "so_far": {
                    "so_far_work_orders": int(so_far_year_work_orders),
                    "total_today_work_orders": int(tot_this_year_work),
                },
                "Footfall_Usage": waste_plot4,
                "day_plot": year_plot,
            },
        ),
        (
            "workweek",
            {
                "Footfalls Prediction": consumption_plot_workweek,
                "Estimated_Resources": man_plot3,
                "so_far": {
                    "so_far_work_orders": int(so_far_workweek_work_orders),
                    "total_today_work_orders": int(tot_this_workweek_work),
                },
                "Footfall_Usage": waste_plot2,
                "day_plot": workweek_plot,
            },
        ),
        (
            "weekend",
            {
                "Footfalls Prediction": consumption_plot_weekend,
                "Estimated_Resources": man_plot4,
                "so_far": {
                    "so_far_work_orders": int(so_far_weekend_work_orders),
                    "total_today_work_orders": int(tot_this_weekend_work),
                },
                "Footfall_Usage": waste_plot1,
                "day_plot": weekend_plot,
            },
        ),
        (
            "Day",
            {
                "Footfalls Prediction": consumption_plot,
                "Estimated_Resources": man_plot,
                "so_far": {
                    "so_far_work_orders": int(so_far_work_orders),
                    "total_today_work_orders": int(total_today_work_orders),
                },
                "Footfall_Usage": waste_plot,
                "day_plot": day_plot,
            },
        ),
    ]

    # Custom JSON encoder to handle numpy.int64 types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            return super(NumpyEncoder, self).default(obj)

    response_json = json.dumps(response, cls=NumpyEncoder)
    return Response(response_json, content_type="application/json")

if __name__ == "__main__":
    app.run(port=5002, debug=True)