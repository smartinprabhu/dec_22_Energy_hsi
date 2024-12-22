from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd
import pandas as pd
import ssl
from datetime import datetime, timedelta
import pandas as pd

from meteostat import Daily, Stations
from meteostat import Point, Hourly
from datetime import datetime, timedelta
import pytz
import ssl
def synthetic_algol(df_energy):
    df_hour = df_energy.set_index("Timestamp_UTC")

    weekday_patterns = df_hour.groupby(df_hour.index.dayofweek)['Energy Consumption (kWh)'].mean()
    hourly_patterns = {}
    for weekday in range(7):
        weekday_data = df_hour[df_hour.index.dayofweek == weekday]
        hourly_patterns[weekday] = weekday_data.groupby(weekday_data.index.hour)['Energy Consumption (kWh)'].mean()

    missing_indices = df_hour[df_hour['Energy Consumption (kWh)'].isna()].index

    consecutive_missing = []
    replaced_values = {}

    def adjust_energy_consumption(timestamp, base_consumption):
        hour = timestamp.hour
        if 6 <= hour < 18:
            return base_consumption * np.random.uniform(1.3, 1.7)
        else:
            return base_consumption * np.random.uniform(0.5, 0.7)

    for index in missing_indices:
        if index + pd.Timedelta(hours=1) in missing_indices:
            consecutive_missing.append(index)
        else:
            weekday = index.dayofweek
            hour = index.hour
            replaced_value = adjust_energy_consumption(index, hourly_patterns[weekday].get(hour, weekday_patterns[weekday]))
            df_hour.loc[index, 'Energy Consumption (kWh)'] = replaced_value
            replaced_values[index] = replaced_value

        if (index + pd.Timedelta(hours=1)) not in missing_indices or index == missing_indices[-1]:
            if consecutive_missing:
                weekday = consecutive_missing[0].dayofweek
                for missing_index in consecutive_missing:
                    hour = missing_index.hour
                    replaced_value = adjust_energy_consumption(missing_index, hourly_patterns[weekday].get(hour, weekday_patterns[weekday]))
                    df_hour.loc[missing_index, 'Energy Consumption (kWh)'] = replaced_value
                    replaced_values[missing_index] = replaced_value
                consecutive_missing = []

    df_hour = df_hour.reset_index()
    df_hour = df_hour.rename(columns={'Timestamp_UTC': 'ds', 'Energy Consumption (kWh)': 'y'})
    return df_hour

def model_energy(df_hour):
    # Prepare the data
    prophet_data = df_hour.copy()  # Copy to avoid modifying the original DataFrame
    prophet_data['ds'] = pd.to_datetime(prophet_data['ds'])
    prophet_data['ds'] = prophet_data['ds'].dt.tz_localize(None)

    # Initialize the Prophet model
    model = Prophet(
        seasonality_mode='multiplicative',  # Proportional seasonal effects

        daily_seasonality=True,             # Capture daily variations (day-night cycles)
        changepoint_prior_scale=0.3,        # Adjust to control overfitting
        seasonality_prior_scale=5.0         # Adjust to control seasonality strength
    )

    # Fit the model
    model.fit(prophet_data)

    # Make future predictions
    future = model.make_future_dataframe(periods=180 * 24, freq='H')  # 180 days into the future
    forecast = model.predict(future)

    # Concatenate the actual and predicted data
    future_predictions = forecast.tail(180 * 24)
    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    energy_data_all = pd.concat([prophet_data, future_predictions])

    return energy_data_all


def model_energy_day(energy_data_all):
    # Resample the data to daily frequency, summing up the energy consumption
    df_daily = energy_data_all.set_index('ds').resample('D').sum().reset_index()

    # Prepare the data for Prophet
    prophet_data = df_daily.copy()
    prophet_data['ds'] = pd.to_datetime(prophet_data['ds']).dt.tz_localize(None)

    # Initialize the Prophet model
    model = Prophet(
        seasonality_mode='multiplicative',  # Use multiplicative seasonality

        daily_seasonality=True,            # Not needed for daily aggregated data
        changepoint_prior_scale=0.3,        # Controls the model's flexibility
        seasonality_prior_scale=10.0        # Increase to strengthen seasonality components
    )

    # Add custom weekly seasonality to differentiate weekdays and weekends
    model.add_seasonality(name='weekend_effect', period=7, fourier_order=3)
    
    # Fit the model
    model.fit(prophet_data)

    # Make future predictions for the next 180 days
    future = model.make_future_dataframe(periods=180, freq='D')
    forecast = model.predict(future)

    # Concatenate the actual and predicted data
    future_predictions = forecast[['ds', 'yhat']].tail(180)
    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    df_daily = pd.concat([prophet_data, future_predictions], ignore_index=True)

    return df_daily
def model_weather(dz_hour):
    dz_hour = dz_hour.rename(columns={'date': 'ds', 'temperature_2m': 'y'})
    dz_hour['ds'] = pd.to_datetime(dz_hour['ds'])
    dz_hour['ds'] = dz_hour['ds'].dt.tz_localize(None)
    df=dz_hour
    # Initialize the Prophet model with hyperparameters
    model = Prophet(
        seasonality_mode='multiplicative',  # Change to 'additive' if appropriate


        changepoint_prior_scale=0.3,  # Example: reduce if overfitting
        seasonality_prior_scale=5.0  # Example: adjust if seasonality is too strong
    )


    # Add custom seasonality if necessary
    model.add_seasonality(name='daily', period=1, fourier_order=5)

    model.fit(df)

    # Make predictions for the next 180 days with an hourly frequency
    future = model.make_future_dataframe(periods=180 * 24, freq='H')  # Extend 180 days into the future in hours
    forecast = model.predict(future)

    # Extract the actual and predicted values for the entire dataset (for evaluation purposes)
    actual_values = df['y'].values
    predicted_values = forecast.iloc[:len(df)]['yhat'].values  # Assuming 'yhat' contains the predicted values in the forecast

    # Calculate the Mean Absolute Error (MAE)
    # mae = mean_absolute_error(actual_values, predicted_values)


    # For the new predictions (next 180 days in hours)
    future_predictions1 = forecast.tail(180 * 24)


    future_predictions1 = future_predictions1.rename(columns={ 'yhat': 'y'})
    weather_data_hour= pd.concat([df, future_predictions1])
    return weather_data_hour



def model_weather_day(dz_day, regressors=None):
    """
    Model weather data using Prophet, optionally including additional regressors.

    Parameters:
    dz_day (pd.DataFrame): DataFrame with historical weather data, including 'date' and 'temperature_2m'.
    regressors (pd.DataFrame): Optional DataFrame with additional regressor columns aligned with 'dz_day'.

    Returns:
    pd.DataFrame: DataFrame with historical and forecasted weather data.
    """

    # Rename columns to fit Prophet's expected format
    dz_day = dz_day.rename(columns={'date': 'ds', 'temperature_2m': 'y'})
    dz_day['ds'] = pd.to_datetime(dz_day['ds'])
    dz_day['ds'] = dz_day['ds'].dt.tz_localize(None)

    # Prepare the DataFrame for Prophet
    df = dz_day.copy()

    # Initialize the Prophet model with hyperparameters
    model = Prophet(
        seasonality_mode='multiplicative',
        daily_seasonality=True,
        changepoint_prior_scale=0.3,
        seasonality_prior_scale=5.0
    )

    # Add custom seasonality (if necessary)
    model.add_seasonality(name='daily', period=1, fourier_order=5)

    # Add additional regressors if provided
    if regressors is not None:
        for reg in regressors.columns:
            model.add_regressor(reg)
        df = pd.concat([df, regressors], axis=1)

    # Fit the model to the data
    model.fit(df)

    # Make predictions for the next 180 days with a daily frequency
    future = model.make_future_dataframe(periods=180, freq='D')

    # Include regressors in future predictions (if provided)
    if regressors is not None:
        future = pd.concat([future, regressors.tail(180).reset_index(drop=True)], axis=1)

    forecast = model.predict(future)

    # Extract the actual and predicted values for the entire dataset (for evaluation purposes)
    actual_values = df['y'].values
    predicted_values = forecast['yhat'].iloc[:len(df)].values

    # Calculate the Mean Absolute Error (MAE)
    mae = mean_absolute_error(actual_values, predicted_values)


    # For the new predictions (next 180 days)
    future_predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(180)
    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    weather_data_day = pd.concat([df, future_predictions])

    return weather_data_day


def weather_present(weather_data_hour):
    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Define the coordinates for Whitefield, Bangalore
    location = Point(12.9698, 77.7500, 900)  # Latitude, Longitude, Altitude in meters

    # Calculate the current time in UTC and the time 52 hours ago in UTC
    end = datetime.utcnow()  # Get current UTC time
    start = end - timedelta(hours=52)  # Calculate start time

    # Fetch hourly weather data
    data = Hourly(location, start, end)
    data = data.fetch()
    data=data.reset_index()
    data= data.rename(columns={'time': 'ds', 'temp': 'y'})

    dz_hour = pd.DataFrame(weather_data_hour)
    df_small = pd.DataFrame(data)

    # Ensure the indices are the timestamps
    dz_hour.set_index('ds', inplace=True)
    df_small.set_index('ds', inplace=True)

    # Update the 'y' column in the larger DataFrame
    dz_hour.loc[df_small.index, 'y'] = df_small['y']

    # Reset index if needed
    dz_hour.reset_index(inplace=True)
    return dz_hour 

def weather_present_day(weather_data_day):
    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Define the coordinates for Whitefield, Bangalore
    location = Point(12.9698, 77.7500, 900)  # Latitude, Longitude, Altitude in meters

    # Calculate the current date and the date 3 days ago
    end = datetime.utcnow()  # Get current UTC datetime
    start = end - timedelta(days=3)  # Calculate start datetime

    # Fetch daily weather data
    data = Daily(location, start, end)
    data = data.fetch()
    data = data.reset_index()
    data = data.rename(columns={'time': 'ds', 'tavg': 'y'})

    # Convert 'ds' to datetime if it's not already
    data['ds'] = pd.to_datetime(data['ds'])

    dz_day = pd.DataFrame(weather_data_day)
    df_small = pd.DataFrame(data)

    # Ensure the indices are the timestamps
    dz_day['ds'] = pd.to_datetime(dz_day['ds'])  # Convert 'ds' to datetime
    df_small.set_index('ds', inplace=True)
    dz_day.set_index('ds', inplace=True)

    # Update the 'y' column in the larger DataFrame
    dz_day.loc[df_small.index, 'y'] = df_small['y']

    # Reset index if needed
    dz_day.reset_index(inplace=True)
    return dz_day
