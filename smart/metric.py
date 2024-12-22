import datetime
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import pandas as pd
import pytz
import pandas as pd
from datetime import datetime, timedelta
import pytz

from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

def cal_met_day(fin,cost_per_hr):
    
    
    # Get the current date
    current_date = datetime.now().date()

    # Filter the DataFrame for the current day's data
    current_day_data = fin[fin['ds'].dt.date == current_date]
    today_total=round(current_day_data['y'].sum())

    yesterday_date = datetime.now().date() - timedelta(days=1)

    # Filter the DataFrame for yesterday's data
    yesterday_data = fin[fin['ds'].dt.date == yesterday_date]
    total_yesterday_consumption=round(yesterday_data['y'].sum())

    current_datetime = datetime.now()

    current_day_data_so_far = fin[
        (fin['ds'].dt.date == current_datetime.date()) &
        (fin['ds'].dt.hour <= current_datetime.hour)
    ]
    total_today_consumption_so_far=round(current_day_data_so_far['y'].sum())
    estimated_cost_today = today_total * cost_per_hr 


    rate_of_change_hour = (
        (today_total - total_yesterday_consumption) / total_yesterday_consumption
    ) * 100
    if rate_of_change_hour >= 0:
        rate_of_change_hour = f"{rate_of_change_hour:.2f} % ▴  "
    else:
        rate_of_change_hour = f"{rate_of_change_hour:.2f} % ▼  "




    # Constants
    num_people_per_tissue_roll = 200  # Number of people per tissue roll
    handwashing_solution_per_person = 0.05  # Amount of handwashing solution used per person (in liters)
    
    waste_generated_per_person = 0.005  # 50 g  Amount of waste generated per person (in kilograms)

    # Initialize cumulative count and tissue roll count
    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []


    fin = pd.DataFrame(fin)

    # Calculate cumulative counts and determine tissue roll usage
    for index, value in enumerate(fin['y'], start=1):
        cumulative_count += value
        cumulative_counts.append(cumulative_count)

        # Calculate number of tissue rolls used based on cumulative count
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)

        # Reset cumulative count if a tissue roll is used
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll

        # Calculate handwashing solution used
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)

        # Calculate waste generated
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    # Assign results to DataFrame
    fin['cumulative_count_tissue'] = cumulative_counts
    fin['tissue_roll_count'] = tissue_roll_counts
    fin['handwashing_solution_used'] = handwashing_solution_used
    fin['waste_generated'] = waste_generated
    
    updated_fin=fin
    # Define your timezone
    tz = pytz.timezone('Asia/Kolkata')

    # Get the current time with the specified timezone
    current_time = datetime.now(tz)

    # Calculate the end of the day
    end_of_day = current_time.replace(hour=23, minute=59, second=59)

    # Assuming 'fin' is your DataFrame
    today = current_time.date()
    today_data = fin[fin['ds'].dt.date == today]

    # Filter for remaining hours
    remaining_hours_data = today_data[(today_data['ds'] > current_time) & (today_data['ds'] <= end_of_day)]
    today_waste_generated=remaining_hours_data['waste_generated'].sum()
    today_handwash=remaining_hours_data['handwashing_solution_used'].sum()
    today_tissue=remaining_hours_data['tissue_roll_count'].sum()
    
    
    tomorrow = current_time.date() + timedelta(days=1)  # Get tomorrow's date
    tomorrow_data = fin[fin['ds'].dt.date == tomorrow]
    tomorrow_waste_generated=tomorrow_data['waste_generated'].sum()
    tomorrow_handwash=tomorrow_data['handwashing_solution_used'].sum()
    tomorrow_tissue=tomorrow_data['tissue_roll_count'].sum()
    
    
    predicted_waste = round(today_waste_generated + tomorrow_waste_generated, 2)
    predicted_handwash=round(today_handwash + tomorrow_handwash, 2)
    predicted_tissue=round(today_tissue + tomorrow_tissue, 2)




    # Get the current time
    current_time = datetime.now()

    # Filter data for today
    today = current_time.date()
    today_data = fin[fin['ds'].dt.date == today]

    # Calculate cumulative counts and determine cleaning schedule
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in today_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    today_data['cumulative_count'] = cumulative_counts
    today_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule
    cleaning_data = today_data[today_data["cleaning_schedule"] == 1]

    # Predict the remaining `y` values for the rest of the day
    remaining_hours = 24 - current_time.hour
    predicted_y = today_data['y'].mean()  # Simple prediction: average of today's data
    predicted_data = pd.DataFrame({
        'ds': pd.date_range(start=current_time + timedelta(hours=1), periods=remaining_hours, freq='H'),
        'y': [predicted_y] * remaining_hours
    })

    # Calculate cumulative counts and determine cleaning schedule for predicted data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in predicted_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    predicted_data['cumulative_count'] = cumulative_counts
    predicted_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for predicted data
    predicted_cleaning_data = predicted_data[predicted_data["cleaning_schedule"] == 1]

    # Combine the actual and predicted cleaning data
    combined_cleaning_data = pd.concat([cleaning_data, predicted_cleaning_data])

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = combined_cleaning_data.shape[0]
    required_man_hours_today = total_cleaning_sessions * cleaning_time_per_session


    # Filter data for tomorrow
    tomorrow = today + timedelta(days=1)
    tomorrow_data = fin[fin['ds'].dt.date == tomorrow]

    # Calculate cumulative counts and determine cleaning schedule for tomorrow
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in tomorrow_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    tomorrow_data['cumulative_count'] = cumulative_counts
    tomorrow_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for tomorrow
    cleaning_data_tomorrow = tomorrow_data[tomorrow_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning for tomorrow
    total_cleaning_sessions_tomorrow = cleaning_data_tomorrow.shape[0]
    required_man_hours_tomorrow = total_cleaning_sessions_tomorrow * cleaning_time_per_session

    predicted_handwash= f"{predicted_handwash:.2f} litres"
    predicted_waste=f"{predicted_waste:.2f} kg"
    #________________
    filtered_data = fin[fin['ds'].dt.date == current_date]
    today_waste = filtered_data['waste_generated'].sum()

    today_handwash = filtered_data['handwashing_solution_used'].sum()
    today_tissue = filtered_data['tissue_roll_count'].sum()
    current_hour = current_datetime.hour

    # Filter the DataFrame for the entire current date from 0th hour to the current hour
    filtered_data_so_far = fin[(fin['ds'].dt.date == current_date) &
                                     (fin['ds'].dt.hour <= current_hour)]

    # Sum the consumption or emissions up to the current hour
    today_so_far_waste = filtered_data_so_far['waste_generated'].sum()
    today_so_far_tissue = filtered_data_so_far['tissue_roll_count'].sum()
    today_so_far_handwash = filtered_data_so_far['handwashing_solution_used'].sum()

    # Get the current time
    current_time = datetime.now()

    # Filter data for today
    today = current_time.date()
    today_data = fin[fin['ds'].dt.date == today]

    # Calculate cumulative counts and determine cleaning schedule
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in today_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    today_data['cumulative_count'] = cumulative_counts
    today_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule
    cleaning_data = today_data[today_data["cleaning_schedule"] == 1]

    # Predict the remaining `y` values for the rest of the day
    remaining_hours = 24 - current_time.hour
    predicted_y = today_data['y'].mean()  # Simple prediction: average of today's data
    predicted_data = pd.DataFrame({
        'ds': pd.date_range(start=current_time + timedelta(hours=1), periods=remaining_hours, freq='H'),
        'y': [predicted_y] * remaining_hours
    })

    # Calculate cumulative counts and determine cleaning schedule for predicted data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in predicted_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    predicted_data['cumulative_count'] = cumulative_counts
    predicted_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for predicted data
    predicted_cleaning_data = predicted_data[predicted_data["cleaning_schedule"] == 1]

    # Combine the actual and predicted cleaning data
    combined_cleaning_data = pd.concat([cleaning_data, predicted_cleaning_data])

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = combined_cleaning_data.shape[0]
    required_man_hours_today = total_cleaning_sessions * cleaning_time_per_session


    # Assuming 'fin' is your DataFrame with datetime column 'ds' and values 'y'

    # Get the current time in the same timezone as your DataFrame
    timezone = pytz.timezone('Asia/Kolkata')  # Replace with your DataFrame's timezone
    current_time = datetime.now(timezone)

    # Filter data for today
    today = current_time.date()
    today_data = fin[fin['ds'].dt.date == today]

    # Calculate cumulative counts and determine cleaning schedule
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in today_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    today_data['cumulative_count'] = cumulative_counts
    today_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule
    cleaning_data = today_data[today_data["cleaning_schedule"] == 1]

    # Calculate required man-hours up to the current hour
    cleaning_sessions_up_to_now = cleaning_data[cleaning_data['ds'] <= current_time]
    total_cleaning_sessions_up_to_now = cleaning_sessions_up_to_now.shape[0]

    # Calculate required man-hours
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    required_man_hours_up_to_now = total_cleaning_sessions_up_to_now * cleaning_time_per_session

    print(f"Required man-hours up to now: {required_man_hours_up_to_now:.2f} hours")
    print(f"Required man-hours : {required_man_hours_today:.2f} hours")

    # Get the current time
    current_time = datetime.now()

    # Calculate yesterday's date
    yesterday = (current_time - timedelta(days=1)).date()

    # Filter data for yesterday
    yesterday_data = fin[fin['ds'].dt.date == yesterday]

    # Calculate cumulative counts and determine cleaning schedule for yesterday's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in yesterday_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    yesterday_data['cumulative_count'] = cumulative_counts
    yesterday_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for yesterday
    cleaning_data = yesterday_data[yesterday_data["cleaning_schedule"] == 1]

    # Predict the remaining `y` values for the rest of yesterday (if any)
    # Assuming the current time is within the same day, we predict for the remaining hours of yesterday
    remaining_hours = 24 - current_time.hour
    predicted_y = yesterday_data['y'].mean()  # Simple prediction: average of yesterday's data
    predicted_data = pd.DataFrame({
        'ds': pd.date_range(start=current_time - timedelta(hours=current_time.hour) + timedelta(hours=1), periods=remaining_hours, freq='H'),
        'y': [predicted_y] * remaining_hours
    })

    # Calculate cumulative counts and determine cleaning schedule for predicted data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in predicted_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    predicted_data['cumulative_count'] = cumulative_counts
    predicted_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for predicted data
    predicted_cleaning_data = predicted_data[predicted_data["cleaning_schedule"] == 1]

    # Combine the actual and predicted cleaning data
    combined_cleaning_data = pd.concat([cleaning_data, predicted_cleaning_data])

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = combined_cleaning_data.shape[0]
    required_man_hours_yesterday = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning yesterday: {required_man_hours_yesterday} hours")



    # Create a 2x2 subplot figure
    fig = make_subplots(rows=2, cols=1, subplot_titles=( 'Tissue', 'Handwash'))


    man_hours_now = round(required_man_hours_up_to_now, 2)
    man_hours_predicted = round(required_man_hours_today, 2)
    tissue_now = int(today_so_far_tissue)  # No decimals for tissue
    tissue_predicted = int(today_tissue)    # No decimals for tissue
    handwash_now = round(today_so_far_handwash, 2)
    handwash_predicted = round(today_handwash, 2)
    waste_now = round(today_so_far_waste, 2)
    waste_predicted = round(today_waste, 2)

    # Add subplots separately with their annotations
    # Tissue subplot (1,2)
    fig.add_trace(go.Bar(
        x=[tissue_now], y=['Tissue'],
        orientation='h', marker_color='#ff7f0e', showlegend=False,
        hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=[tissue_predicted - tissue_now], y=['Tissue'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
    ), row=1, col=1)

    # Annotation for Tissue
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
    fig.add_annotation(x=8, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
    fig.add_annotation(x=8, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

    # Handwash subplot (2,1)
    fig.add_trace(go.Bar(
        x=[handwash_now], y=['Handwash'],
        orientation='h', marker_color='#2ca02c', showlegend=False,
        hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        x=[handwash_predicted - handwash_now], y=['Handwash'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
    ), row=2, col=1)

    # Annotation for Handwash
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
    fig.add_annotation(x=160, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
    fig.add_annotation(x=160, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

    # Update layout for the entire figure
    fig.update_layout(
        template="plotly_dark",
        title='Estimated Consumables',
        title_y=0.92,
        title_x=0.03,
        height=300,
        width=300,
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        barmode='stack',
        bargap=0.2,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis2=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
        yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot

        margin=dict(l=30, r=30, t=100, b=50)
    )


    plot = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))

    return plot,required_man_hours_up_to_now,total_yesterday_consumption,updated_fin,required_man_hours_tomorrow,required_man_hours_today,predicted_waste,predicted_handwash,predicted_tissue,total_today_consumption_so_far,today_total,rate_of_change_hour,estimated_cost_today

def cal_met_week(df_daily,updated_fin,tz,cost_per_hr):
    


    # Assuming df_daily is your DataFrame and it has a 'date' column
    # Convert 'date' column to datetime format if it's not already
    df_daily['ds'] = pd.to_datetime(df_daily['ds'])

    # Get the current date with timezone info (Asia/Kolkata)
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Calculate the start of the current week (Monday) with timezone info
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current week (Sunday) with timezone info
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter the DataFrame for the current week's data
    current_week_data = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_week)]
    current_week_total=round(current_week_data['y'].sum())
    # Assuming df_daily is your DataFrame and it has a 'date' column
    # Convert 'date' column to datetime format if it's not already
    df_daily['ds'] = pd.to_datetime(df_daily['ds'])

    # Get the current date with timezone info (Asia/Kolkata)


    # Calculate the start of the current week (Monday) with timezone info
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # The end date is today with the current time
    end_of_today = current_date

    # Filter the DataFrame for the current week's data up to today
    current_week_data_up_to_today = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_today)]

    # Display the filtered DataFrame
    print(current_week_data_up_to_today)

    total_current_week_consumption_so_far =round( current_week_data_up_to_today['y'].sum())

    # Calculate the start of the current week (Monday) with timezone info
    start_of_current_week = current_date - timedelta(days=current_date.weekday())
    start_of_current_week = start_of_current_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the start of the previous week (Monday) with timezone info
    start_of_previous_week = start_of_current_week - timedelta(days=7)

    # Calculate the end of the previous week (Sunday) with timezone info
    end_of_previous_week = start_of_current_week - timedelta(seconds=1)

    # Filter the DataFrame for the previous week's data
    previous_week_data = df_daily[(df_daily['ds'] >= start_of_previous_week) & (df_daily['ds'] <= end_of_previous_week)]

    total_previous_week_consumption = previous_week_data['y'].sum()  # Previous week total

    # Output the results
    print(f"Total consumption for the current week: {current_week_total}")
    print(f"Total consumption for the current week up to today: {total_current_week_consumption_so_far}")
    print(f"Total consumption for the previous week: {total_previous_week_consumption}")


    rate_of_change_week = (
        (current_week_total - total_previous_week_consumption)
        / total_previous_week_consumption
    ) * 100

    if rate_of_change_week >= 0:
        rate_of_change_week = f"{rate_of_change_week:.2f} % ▴   "
    else:
        rate_of_change_week = f"{rate_of_change_week:.2f} % ▼    "

    estimated_cost_current_week = current_week_total * cost_per_hr
    

    # Assuming 'fin' is your DataFrame
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware
    start_of_week = current_time - pd.Timedelta(days=current_time.weekday())  # Get the start of the week (Monday)
    end_of_week = start_of_week + pd.Timedelta(days=6)  # Get the end of the week (Sunday)

    # Filter for remaining days of the week
    remaining_week_data = updated_fin[(updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_week)]

    # Determine the start of next week (next Monday)
    start_of_next_week = current_time + pd.Timedelta(days=(7 - current_time.weekday()))

    # Determine the end of next week (next Sunday)
    end_of_next_week = start_of_next_week + pd.Timedelta(days=6)  # This gives you the full week
    updated_fin=updated_fin.set_index('ds').resample('D').sum().reset_index()
    # Filter for the entire next week
    next_week_data = updated_fin[(updated_fin['ds'] > start_of_next_week) & (updated_fin['ds'] <= end_of_next_week)]

    # Calculate today's totals for remaining days of this week
    thisweek_waste_generated = remaining_week_data['waste_generated'].sum()
    thisweek_handwash = remaining_week_data['handwashing_solution_used'].sum()
    thisweek_tissue = remaining_week_data['tissue_roll_count'].sum()

    next_week_waste_generated = next_week_data['waste_generated'].sum()
    next_week_handwash = next_week_data['handwashing_solution_used'].sum()
    next_week_tissue = next_week_data['tissue_roll_count'].sum()
    predicted_tissue_week=round(thisweek_tissue + next_week_tissue, 2)
    predicted_handwash_week=round(thisweek_handwash + next_week_handwash, 2)
    predicted_waste_week=round(thisweek_waste_generated + next_week_waste_generated, 2)
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware
    start_of_week = current_time - pd.Timedelta(days=current_time.weekday())  # Get the start of the week (Monday)
    end_of_week = start_of_week + pd.Timedelta(days=6)  # Get the end of the week (Sunday)

    # Filter for remaining days of the week
    remaining_week_data = updated_fin[(updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_week)]
    # Determine the start of next week (next Monday)
    start_of_next_week = end_of_week + timedelta(days=0)

    # Determine the end of next week (next Sunday)
    end_of_next_week = start_of_next_week + pd.Timedelta(days=6)  # This gives you the full week
    # Filter for the entire next week
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours

    next_week_data = updated_fin[(updated_fin['ds'] >= start_of_next_week) & (updated_fin['ds'] <= end_of_next_week)]
    cleaning_data_tomorrow = next_week_data["cleaning_schedule"].sum()
    required_man_hours_next_week = cleaning_data_tomorrow * cleaning_time_per_session
    cleaning_data_today = remaining_week_data["cleaning_schedule"].sum()
    required_man_hours_current_week = cleaning_data_today* cleaning_time_per_session
    
    

    predicted_handwash_week= f"{predicted_handwash_week:.2f} litres"
    predicted_waste_week=f"{predicted_waste_week:.2f} kg"
    # Get the current time in the same timezone as your DataFrame
    timezone = pytz.timezone('Asia/Kolkata')  # Replace with your DataFrame's timezone
    current_time = datetime.now(timezone)

    # Calculate the start and end of the current week
    start_of_week = current_time - timedelta(days=current_time.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    end_of_week = start_of_week + timedelta(days=6)

    # Filter data for the current week
    week_data = updated_fin[(updated_fin['ds'] >= start_of_week) & (updated_fin['ds'] <= end_of_week)]

    week_data=week_data.set_index('ds').resample('D').sum().reset_index()
    # Calculate cumulative counts and determine cleaning schedule for the current week
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in week_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    week_data['cumulative_count'] = cumulative_counts
    week_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule
    cleaning_data = week_data[week_data["cleaning_schedule"] == 1]

    # Calculate required man-hours up to the current hour
    cleaning_sessions_up_to_now = cleaning_data[cleaning_data['ds'] <= current_time]
    total_cleaning_sessions_up_to_now = cleaning_sessions_up_to_now.shape[0]

    # Calculate required man-hours
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    required_man_hours_up_to_now = total_cleaning_sessions_up_to_now * cleaning_time_per_session

    # Predict the remaining `y` values for the rest of the week
    remaining_days = (end_of_week - current_time).days
    remaining_hours = remaining_days * 24 + (24 - current_time.hour)
    predicted_y = week_data['y'].mean()  # Simple prediction: average of this week's data
    predicted_data = pd.DataFrame({
        'ds': pd.date_range(start=current_time + timedelta(hours=1), periods=remaining_hours, freq='H'),
        'y': [predicted_y] * remaining_hours
    })

    # Calculate cumulative counts and determine cleaning schedule for predicted data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in predicted_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    predicted_data['cumulative_count'] = cumulative_counts
    predicted_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for predicted data
    predicted_cleaning_data = predicted_data[predicted_data["cleaning_schedule"] == 1]

    # Combine the actual and predicted cleaning data
    combined_cleaning_data = pd.concat([cleaning_data, predicted_cleaning_data])

    # Calculate the required man-hours for cleaning for the entire week
    total_cleaning_sessions = combined_cleaning_data.shape[0]
    required_man_hours_week = total_cleaning_sessions * cleaning_time_per_session
    current_datetime = pd.Timestamp.now(tz)
    # Print the results
    print(f"Required man-hours up to now: {required_man_hours_up_to_now} hours")
    print(f"Total required man-hours for the week: {required_man_hours_week} hours")
    current_date = current_datetime.date()
    start_date = current_date - pd.Timedelta(days=current_date.weekday())
    end_date = start_date + pd.Timedelta(days=6)

    # Filter data for the current week
    DG_week = updated_fin[(updated_fin['ds'].dt.date >= start_date) & (updated_fin['ds'].dt.date <= end_date)]
    weekly_tissue = DG_week['tissue_roll_count'].sum()
    weekly_wash = DG_week['handwashing_solution_used'].sum()
    weekly_waste = DG_week['waste_generated'].sum()
    DG_week_today = DG_week[DG_week['ds'].dt.date <= current_date]
    weekly_so_far_tissue = DG_week_today['tissue_roll_count'].sum()
    weekly_so_far_wash = DG_week_today['handwashing_solution_used'].sum()
    weekly_so_far_waste = DG_week_today['waste_generated'].sum()
    DG_week_today = DG_week[DG_week['ds'].dt.date <= current_date]
    # weekly_so_far_emission_dg = DG_week_today['emission'].sum()

    # Create a 2x2 subplot figure
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Man Hours', 'Tissue', 'Handwash', 'Waste'))

    # Data values for each subplot
    man_hours_now = round(required_man_hours_up_to_now, 2)
    man_hours_predicted = round(required_man_hours_week, 2)
    tissue_now = int(weekly_so_far_tissue)  # No decimals for tissue
    tissue_predicted = int(weekly_tissue)    # No decimals for tissue
    handwash_now = round(weekly_so_far_wash, 2)
    handwash_predicted = round(weekly_wash, 2)
    waste_now = round(weekly_so_far_waste, 2)
    waste_predicted = round(weekly_waste, 2)

    # Add subplots separately with their annotations

    # Man Hours subplot (1,1)
    fig.add_trace(go.Bar(
        x=[man_hours_now], y=['Man Hours'],
        orientation='h', marker_color='#1f77b4', showlegend=False,
        hovertemplate=f'Till Now: {man_hours_now} Hrs'
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=[man_hours_predicted - man_hours_now], y=['Man Hours'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {man_hours_predicted} Hrs'
    ), row=1, col=1)

    # Annotation for Man Hours
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{man_hours_now} Hrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
    fig.add_annotation(x=8.8, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
    fig.add_annotation(x=8.8, y=-1, text=f'{man_hours_predicted} Hrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")

    # Tissue subplot (1,2)
    fig.add_trace(go.Bar(
        x=[tissue_now], y=['Tissue'],
        orientation='h', marker_color='#ff7f0e', showlegend=False,
        hovertemplate=f'Till Now: {tissue_now} Rolls'
    ), row=1, col=2)
    fig.add_trace(go.Bar(
        x=[tissue_predicted - tissue_now], y=['Tissue'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {tissue_predicted} Rolls'
    ), row=1, col=2)

    # Annotation for Tissue
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
    fig.add_annotation(x=8, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
    fig.add_annotation(x=8, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                    font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

    # Handwash subplot (2,1)
    fig.add_trace(go.Bar(
        x=[handwash_now], y=['Handwash'],
        orientation='h', marker_color='#2ca02c', showlegend=False,
        hovertemplate=f'Till Now: {handwash_now} Ltrs'
    ), row=2, col=1)
    fig.add_trace(go.Bar(
        x=[handwash_predicted - handwash_now], y=['Handwash'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {handwash_predicted} Ltrs'
    ), row=2, col=1)

    # Annotation for Handwash
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x3", yref="y3", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x3", yref="y3", xanchor="left")
    fig.add_annotation(x=155, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x3", yref="y3", xanchor="right")
    fig.add_annotation(x=155, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                    font=dict(color="white", size=12), xref="x3", yref="y3", xanchor="right")

    # Waste subplot (2,2)
    fig.add_trace(go.Bar(
        x=[waste_now], y=['Waste'],
        orientation='h', marker_color='#f05a5a', showlegend=False,
        hovertemplate=f'Till Now: {waste_now} Kg'
    ), row=2, col=2)
    fig.add_trace(go.Bar(
        x=[waste_predicted - waste_now], y=['Waste'],
        orientation='h', marker_color='gray', showlegend=False,
        hovertemplate=f'Predicted: {waste_predicted} Kg'
    ), row=2, col=2)

    # Annotation for Waste
    fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                    font=dict(color="white", size=12), xref="x4", yref="y4", xanchor="left")
    fig.add_annotation(x=0, y=-1, text=f'{waste_now} Kg', showarrow=False,
                    font=dict(color="white", size=12), xref="x4", yref="y4", xanchor="left")
    fig.add_annotation(x=78, y=0.7, text=f'Predicted', showarrow=False,
                    font=dict(color="white", size=12), xref="x4", yref="y4", xanchor="right")
    fig.add_annotation(x=78, y=-1, text=f'{waste_predicted} Kg', showarrow=False,
                    font=dict(color="white", size=12), xref="x4", yref="y4", xanchor="right")

    # Update layout for the entire figure
    fig.update_layout(
        template="plotly_dark",
        title='Estimated Consumables',
        title_y=0.92,
        title_x=0.03,
        height=300,
        width=800,
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
        barmode='stack',
        bargap=0.2,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis2=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis3=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis4=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    plot1 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))


     
    return plot1,total_previous_week_consumption,required_man_hours_current_week,required_man_hours_next_week,predicted_waste_week,predicted_tissue_week,predicted_handwash_week, total_current_week_consumption_so_far,current_week_total,rate_of_change_week,estimated_cost_current_week
def cal_met_month(df_daily,tz,updated_fin,cost_per_hr):
    current_datetime = datetime.now(tz)
    # Calculate the start of the current month

    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current month
    if current_datetime.month == 12:
        end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(seconds=1)
    else:
        end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(seconds=1)

    # Ensure both are timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))
    end_of_month = tz.localize(end_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's datacurrent_datetime
    current_month_data = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= end_of_month)
    ]
    current_month_total=current_month_data['y'].sum() #### 1 curent month total
    # Calculate the start of the previous month
    start_of_previous_month = (current_datetime.replace(day=1) - relativedelta(months=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the previous month
    end_of_previous_month = (current_datetime.replace(day=1) - timedelta(seconds=1)).replace(hour=23, minute=59, second=59)

    # Ensure both are timezone-aware
    start_of_previous_month = tz.localize(start_of_previous_month.replace(tzinfo=None))
    end_of_previous_month = tz.localize(end_of_previous_month.replace(tzinfo=None))

    # Filter the DataFrame for the previous month's data
    previous_month_data = df_daily[
        (df_daily['ds'] >= start_of_previous_month) & (df_daily['ds'] <= end_of_previous_month)
    ]
    total_previous_month_consumption=previous_month_data['y'].sum() #### 2 previous month total
    current_datetime = datetime.now(tz)

    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Ensure the start of the month is timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's data up to today
    current_month_data_up_to_today = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= current_datetime)
    ]
    total_current_month_consumption_so_far=current_month_data_up_to_today['y'].sum() ### 3 so far this  month
    rate_of_change_month = (
        (current_month_total - total_previous_month_consumption)
        / total_previous_month_consumption
    ) * 100
    if rate_of_change_month >= 0:
        rate_of_change_month = f"{rate_of_change_month:.2f} % ▴  "
    else:
        rate_of_change_month = f"{rate_of_change_month:.2f} % ▼   "
    
    estimated_cost_current_month = current_month_total * cost_per_hr 



    # Assuming 'updated_fin' is your DataFrame and 'tz' is defined
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware

    # Set the DataFrame index and resample by day
    updated_fin = updated_fin.set_index('ds').resample('D').sum().reset_index()

    # Get the current month and year
    current_month = current_time.month
    current_year = current_time.year

    # Determine the start of the current month and the end of the current month
    start_of_current_month = current_time.replace(day=1)
    end_of_current_month = (start_of_current_month + pd.offsets.MonthEnd(0))

    # Determine the start of the next month
    start_of_next_month = end_of_current_month + timedelta(days=1)

    # Determine the end of the next month
    end_of_next_month = start_of_next_month + pd.offsets.MonthEnd(0)

    # Filter for the remaining days of the current month and the entire next month
    remaining_and_next_month_data = updated_fin[(updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_next_month)]

    # Calculate totals for the remaining days of the current month and the entire next month
    total_waste_generated = remaining_and_next_month_data['waste_generated'].sum()
    total_handwash = remaining_and_next_month_data['handwashing_solution_used'].sum()
    total_tissue = remaining_and_next_month_data['tissue_roll_count'].sum()

    # Predict totals for the month
    predicted_tissue_month = round(total_tissue, 2)
    predicted_handwash_month = round(total_handwash, 2)
    predicted_waste_month = round(total_waste_generated, 2)


    # Get the current month and year
    current_month = current_time.month
    current_year = current_time.year

    # Determine the start of the current month and the end of the current month
    start_of_current_month = current_time.replace(day=1)
    end_of_current_month = (start_of_current_month + pd.offsets.MonthEnd(0))

    # Determine the start of the next month
    start_of_next_month = end_of_current_month + timedelta(days=1)

    # Determine the end of the next month
    end_of_next_month = start_of_next_month + pd.offsets.MonthEnd(0)



    # Calculate the required man-hours for cleaning for the remaining days of the current month and next month
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    remaining_data = updated_fin[(updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_current_month)]
    cleaning_data_this_month = remaining_data["cleaning_schedule"].sum()
    required_man_hours_current_month = cleaning_data_this_month * cleaning_time_per_session
    next_month_data = updated_fin[(updated_fin['ds'] >= start_of_next_month) & (updated_fin['ds'] <= end_of_next_month)]
    cleaning_data_next_month = next_month_data["cleaning_schedule"].sum()
    required_man_hours_next_month = cleaning_data_next_month * cleaning_time_per_session

    predicted_handwash_month= f"{predicted_handwash_month:.2f} litres"
    predicted_waste_month=f"{predicted_waste_month:.2f} kg"
    return total_previous_month_consumption,required_man_hours_current_month,required_man_hours_next_month,cleaning_data_next_month,predicted_tissue_month,predicted_handwash_month,predicted_waste_month,total_current_month_consumption_so_far,current_month_total,rate_of_change_month,estimated_cost_current_month
def cal_met_year(df_monthly,updated_fin,cost_per_hr):


    # Get the current year
    current_year = datetime.now().year

    df_current_year = df_monthly[df_monthly['ds'].dt.year == current_year]
    current_year_total=df_current_year['y'].sum() 

    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Filter the dataframe to get data up to the current month
    df_current_year_month = df_current_year[(df_current_year['ds'].dt.year <= current_year) & (df_current_year['ds'].dt.month <= current_month)]
    total_current_year_consumption_so_far=df_current_year_month['y'].sum()


    # Get the current year
    current_year = datetime.now().year

    # Get the previous year
    previous_year = current_year - 1

    # Filter the dataframe to get data for the previous year
    df_previous_year = df_monthly[df_monthly['ds'].dt.year == previous_year]
    total_previous_year_consumption=df_previous_year['y'].sum() #### 3

    # Calculate the rate of change
    rate_of_change_year = (
        (current_year_total - total_previous_year_consumption) / total_previous_year_consumption
    ) * 100
    estimated_cost_current_year=current_year_total*cost_per_hr
    if rate_of_change_year >= 0:
        rate_of_change_year = f"{rate_of_change_year:.2f} % ▴  "
    else:
        rate_of_change_year = f"{rate_of_change_year:.2f} % ▼    "
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware

    # Set the DataFrame index and resample by month
    updated_fin = updated_fin.set_index('ds').resample('M').sum().reset_index()

    # Get the current year
    current_year = current_time.year

    # Determine the start and end of the current year
    start_of_current_year = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_current_year = current_time.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # Determine the start and end of the next year
    start_of_next_year = end_of_current_year + timedelta(days=1)
    end_of_next_year = start_of_next_year.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # Filter for the remaining days of the current year and the entire next year
    remaining_and_next_year_data = updated_fin[
        (updated_fin['ds'] > current_time) &
        ((updated_fin['ds'] <= end_of_current_year) | (updated_fin['ds'] >= start_of_next_year) & (updated_fin['ds'] <= end_of_next_year))
    ]

    # Calculate totals for the remaining days of the current year and the entire next year
    total_waste_generated = remaining_and_next_year_data['waste_generated'].sum()
    total_handwash = remaining_and_next_year_data['handwashing_solution_used'].sum()
    total_tissue = remaining_and_next_year_data['tissue_roll_count'].sum()

    # Predict totals for the years
    predicted_tissue_year = round(total_tissue, 2)
    predicted_handwash_year = round(total_handwash, 2)
    predicted_waste_year = round(total_waste_generated, 2)

    # Get the current year
    current_year = current_time.year

    # Determine the start and end of the current year
    start_of_current_year = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_current_year = current_time.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # Determine the start and end of the next year
    start_of_next_year = end_of_current_year + timedelta(days=1)
    end_of_next_year = start_of_next_year.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    # Filter for the remaining days of the current year
    remaining_current_year_data = updated_fin[(updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_current_year)]

    # Filter for the entire next year
    next_year_data = updated_fin[(updated_fin['ds'] >= start_of_next_year) & (updated_fin['ds'] <= end_of_next_year)]

    # Calculate the required man-hours for cleaning for the remaining days of the current year
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    
    cleaning_data_this_month = remaining_current_year_data["cleaning_schedule"].sum()
    required_man_hours_current_year = cleaning_data_this_month * cleaning_time_per_session

    cleaning_data_next_month = next_year_data["cleaning_schedule"].sum()
    required_man_hours_next_year = cleaning_data_next_month * cleaning_time_per_session
    predicted_handwash_year= f"{predicted_handwash_year:.2f} litres"
    predicted_waste_year=f"{predicted_waste_year:.2f} kg"
    return predicted_tissue_year,required_man_hours_next_year,required_man_hours_current_year,predicted_handwash_year,predicted_waste_year,total_previous_year_consumption,total_current_year_consumption_so_far,current_year_total,rate_of_change_year,estimated_cost_current_year

def cal_met_workweek(df_workweek,updated_fin,tz,cost_per_hr):

    # Get the current date and time in the specified timezone
    current_datetime = datetime.now(tz)

    # Find the start of the week (Sunday) in the specified timezone
    start_of_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # Find the end of the week (Saturday) in the specified timezone
    end_of_week = start_of_week + timedelta(days=6)

    # Convert both to timezone-aware datetimes
    start_of_week = tz.localize(start_of_week.replace(tzinfo=None))
    end_of_week = tz.localize(end_of_week.replace(tzinfo=None))

    # Filter the DataFrame for the current week's data
    weekly_data_workweek = df_workweek[
        (df_workweek['ds'] >= start_of_week) & (df_workweek['ds'] <= end_of_week)
    ]
    current_workweek_total=weekly_data_workweek['y'].sum() 

    # Find the start of the week (Sunday) in the specified timezone
    start_of_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # Ensure start_of_week is timezone-aware
    start_of_week = tz.localize(start_of_week.replace(tzinfo=None))

    # Filter the DataFrame for the current week's data up to today
    workweek_data_up_to_today = df_workweek[
        (df_workweek['ds'] >= start_of_week) & (df_workweek['ds'] <= current_datetime)]
    total_current_workweek_consumption_so_far=workweek_data_up_to_today['y'].sum()
    start_of_current_week = current_datetime - timedelta(days=current_datetime.weekday() + 1)

    # Calculate the start and end of last week
    start_of_last_week = start_of_current_week - timedelta(days=7)
    end_of_last_week = start_of_current_week - timedelta(seconds=1) 

    # Ensure both are timezone-aware
    start_of_last_week = tz.localize(start_of_last_week.replace(tzinfo=None))
    end_of_last_week = tz.localize(end_of_last_week.replace(tzinfo=None))

    # Filter the DataFrame for last week's data
    last_workweek_data = df_workweek[
        (df_workweek['ds'] >= start_of_last_week) & (df_workweek['ds'] <= end_of_last_week)
        
    ]
    total_previous_workweek_consumption=last_workweek_data['y'].sum()
    rate_of_change_workweek = (
        (current_workweek_total - total_previous_workweek_consumption)
        / total_previous_workweek_consumption
    ) * 100

    if rate_of_change_workweek >= 0:
        rate_of_change_workweek = f"{rate_of_change_workweek:.2f} % ▴   "
    else:
        rate_of_change_workweek = f"{rate_of_change_workweek:.2f} % ▼    "

    estimated_cost_current_workweek=current_workweek_total*cost_per_hr
    
    


    # Assuming 'updated_fin' is your DataFrame and 'tz' is defined
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware

    # Set the DataFrame index and resample by day
    updated_fin = updated_fin.set_index('ds').resample('D').sum().reset_index()

    # Determine the start and end of the current workweek (Monday to Friday)
    current_weekday = current_time.weekday()
    start_of_current_workweek = current_time - timedelta(days=current_weekday)
    start_of_current_workweek = start_of_current_workweek.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_current_workweek = start_of_current_workweek + timedelta(days=4, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Determine the start and end of the next workweek
    start_of_next_workweek = end_of_current_workweek + timedelta(days=3)  # Skip the weekend
    end_of_next_workweek = start_of_next_workweek + timedelta(days=4, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter for the remaining days of the current workweek and the entire next workweek
    remaining_and_next_workweek_data = updated_fin[
        (updated_fin['ds'] > current_time) &
        ((updated_fin['ds'] <= end_of_current_workweek) | (updated_fin['ds'] >= start_of_next_workweek) & (updated_fin['ds'] <= end_of_next_workweek))
    ]

    # Calculate totals for the remaining days of the current workweek and the entire next workweek
    total_waste_generated = remaining_and_next_workweek_data['waste_generated'].sum()
    total_handwash = remaining_and_next_workweek_data['handwashing_solution_used'].sum()
    total_tissue = remaining_and_next_workweek_data['tissue_roll_count'].sum()

    # Predict totals for the workweeks
    predicted_tissue_workweek = round(total_tissue, 2)
    predicted_handwash_workweek = round(total_handwash, 2)
    predicted_waste_workweek = round(total_waste_generated, 2)
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours

    # Determine the start and end of the current workweek (Monday to Friday)
    current_weekday = current_time.weekday()
    start_of_current_workweek = current_time - timedelta(days=current_weekday)
    start_of_current_workweek = start_of_current_workweek.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_current_workweek = start_of_current_workweek + timedelta(days=4, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Determine the start and end of the next workweek
    start_of_next_workweek = end_of_current_workweek + timedelta(days=3)  # Skip the weekend
    end_of_next_workweek = start_of_next_workweek + timedelta(days=4, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter for the remaining days of the current workweek
    remaining_workweek_data = updated_fin[
        (updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_current_workweek)
    ]

    # Filter for the entire next workweek
    next_workweek_data = updated_fin[
        (updated_fin['ds'] >= start_of_next_workweek) & (updated_fin['ds'] <= end_of_next_workweek)
    ]
    cleaning_data_this_month = remaining_workweek_data["cleaning_schedule"].sum()
    required_man_hours_current_workweek = cleaning_data_this_month * cleaning_time_per_session

    cleaning_data_next_month = next_workweek_data["cleaning_schedule"].sum()
    required_man_hours_next_workweek = cleaning_data_next_month * cleaning_time_per_session
    predicted_handwash_workweek = f"{predicted_handwash_workweek:.2f} litres"
    predicted_waste_workweek=f"{predicted_waste_workweek:.2f} kg"
    return total_previous_workweek_consumption,required_man_hours_next_workweek,required_man_hours_current_workweek,predicted_waste_workweek,predicted_handwash_workweek,predicted_tissue_workweek,total_current_workweek_consumption_so_far,current_workweek_total,rate_of_change_workweek,estimated_cost_current_workweek

def cal_met_weekend(forecast_data_weekend_cal,updated_fin, historical_data_daily, df_daily, cost_per_hr):
    current_weekend_total = forecast_data_weekend_cal['y'].sum()
    last_weekend = historical_data_daily[historical_data_daily['ds'].dt.weekday >= 5].iloc[-3:-1]
    total_previous_weekend_consumption = last_weekend['y'].sum()

    # Get the current weekend's data
    today = pd.Timestamp.today().date()
    current_weekend_s = df_daily[(df_daily['ds'].dt.date >= today - pd.Timedelta(days=today.weekday() - 5)) & 
                                 (df_daily['ds'].dt.date <= today)]
    total_current_weekend_consumption_so_far = current_weekend_s['y'].sum()

    rate_of_change_weekend = 0
    if total_previous_weekend_consumption > 0:  # To avoid division by zero
        rate_of_change_weekend = (
            (current_weekend_total - total_previous_weekend_consumption)
            / total_previous_weekend_consumption
        ) * 100

    if rate_of_change_weekend >= 0:
        rate_of_change_weekend = f"{rate_of_change_weekend:.2f}  ▴   "
    else:
        rate_of_change_weekend = f"{rate_of_change_weekend:.2f}  ▼  "


    estimated_cost_current_weekend = current_weekend_total * cost_per_hr
    tz = pytz.timezone("Asia/Kolkata")
    # Assuming 'updated_fin' is your DataFrame and 'tz' is defined
    current_time = datetime.now(tz)  # Ensure current_time is timezone-aware

    # Set the DataFrame index and resample by day
    updated_fin = updated_fin.set_index('ds').resample('D').sum().reset_index()

    # Determine the start and end of the current weekend (Saturday to Sunday)
    current_weekday = current_time.weekday()
    if current_weekday < 5:  # If today is a weekday (Monday to Friday)
        start_of_current_weekend = current_time + timedelta(days=(5 - current_weekday))
        start_of_current_weekend = start_of_current_weekend.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_current_weekend = start_of_current_weekend + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)
    else:  # If today is Saturday or Sunday
        start_of_current_weekend = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_current_weekend = start_of_current_weekend + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Determine the start and end of the next weekend
    start_of_next_weekend = end_of_current_weekend + timedelta(days=6)  # Skip the weekdays
    end_of_next_weekend = start_of_next_weekend + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter for the remaining days of the current weekend and the entire next weekend
    remaining_and_next_weekend_data = updated_fin[
        (updated_fin['ds'] > current_time) &
        ((updated_fin['ds'] <= end_of_current_weekend) | (updated_fin['ds'] >= start_of_next_weekend) & (updated_fin['ds'] <= end_of_next_weekend))
    ]

    # Calculate totals for the remaining days of the current weekend and the entire next weekend
    total_waste_generated = remaining_and_next_weekend_data['waste_generated'].sum()
    total_handwash = remaining_and_next_weekend_data['handwashing_solution_used'].sum()
    total_tissue = remaining_and_next_weekend_data['tissue_roll_count'].sum()

    # Predict totals for the weekends
    predicted_tissue_weekend = round(total_tissue, 2)
    predicted_handwash_weekend = round(total_handwash, 2)
    predicted_waste_weekend = round(total_waste_generated, 2)

    # Determine the start and end of the next weekend
    start_of_next_weekend = end_of_current_weekend + timedelta(days=6)  # Skip the weekdays
    end_of_next_weekend = start_of_next_weekend + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter for the remaining days of the current weekend
    remaining_weekend_data = updated_fin[
        (updated_fin['ds'] > current_time) & (updated_fin['ds'] <= end_of_current_weekend)
    ]

    # Filter for the entire next weekend
    next_weekend_data = updated_fin[
        (updated_fin['ds'] >= start_of_next_weekend) & (updated_fin['ds'] <= end_of_next_weekend)
    ]

    # Calculate the required man-hours for cleaning for the remaining days of the current weekend
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    
    cleaning_data_this_month = remaining_weekend_data["cleaning_schedule"].sum()
    required_man_hours_current_weekend = cleaning_data_this_month * cleaning_time_per_session

    cleaning_data_next_month = next_weekend_data["cleaning_schedule"].sum()
    required_man_hours_next_weekend = cleaning_data_next_month * cleaning_time_per_session
    predicted_handwash_weekend = f"{predicted_handwash_weekend:.2f} litres"
    predicted_waste_weekend=f"{predicted_waste_weekend:.2f} kg"

    return (
        required_man_hours_current_weekend,
        required_man_hours_next_weekend,
        predicted_tissue_weekend,
        predicted_handwash_weekend,
        predicted_waste_weekend,
        total_previous_weekend_consumption,
        total_current_weekend_consumption_so_far,
        current_weekend_total,
        rate_of_change_weekend,
        estimated_cost_current_weekend,
    )
