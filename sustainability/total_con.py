import pandas as pd
import plotly.graph_objects as go
import json
import plotly
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

def total_consumption(energy_data_all, current_datetime):
    # Extract the current date
    current_date = current_datetime.date()

    # Filter the DataFrame for the entire current date (from 0th hour to 23rd hour)
    filtered_data = energy_data_all[energy_data_all['ds'].dt.date == current_date]

    # Sum the consumption for the entire day (Predicted Today)
    total_daily_consumption = filtered_data['y'].sum()

    # Sum the consumption up to the current hour (So Far Today)
    filtered_data_so_far = energy_data_all[
        (energy_data_all['ds'].dt.date == current_datetime.date()) &
        (energy_data_all['ds'].dt.hour <= current_datetime.hour)
    ]
    
    total_consumption_so_far = filtered_data_so_far['y'].sum()

    # Calculate remaining consumption for today
    remaining_consumption_today = total_daily_consumption - total_consumption_so_far

    # Filter the DataFrame for yesterday (from 0th hour to 23rd hour)
    yesterday_date = current_datetime.date() - pd.Timedelta(days=1)
    filtered_data_yesterday = energy_data_all[energy_data_all['ds'].dt.date == yesterday_date]

    # Sum the consumption for the entire day yesterday (Yesterday Total)
    total_yesterday_consumption = filtered_data_yesterday['y'].sum()

    # Create a bar chart
    fig = go.Figure()

    # Add bar for yesterday's total consumption
    fig.add_trace(go.Bar(
        x=['Last<br>Day'],
        y=[total_yesterday_consumption],
        name='Yesterday Total',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for today's consumption so far
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[total_consumption_so_far],
        name='So Far Today',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for remaining consumption today
    fig.add_trace(go.Bar(
        x=['This<br>Day'],
        y=[remaining_consumption_today],
        name='Remaining Today',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'Today' bars
    fig.update_layout(
        autosize=False,
        height=300,
        title='',
        yaxis_title='Consumption (kWh)',
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

    # Calculate the percentage change
    percentage_change = (total_daily_consumption - total_yesterday_consumption) / total_yesterday_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'
    fig.add_annotation(
        x=1, y=total_yesterday_consumption,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Day<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{total_yesterday_consumption:.2f} kWh</b></span>",

        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
        yshift=-25,  # Adjust for placement to be below the second annotation
    )

    fig.add_annotation(
        x=1, y=total_daily_consumption,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted Today<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{total_daily_consumption:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
        yshift=-100,  # Adjust for placement to be below the first annotation
    )

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=total_daily_consumption,
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b> </span> <span style=' font-size:17px; font-family:Mulish;'><br>  Predicted  Change</span>",
        showarrow=False,
        font=dict(size=17),
        xshift=130,  # Adjust for placement
        yshift=-165,  # Adjust for placement
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
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for this week's consumption so far
    fig.add_trace(go.Bar(
        x=[f'W{current_week_number}'],
        y=[total_current_week_consumption_so_far],
        name='Current Week so Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for remaining consumption this week
    fig.add_trace(go.Bar(
        x=[f'W{current_week_number}'],
        y=[remaining_consumption_today],
        name='Current Week Remaining ',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Week' bars
    fig.update_layout(
        autosize=False,
        height=300,
        title='',
        yaxis_title='Consumption (kWh)',
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

    # Calculate the percentage change
    percentage_change = (current_week_total - total_previous_week_consumption) / total_previous_week_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=current_week_total,
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b></span> <span style=' font-size:17px; font-family:Mulish;'><br>Predicted Change</span>",
        showarrow=False,

        font=dict(size=17),
        xshift=130,  # Adjust for placement
        yshift=-175,  # Adjust for placement
    )

    fig.add_annotation(
        x=1, y=current_week_total,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Week<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{current_week_total:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-110,  # Adjust for placement to be below the first annotation
    )

    fig.add_annotation(
        x=1, y=total_previous_week_consumption,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Week<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{total_previous_week_consumption:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-40,  # Adjust for placement to be below the second annotation
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
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for this month's consumption so far
    fig.add_trace(go.Bar(
        x=[current_month_name],
        y=[total_current_month_consumption_so_far],
        name='Current Month So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for remaining consumption this month
    fig.add_trace(go.Bar(
        x=[current_month_name],
        y=[remaining_consumption_today],
        name='Current Month Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Month' bars
    fig.update_layout(
        autosize=False,
        height=300,
        title='',
        yaxis_title='Consumption (kWh)',
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

    # Calculate the percentage change
    percentage_change = (current_month_total - total_previous_month_consumption) / total_previous_month_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=current_month_total,
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'> <b>{symbol} {abs(percentage_change):.2f}%</b></span> <span style='font-size:17px; font-family:Mulish;'> <br>Predicted Change</span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-140,  # Adjust for placement
    )

    fig.add_annotation(
        x=1, y=current_month_total,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Month<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{current_month_total:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-60,  # Adjust for placement to be below the first annotation
    )

    fig.add_annotation(
        x=1, y=total_previous_month_consumption,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Last Month <br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{total_previous_month_consumption:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-30,  # Adjust for placement to be below the second annotation
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
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for this year's consumption so far
    fig.add_trace(go.Bar(
        x=[str(current_year)],
        y=[total_current_year_consumption_so_far],
        name='Current Year So Far',
        marker_color='#1f77b4',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
    ))

    # Add bar for remaining consumption this year
    fig.add_trace(go.Bar(
        x=[str(current_year)],
        y=[remaining_consumption_year],
        name='Current Year Remaining',
        marker_color='#1f77b4', marker_opacity=0.4,
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br>Consumption: %{y:.2f} kWh<br>',
        opacity=0.6,
    ))

    # Update layout to stack the 'This Year' bars
    fig.update_layout(
        autosize=False,
        height=300,
        title='',
        yaxis_title='Consumption (kWh)',
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

    # Calculate the percentage change
    percentage_change = (current_year_total - total_previous_year_consumption) / total_previous_year_consumption * 100

    # Determine the annotation symbol and color based on whether the change is positive (red) or negative (green)
    symbol = '▲' if percentage_change > 0 else '▼'
    color = 'red' if percentage_change > 0 else 'green'

    # Add annotation for percentage change
    fig.add_annotation(
        x=1, y=current_year_total,
        text=f"<span style='color:{color}; font-size:17px; font-family:Mulish;'><b> {symbol} {abs(percentage_change):.2f}%</b></span> <span style=' font-size:17px; font-family:Mulish;'><br>Predicted Change</span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-180,  # Adjust for placement
    )

    fig.add_annotation(
        x=1, y=current_year_total,
        text=f"<span style='font-size:17px; font-family:Mulish;'>Predicted This Year<br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{current_year_total:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=-120,  # Adjust for placement to be below the first annotation
    )

    fig.add_annotation(
        x=1, y=total_previous_year_consumption,
        text=f"<span style='font-size:17px ; font-family:Mulish;'>Last Year <br><span style='display:normal; line-height:6.0;'></span><span style='color:#ff8200; font-size:17px;'><b>{total_previous_year_consumption:.2f} kWh</b></span>",
        showarrow=False,
        font=dict(size=14),
        xshift=130,  # Adjust for placement
        yshift=125,  # Adjust for placement to be below the second annotation
    )

    consumption_plot_year = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )
    )

    return consumption_plot_year
