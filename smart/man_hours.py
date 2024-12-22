import pandas as pd
from datetime import datetime, timedelta
import json
from datetime import timedelta

import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.graph_objects as go
import pandas as pd

from datetime import datetime, timedelta
import pytz

def man_hours(fin):
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

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_yesterday = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning yesterday: {required_man_hours_yesterday} hours")

    # Get the current time
    current_time = datetime.now()

    # Calculate today's date
    today = current_time.date()

    # Filter data for today
    today_data = fin[fin['ds'].dt.date == today]

    # Calculate cumulative counts and determine cleaning schedule for today's data
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

    # Filter the DataFrame to get the cleaning schedule for today
    cleaning_data = today_data[today_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_today = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning today: {required_man_hours_today} hours")

    # Get the current time
    current_time = datetime.now()

    # Calculate today's date
    today = current_time.date()

    # Filter data for today
    today_data = fin[fin['ds'].dt.date == today]

    # Filter data up to the current hour
    current_hour = current_time.hour
    today_data_upto_current_hour = today_data[today_data['ds'].dt.hour <= current_hour]
    # Calculate cumulative counts and determine cleaning schedule for today's data up to the current hour
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in today_data_upto_current_hour['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    today_data_upto_current_hour['cumulative_count'] = cumulative_counts
    today_data_upto_current_hour['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for today up to the current hour
    cleaning_data = today_data_upto_current_hour[today_data_upto_current_hour["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_today_upto_current_hour = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning today up to the current hour: {required_man_hours_today_upto_current_hour} hours")


    total_yesterday_consumption=required_man_hours_yesterday
    this_day=required_man_hours_today
    total_consumption_so_far=required_man_hours_today_upto_current_hour

    remaining_consumption_today=required_man_hours_today-total_consumption_so_far
    # Create a bar chart
    
    fig = go.Figure()

    # Add bar for yesterday's total Footfalls
    fig.add_trace(go.Bar(
        x=['Last<br>Day'],
        y=[total_yesterday_consumption],
        name='Yesterday Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bar for today's Footfalls so far
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[total_consumption_so_far],
        name='So Far Today',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bar for remaining Footfalls today
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[remaining_consumption_today],
        name='Remaining Today',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Day', 'This<br>Day'],
            ticktext=['Last<br>Day', 'This<br>Day'],
            range=[-0.5, 1.5]
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_yesterday_consumption, total_consumption_so_far + remaining_consumption_today)

    # Add annotation for last day
    fig.add_annotation(
        x=1, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Day<br><span style='color:#ff8200; font-size:17px;'><b>{total_yesterday_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Add annotation for predicted value
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted Today<br><span style='color:#ff8200; font-size:17px;'><b>{this_day:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Calculate the percentage change
    percentage_change = (this_day - total_yesterday_consumption) / total_yesterday_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for placement
    )

    
    man_plot = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return man_plot
def man_hours1(fin):
    # Get the current time
    current_time = datetime.now()

    # Calculate the start and end dates for the last week and the current week
    start_of_last_week = current_time - timedelta(days=current_time.weekday() + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    start_of_this_week = current_time - timedelta(days=current_time.weekday())
    end_of_this_week = start_of_this_week + timedelta(days=6)

    # Filter data for the last week
    last_week_data = fin[(fin['ds'].dt.date >= start_of_last_week.date()) & (fin['ds'].dt.date <= end_of_last_week.date())]

    # Calculate cumulative counts and determine cleaning schedule for last week's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in last_week_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    last_week_data['cumulative_count'] = cumulative_counts
    last_week_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for last week
    cleaning_data = last_week_data[last_week_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_last_week = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning last week: {required_man_hours_last_week} hours")

    # Filter data for the current week
    this_week_data = fin[(fin['ds'].dt.date >= start_of_this_week.date()) & (fin['ds'].dt.date <= end_of_this_week.date())]

    # Calculate cumulative counts and determine cleaning schedule for this week's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in this_week_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    this_week_data['cumulative_count'] = cumulative_counts
    this_week_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for this week
    cleaning_data = this_week_data[this_week_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_this_week = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning this week: {required_man_hours_this_week} hours")

    # Filter data for the current week up to the current day
    this_week_data_upto_current_day = this_week_data[this_week_data['ds'].dt.date <= current_time.date()]

    # Calculate cumulative counts and determine cleaning schedule for this week's data up to the current day
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in this_week_data_upto_current_day['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    this_week_data_upto_current_day['cumulative_count'] = cumulative_counts
    this_week_data_upto_current_day['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for this week up to the current day
    cleaning_data = this_week_data_upto_current_day[this_week_data_upto_current_day["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_this_week_upto_current_day = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning this week up to the current day: {required_man_hours_this_week_upto_current_day} hours")

    # Calculate remaining man-hours for the current week
    remaining_man_hours_this_week = required_man_hours_this_week - required_man_hours_this_week_upto_current_day

    # Prepare data for the bar chart
    total_last_week_consumption = required_man_hours_last_week
    total_this_week_consumption = required_man_hours_this_week
    total_this_week_upto_current_day_consumption = required_man_hours_this_week_upto_current_day
    remaining_this_week_consumption = remaining_man_hours_this_week
    # Create a bar chart


    fig = go.Figure()

    # Add bars for last week's total man-hours
    fig.add_trace(go.Bar(
        x=['Last<br>Week'],
        y=[total_last_week_consumption],
        name='Last Week Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for this week's man-hours so far
    fig.add_trace(go.Bar(
        x=['This<br>Week'],
        y=[total_this_week_upto_current_day_consumption],
        name='So Far This Week',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for remaining man-hours this week
    fig.add_trace(go.Bar(
        x=['This<br>Week'],
        y=[remaining_this_week_consumption],
        name='Remaining This Week',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Week', 'This<br>Week'],
            ticktext=['Last<br>Week', 'This<br>Week'],
            range=[-0.5, 1.5]
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_last_week_consumption, total_this_week_upto_current_day_consumption + remaining_this_week_consumption)

    # Add annotation for last week
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_last_week_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for proper placement
    )

    # Add annotation for predicted value this week
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_this_week_consumption:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Calculate the percentage change for this week
    percentage_change_week = (total_this_week_consumption - total_last_week_consumption) / total_last_week_consumption * 100
    symbol_week = '▲' if percentage_change_week > 0 else '▼'
    color_week = 'red' if percentage_change_week > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color_week}; font-size:17px; font-family:Mulish;'> <b>{symbol_week} {abs(percentage_change_week):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for placement
    )




    man_plot1 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    # Show the figure
    return man_plot1
def man_hours2(fin):
    current_time = datetime.now()

    # Calculate the start and end dates for the last month and the current month
    start_of_last_month = (current_time.replace(day=1) - timedelta(days=1)).replace(day=1)
    end_of_last_month = (current_time.replace(day=1) - timedelta(days=1))
    start_of_this_month = current_time.replace(day=1)
    end_of_this_month = (start_of_this_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Filter data for the last month
    last_month_data = fin[(fin['ds'].dt.date >= start_of_last_month.date()) & (fin['ds'].dt.date <= end_of_last_month.date())]

    # Calculate cumulative counts and determine cleaning schedule for last month's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in last_month_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    last_month_data['cumulative_count'] = cumulative_counts
    last_month_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for last month
    cleaning_data = last_month_data[last_month_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_last_month = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning last month: {required_man_hours_last_month} hours")

    # Filter data for the current month
    this_month_data = fin[(fin['ds'].dt.date >= start_of_this_month.date()) & (fin['ds'].dt.date <= end_of_this_month.date())]

    # Calculate cumulative counts and determine cleaning schedule for this month's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in this_month_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    this_month_data['cumulative_count'] = cumulative_counts
    this_month_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for this month
    cleaning_data = this_month_data[this_month_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_this_month = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning this month: {required_man_hours_this_month} hours")

    # Filter data for the current month up to the current day
    this_month_data_upto_current_day = this_month_data[this_month_data['ds'].dt.date <= current_time.date()]

    # Calculate cumulative counts and determine cleaning schedule for this month's data up to the current day
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in this_month_data_upto_current_day['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    this_month_data_upto_current_day['cumulative_count'] = cumulative_counts
    this_month_data_upto_current_day['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for this month up to the current day
    cleaning_data = this_month_data_upto_current_day[this_month_data_upto_current_day["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_this_month_upto_current_day = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning this month up to the current day: {required_man_hours_this_month_upto_current_day} hours")

    # Calculate remaining man-hours for the current month
    remaining_man_hours_this_month = required_man_hours_this_month - required_man_hours_this_month_upto_current_day

    # Prepare data for the bar chart
    total_last_month_consumption = required_man_hours_last_month
    total_this_month_consumption = required_man_hours_this_month
    total_this_month_upto_current_day_consumption = required_man_hours_this_month_upto_current_day
    remaining_this_month_consumption = remaining_man_hours_this_month


    fig = go.Figure()

    # Add bars for last month's total man-hours
    fig.add_trace(go.Bar(
        x=['Last<br>Month'],
        y=[total_last_month_consumption],
        name='Last Month Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for this month's man-hours so far
    fig.add_trace(go.Bar(
        x=['This<br>Month'],
        y=[total_this_month_upto_current_day_consumption],
        name='So Far This Month',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for remaining man-hours this month
    fig.add_trace(go.Bar(
        x=['This<br>Month'],
        y=[remaining_this_month_consumption],
        name='Remaining This Month',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Month', 'This<br>Month'],
            ticktext=['Last<br>Month', 'This<br>Month'],
            range=[-0.5, 1.5]
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_last_month_consumption, total_this_month_upto_current_day_consumption + remaining_this_month_consumption)

    # Add annotation for last month
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Month<br><span style='color:#ff8200; font-size:17px;'><b>{total_last_month_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for proper placement
    )

    # Add annotation for predicted value this month
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Month<br><span style='color:#ff8200; font-size:17px;'><b>{total_this_month_consumption:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Calculate the percentage change for this month
    percentage_change_month = (total_this_month_consumption - total_last_month_consumption) / total_last_month_consumption * 100
    symbol_month = '▲' if percentage_change_month > 0 else '▼'
    color_month = 'red' if percentage_change_month > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color_month}; font-size:17px; font-family:Mulish;'> <b>{symbol_month} {abs(percentage_change_month):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for placement
    )



    man_plot2 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
    # Show the figure
    return man_plot2
def man_hours3(fin):
    current_time = datetime.now()

    # Calculate the start and end dates for the last workweek and the current workweek
    def get_workweek_dates(current_time):
        # Calculate the start of the current workweso_farek (Monday)
        start_of_current_workweek = current_time - timedelta(days=current_time.weekday())
        # Calculate the end of the current workweek (Friday)
        end_of_current_workweek = start_of_current_workweek + timedelta(days=4)
        # Calculate the start of the last workweek (Monday)
        start_of_last_workweek = start_of_current_workweek - timedelta(days=7)
        # Calculate the end of the last workweek (Friday)
        end_of_last_workweek = start_of_last_workweek + timedelta(days=4)
        return start_of_last_workweek, end_of_last_workweek, start_of_current_workweek, end_of_current_workweek

    start_of_last_workweek, end_of_last_workweek, start_of_current_workweek, end_of_current_workweek = get_workweek_dates(current_time)

    # Filter data for the last workweek
    last_workweek_data = fin[(fin['ds'].dt.date >= start_of_last_workweek.date()) & (fin['ds'].dt.date <= end_of_last_workweek.date())]

    # Calculate cumulative counts and determine cleaning schedule for last workweek's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in last_workweek_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    last_workweek_data['cumulative_count'] = cumulative_counts
    last_workweek_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for last workweek
    cleaning_data = last_workweek_data[last_workweek_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_last_workweek = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning last workweek: {required_man_hours_last_workweek} hours")

    # Filter data for the current workweek
    current_workweek_data = fin[(fin['ds'].dt.date >= start_of_current_workweek.date()) & (fin['ds'].dt.date <= end_of_current_workweek.date())]

    # Calculate cumulative counts and determine cleaning schedule for current workweek's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_workweek_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_workweek_data['cumulative_count'] = cumulative_counts
    current_workweek_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current workweek
    cleaning_data = current_workweek_data[current_workweek_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_workweek = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current workweek: {required_man_hours_current_workweek} hours")

    # Filter data for the current workweek up to the current day
    current_workweek_data_upto_current_day = current_workweek_data[current_workweek_data['ds'].dt.date <= current_time.date()]

    # Calculate cumulative counts and determine cleaning schedule for current workweek's data up to the current day
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_workweek_data_upto_current_day['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_workweek_data_upto_current_day['cumulative_count'] = cumulative_counts
    current_workweek_data_upto_current_day['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current workweek up to the current day
    cleaning_data = current_workweek_data_upto_current_day[current_workweek_data_upto_current_day["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_workweek_upto_current_day = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current workweek up to the current day: {required_man_hours_current_workweek_upto_current_day} hours")

    # Calculate remaining man-hours for the current workweek
    remaining_man_hours_current_workweek = required_man_hours_current_workweek - required_man_hours_current_workweek_upto_current_day

    # Prepare data for the bar chart
    total_last_workweek_consumption = required_man_hours_last_workweek
    total_current_workweek_consumption = required_man_hours_current_workweek
    total_current_workweek_upto_current_day_consumption = required_man_hours_current_workweek_upto_current_day
    remaining_current_workweek_consumption = remaining_man_hours_current_workweek
    # Create a bar chart

    fig = go.Figure()

    # Add bars for last workweek's total man-hours
    fig.add_trace(go.Bar(
        x=['Last<br>Workweek'],
        y=[total_last_workweek_consumption],
        name='Last Workweek Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for current workweek's man-hours so far
    fig.add_trace(go.Bar(
        x=['This<br>Workweek'],
        y=[total_current_workweek_upto_current_day_consumption],
        name='So Far This Workweek',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for remaining man-hours this workweek
    fig.add_trace(go.Bar(
        x=['This<br>Workweek'],
        y=[remaining_current_workweek_consumption],
        name='Remaining This Workweek',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Workweek', 'This<br>Workweek'],
            ticktext=['Last<br>Workweek', 'This<br>Workweek'],
            range=[-0.5, 1.5]
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_last_workweek_consumption, total_current_workweek_upto_current_day_consumption + remaining_current_workweek_consumption)

    # Add annotation for last workweek
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_last_workweek_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for proper placement
    )

    # Add annotation for predicted value this workweek
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_current_workweek_consumption:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Calculate the percentage change for this workweek
    percentage_change_workweek = (total_current_workweek_consumption - total_last_workweek_consumption) / total_last_workweek_consumption * 100
    symbol_workweek = '▲' if percentage_change_workweek > 0 else '▼'
    color_workweek = 'red' if percentage_change_workweek > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color_workweek}; font-size:17px; font-family:Mulish;'> <b>{symbol_workweek} {abs(percentage_change_workweek):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for placement
    )


    man_plot3 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
    # Show the figure
    return man_plot3
def man_hours4(fin):
    current_time = datetime.now()

    # Calculate the start and end dates for the last weekend and the current weekend
    def get_weekend_dates(current_time):
        # Calculate the start of the current weekend (Saturday)
        days_until_saturday = (5 - current_time.weekday()) % 7
        start_of_current_weekend = current_time - timedelta(days=current_time.weekday() - 5)
        # Calculate the end of the current weekend (Sunday)
        end_of_current_weekend = start_of_current_weekend + timedelta(days=1)
        # Calculate the start of the last weekend (Saturday)
        start_of_last_weekend = start_of_current_weekend - timedelta(days=7)
        # Calculate the end of the last weekend (Sunday)
        end_of_last_weekend = start_of_last_weekend + timedelta(days=1)
        return start_of_last_weekend, end_of_last_weekend, start_of_current_weekend, end_of_current_weekend

    start_of_last_weekend, end_of_last_weekend, start_of_current_weekend, end_of_current_weekend = get_weekend_dates(current_time)

    # Filter data for the last weekend
    last_weekend_data = fin[(fin['ds'].dt.date >= start_of_last_weekend.date()) & (fin['ds'].dt.date <= end_of_last_weekend.date())]

    # Calculate cumulative counts and determine cleaning schedule for last weekend's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in last_weekend_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    last_weekend_data['cumulative_count'] = cumulative_counts
    last_weekend_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for last weekend
    cleaning_data = last_weekend_data[last_weekend_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_last_weekend = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning last weekend: {required_man_hours_last_weekend} hours")

    # Filter data for the current weekend
    current_weekend_data = fin[(fin['ds'].dt.date >= start_of_current_weekend.date()) & (fin['ds'].dt.date <= end_of_current_weekend.date())]

    # Calculate cumulative counts and determine cleaning schedule for current weekend's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_weekend_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_weekend_data['cumulative_count'] = cumulative_counts
    current_weekend_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current weekend
    cleaning_data = current_weekend_data[current_weekend_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_weekend = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current weekend: {required_man_hours_current_weekend} hours")

    # Filter data for the current weekend up to the current day
    current_weekend_data_upto_current_day = current_weekend_data[current_weekend_data['ds'].dt.date <= current_time.date()]

    # Calculate cumulative counts and determine cleaning schedule for current weekend's data up to the current day
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_weekend_data_upto_current_day['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_weekend_data_upto_current_day['cumulative_count'] = cumulative_counts
    current_weekend_data_upto_current_day['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current weekend up to the current day
    cleaning_data = current_weekend_data_upto_current_day[current_weekend_data_upto_current_day["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_weekend_upto_current_day = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current weekend up to the current day: {required_man_hours_current_weekend_upto_current_day} hours")

    # Calculate remaining man-hours for the current weekend
    remaining_man_hours_current_weekend = required_man_hours_current_weekend - required_man_hours_current_weekend_upto_current_day

    # Prepare data for the bar chart
    total_last_weekend_consumption = required_man_hours_last_weekend
    total_current_weekend_consumption = required_man_hours_current_weekend
    total_current_weekend_upto_current_day_consumption = required_man_hours_current_weekend_upto_current_day
    remaining_current_weekend_consumption = remaining_man_hours_current_weekend


    fig = go.Figure()

    # Add bars for last weekend's total man-hours
    fig.add_trace(go.Bar(
        x=['Last<br>Weekend'],
        y=[total_last_weekend_consumption],
        name='Last Weekend Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for current weekend's man-hours so far
    fig.add_trace(go.Bar(
        x=['This<br>Weekend'],
        y=[total_current_weekend_upto_current_day_consumption],
        name='So Far This Weekend',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for remaining man-hours this weekend
    fig.add_trace(go.Bar(
        x=['This<br>Weekend'],
        y=[remaining_current_weekend_consumption],
        name='Remaining This Weekend',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Weekend', 'This<br>Weekend'],
            ticktext=['Last<br>Weekend', 'This<br>Weekend'],
            range=[-0.5, 1.5]
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_last_weekend_consumption, total_current_weekend_upto_current_day_consumption + remaining_current_weekend_consumption)

    # Add annotation for last weekend
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Weekend<br><span style='color:#ff8200; font-size:17px;'><b>{total_last_weekend_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for proper placement
    )

    # Add annotation for predicted value this weekend
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Weekend<br><span style='color:#ff8200; font-size:17px;'><b>{total_current_weekend_consumption:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for proper placement
    )

    # Calculate the percentage change for this weekend
    percentage_change_weekend = (total_current_weekend_consumption - total_last_weekend_consumption) / total_last_weekend_consumption * 100
    symbol_weekend = '▲' if percentage_change_weekend > 0 else '▼'
    color_weekend = 'red' if percentage_change_weekend > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color_weekend}; font-size:17px; font-family:Mulish;'> <b>{symbol_weekend} {abs(percentage_change_weekend):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=120,  # Adjust for placement
    )

    man_plot4 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
    # Show the figure
    return man_plot4
def man_hours5(fin):

    # Assuming `fin` is your DataFrame and it has columns 'ds' (datetime) and 'y' (values)

    # Get the current time
    current_time = datetime.now()

    # Calculate the start and end dates for the last year and the current year
    def get_year_dates(current_time):
        # Calculate the start of the current year
        start_of_current_year = datetime(current_time.year, 1, 1)
        # Calculate the end of the current year
        end_of_current_year = datetime(current_time.year, 12, 31)
        # Calculate the start of the last year
        start_of_last_year = datetime(current_time.year - 1, 1, 1)
        # Calculate the end of the last year
        end_of_last_year = datetime(current_time.year - 1, 12, 31)
        return start_of_last_year, end_of_last_year, start_of_current_year, end_of_current_year

    start_of_last_year, end_of_last_year, start_of_current_year, end_of_current_year = get_year_dates(current_time)

    # Filter data for the last year
    last_year_data = fin[(fin['ds'].dt.date >= start_of_last_year.date()) & (fin['ds'].dt.date <= end_of_last_year.date())]

    # Calculate cumulative counts and determine cleaning schedule for last year's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in last_year_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    last_year_data['cumulative_count'] = cumulative_counts
    last_year_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for last year
    cleaning_data = last_year_data[last_year_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    cleaning_time_per_session = 20 / 60  # 20 minutes per cleaning session in hours
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_last_year = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning last year: {required_man_hours_last_year} hours")

    # Filter data for the current year
    current_year_data = fin[(fin['ds'].dt.date >= start_of_current_year.date()) & (fin['ds'].dt.date <= end_of_current_year.date())]

    # Calculate cumulative counts and determine cleaning schedule for current year's data
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_year_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_year_data['cumulative_count'] = cumulative_counts
    current_year_data['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current year
    cleaning_data = current_year_data[current_year_data["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_year = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current year: {required_man_hours_current_year} hours")

    # Filter data for the current year up to the current day
    current_year_data_upto_current_day = current_year_data[current_year_data['ds'].dt.date <= current_time.date()]

    # Calculate cumulative counts and determine cleaning schedule for current year's data up to the current day
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    for value in current_year_data_upto_current_day['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0

    # Assign results to DataFrame
    current_year_data_upto_current_day['cumulative_count'] = cumulative_counts
    current_year_data_upto_current_day['cleaning_schedule'] = cleaning_schedule

    # Filter the DataFrame to get the cleaning schedule for current year up to the current day
    cleaning_data = current_year_data_upto_current_day[current_year_data_upto_current_day["cleaning_schedule"] == 1]

    # Calculate the required man-hours for cleaning
    total_cleaning_sessions = cleaning_data.shape[0]
    required_man_hours_current_year_upto_current_day = total_cleaning_sessions * cleaning_time_per_session

    # Output the required man-hours for cleaning
    print(f"Required man-hours for cleaning current year up to the current day: {required_man_hours_current_year_upto_current_day} hours")

    # Calculate remaining man-hours for the current year
    remaining_man_hours_current_year = required_man_hours_current_year - required_man_hours_current_year_upto_current_day

    # Prepare data for the bar chart
    total_last_year_consumption = required_man_hours_last_year
    total_current_year_consumption = required_man_hours_current_year
    total_current_year_upto_current_day_consumption = required_man_hours_current_year_upto_current_day
    remaining_current_year_consumption = remaining_man_hours_current_year
    # Create a bar chart


    fig = go.Figure()

    # Add bars for last year's total man-hours
    fig.add_trace(go.Bar(
        x=['Last<br>Year'],
        y=[total_last_year_consumption],
        name='Last Year Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for current year's man-hours so far
    fig.add_trace(go.Bar(
        x=['This<br>Year'],
        y=[total_current_year_upto_current_day_consumption],
        name='So Far This Year',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
    ))

    # Add bars for remaining man-hours this year
    fig.add_trace(go.Bar(
        x=['This<br>Year'],
        y=[remaining_current_year_consumption],
        name='Remaining This Year',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Man-hours: %{y:.0f} hrs. <br>',
        opacity=0.6,
    ))

    # Update layout
    fig.update_layout(
        autosize=False,
        height=300,
        width=380,  # Increase width to allow more room for annotations
        title='Estimated Man-hours',
        title_x=0.05,
        title_y=0.92,
        yaxis_title='Man-hours',
        barmode='stack',
        xaxis=dict(
            tickvals=['Last<br>Year', 'This<br>Year'],
            ticktext=['Last<br>Year', 'This<br>Year'],
            range=[-0.5, 1.5]
        ),
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=180, t=40, b=40),  # Increase right margin for annotations
        bargap=0.1,
        bargroupgap=0.2
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_last_year_consumption, total_current_year_upto_current_day_consumption + remaining_current_year_consumption)

    # Add annotation for last year
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; text-align:center; font-family:Mulish;'>Last Year<br><span style='color:#ff8200; font-size:17px;'><b>{total_last_year_consumption:.1f} hrs.</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for proper placement
    )

    # Add annotation for predicted value this year
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Year<br><span style='color:#ff8200; font-size:17px;'><b>{total_current_year_consumption:.1f} hrs. </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for proper placement
    )

    # Calculate the percentage change for this year
    percentage_change_year = (total_current_year_consumption - total_last_year_consumption) / total_last_year_consumption * 100
    symbol_year = '▲' if percentage_change_year > 0 else '▼'
    color_year = 'red' if percentage_change_year > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color_year}; font-size:17px; font-family:Mulish;'> <b>{symbol_year} {abs(percentage_change_year):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Man-hours</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )





    man_plot5 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
    # Show the figure
    return man_plot5