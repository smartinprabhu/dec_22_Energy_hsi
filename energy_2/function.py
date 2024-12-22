import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta

def function_target(energy_data_all,dz_hour,tz):

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



    return data


