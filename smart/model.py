"""
This module provides functionality for time series forecasting using the Prophet library and calculating costs based on smart washroom data.
"""

import numpy as np
import pandas as pd
from prophet import Prophet


def modeling_hour_count(pplin):


    # Initialize the Prophet model
    model = Prophet(changepoint_prior_scale=0.021151243479469943, seasonality_prior_scale=0.10548034148658945)

    # Fit the Prophet model to the dataset
    model.fit(pplin)



    # Calculate future start date
    future_start_date = pplin['ds'].max() + pd.Timedelta(hours=1)

    # Set future end date to the current day plus one month
    future_end_date = pd.Timestamp.now() + pd.DateOffset(months=2)


    # Create a DataFrame for future dates for forecasting
    future = pd.DataFrame({'ds': pd.date_range(start=future_start_date, end=future_end_date, freq='H')})

    # Make predictions for the future period
    future_forecast = model.predict(future)

    future_forecast['yhat'] = future_forecast['yhat'].apply(lambda x: np.exp(x) if x < 0 else x)
    future_forecast=future_forecast.rename(columns={'yhat':'y'})
    fin = pd.concat([pplin, future_forecast], ignore_index=True)
    return fin,future_forecast
    
    
    
    
    
def modeling_hour_iaqz(iaqz):
        
    # Initialize the Prophet model
    model = Prophet()

    # Fit the Prophet model to the dataset
    model.fit(iaqz)



    # Calculate future start date
    future_start_date1 = iaqz['ds'].max() + pd.Timedelta(hours=1)

    # Set future end date to the current day plus one month
    future_end_date1 = pd.Timestamp.now() + pd.DateOffset(months=2)

    # Create a DataFrame for future dates for forecasting
    future1 = pd.DataFrame({'ds': pd.date_range(start=future_start_date1, end=future_end_date1, freq='H')})

    # Make predictions for the future period
    future_forecast1 = model.predict(future1)
    future_forecast1=future_forecast1.rename(columns={'yhat':'y'})
    fin1 = pd.concat([iaqz, future_forecast1], ignore_index=True)
    return fin1,future_forecast1

def modeling_day(pplin):
    energy_data = pplin.set_index("ds").resample('D').sum().reset_index()
        
    # Initialize the Prophet model
    model = Prophet()

    # Fit the Prophet model to the dataset
    model.fit(energy_data)



    # Calculate future start date
    future_start_date = energy_data['ds'].max() + pd.Timedelta(days=1)

    # Set future end date to the current day plus one month
    future_end_date = pd.Timestamp.now() + pd.DateOffset(months=2)


    # Create a DataFrame for future dates for forecasting
    future = pd.DataFrame({'ds': pd.date_range(start=future_start_date, end=future_end_date, freq='D')})

    # Make predictions for the future period
    future_forecast = model.predict(future)
    future_forecast['yhat'] = future_forecast['yhat'].apply(lambda x: np.exp(x) if x < 0 else x)
    future_forecast=future_forecast.rename(columns={'yhat':'y'})
    df_daily = pd.concat([energy_data, future_forecast], ignore_index=True)
    return df_daily


