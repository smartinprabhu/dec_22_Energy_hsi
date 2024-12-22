import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import numpy as np
def processing_eb(EB1_hour):

    # Convert to datetime and numeric
    EB1_hour['measured_ts'] = pd.to_datetime(EB1_hour['measured_ts'], errors='coerce')
    EB1_hour['Energy_Consumption'] = pd.to_numeric(EB1_hour['Energy_Consumption'], errors='coerce')

    # Filter for Energy_Consumption values below 10,000
    EB1_hour = EB1_hour[EB1_hour['Energy_Consumption'] < 10000]




    # Set the index to 'measured_ts'
    EB1_hour = EB1_hour.set_index("measured_ts")

    # Calculate weekday and hourly patterns
    weekday_patterns = EB1_hour.groupby(EB1_hour.index.dayofweek)['Energy_Consumption'].mean()
    hourly_patterns = {}
    for weekday in range(7):
        weekday_data = EB1_hour[EB1_hour.index.dayofweek == weekday]
        hourly_patterns[weekday] = weekday_data.groupby(weekday_data.index.hour)['Energy_Consumption'].mean()

    # Identify and remove values exceeding 10,000, marking them as missing
    EB1_hour.loc[EB1_hour['Energy_Consumption'] > 10000, 'Energy_Consumption'] = np.nan

    # Identify missing values
    missing_indices = EB1_hour[EB1_hour['Energy_Consumption'].isna()].index

    consecutive_missing = []
    replaced_values = {}

    def adjust_energy_consumption(timestamp, base_consumption):
        hour = timestamp.hour
        if 6 <= hour < 18:
            return base_consumption * np.random.uniform(1.3, 1.7)
        else:
            return base_consumption * np.random.uniform(0.5, 0.7)

    # Replace missing values using synthetic data
    for index in missing_indices:
        if index + pd.Timedelta(hours=1) in missing_indices:
            consecutive_missing.append(index)
        else:
            weekday = index.dayofweek
            hour = index.hour
            replaced_value = adjust_energy_consumption(index, hourly_patterns[weekday].get(hour, weekday_patterns[weekday]))
            EB1_hour.loc[index, 'Energy_Consumption'] = replaced_value
            replaced_values[index] = replaced_value

        if (index + pd.Timedelta(hours=1)) not in missing_indices or index == missing_indices[-1]:
            if consecutive_missing:
                weekday = consecutive_missing[0].dayofweek
                for missing_index in consecutive_missing:
                    hour = missing_index.hour
                    replaced_value = adjust_energy_consumption(missing_index, hourly_patterns[weekday].get(hour, weekday_patterns[weekday]))
                    EB1_hour.loc[missing_index, 'Energy_Consumption'] = replaced_value
                    replaced_values[missing_index] = replaced_value
                consecutive_missing = []

    # Reset index and rename columns
    EB1_hour = EB1_hour.reset_index()
    EB1_hour = EB1_hour.rename(columns={'measured_ts': 'ds', 'Energy_Consumption': 'y'})

    EB1_hour['day_night'] = EB1_hour['ds'].apply(lambda x: 1 if 6 <= x.hour < 18 else 0)
    # Create holidays dataframe (example for Sundays)
    holidays = pd.DataFrame({
        'holiday': 'sunday',
        'ds': EB1_hour[EB1_hour['ds'].dt.dayofweek == 6]['ds'],  # Sunday is day 6 in Python's weekday convention
        'lower_window': 0,
        'upper_window': 1,
    })
    model = Prophet(
        yearly_seasonality=True, 
        weekly_seasonality=True, 
        holidays=holidays,
        changepoint_prior_scale=0.1,
        seasonality_prior_scale=0.1,
        holidays_prior_scale=0.1,
        seasonality_mode='multiplicative',
        changepoint_range=0.8
    )
    train_data = EB1_hour[:-720]  # Assuming hourly data, last 720 hours (~30 days) for testing
    test_data = EB1_hour[-720:]
    model.add_regressor('day_night')
    model.fit(EB1_hour)

    # Create a future dataframe
    future = model.make_future_dataframe(periods=180 * 24, freq='H')  # 180 days into the future
    future['day_night'] = future['ds'].apply(lambda x: 1 if 6 <= x.hour < 18 else 0)

    # Make predictions
    forecast = model.predict(future)
    future_predictions = forecast.tail(180 * 24)
    # Evaluate with test data
    results = forecast.set_index('ds')[['yhat']].join(test_data.set_index('ds')['y'], how='inner')
    # Calculate MAE
    mae = mean_absolute_error(results['y'], results['yhat'])
    # print(f'Mean Absolute Error (MAE): {mae}')
    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    EB_hour = pd.concat([EB1_hour, future_predictions])

    return EB_hour
    


