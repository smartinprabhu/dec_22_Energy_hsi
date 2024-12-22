import pandas as pd

from datetime import datetime
import datetime
import numpy as np

from datetime import datetime, timedelta

def calcualte(DG_hour,EB_hour,solar_hour,current_date):
    combined_df = pd.concat([DG_hour, EB_hour, solar_hour], ignore_index=True)

    # Group the data by the 'ds' column and sum the 'y' column
    energy_data_all = combined_df.groupby('ds')['y'].sum().reset_index()
    
    # Convert the 'ds' column to datetime
    energy_data_all['ds'] = pd.to_datetime(energy_data_all['ds'])


    building_area = 100000

    # Assume a population of 50,000 people
    population = 5000

    # Group the data by day and calculate the energy intensity for each day
    energy_intensities_per_sqft = []
    energy_intensities_per_capita = []
    for day, day_df in energy_data_all.groupby(energy_data_all['ds'].dt.date):
        total_consumption = day_df['y'].sum()
        energy_intensity_per_sqft = total_consumption / building_area
        energy_intensity_per_capita = total_consumption / population
        energy_intensities_per_sqft.append(energy_intensity_per_sqft)
        energy_intensities_per_capita.append(energy_intensity_per_capita)


    # Create the DataFrame
    energy_intensity_df = pd.DataFrame({
        'ds': energy_data_all['ds'].dt.date.unique(),
        'energy_intensity_per_sqft': energy_intensities_per_sqft,
        'energy_intensity_per_capita': energy_intensities_per_capita
    })
    energy_intensity_df['ds'] = pd.to_datetime(energy_intensity_df['ds'])


    filtered_E = energy_intensity_df[energy_intensity_df['ds'].dt.date == current_date]
    EIO = filtered_E['energy_intensity_per_capita'].values[0]
    EUI=filtered_E['energy_intensity_per_sqft'].values[0]
    EIO = f"{EIO:.2f}  ",
    EUI = f"{EUI:.2f}  ",
    return energy_data_all,building_area,population,EIO,EUI

def calcualte1(energy_data_all,current_date):

    # Convert the 'ds' column to datetime
    energy_data_all['ds'] = pd.to_datetime(energy_data_all['ds'])

    building_area = 100000
    population = 5000

    # Group the data by week number and year, and calculate the energy intensity for each week
    energy_intensities_per_sqft = []
    energy_intensities_per_capita = []
    week_numbers = []
    years = []

    # Group by year and week number, and calculate the total consumption for each week
    for (year, week_number), week_df in energy_data_all.groupby([energy_data_all['ds'].dt.isocalendar().year, energy_data_all['ds'].dt.isocalendar().week]):
        total_consumption = week_df['y'].sum()
        energy_intensity_per_sqft = total_consumption / building_area
        energy_intensity_per_capita = total_consumption / population
        energy_intensities_per_sqft.append(energy_intensity_per_sqft)
        energy_intensities_per_capita.append(energy_intensity_per_capita)
        week_numbers.append(week_number)
        years.append(year)

    # Create the DataFrame
    energy_intensity_df = pd.DataFrame({
        'year': years,
        'week_number': week_numbers,
        'energy_intensity_per_sqft': energy_intensities_per_sqft,
        'energy_intensity_per_capita': energy_intensities_per_capita
    })




    # Get the current date, year, and week number
    current_date = datetime.now()
    current_year = current_date.isocalendar().year
    current_week_number = current_date.isocalendar().week

    # Filter the DataFrame for the current week
    filtered_E = energy_intensity_df[(energy_intensity_df['year'] == current_year) & (energy_intensity_df['week_number'] == current_week_number)]

    if not filtered_E.empty:
        EIO1 = filtered_E['energy_intensity_per_capita'].values[0]
        EUI1 = filtered_E['energy_intensity_per_sqft'].values[0]
        EIO1 = f"{EIO1:.2f}  ",
        EUI1 = f"{EUI1:.2f}  ",
    return EIO1,EUI1

def calculate2(energy_data_all,current_date):
    # Convert the 'ds' column to datetime
    energy_data_all['ds'] = pd.to_datetime(energy_data_all['ds'])

    building_area = 100000
    population = 5000

    # Group the data by year and month, and calculate the energy intensity for each month
    energy_intensities_per_sqft = []
    energy_intensities_per_capita = []
    years = []
    months = []

    # Group by year and month, and calculate the total consumption for each month
    for (year, month), month_df in energy_data_all.groupby([energy_data_all['ds'].dt.year, energy_data_all['ds'].dt.month]):
        total_consumption = month_df['y'].sum()
        energy_intensity_per_sqft = total_consumption / building_area
        energy_intensity_per_capita = total_consumption / population
        energy_intensities_per_sqft.append(energy_intensity_per_sqft)
        energy_intensities_per_capita.append(energy_intensity_per_capita)
        years.append(year)
        months.append(month)

    # Create the DataFrame
    energy_intensity_df = pd.DataFrame({
        'year': years,
        'month': months,
        'energy_intensity_per_sqft': energy_intensities_per_sqft,
        'energy_intensity_per_capita': energy_intensities_per_capita
    })


    # Get the current date, year, and month
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Filter the DataFrame for the current month
    filtered_E = energy_intensity_df[(energy_intensity_df['year'] == current_year) & (energy_intensity_df['month'] == current_month)]

    if not filtered_E.empty:
        EIO2 = filtered_E['energy_intensity_per_capita'].values[0]
        EUI2 = filtered_E['energy_intensity_per_sqft'].values[0]
        EIO2 = f"{EIO2:.2f}  ",
        EUI2 = f"{EUI2:.2f}  ",
    return EIO2,EUI2

def calculate3(energy_data_all, current_date):
    # Convert the 'ds' column to datetime
    energy_data_all['ds'] = pd.to_datetime(energy_data_all['ds'])

    building_area = 100000
    population = 5000

    # Group the data by year and calculate the energy intensity for each year
    energy_intensities_per_sqft = []
    energy_intensities_per_capita = []
    years = []

    # Group by year, and calculate the total consumption for each year
    for year, year_df in energy_data_all.groupby(energy_data_all['ds'].dt.year):
        total_consumption = year_df['y'].sum()
        energy_intensity_per_sqft = total_consumption / building_area
        energy_intensity_per_capita = total_consumption / population
        energy_intensities_per_sqft.append(energy_intensity_per_sqft)
        energy_intensities_per_capita.append(energy_intensity_per_capita)
        years.append(year)

    # Create the DataFrame
    energy_intensity_df = pd.DataFrame({
        'year': years,
        'energy_intensity_per_sqft': energy_intensities_per_sqft,
        'energy_intensity_per_capita': energy_intensities_per_capita
    })


    # Get the current year
    current_year = current_date.year

    # Filter the DataFrame for the current year
    filtered_E = energy_intensity_df[energy_intensity_df['year'] == current_year]

    if not filtered_E.empty:
        EIO3 = filtered_E['energy_intensity_per_capita'].values[0]
        EUI3 = filtered_E['energy_intensity_per_sqft'].values[0]
        EIO3 = f"{EIO3:.2f}  ",
        EUI3 = f"{EUI3:.2f}  ",
    return EIO3, EUI3

