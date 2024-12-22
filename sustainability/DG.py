import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import numpy as np


def processing(DG1_hour):
    
    df = pd.DataFrame(DG1_hour)
    df['ds'] = pd.to_datetime(df['ds'])

    # Initialize and fit the Prophet model
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)

    # Optionally add custom seasonalities
    model.add_seasonality(name='daily', period=24, fourier_order=8)
    model.add_seasonality(name='weekly', period=7, fourier_order=3)

    model.fit(df)

    # Create a dataframe with future dates
    future = model.make_future_dataframe(periods=180*24, freq='H')  # 30 days into the future

    # Forecast
    forecast = model.predict(future)


    def adjust_predictions_based_on_pattern(df):
        # Example adjustment logic (update as needed based on actual patterns)
        # For instance, if EB is operational, DG usage should be zero or minimal
        # Implement actual pattern-based adjustments here
        df['adjusted_yhat'] = df['yhat']
        df.loc[df['ds'].dt.hour.between(8, 20), 'adjusted_yhat'] = 0  # Example: zero usage during daytime hours
        return df

    forecast = adjust_predictions_based_on_pattern(forecast)

    forecast['yhat'] = forecast['yhat'].apply(lambda x: np.exp(x) if x < 0 else x)
    future_predictions = forecast.tail(180 * 24)

    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    DG_hour = pd.concat([DG1_hour, future_predictions])
    DG_hour['y'] = DG_hour['y'].round(2)



  
    return DG_hour