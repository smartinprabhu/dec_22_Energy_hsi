import pandas as pd
import plotly.graph_objects as go
import json
import plotly
import datetime
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import pytz
import plotly.graph_objs as go
import plotly
import json
from datetime import datetime, timedelta


def pie(DG_hour, EB_hour, solar_hour, current_datetime):
    # Calculate the total values for the current date    current_date = current_datetime.date()
   # Create the donut chart
 # Define the timezone
    timezone = pytz.timezone("Asia/Kolkata")

    # Get the current date, week, month, and year in the specified timezone
    current_datetime = pd.Timestamp.now(timezone)
    dg_value1 = DG_hour[
        (DG_hour['ds'].dt.date == current_datetime.date()) &
        (DG_hour['ds'].dt.hour <= current_datetime.hour)
    ]
    eb_value1 = EB_hour[
        (EB_hour['ds'].dt.date == current_datetime.date()) &
        (EB_hour['ds'].dt.hour <= current_datetime.hour)
    ]
    solar_value1 = solar_hour[
        (solar_hour['ds'].dt.date == current_datetime.date()) &
        (solar_hour['ds'].dt.hour <= current_datetime.hour)
    ]
    solar_value=solar_value1['y'].sum()
    eb_value=eb_value1['y'].sum()
    dg_value=dg_value1['y'].sum()
    # Data
    labels = ['EB', 'DG', 'Solar']
    values = [eb_value, dg_value, solar_value]

    # Define colors for each segment that contrast well with a dark background
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',  # Display label and percent
        textposition='inside',  # Position the text inside the slices
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} kWh<br>Percentage: %{percent:.1%}<extra></extra>',
        marker=dict(colors=colors),
        domain=dict(x=[0.1, 0.5]),
        sort=False,  # Prevent automatic sorting
        customdata=[0, 1, 2],  # Shift the chart to the left by reducing the right bound# Shift the chart to the left by reducing the right bound
    )])

    total = eb_value + dg_value + solar_value

    # Apply the dark theme and make layout adjustments for responsiveness
    fig.update_layout(
        template='plotly_dark',
        title='',
        annotations=[
            dict(
                text='Consumption',
                x=1.12,  # Adjust this value to move the text further to the left or right
                y=0.781,  # Adjust this value to move the text up or down
                font=dict(
                    size=14,  # Font size for the main text
                    color='white'
                ),
                showarrow=False,
            ),
            dict(text='(kWh)', x=1.13, y=0.72, font_size=8, showarrow=False, font_color='white'),
            dict(text='Source', x=0.65, y=0.78, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{eb_value:.2f}', x=1.12, y=0.63, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{dg_value:.2f}', x=1.12, y=0.532, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{solar_value:.2f}', x=1.12, y=0.445, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{total:.2f}', x=1.12, y=0.28, font_size=14, showarrow=False, font_color='white'),
            dict(text='Total', x=0.74, y=0.28, font_size=14, showarrow=False, font_color='white'),
        ],
        shapes=[
            # Horizontal line above "Total"
            dict(
                type='line',
                xref='paper',
                yref='paper',
                x0=0.65,  # Start of the line
                y0=0.38,  # Just above the "Total" text
                x1=1.12,  # End of the line
                y1=0.38,  # Just above the "Total" text
                line=dict(
                    color='white',
                    width=1,
                )
            ),
        ],
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.37,
            xanchor="center",
            x=0.7,
            font=dict(size=14)
        ),
        autosize=False,  # Ensure the chart resizes with the container
        margin=dict(l=20, r=20, t=20, b=20),  # Adjust margins for smaller screens
        height=None,  # Remove fixed height to let the chart adapt
    )


    # Convert the figure to a JSON object for use in the React component
    pie_plot = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return pie_plot, total


def pie1(DG_hour,EB_hour,solar_hour,current_date):


    # Set the timezone to Asia/Kolkata
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)
    EB_hour=EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour=DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour=solar_hour.set_index('ds').resample('D').sum().reset_index()

    current_datetime = datetime.now(tz)

    # Extract the date part and convert it to a timezone-aware datetime object
    current_date = current_datetime.date()
    current_date = tz.localize(datetime.combine(current_date, datetime.min.time()))

    # Calculate the start of the week (Monday)
    week_start_date = current_date - timedelta(days=current_date.weekday())

    # Function to ensure datetime objects are timezone-aware
    def ensure_timezone_aware(df, column, tz):
        if df[column].dt.tz is None:
            # If the datetime objects are timezone-naive, localize them
            df[column] = df[column].dt.tz_localize(tz)
        else:
            # If the datetime objects are already timezone-aware, convert them
            df[column] = df[column].dt.tz_convert(tz)

    # Ensure the datetime objects in the DataFrame are timezone-aware
    ensure_timezone_aware(DG_hour, 'ds', tz)
    ensure_timezone_aware(EB_hour, 'ds', tz)
    ensure_timezone_aware(solar_hour, 'ds', tz)

    # Calculate the total values for the week up to the current date
    dg_value = DG_hour[(DG_hour['ds'] >= week_start_date) &
                    (DG_hour['ds'] <= current_date)]['y'].sum()
    eb_value = EB_hour[(EB_hour['ds'] >= week_start_date) &
                    (EB_hour['ds'] <= current_date)]['y'].sum()
    solar_value = solar_hour[(solar_hour['ds'] >= week_start_date) &
                            (solar_hour['ds'] <= current_date)]['y'].sum()
    # Data
    labels = ['EB', 'DG', 'Solar']
    values = [eb_value, dg_value, solar_value]

    # Define colors for each segment that contrast well with a dark background
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',  # Display label and percent
        textposition='inside',  # Position the text inside the slices
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} kWh<br>Percentage: %{percent:.1%}<extra></extra>',
        marker=dict(colors=colors),
        domain=dict(x=[0.1, 0.5]) ,
        sort=False,  # Prevent automatic sorting
        customdata=[0, 1, 2],  # Shift the chart to the left by reducing the right bound
    )])


    total1 = eb_value + dg_value + solar_value

    # Apply the dark theme and make layout adjustments for responsiveness
    fig.update_layout(
        template='plotly_dark',
        title='',
        annotations=[
            dict(
                text='Consumption',
                x=1.12,  # Adjust this value to move the text further to the left or right
                y=0.781,  # Adjust this value to move the text up or down
                font=dict(
                    size=14,  # Font size for the main text
                    color='white'
                ),
                showarrow=False,
            ),
            dict(text='(kWh)', x=1.13, y=0.72, font_size=8, showarrow=False, font_color='white'),
            dict(text='Source', x=0.65, y=0.78, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{eb_value:.2f}', x=1.12, y=0.63, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{dg_value:.2f}', x=1.12, y=0.532, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{solar_value:.2f}', x=1.12, y=0.445, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{total1:.2f}', x=1.12, y=0.28, font_size=14, showarrow=False, font_color='white'),
            dict(text='Total', x=0.74, y=0.28, font_size=14, showarrow=False, font_color='white'),
        ],
        shapes=[
            # Horizontal line above "Total"
            dict(
                type='line',
                xref='paper',
                yref='paper',
                x0=0.65,  # Start of the line
                y0=0.38,  # Just above the "Total" text
                x1=1.12,  # End of the line
                y1=0.38,  # Just above the "Total" text
                line=dict(
                    color='white',
                    width=1,
                )
            ),
        ],
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.37,
            xanchor="center",
            x=0.7,
            font=dict(size=14)
        ),
        autosize=False,  # Ensure the chart resizes with the container
        margin=dict(l=20, r=20, t=20, b=20),  # Adjust margins for smaller screens
        height=None,  # Remove fixed height to let the chart adapt
    )


    pie_plot1 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return pie_plot1,total1,solar_value

def pie2(DG_hour,EB_hour,solar_hour,current_date):

    tz = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in the Asia/Kolkata timezone
    current_datetime = datetime.now(tz)

    # Extract the date part and convert it to a timezone-aware datetime object
    current_date = current_datetime.date()
    current_date = tz.localize(datetime.combine(current_date, datetime.min.time()))
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)
    EB_hour=EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour=DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour=solar_hour.set_index('ds').resample('D').sum().reset_index()

    # Calculate the start of the month
    month_start_date = current_date.replace(day=1)

    # Function to ensure datetime objects are timezone-aware
    def ensure_timezone_aware(df, column, tz):
        if df[column].dt.tz is None:
            # If the datetime objects are timezone-naive, localize them
            df[column] = df[column].dt.tz_localize(tz)
        else:
            # If the datetime objects are already timezone-aware, convert them
            df[column] = df[column].dt.tz_convert(tz)

    # Ensure the datetime objects in the DataFrame are timezone-aware
    ensure_timezone_aware(DG_hour, 'ds', tz)
    ensure_timezone_aware(EB_hour, 'ds', tz)
    ensure_timezone_aware(solar_hour, 'ds', tz)

    # Calculate the total values for the month up to the current date
    dg_value = DG_hour[(DG_hour['ds'] >= month_start_date) &
                    (DG_hour['ds'] <= current_date)]['y'].sum()
    eb_value = EB_hour[(EB_hour['ds'] >= month_start_date) &
                    (EB_hour['ds'] <= current_date)]['y'].sum()
    solar_value1 = solar_hour[(solar_hour['ds'] >= month_start_date) &
                            (solar_hour['ds'] <= current_date)]['y'].sum()


    # Data
    labels = ['EB', 'DG', 'Solar']
    values = [eb_value, dg_value, solar_value1]

    # Define colors for each segment that contrast well with a dark background
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',  # Display label and percent
        textposition='inside',  # Position the text inside the slices
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} kWh<br>Percentage: %{percent:.1%}<extra></extra>',
        marker=dict(colors=colors),
        domain=dict(x=[0.1, 0.5]) ,
        sort=False,  # Prevent automatic sorting
        customdata=[0, 1, 2],# Shift the chart to the left by reducing the right bound
    )])


    total2 = eb_value + dg_value + solar_value1
    # Apply the dark theme and make layout adjustments for responsiveness
    fig.update_layout(
        template='plotly_dark',
        title='',
        annotations=[
            dict(
                text='Consumption',
                x=1.12,  # Adjust this value to move the text further to the left or right
                y=0.781,  # Adjust this value to move the text up or down
                font=dict(
                    size=14,  # Font size for the main text
                    color='white'
                ),
                showarrow=False,
            ),
            dict(text='(kWh)', x=1.13, y=0.72, font_size=8, showarrow=False, font_color='white'),
            dict(text='Source', x=0.65, y=0.78, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{eb_value:.2f}', x=1.12, y=0.63, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{dg_value:.2f}', x=1.12, y=0.532, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{solar_value1:.2f}', x=1.12, y=0.445, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{total2:.2f}', x=1.12, y=0.28, font_size=14, showarrow=False, font_color='white'),
            dict(text='Total', x=0.74, y=0.28, font_size=14, showarrow=False, font_color='white'),
        ],
        shapes=[
            # Horizontal line above "Total"
            dict(
                type='line',
                xref='paper',
                yref='paper',
                x0=0.65,  # Start of the line
                y0=0.38,  # Just above the "Total" text
                x1=1.12,  # End of the line
                y1=0.38,  # Just above the "Total" text
                line=dict(
                    color='white',
                    width=1,
                )
            ),
        ],
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.37,
            xanchor="center",
            x=0.7,
            font=dict(size=14)
        ),
        autosize=False,  # Ensure the chart resizes with the container
        margin=dict(l=20, r=20, t=20, b=20),  # Adjust margins for smaller screens
        height=None,  # Remove fixed height to let the chart adapt
    )

    pie_plot2 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return pie_plot2,total2,solar_value1
def pie3(DG_hour,EB_hour,solar_hour,current_date):



    # Calculate the start of the year and end of the current month
    # Set the timezone to Asia/Kolkata
    tz = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in the Asia/Kolkata timezone
    current_datetime = datetime.now(tz)

    # Extract the date part and convert it to a timezone-aware datetime object

    current_date = tz.localize(datetime.combine(current_date, datetime.min.time()))
    current_date = current_datetime.date()
    current_date = tz.localize(datetime.combine(current_date, datetime.min.time()))

    # Calculate the start of the year and the current date
    year_start_date = tz.localize(datetime(current_date.year, 1, 1))
    current_date = tz.localize(datetime.combine(current_date, datetime.min.time()))

    # Function to ensure datetime objects are timezone-aware
    def ensure_timezone_aware(df, column, tz):
        if df[column].dt.tz is None:
            # If the datetime objects are timezone-naive, localize them
            df[column] = df[column].dt.tz_localize(tz)
        else:
            # If the datetime objects are already timezone-aware, convert them
            df[column] = df[column].dt.tz_convert(tz)

    # Ensure the datetime objects in the DataFrame are timezone-aware
    ensure_timezone_aware(DG_hour, 'ds', tz)
    ensure_timezone_aware(EB_hour, 'ds', tz)
    ensure_timezone_aware(solar_hour, 'ds', tz)

    # Calculate the total values from the start of the year to the current date
    dg_value = DG_hour[(DG_hour['ds'] >= year_start_date) &
                        (DG_hour['ds'] <= current_date)]['y'].sum()
    eb_value = EB_hour[(EB_hour['ds'] >= year_start_date) &
                        (EB_hour['ds'] <= current_date)]['y'].sum()
    solar_value2 = solar_hour[(solar_hour['ds'] >= year_start_date) &
                                (solar_hour['ds'] <= current_date)]['y'].sum()


    labels = ['EB', 'DG', 'Solar']
    values = [eb_value, dg_value, solar_value2]

    # Define colors for each segment that contrast well with a dark background
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',  # Display label and percent
        textposition='inside',  # Position the text inside the slices
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2f} kWh<br>Percentage: %{percent:.1%}<extra></extra>',
        marker=dict(colors=colors),
        domain=dict(x=[0.1, 0.5]),
        sort=False,  # Prevent automatic sorting
        customdata=[0, 1, 2],# Shift the chart to the left by reducing the right bound
    )])


    total3 = eb_value + dg_value + solar_value2
    # Apply the dark theme and make layout adjustments for responsiveness
    fig.update_layout(
        template='plotly_dark',
        title='',
        annotations=[
            dict(
                text='Consumption',
                x=1.12,  # Adjust this value to move the text further to the left or right
                y=0.781,  # Adjust this value to move the text up or down
                font=dict(
                    size=14,  # Font size for the main text
                    color='white'
                ),
                showarrow=False,
            ),
            dict(text='(kWh)', x=1.13, y=0.72, font_size=8, showarrow=False, font_color='white'),
            dict(text='Source', x=0.65, y=0.78, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{eb_value:.2f}', x=1.12, y=0.63, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{dg_value:.2f}', x=1.12, y=0.532, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{solar_value2:.2f}', x=1.12, y=0.445, font_size=14, showarrow=False, font_color='white'),
            dict(text=f'{total3:.2f}', x=1.12, y=0.28, font_size=14, showarrow=False, font_color='white'),
            dict(text='Total', x=0.74, y=0.28, font_size=14, showarrow=False, font_color='white'),
        ],
        shapes=[
            # Horizontal line above "Total"
            dict(
                type='line',
                xref='paper',
                yref='paper',
                x0=0.65,  # Start of the line
                y0=0.38,  # Just above the "Total" text
                x1=1.12,  # End of the line
                y1=0.38,  # Just above the "Total" text
                line=dict(
                    color='white',
                    width=1,
                )
            ),
        ],
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.37,
            xanchor="center",
            x=0.7,
            font=dict(size=14)
        ),
        autosize=False,  # Ensure the chart resizes with the container
        margin=dict(l=20, r=20, t=20, b=20),  # Adjust margins for smaller screens
        height=None,  # Remove fixed height to let the chart adapt
    )


    pie_plot3 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return pie_plot3,total3,solar_value2
