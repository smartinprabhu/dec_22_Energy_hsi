import json
import pandas as pd
import pytz
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from dateutil.relativedelta import relativedelta
from load_data import load_and_process_data
from saving_plot import sav_plot1

from process import synthetic_algol, model_energy, model_weather, model_weather_day, weather_present, weather_present_day, model_energy_day
from fig_week import sav_plot_week,sav_plot_workweek
from fig_month import sav_plot_month
from fig_weekend import sav_plot_weekend
from fig_year import sav_plot_year
from format_add_on import format
app = Flask(__name__)
CORS(app)
cost_per_kw = 6.09
num_days = 120

df_energy, dz_hour = load_and_process_data()
dz_hour['date'] = pd.to_datetime(dz_hour['date'])
dz_hour = dz_hour.set_index('date')
dz_day = dz_hour.resample('D').mean().reset_index()
dz_hour = dz_hour.reset_index()
df_energy["Timestamp_UTC"] = pd.to_datetime(df_energy["Timestamp_UTC"], errors="coerce")

df_hour = synthetic_algol(df_energy)
energy_data_all = model_energy(df_hour)
df_daily = model_energy_day(energy_data_all)
weather_data_hour = model_weather(dz_hour)
dz_hour = weather_present(weather_data_hour)
weather_data_day = model_weather_day(dz_day)
dz_day = weather_present_day(weather_data_day)


@app.route("/energy/forecast/static", methods=["POST"])
def get_energy_data_static():
    try:

        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        # Get the increase_percent input from the request
        increase_value = request.json.get('increase_value')

        # If increase_percent is None or an empty string, set it to 0
        if increase_value is None or increase_value == "":
            increase_value = 5

        # Validate increase_percent
        try:
            increase_value = float(increase_value)
            if not (0 <= increase_value <= 10000):
                return jsonify({"error": "increase_value must be a number between 0 and 100"}), 400
        except ValueError:
            return jsonify({"error": "increase_value must be a number"}), 400

        tz = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(tz)
        current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
        current_time_dt641 = current_time_dt64 + pd.Timedelta(hours=1)
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

        # Assume 'data' DataFrame contains 'ds' (datetime) and 'y' (consumption)
        data = energy_data_all.copy()

        # 1. Base Target: Hourly Level (average + standard deviation)
        data['hour'] = data['ds'].dt.hour
        hourly_stats = data.groupby('hour')['y'].agg(['mean', 'std'])
        base_hourly_target = hourly_stats['mean'] + hourly_stats['std']
        data['base_target'] = data['hour'].map(base_hourly_target)

        # 2. Adjust for Weekday/Weekend
        data['weekday'] = data['ds'].dt.weekday
        data['is_weekend'] = np.where(data['weekday'] >= 5, 1, 0)  # 1 for weekends, 0 for weekdays
        weekend_adjustment = data.groupby('is_weekend')['y'].mean() - data['y'].mean()
        data['weekday_adjusted_target'] = data['base_target'] + data['is_weekend'].map(weekend_adjustment)

        # 3. Adjust for Monthly Trends
        data['month'] = data['ds'].dt.month
        monthly_adjustment = data.groupby('month')['y'].mean() - data['weekday_adjusted_target'].mean()
        data['monthly_adjusted_target'] = data['weekday_adjusted_target'] + data['month'].map(monthly_adjustment)

        # 4. Seasonal Adjustment (Winter, Spring, Summer, Fall)
        data['season'] = np.where(data['month'].isin([12, 1, 2]), 'Winter',
                                   np.where(data['month'].isin([3, 4, 5]), 'Spring',
                                            np.where(data['month'].isin([6, 7, 8]), 'Summer', 'Fall')))
        seasonal_adjustment = data.groupby('season')['y'].mean() - data['monthly_adjusted_target'].mean()
        data['seasonally_adjusted_target'] = data['monthly_adjusted_target'] + data['season'].map(seasonal_adjustment)

        # 5. Peak and Off-Peak Adjustment
        data['is_peak'] = np.where(data['hour'].between(8, 22), 1, 0)  # 1 for peak hours (8 AM to 10 PM)
        peak_adjustment = data.groupby('is_peak')['y'].mean() - data['seasonally_adjusted_target'].mean()
        data['final_target'] = data['seasonally_adjusted_target'] + data['is_peak'].map(peak_adjustment)

        # Apply the static value to the final target
        data['final_target'] = increase_value

        # Calculate potential savings where actual usage exceeds the target
        data['breach'] = data['y'] > data['final_target']
        data['savings'] = np.where(data['breach'], data['y'] - data['final_target'], 0)

        dz_hour['ds'] = pd.to_datetime(dz_hour['ds'])
        dz_hour.rename(columns={'y': 'temperature'}, inplace=True)

        # Assuming 'data' is already defined and contains a 'ds' column
        data['ds'] = pd.to_datetime(data['ds'])

        # Merge the dataframes
        data = data.merge(dz_hour[['ds', 'temperature']], on='ds', how='left')
        sav_plot, total_yesterday_consumption,target_consumption,target_cost,target_emission, percentage_deviation,total_today_consumption_so_far, today_total, rate_of_change_hour,emission_yesterday,emission_today_so_far,emission_today_predicted,estimated_cost_yesterday,estimated_cost_today_so_far,estimated_cost_today_predicted=sav_plot1(data, current_time, current_time_dt641, cost_per_kw)

        sav_week, total_last_week_consumption, target_consumption_week, target_cost_week, target_emission_week,percentage_deviation1, total_current_week_consumption_so_far, this_week_total, rate_of_change_week, emission_last_week, emission_this_week_so_far, emission_this_week_predicted, rate_of_change_week2, estimated_cost_last_week, estimated_cost_this_week_so_far, estimated_cost_this_week_predicted, rate_of_change_week1=sav_plot_week(data, current_time, current_time_dt641, cost_per_kw)
        
        sav_month, total_last_month_consumption,percentage_deviation2, target_consumption_month, target_cost_month, target_emission_month, total_current_month_consumption_so_far, this_month_total, rate_of_change_month, emission_last_month, emission_this_month_so_far, emission_this_month_predicted, rate_of_change_month2, estimated_cost_last_month, estimated_cost_this_month_so_far, estimated_cost_this_month_predicted, rate_of_change_month1= sav_plot_month(data, current_time, current_time_dt641, cost_per_kw)
        sav_workweek, total_last_workweek_consumption, target_consumption_workweek, target_cost_workweek, target_emission_workweek, total_current_workweek_consumption_so_far, this_workweek_total, rate_of_change_workweek, emission_last_workweek, emission_this_workweek_so_far, emission_this_workweek_predicted, rate_of_change_workweek2, estimated_cost_last_workweek, estimated_cost_this_workweek_so_far, estimated_cost_this_workweek_predicted, rate_of_change_workweek1, percentage_deviation4=sav_plot_workweek(data, current_time, current_time_dt641, cost_per_kw)
        sav_weekend, total_last_weekend_consumption, target_consumption_weekend, target_cost_weekend, target_emission_weekend, total_current_weekend_consumption_so_far, this_weekend_total, rate_of_change_weekend, emission_last_weekend, emission_this_weekend_so_far, emission_this_weekend_predicted, rate_of_change_weekend2, estimated_cost_last_weekend, estimated_cost_this_weekend_so_far, estimated_cost_this_weekend_predicted, rate_of_change_weekend1, percentage_deviation5=sav_plot_weekend(data, current_time, current_time_dt641, cost_per_kw)    
        sav_year, total_last_year_consumption,percentage_deviation3, target_emission_year, target_cost_year, target_consumption_year, total_current_year_consumption_so_far, this_year_total, rate_of_change_year, emission_last_year, emission_this_year_so_far, emission_this_year_predicted, rate_of_change_year2, estimated_cost_last_year, estimated_cost_this_year_so_far, estimated_cost_this_year_predicted, rate_of_change_year1=sav_plot_year(data, current_time, current_time_dt641, cost_per_kw)
        percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend=format(percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend)       
        response = ([
            ('week', {
                'Consumption': {
                    'Previous_Week': f"{total_last_week_consumption:.2f} kWh",
                    'Current_Week_so_far': f"{total_current_week_consumption_so_far:2f} kWh",
                    'Predicted_this_Week': f"{this_week_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_week,

                },
                'Estimated_Cost': {
                    'Previous_Week': f"{estimated_cost_last_week:.2f} $",
                    'Current_Week_so_far': f"{estimated_cost_this_week_so_far:.2f} $",
                    'Predicted_this_Week': f"{estimated_cost_this_week_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_week,

                },
                'Emissions': {
                    'Previous_Week': f"{emission_last_week:.2f} tCO2e",
                    'Current_Week_so_far': f"{emission_this_week_so_far:.2f} tCO2e",
                    'Predicted_this_Week': f"{emission_this_week_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_week,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_week:.2f} kWh",
                    'Target_Cost': f"{target_cost_week:.2f} $",
                    'Target_Emission': f"{target_emission_week:.2f} tCO2e",
                    'Deviation %': percentage_deviation1,

                },
                'week_plot': sav_week
            }),
            ('Month', {
                'Consumption': {
                    'Previous_Month': f"{total_last_month_consumption:.2f} kWh",
                    'Current_Month_so_far': f"{total_current_month_consumption_so_far:.2f} kWh",
                    'Predicted_this_Month': f"{this_month_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_month,

                },
                'Estimated_Cost': {
                    'Previous_Month': f"{estimated_cost_last_month:.2f} $",
                    'Current_Month_so_far': f"{estimated_cost_this_month_so_far:.2f} $",
                    'Predicted_this_Month': f"{estimated_cost_this_month_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_month,

                },
                'Emissions': {
                    'Previous_Month': f"{emission_last_month:.2f} tCO2e",
                    'Current_Month_so_far': f"{emission_this_month_so_far:.2f} tCO2e",
                    'Predicted_this_Month': f"{emission_this_month_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_month,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_month:.2f} kWh",
                    'Target_Cost': f"{target_cost_month:.2f} $",
                    'Target_Emission': f"{target_emission_month:.2f} tCO2e",
                    'Deviation %': percentage_deviation2,

                },
                'month_plot': sav_month
            }),
            ('Year', {
                'Consumption': {
                    'Previous_Year': f"{total_last_year_consumption:.2f} kWh",
                    'Current_Year_so_far': f"{total_current_year_consumption_so_far:.2f} kWh",
                    'Predicted_this_Year': f"{this_year_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_year,

                },
                'Estimated_Cost': {
                    'Previous_Year': f"{estimated_cost_last_year:.2f} $",
                    'Current_Year_so_far': f"{estimated_cost_this_year_so_far:.2f} $",
                    'Predicted_this_Year': f"{estimated_cost_this_year_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_year,

                },
                'Emissions': {
                    'Previous_Year': f"{emission_last_year:.2f} tCO2e",
                    'Current_Year_so_far': f"{emission_this_year_so_far:.2f} tCO2e",
                    'Predicted_this_Year': f"{emission_this_year_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_year,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_year:.2f} kWh",
                    'Target_Cost': f"{target_cost_year:.2f} $",
                    'Target_Emission': f"{target_emission_year:.2f} tCO2e",
                    'Deviation %': percentage_deviation3,

                },
                'year_plot': sav_year
            }),
            ('workweek', {
                'Consumption': {
                    'Previous_Week': f"{total_last_workweek_consumption:.2f} kWh",
                    'Current_Workweek_so_far': f"{total_current_workweek_consumption_so_far:.2f} kWh",
                    'Predicted_this_Week': f"{this_workweek_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_workweek,

                },
                'Estimated_Cost': {
                    'Previous_Week': f"{estimated_cost_last_workweek:.2f} $",
                    'Current_Workweek_so_far': f"{estimated_cost_this_workweek_so_far:.2f} $",
                    'Predicted_this_Week': f"{estimated_cost_this_workweek_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_workweek,

                },
                'Emissions': {
                    'Previous_Week': f"{emission_last_workweek:.2f} tCO2e",
                    'Current_Workweek_so_far': f"{emission_this_workweek_so_far:.2f} tCO2e",
                    'Predicted_this_Week': f"{emission_this_workweek_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_workweek,
                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_workweek:.2f} kWh",
                    'Target_Cost': f"{target_cost_workweek:.2f} $",
                    'Target_Emission': f"{target_emission_workweek:.2f} tCO2e",
                    'Deviation %': percentage_deviation4,

                },
                'workweek_plot': sav_workweek
            }),
            ('weekend', {
                'Consumption': {
                    'Previous_Weekend': f"{total_last_weekend_consumption:.2f} kWh",
                    'Current_Weekend_so_far': f"{total_current_weekend_consumption_so_far:.2f} kWh",
                    'Predicted_this_Weekend': f"{this_weekend_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Estimated_Cost': {
                    'Previous_Weekend': f"{estimated_cost_last_weekend:.2f} $",
                    'Current_Weekend_so_far': f"{estimated_cost_this_weekend_so_far:.2f} $",
                    'Predicted_this_Weekend': f"{estimated_cost_this_weekend_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Emissions': {
                    'Previous_Weekend': f"{emission_last_weekend:.2f} tCO2e",
                    'Current_Weekend_so_far': f"{emission_this_weekend_so_far:.2f} tCO2e",
                    'Predicted_this_Weekend': f"{emission_this_weekend_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_weekend:.2f} kWh",
                    'Target_Cost': f"{target_cost_weekend:.2f} $",
                    'Target_Emission': f"{target_emission_weekend:.2f} tCO2e",
                    'Deviation %': percentage_deviation5,

                },
                'weekend_plot': sav_weekend
            }),
            ('Day', {
                'Consumption': {
                    'Yesterday': f"{total_yesterday_consumption:.2f} kWh",
                    'So_far_Today': f"{total_today_consumption_so_far:.2f} kWh",
                    'Predicted_Today': f"{today_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today,
                    # 'Target':Target_status,
                },
                'Estimated_Cost': {
                    'Yesterday': f"{estimated_cost_yesterday:.2f} $",
                    'So_far_Today': f"{estimated_cost_today_so_far:.2f} $",
                    'Predicted_Today': f"{estimated_cost_today_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today_cost,
                    # 'Target':Target_status,
                },
                'Emissions': {
                    'Yesterday': f"{emission_yesterday:.2f} tCO2e",
                    'So_far_Today': f"{emission_today_so_far:.2f} tCO2e",
                    'Predicted_Today': f"{emission_today_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today_emission,
                    # 'Target':Target_status,
                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption:.2f} kWh",
                    'Target_Cost': f"{target_cost:.2f} $",
                    'Target_Emission': f"{target_emission:.2f} tCO2e",
                    'Deviation %': percentage_deviation,

                },
                'day_plot': sav_plot
            }),
        ])
        response_json = json.dumps(response)
        return Response(response_json, content_type='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route("/energy/forecast/dynamic", methods=["POST"])
def get_energy_data_dynamic():
    try:

        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        # Get the increase_percent input from the request
        increase_percent = request.json.get('increase_percent')

        # If increase_percent is None or an empty string, set it to 0
        if increase_percent is None or increase_percent == "":
            increase_percent = 0

        # Validate increase_percent
        try:
            increase_percent = float(increase_percent)
            if not (0 <= increase_percent <= 100):
                return jsonify({"error": "increase_percent must be a number between 0 and 100"}), 400
        except ValueError:
            return jsonify({"error": "increase_percent must be a number"}), 400

        # Convert increase_percent to a percentage
        increase_percent = increase_percent / 100

        tz = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(tz)
        current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
        current_time_dt641 = current_time_dt64 + pd.Timedelta(hours=1)
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

        # Assume 'data' DataFrame contains 'ds' (datetime) and 'y' (consumption)
        data = energy_data_all.copy()

        # 1. Base Target: Hourly Level (average + standard deviation)
        data['hour'] = data['ds'].dt.hour
        hourly_stats = data.groupby('hour')['y'].agg(['mean', 'std'])
        base_hourly_target = hourly_stats['mean'] + hourly_stats['std']
        data['base_target'] = data['hour'].map(base_hourly_target)

        # 2. Adjust for Weekday/Weekend
        data['weekday'] = data['ds'].dt.weekday
        data['is_weekend'] = np.where(data['weekday'] >= 5, 1, 0)  # 1 for weekends, 0 for weekdays
        weekend_adjustment = data.groupby('is_weekend')['y'].mean() - data['y'].mean()
        data['weekday_adjusted_target'] = data['base_target'] + data['is_weekend'].map(weekend_adjustment)

        # 3. Adjust for Monthly Trends
        data['month'] = data['ds'].dt.month
        monthly_adjustment = data.groupby('month')['y'].mean() - data['weekday_adjusted_target'].mean()
        data['monthly_adjusted_target'] = data['weekday_adjusted_target'] + data['month'].map(monthly_adjustment)

        # 4. Seasonal Adjustment (Winter, Spring, Summer, Fall)
        data['season'] = np.where(data['month'].isin([12, 1, 2]), 'Winter',
                                   np.where(data['month'].isin([3, 4, 5]), 'Spring',
                                            np.where(data['month'].isin([6, 7, 8]), 'Summer', 'Fall')))
        seasonal_adjustment = data.groupby('season')['y'].mean() - data['monthly_adjusted_target'].mean()
        data['seasonally_adjusted_target'] = data['monthly_adjusted_target'] + data['season'].map(seasonal_adjustment)

        # 5. Peak and Off-Peak Adjustment
        data['is_peak'] = np.where(data['hour'].between(8, 22), 1, 0)  # 1 for peak hours (8 AM to 10 PM)
        peak_adjustment = data.groupby('is_peak')['y'].mean() - data['seasonally_adjusted_target'].mean()
        data['final_target'] = data['seasonally_adjusted_target'] + data['is_peak'].map(peak_adjustment)

        # Apply the increase percentage to the final target
        data['final_target'] = data['final_target'] * (1 - increase_percent)

        # Calculate potential savings where actual usage exceeds the target
        data['breach'] = data['y'] > data['final_target']
        data['savings'] = np.where(data['breach'], data['y'] - data['final_target'], 0)

        dz_hour['ds'] = pd.to_datetime(dz_hour['ds'])
        dz_hour.rename(columns={'y': 'temperature'}, inplace=True)

        # Assuming 'data' is already defined and contains a 'ds' column
        data['ds'] = pd.to_datetime(data['ds'])

        # Merge the dataframes
        data = data.merge(dz_hour[['ds', 'temperature']], on='ds', how='left')
        
        sav_plot, total_yesterday_consumption,target_consumption,target_cost,target_emission, percentage_deviation,total_today_consumption_so_far, today_total, rate_of_change_hour,emission_yesterday,emission_today_so_far,emission_today_predicted,estimated_cost_yesterday,estimated_cost_today_so_far,estimated_cost_today_predicted=sav_plot1(data, current_time, current_time_dt641, cost_per_kw)

        sav_week, total_last_week_consumption, target_consumption_week, target_cost_week, target_emission_week,percentage_deviation1, total_current_week_consumption_so_far, this_week_total, rate_of_change_week, emission_last_week, emission_this_week_so_far, emission_this_week_predicted, rate_of_change_week2, estimated_cost_last_week, estimated_cost_this_week_so_far, estimated_cost_this_week_predicted, rate_of_change_week1=sav_plot_week(data, current_time, current_time_dt641, cost_per_kw)
        
        sav_month, total_last_month_consumption,percentage_deviation2, target_consumption_month, target_cost_month, target_emission_month, total_current_month_consumption_so_far, this_month_total, rate_of_change_month, emission_last_month, emission_this_month_so_far, emission_this_month_predicted, rate_of_change_month2, estimated_cost_last_month, estimated_cost_this_month_so_far, estimated_cost_this_month_predicted, rate_of_change_month1= sav_plot_month(data, current_time, current_time_dt641, cost_per_kw)
        sav_workweek, total_last_workweek_consumption, target_consumption_workweek, target_cost_workweek, target_emission_workweek, total_current_workweek_consumption_so_far, this_workweek_total, rate_of_change_workweek, emission_last_workweek, emission_this_workweek_so_far, emission_this_workweek_predicted, rate_of_change_workweek2, estimated_cost_last_workweek, estimated_cost_this_workweek_so_far, estimated_cost_this_workweek_predicted, rate_of_change_workweek1, percentage_deviation4=sav_plot_workweek(data, current_time, current_time_dt641, cost_per_kw)
        sav_weekend, total_last_weekend_consumption, target_consumption_weekend, target_cost_weekend, target_emission_weekend, total_current_weekend_consumption_so_far, this_weekend_total, rate_of_change_weekend, emission_last_weekend, emission_this_weekend_so_far, emission_this_weekend_predicted, rate_of_change_weekend2, estimated_cost_last_weekend, estimated_cost_this_weekend_so_far, estimated_cost_this_weekend_predicted, rate_of_change_weekend1, percentage_deviation5=sav_plot_weekend(data, current_time, current_time_dt641, cost_per_kw)       
        sav_year, total_last_year_consumption,percentage_deviation3, target_emission_year, target_cost_year, target_consumption_year, total_current_year_consumption_so_far, this_year_total, rate_of_change_year, emission_last_year, emission_this_year_so_far, emission_this_year_predicted, rate_of_change_year2, estimated_cost_last_year, estimated_cost_this_year_so_far, estimated_cost_this_year_predicted, rate_of_change_year1=sav_plot_year(data, current_time, current_time_dt641, cost_per_kw)
        percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend=format(percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend)       
        response = ([
            ('week', {
                'Consumption': {
                    'Previous_Week': f"{total_last_week_consumption:.2f} kWh",
                    'Current_Week_so_far': f"{total_current_week_consumption_so_far:2f} kWh",
                    'Predicted_this_Week': f"{this_week_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_week,

                },
                'Estimated_Cost': {
                    'Previous_Week': f"{estimated_cost_last_week:.2f} $",
                    'Current_Week_so_far': f"{estimated_cost_this_week_so_far:.2f} $",
                    'Predicted_this_Week': f"{estimated_cost_this_week_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_week,

                },
                'Emissions': {
                    'Previous_Week': f"{emission_last_week:.2f} tCO2e",
                    'Current_Week_so_far': f"{emission_this_week_so_far:.2f} tCO2e",
                    'Predicted_this_Week': f"{emission_this_week_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_week,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_week:.2f} kWh",
                    'Target_Cost': f"{target_cost_week:.2f} $",
                    'Target_Emission': f"{target_emission_week:.2f} tCO2e",
                    'Deviation %': percentage_deviation1,

                },
                'week_plot': sav_week
            }),
            ('Month', {
                'Consumption': {
                    'Previous_Month': f"{total_last_month_consumption:.2f} kWh",
                    'Current_Month_so_far': f"{total_current_month_consumption_so_far:.2f} kWh",
                    'Predicted_this_Month': f"{this_month_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_month,

                },
                'Estimated_Cost': {
                    'Previous_Month': f"{estimated_cost_last_month:.2f} $",
                    'Current_Month_so_far': f"{estimated_cost_this_month_so_far:.2f} $",
                    'Predicted_this_Month': f"{estimated_cost_this_month_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_month,

                },
                'Emissions': {
                    'Previous_Month': f"{emission_last_month:.2f} tCO2e",
                    'Current_Month_so_far': f"{emission_this_month_so_far:.2f} tCO2e",
                    'Predicted_this_Month': f"{emission_this_month_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_month,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_month:.2f} kWh",
                    'Target_Cost': f"{target_cost_month:.2f} $",
                    'Target_Emission': f"{target_emission_month:.2f} tCO2e",
                    'Deviation %': percentage_deviation2,

                },
                'month_plot': sav_month
            }),
            ('Year', {
                'Consumption': {
                    'Previous_Year': f"{total_last_year_consumption:.2f} kWh",
                    'Current_Year_so_far': f"{total_current_year_consumption_so_far:.2f} kWh",
                    'Predicted_this_Year': f"{this_year_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_year,

                },
                'Estimated_Cost': {
                    'Previous_Year': f"{estimated_cost_last_year:.2f} $",
                    'Current_Year_so_far': f"{estimated_cost_this_year_so_far:.2f} $",
                    'Predicted_this_Year': f"{estimated_cost_this_year_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_year,

                },
                'Emissions': {
                    'Previous_Year': f"{emission_last_year:.2f} tCO2e",
                    'Current_Year_so_far': f"{emission_this_year_so_far:.2f} tCO2e",
                    'Predicted_this_Year': f"{emission_this_year_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_year,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_year:.2f} kWh",
                    'Target_Cost': f"{target_cost_year:.2f} $",
                    'Target_Emission': f"{target_emission_year:.2f} tCO2e",
                    'Deviation %': percentage_deviation3,

                },
                'year_plot': sav_year
            }),
            ('workweek', {
                'Consumption': {
                    'Previous_Week': f"{total_last_workweek_consumption:.2f} kWh",
                    'Current_Workweek_so_far': f"{total_current_workweek_consumption_so_far:.2f} kWh",
                    'Predicted_this_Week': f"{this_workweek_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_workweek,

                },
                'Estimated_Cost': {
                    'Previous_Week': f"{estimated_cost_last_workweek:.2f} $",
                    'Current_Workweek_so_far': f"{estimated_cost_this_workweek_so_far:.2f} $",
                    'Predicted_this_Week': f"{estimated_cost_this_workweek_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_workweek,

                },
                'Emissions': {
                    'Previous_Week': f"{emission_last_workweek:.2f} tCO2e",
                    'Current_Workweek_so_far': f"{emission_this_workweek_so_far:.2f} tCO2e",
                    'Predicted_this_Week': f"{emission_this_workweek_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_workweek,
                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_workweek:.2f} kWh",
                    'Target_Cost': f"{target_cost_workweek:.2f} $",
                    'Target_Emission': f"{target_emission_workweek:.2f} tCO2e",
                    'Deviation %': percentage_deviation4,

                },
                'workweek_plot': sav_workweek
            }),
            ('weekend', {
                'Consumption': {
                    'Previous_Weekend': f"{total_last_weekend_consumption:.2f} kWh",
                    'Current_Weekend_so_far': f"{total_current_weekend_consumption_so_far:.2f} kWh",
                    'Predicted_this_Weekend': f"{this_weekend_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Estimated_Cost': {
                    'Previous_Weekend': f"{estimated_cost_last_weekend:.2f} $",
                    'Current_Weekend_so_far': f"{estimated_cost_this_weekend_so_far:.2f} $",
                    'Predicted_this_Weekend': f"{estimated_cost_this_weekend_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Emissions': {
                    'Previous_Weekend': f"{emission_last_weekend:.2f} tCO2e",
                    'Current_Weekend_so_far': f"{emission_this_weekend_so_far:.2f} tCO2e",
                    'Predicted_this_Weekend': f"{emission_this_weekend_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_weekend,

                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption_weekend:.2f} kWh",
                    'Target_Cost': f"{target_cost_weekend:.2f} $",
                    'Target_Emission': f"{target_emission_weekend:.2f} tCO2e",
                    'Deviation %': percentage_deviation5,

                },
                'weekend_plot': sav_weekend
            }),
            ('Day', {
                'Consumption': {
                    'Yesterday': f"{total_yesterday_consumption:.2f} kWh",
                    'So_far_Today': f"{total_today_consumption_so_far:.2f} kWh",
                    'Predicted_Today': f"{today_total:.2f} kWh",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today,
                    # 'Target':Target_status,
                },
                'Estimated_Cost': {
                    'Yesterday': f"{estimated_cost_yesterday:.2f} $",
                    'So_far_Today': f"{estimated_cost_today_so_far:.2f} $",
                    'Predicted_Today': f"{estimated_cost_today_predicted:.2f} $",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today_cost,
                    # 'Target':Target_status,
                },
                'Emissions': {
                    'Yesterday': f"{emission_yesterday:.2f} tCO2e",
                    'So_far_Today': f"{emission_today_so_far:.2f} tCO2e",
                    'Predicted_Today': f"{emission_today_predicted:.2f} tCO2e",
                    'Percentage_Change': rate_of_change_hour,
                    # 'Target Reduction': target_reduction_today_emission,
                    # 'Target':Target_status,
                },
                'Target Goal': {
                    'Target_Consumption': f"{target_consumption:.2f} kWh",
                    'Target_Cost': f"{target_cost:.2f} $",
                    'Target_Emission': f"{target_emission:.2f} tCO2e",
                    'Deviation %': percentage_deviation,

                },
                'day_plot': sav_plot
            }),
        ])
        response_json = json.dumps(response)
        return Response(response_json, content_type='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5011)
