import pandas as pd
import plotly.graph_objects as go
import json
import plotly
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
def total_consumption(fin,tz):

    current_datetime = pd.Timestamp.now(tz)
    current_date = current_datetime.date()

    # Filter the DataFrame for the entire current date (from 0th hour to 23rd hour)
    filtered_data = fin[fin['ds'].dt.date == current_date]

    # Sum the consumption for the entire day (Predicted Today)
    total_daily_consumption = filtered_data['y'].sum()

    # Sum the consumption up to the current hour (So Far Today)
    filtered_data_so_far = fin[
        (fin['ds'].dt.date == current_datetime.date()) &
        (fin['ds'].dt.hour <= current_datetime.hour)
    ]
    
    total_consumption_so_far = filtered_data_so_far['y'].sum()

    # Calculate remaining consumption for today
    remaining_consumption_today = total_daily_consumption - total_consumption_so_far

    # Filter the DataFrame for yesterday (from 0th hour to 23rd hour)
    yesterday_date = current_datetime.date() - pd.Timedelta(days=1)
    filtered_data_yesterday = fin[fin['ds'].dt.date == yesterday_date]

    # Sum the consumption for the entire day yesterday (Yesterday Total)
    total_yesterday_consumption = round(filtered_data_yesterday['y'].sum())
    total_consumption_so_far=round(total_consumption_so_far)
    remaining_consumption_today=round(remaining_consumption_today)


    fig = go.Figure()

    # Add bar for yesterday's total Footfalls
    fig.add_trace(go.Bar(
        x=['Last<br>Day'],
        y=[total_yesterday_consumption],
        name='Yesterday Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for today's Footfalls so far
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[total_consumption_so_far],
        name='So Far Today',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining Footfalls today
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[remaining_consumption_today],
        name='Remaining Today',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        title_x=0.05,  # Center the title horizontally (0.0 is left, 1.0 is right)
        title_y=0.92,  # Adjust the vertical position (0.0 is bottom, 1.0 is top)
        yaxis_title='Footfalls ',
        barmode='stack',
        xaxis=dict(tickvals=['Last<br>Day', 'This<br>Day'], ticktext=['Last<br>Day', 'This<br>Day']),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_yesterday_consumption, total_consumption_so_far + remaining_consumption_today)

    # Calculate the percentage change
    percentage_change = (total_daily_consumption - total_yesterday_consumption) / total_yesterday_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last day
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Day<br><span style='color:#ff8200; font-size:17px;'><b>{total_yesterday_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=200,  # Adjust for placement
    )

    # Add annotation for predicted value today
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted Today<br><span style='color:#ff8200; font-size:17px;'><b>{total_daily_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )



    consumption_plot = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot


def tot_con_week(df_daily):
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    # Calculate the start of the current week (Monday) with timezone info
    start_of_week = current_date - timedelta(days=current_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current week (Sunday) with timezone info
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter the DataFrame for the current week's data
    current_week_data = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_week)]
    current_week_total = current_week_data['y'].sum()

    # The end date is today with the current time
    end_of_today = current_date

    # Filter the DataFrame for the current week's data up to today
    current_week_data_up_to_today = df_daily[(df_daily['ds'] >= start_of_week) & (df_daily['ds'] <= end_of_today)]

    total_current_week_consumption_so_far = current_week_data_up_to_today['y'].sum()

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

    # Calculate remaining consumption for today
    remaining_consumption_today = current_week_total - total_current_week_consumption_so_far

    # Get the current week number
    current_week_number = datetime.now().isocalendar()[1]

    # Get the previous week number
    previous_week_number = (datetime.now() - timedelta(weeks=1)).isocalendar()[1]


    # Create a bar chart
    fig = go.Figure()

    # Add bar for last week's total consumption
    fig.add_trace(go.Bar(
        x=[f'W{previous_week_number}'],
        y=[total_previous_week_consumption],
        name='Last Week Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for this week's Footfalls so far
    fig.add_trace(go.Bar(
        x=[f'W{current_week_number}'],
        y=[total_current_week_consumption_so_far],
        name='Current Week so Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining consumption this week
    fig.add_trace(go.Bar(
        x=[f'W{current_week_number}'],
        y=[remaining_consumption_today],
        name='Current Week Remaining ',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Week' bars
    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        yaxis_title='Footfalls',
        barmode='stack',
        xaxis=dict(tickvals=[f'W{previous_week_number}', f'W{current_week_number}'], ticktext=[f'W{previous_week_number}', f'W{current_week_number}']),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_previous_week_consumption, total_current_week_consumption_so_far + remaining_consumption_today)

    # Calculate the percentage change
    percentage_change = (current_week_total - total_previous_week_consumption) / total_previous_week_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last week
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_previous_week_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=200,  # Adjust for placement
    )

    # Add annotation for predicted value this week
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Week<br><span style='color:#ff8200; font-size:17px;'><b>{current_week_total:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )


    consumption_plot_week = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_week


def tot_con_month(df_daily, current_datetime):
    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    tz = pytz.timezone("Asia/Kolkata")

    # Calculate the end of the current month
    if current_datetime.month == 12:
        end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(seconds=1)
    else:
        end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(seconds=1)

    # Ensure both are timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))
    end_of_month = tz.localize(end_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's data
    current_month_data = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= end_of_month)
    ]
    current_month_total = current_month_data['y'].sum()

    # Calculate the start of the current month
    start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Ensure the start of the month is timezone-aware
    start_of_month = tz.localize(start_of_month.replace(tzinfo=None))

    # Filter the DataFrame for the current month's data up to today
    current_month_data_up_to_today = df_daily[
        (df_daily['ds'] >= start_of_month) & (df_daily['ds'] <= current_datetime)
    ]
    total_current_month_consumption_so_far = current_month_data_up_to_today['y'].sum()

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
    total_previous_month_consumption = previous_month_data['y'].sum()

    remaining_consumption_today = current_month_total - total_current_month_consumption_so_far

    # Get the current month name
    current_month_name = datetime.now().strftime('%b')

    # Get the previous month name
    previous_month_date = datetime.now().replace(day=1) - timedelta(days=1)
    previous_month_name = previous_month_date.strftime('%b')


    # Create a bar chart
    fig = go.Figure()

    # Add bar for last month's total consumption
    fig.add_trace(go.Bar(
        x=[previous_month_name],
        y=[total_previous_month_consumption],
        name='Last Month Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for this month's consumption so far
    fig.add_trace(go.Bar(
        x=[current_month_name],
        y=[total_current_month_consumption_so_far],
        name='Current Month So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining consumption this month
    fig.add_trace(go.Bar(
        x=[current_month_name],
        y=[remaining_consumption_today],
        name='Current Month Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Month' bars
    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        yaxis_title='Footfalls',
        barmode='stack',
        xaxis=dict(tickvals=[previous_month_name, current_month_name], ticktext=[previous_month_name, current_month_name]),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_previous_month_consumption, total_current_month_consumption_so_far + remaining_consumption_today)

    # Calculate the percentage change
    percentage_change = (current_month_total - total_previous_month_consumption) / total_previous_month_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last month
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Month<br><span style='color:#ff8200; font-size:17px;'><b>{total_previous_month_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for placement
    )

    # Add annotation for predicted value this month
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Month<br><span style='color:#ff8200; font-size:17px;'><b>{current_month_total:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )


    consumption_plot_month = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_month

def tot_con_year(df_daily, current_datetime):
    # Extract the current year
    current_year = current_datetime.year

    # Calculate the start and end of the current year
    start_of_current_year = datetime(current_year, 1, 1, tzinfo=pytz.timezone('Asia/Kolkata'))
    end_of_current_year = datetime(current_year, 12, 31, 23, 59, 59, tzinfo=pytz.timezone('Asia/Kolkata'))

    # Filter the DataFrame for the current year's data
    current_year_data = df_daily[
        (df_daily['ds'] >= start_of_current_year) & (df_daily['ds'] <= end_of_current_year)
    ]
    current_year_total = current_year_data['y'].sum()

    # Filter the DataFrame for the current year's data up to today
    current_year_data_up_to_today = df_daily[
        (df_daily['ds'] >= start_of_current_year) & (df_daily['ds'] <= current_datetime)
    ]
    total_current_year_consumption_so_far = current_year_data_up_to_today['y'].sum()

    # Calculate the start and end of the previous year
    start_of_previous_year = datetime(current_year - 1, 1, 1, tzinfo=pytz.timezone('Asia/Kolkata'))
    end_of_previous_year = datetime(current_year - 1, 12, 31, 23, 59, 59, tzinfo=pytz.timezone('Asia/Kolkata'))

    # Filter the DataFrame for the previous year's data
    previous_year_data = df_daily[
        (df_daily['ds'] >= start_of_previous_year) & (df_daily['ds'] <= end_of_previous_year)
    ]
    total_previous_year_consumption = previous_year_data['y'].sum()

    # Calculate remaining consumption for the current year
    remaining_consumption_year = current_year_total - total_current_year_consumption_so_far


    # Create a bar chart
    fig = go.Figure()

    # Add bar for last year's total consumption
    fig.add_trace(go.Bar(
        x=[str(current_year - 1)],
        y=[total_previous_year_consumption],
        name='Last Year Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for this year's consumption so far
    fig.add_trace(go.Bar(
        x=[str(current_year)],
        y=[total_current_year_consumption_so_far],
        name='Current Year So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining consumption this year
    fig.add_trace(go.Bar(
        x=[str(current_year)],
        y=[remaining_consumption_year],
        name='Current Year Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Year' bars
    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        yaxis_title='Footfalls',
        barmode='stack',
        xaxis=dict(tickvals=[str(current_year - 1), str(current_year)], ticktext=[str(current_year - 1), str(current_year)]),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_previous_year_consumption, total_current_year_consumption_so_far + remaining_consumption_year)

    # Calculate the percentage change
    percentage_change = (current_year_total - total_previous_year_consumption) / total_previous_year_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last year
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Year<br><span style='color:#ff8200; font-size:17px;'><b>{total_previous_year_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for placement
    )

    # Add annotation for predicted value this year
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Year<br><span style='color:#ff8200; font-size:17px;'><b>{current_year_total:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )



    consumption_plot_year = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_year
def tot_con_weekend(df_daily):
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Calculate the start of the current weekend (Saturday)
    start_of_weekend = current_datetime - timedelta(days=current_datetime.weekday() - 5)
    start_of_weekend = start_of_weekend.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current weekend (Sunday)
    end_of_weekend = start_of_weekend + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter the DataFrame for the current weekend's data
    current_weekend_data = df_daily[(df_daily['ds'] >= start_of_weekend) & (df_daily['ds'] <= end_of_weekend)]
    current_weekend_total = current_weekend_data['y'].sum()

    # Filter the DataFrame for the current weekend's data up to today
    current_weekend_data_up_to_today = df_daily[(df_daily['ds'] >= start_of_weekend) & (df_daily['ds'] <= current_datetime)]
    total_current_weekend_consumption_so_far = current_weekend_data_up_to_today['y'].sum()

    # Calculate the start of the previous weekend (Saturday)
    start_of_previous_weekend = start_of_weekend - timedelta(days=7)

    # Calculate the end of the previous weekend (Sunday)
    end_of_previous_weekend = start_of_weekend - timedelta(seconds=1)

    # Filter the DataFrame for the previous weekend's data
    previous_weekend_data = df_daily[(df_daily['ds'] >= start_of_previous_weekend) & (df_daily['ds'] <= end_of_previous_weekend)]
    total_previous_weekend_consumption = previous_weekend_data['y'].sum()

    # Calculate remaining consumption for the current weekend
    remaining_consumption_weekend = current_weekend_total - total_current_weekend_consumption_so_far

    # Get the current weekend number
    current_weekend_number = datetime.now().isocalendar()[1]

    # Get the previous weekend number
    previous_weekend_number = (datetime.now() - timedelta(weeks=1)).isocalendar()[1]



    # Create a bar chart
    fig = go.Figure()

    # Add bar for last weekend's total consumption
    fig.add_trace(go.Bar(
        x=[f'W{previous_weekend_number}'],
        y=[total_previous_weekend_consumption],
        name='Last Weekend Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for this weekend's consumption so far
    fig.add_trace(go.Bar(
        x=[f'W{current_weekend_number}'],
        y=[total_current_weekend_consumption_so_far],
        name='Current Weekend So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining consumption this weekend
    fig.add_trace(go.Bar(
        x=[f'W{current_weekend_number}'],
        y=[remaining_consumption_weekend],
        name='Current Weekend Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Weekend' bars
    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        yaxis_title='Footfalls',
        barmode='stack',
        xaxis=dict(tickvals=[f'W{previous_weekend_number}', f'W{current_weekend_number}'], ticktext=[f'W{previous_weekend_number}', f'W{current_weekend_number}']),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_previous_weekend_consumption, total_current_weekend_consumption_so_far + remaining_consumption_weekend)

    # Calculate the percentage change
    percentage_change = (current_weekend_total - total_previous_weekend_consumption) / total_previous_weekend_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last weekend
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Weekend<br><span style='color:#ff8200; font-size:17px;'><b>{total_previous_weekend_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for placement
    )

    # Add annotation for predicted value this weekend
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Weekend<br><span style='color:#ff8200; font-size:17px;'><b>{current_weekend_total:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )




    consumption_plot_weekend = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_weekend
def tot_con_workweek(df_daily):
    current_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))

    # Calculate the start of the current workweek (Monday)
    start_of_workweek = current_datetime - timedelta(days=current_datetime.weekday())
    start_of_workweek = start_of_workweek.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate the end of the current workweek (Friday)
    end_of_workweek = start_of_workweek + timedelta(days=4, hours=23, minutes=59, seconds=59, microseconds=999999)

    # Filter the DataFrame for the current workweek's data
    current_workweek_data = df_daily[(df_daily['ds'] >= start_of_workweek) & (df_daily['ds'] <= end_of_workweek)]
    current_workweek_total = current_workweek_data['y'].sum()

    # Filter the DataFrame for the current workweek's data up to today
    current_workweek_data_up_to_today = df_daily[(df_daily['ds'] >= start_of_workweek) & (df_daily['ds'] <= current_datetime)]
    total_current_workweek_consumption_so_far = current_workweek_data_up_to_today['y'].sum()

    # Calculate the start of the previous workweek (Monday)
    start_of_previous_workweek = start_of_workweek - timedelta(days=7)

    # Calculate the end of the previous workweek (Friday)
    end_of_previous_workweek = start_of_workweek - timedelta(seconds=1)

    # Filter the DataFrame for the previous workweek's data
    previous_workweek_data = df_daily[(df_daily['ds'] >= start_of_previous_workweek) & (df_daily['ds'] <= end_of_previous_workweek)]
    total_previous_workweek_consumption = previous_workweek_data['y'].sum()

    # Calculate remaining consumption for the current workweek
    remaining_consumption_workweek = current_workweek_total - total_current_workweek_consumption_so_far

    # Get the current workweek number
    current_workweek_number = datetime.now().isocalendar()[1]

    # Get the previous workweek number
    previous_workweek_number = (datetime.now() - timedelta(weeks=1)).isocalendar()[1]



    # Create a bar chart
    fig = go.Figure()

    # Add bar for last workweek's total consumption
    fig.add_trace(go.Bar(
        x=[f'W{previous_workweek_number}'],
        y=[total_previous_workweek_consumption],
        name='Last Workweek Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for this workweek's consumption so far
    fig.add_trace(go.Bar(
        x=[f'W{current_workweek_number}'],
        y=[total_current_workweek_consumption_so_far],
        name='Current Workweek So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
    ))

    # Add bar for remaining consumption this workweek
    fig.add_trace(go.Bar(
        x=[f'W{current_workweek_number}'],
        y=[remaining_consumption_workweek],
        name='Current Workweek Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Footfalls: %{y:.0f} <br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Workweek' bars
    fig.update_layout(
        autosize=False,
        height=300,
        width=400,
        title='Footfalls Prediction',
        yaxis_title='Footfalls',
        barmode='stack',
        xaxis=dict(tickvals=[f'W{previous_workweek_number}', f'W{current_workweek_number}'], ticktext=[f'W{previous_workweek_number}', f'W{current_workweek_number}']),
        legend_title='Legend',
        template='plotly_dark',  # Dark theme
        showlegend=False,  # Hides the legend for a cleaner look
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=20, r=20, t=40, b=40),  # Tighten up the margins for responsiveness
    )

    # Calculate the maximum y-value for dynamic positioning
    max_y = max(total_previous_workweek_consumption, total_current_workweek_consumption_so_far + remaining_consumption_workweek)

    # Calculate the percentage change
    percentage_change = (current_workweek_total - total_previous_workweek_consumption) / total_previous_workweek_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for last workweek
    fig.add_annotation(
        x=0, y=max_y * 1.1,  # Position above the highest bar
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Week<br><span style='color:#ff8200; font-size:17px;'><b>{total_previous_workweek_consumption:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=190,  # Adjust for placement
    )

    # Add annotation for predicted value this workweek
    fig.add_annotation(
        x=1, y=max_y * 0.6,  # Position in the middle
        xref='x', yref='y',
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Week<br><span style='color:#ff8200; font-size:17px;'><b>{current_workweek_total:.0f} </b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=max_y * 0.1,  # Position at the bottom
        xref='x', yref='y',
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style='; font-size:17px; font-family:Mulish;'><br> Change in Footfalls</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
    )




    consumption_plot_workweek = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_workweek
