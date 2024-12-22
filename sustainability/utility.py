import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import numpy as np

def utility_process(df):

    # Convert to datetime and numeric
    df['measured_ts'] = pd.to_datetime(df['measured_ts'], errors='coerce')
    df['Energy_Consumption'] = pd.to_numeric(df['Energy_Consumption'], errors='coerce')
    if df.empty:
        raise ValueError("Dataframe is empty after filtering.")

    # Set the index to 'measured_ts'
    df = df.set_index("measured_ts")

    # Calculate weekday and hourly patterns
    weekday_patterns = df.groupby(df.index.dayofweek)['Energy_Consumption'].mean()
    hourly_patterns = {}
    for weekday in range(7):
        weekday_data = df[df.index.dayofweek == weekday]
        hourly_patterns[weekday] = weekday_data.groupby(weekday_data.index.hour)['Energy_Consumption'].mean()

    missing_indices = df[df['Energy_Consumption'].isna()].index

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
            df.loc[index, 'Energy_Consumption'] = replaced_value
            replaced_values[index] = replaced_value

        if (index + pd.Timedelta(hours=1)) not in missing_indices or index == missing_indices[-1]:
            if consecutive_missing:
                weekday = consecutive_missing[0].dayofweek
                for missing_index in consecutive_missing:
                    hour = missing_index.hour
                    replaced_value = adjust_energy_consumption(missing_index, hourly_patterns[weekday].get(hour, weekday_patterns[weekday]))
                    df.loc[missing_index, 'Energy_Consumption'] = replaced_value
                    replaced_values[missing_index] = replaced_value
                consecutive_missing = []



    # Reset index and rename columns
    df = df.reset_index()
    df = df.rename(columns={'measured_ts': 'ds', 'Energy_Consumption': 'y'})

    # Add the 'day_night' regressor
    df['day_night'] = df['ds'].apply(lambda x: 1 if 6 <= x.hour < 18 else 0)

    # Create holidays dataframe (example for Sundays)
    holidays = pd.DataFrame({
        'holiday': 'sunday',
        'ds': df[df['ds'].dt.dayofweek == 6]['ds'],  # Sunday is day 6 in Python's weekday convention
        'lower_window': 0,
        'upper_window': 1,
    })



    # Check if the dataframe has enough valid rows to proceed
    if df['y'].notna().sum() < 2:
        raise ValueError("Dataframe has less than 2 non-NaN rows after processing.")

    # Initialize the Prophet model
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

    train_data = df[:-720]  # Assuming hourly data, last 720 hours (~30 days) for testing
    test_data = df[-720:]

    model.add_regressor('day_night')
    model.fit(df)

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


    future_predictions = future_predictions.rename(columns={'yhat': 'y'})
    df = pd.concat([df, future_predictions])

    return df


