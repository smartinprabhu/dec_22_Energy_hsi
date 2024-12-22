

    

import json
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz
def sav_plot1(data, current_time, current_time_dt641, cost_per_kw):

    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)

    # Calculate the date range for yesterday, today, and tomorrow
    yesterday = current_time_dt64 - timedelta(days=1)
    tomorrow = current_time_dt64 + timedelta(days=1)

    # Filter the data to include only these three days
    filtered_data = data[(data['ds'] >= yesterday) & (data['ds'] <= tomorrow)]

    # Separate data into actual and forecasted
    actual_data = filtered_data[filtered_data['ds'] <= current_time_dt64]
    forecasted_data = filtered_data[filtered_data['ds'] > current_time_dt64]

    today_start = current_time_dt641.normalize()
    emission_factor = 0.87

    # Calculate consumption and savings
    data['consumption'] = np.where(data['y'] <= data['final_target'], data['y'], data['final_target'])
    data['savings'] = np.where(data['y'] > data['final_target'], data['y'] - data['final_target'], 0)

    # Get the current date
    current_date = datetime.now().date()

    # Filter the DataFrame for the current day's data
    current_day_data = data[data['ds'].dt.date == current_date]
    today_total = current_day_data['y'].sum()
    today_savings = current_day_data['savings'].sum()
    target_reduction_today = today_savings

    yesterday_date = datetime.now().date() - timedelta(days=1)

    # Filter the DataFrame for yesterday's data
    yesterday_data = data[data['ds'].dt.date == yesterday_date]
    total_yesterday_consumption = yesterday_data['y'].sum()

    current_datetime = datetime.now()

    current_day_data_so_far = data[
        (data['ds'].dt.date == current_datetime.date()) &
        (data['ds'].dt.hour <= current_datetime.hour)
    ]
    total_today_consumption_so_far = current_day_data_so_far['y'].sum()
    t_savings_so = current_day_data_so_far['savings'].sum()
    so_far_today_reduction = total_today_consumption_so_far - t_savings_so
    rate_of_change_hour = (
        (today_total - total_yesterday_consumption) / total_yesterday_consumption
    ) * 100

    total_yesterday_consumption = float(total_yesterday_consumption)
    total_today_consumption_so_far = float(total_today_consumption_so_far)
    today_total = float(today_total)
    rate_of_change_hour = float(rate_of_change_hour)
    target_reduction_today = float(target_reduction_today)

    emission_yesterday = float(total_yesterday_consumption * emission_factor)
    emission_today_so_far = float(total_today_consumption_so_far * emission_factor)
    emission_today_predicted = float(today_total * emission_factor)
    target_reduction_today_emission = float(target_reduction_today * emission_factor)
    rate_of_change_hour2 = (
        (emission_today_predicted - emission_yesterday) / emission_today_predicted
    ) * 100
    rate_of_change_hour2 = float(rate_of_change_hour2)

    estimated_cost_yesterday = float(total_yesterday_consumption * cost_per_kw)
    estimated_cost_today_so_far = float(total_today_consumption_so_far * cost_per_kw)
    estimated_cost_today_predicted = float(today_total * cost_per_kw)

    rate_of_change_hour1 = (
        (emission_today_predicted - emission_yesterday) / emission_today_predicted
    ) * 100
    rate_of_change_hour1 = float(rate_of_change_hour1)

    target_reduction_today_cost = float(target_reduction_today * cost_per_kw)

    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)

    yesterday_start = (current_time_dt64 - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_end = yesterday_start + timedelta(hours=23, minutes=59, seconds=59)

    today_start = current_time_dt64.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(hours=23, minutes=59, seconds=59)

    tomorrow_start = today_start + timedelta(days=1)
    tomorrow_end = tomorrow_start + timedelta(hours=23, minutes=59, seconds=59)

    # Filter the data to include only these three days
    filtered_data = data[
        (data['ds'] >= yesterday_start) & (data['ds'] <= tomorrow_end)
    ]
    # Separate data into actual and forecasted
    actual_data = filtered_data[filtered_data['ds'] <= current_time_dt64]
    forecasted_data = filtered_data[filtered_data['ds'] > current_time_dt64]

    # Create the plot
    fig = go.Figure()

    # Plot actual consumption up to the target level (no breach)
    # Calculate the y values for the second trace to stack on top of the first
    savings_y_values = actual_data['consumption'] + actual_data['savings']

    # Add the first trace for Consumption
    fig.add_trace(go.Bar(
        x=actual_data['ds'],
        y=actual_data['consumption'],
        name='Consumption',
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh <br><b>Cost</b>: %{customdata:.2f}',
        customdata=actual_data['consumption'] * cost_per_kw,
        marker=dict(color="#2275e0"),
        showlegend=True,
        legendgroup="",
    ))


    fig.add_trace(
        go.Bar(
            x=actual_data["ds"],
            y=actual_data["savings"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span> %{y:.2f} kWh ',
            name="Above Target",
            marker=dict(color="#c1deda"),
            showlegend=False,
            legendgroup="",
        )
    )

    # Plot forecasted consumption up to the target level (no breach)
    fig.add_trace(go.Bar(
        x=forecasted_data['ds'],
        y=forecasted_data['consumption'],
        name='Consumption',
        marker=dict(color="#2275e0", opacity=0.4),
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh <br><b>Cost</b>: %{customdata:.2f}',
        customdata=actual_data['y'] * cost_per_kw,
        showlegend=False,
        legendgroup="A",
    ))


    fig.add_trace(
        go.Bar(
            x=forecasted_data["ds"],
            y=forecasted_data["savings"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span> %{y:.2f} kWh ',
            name="Above Target",
            marker=dict(color="#c1deda",opacity=0.4),
            showlegend=True,
            legendgroup="CA",
        )
    )

    # Add target line
    fig.add_trace(go.Scatter(
        x=filtered_data['ds'],
        y=filtered_data['final_target'],
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span> %{y:.2f} kWh ',

        mode='lines',
        name='Target',
        line=dict(color='green', dash='dot', width=1.5)
    ))

    # Add actual temperature data trace
    fig.add_trace(go.Scatter(
        x=actual_data['ds'],
        y=actual_data['temperature'],
        mode='lines+markers',
        name="Temp °C",
        showlegend=True,
        legendgroup="CA",
        yaxis="y2",
        line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
        marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
        connectgaps=True,
        text=[f"{y:.2f}" for y in actual_data["temperature"]],
        hovertemplate="Temp: %{text}°C<extra></extra>",  # Orange with 0.8 opacity for actual
        visible=False  # Hide initially
    ))

    last_point_trace_1 = dict(
        x=actual_data["ds"].iloc[-1],
        y=actual_data["temperature"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=forecasted_data["ds"].iloc[0],
        y=forecasted_data["temperature"].iloc[0],
    )

    fig.add_trace(
        go.Scatter(
            x=[last_point_trace_1["x"], first_point_trace_2["x"]],
            y=[last_point_trace_1["y"], first_point_trace_2["y"]],
            mode="lines+markers",
            showlegend=False,
            legendgroup="CA",
            yaxis="y2",
            line=dict(color="#FFA500", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            hoverinfo="skip",
            visible=False  # Hide initially
        )
    )

    # Add forecasted temperature data trace
    fig.add_trace(go.Scatter(
        x=forecasted_data['ds'],
        y=forecasted_data['temperature'],
        mode='lines+markers',
        name="Temp °C",
        showlegend=False,
        legendgroup="CA",
        yaxis="y2",
        line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
        marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
        connectgaps=True,
        opacity=0.4,
        text=[f"{y:.2f}" for y in forecasted_data["temperature"]],
        hovertemplate="Temp: %{text}°C<extra></extra>",
        visible=False  # Hide initially
    ))

    # Update the layout to include the secondary y-axis
    fig.update_layout(
        template="plotly_dark",
        barmode='stack',  # Stack the bars
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white'),
            font_family='Mulish'
        ),
        title='',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            traceorder="normal",  # Ensure the legend items are in the order they were added
            # entrywidth=100,  # Adjust the width of each legend entry
            font=dict(size=10)  # Adjust the font size of the legend
        ),
        xaxis_title='',
        yaxis=dict(
            title='Consumption (kWh)',
            titlefont=dict(color="#2275e0"),
            tickfont=dict(color="#2275e0")
        ),
        yaxis2=dict(
            title='',
            titlefont=dict(color="rgba(0,0,0,0)"),
            tickfont=dict(color="rgba(0,0,0,0)"),
            overlaying='y',
            side='right'
        ),
        # barmode='overlay',  # Using 'overlay' for comparison
        hovermode='x unified',
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True, True, True, True, True, True, True, True]},
                            {"yaxis2.title.text": "Temperature (°C)", "yaxis2.tickfont.color": "orange", "yaxis2.titlefont.color": "orange"}],
                        label="Show Temp",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [True, True, True, True, True, False, False, False]},
                            {"yaxis2.title.text": "", "yaxis2.tickfont.color": "rgba(0,0,0,0)", "yaxis2.titlefont.color": "rgba(0,0,0,0)"}],
                        label="Hide Temp",
                        method="update"
                    )
                ]),
                pad={"r": 10, "t": -20},
                showactive=True,
                x=0.81,
                xanchor="left",
                y=1.1,
                yanchor="top",
                active=1  # Set the "Hide Temp" button as active initially
            ),
        ]
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    # Get the target and consumption for today
    target_consumption = float(current_day_data['consumption'].sum())
    target_cost=float(target_consumption * cost_per_kw)
    target_emission=float(target_consumption * emission_factor)

    
    overall_consumption = current_day_data['y'].sum()
    target =target_consumption
    # Assuming current_day_data is a DataFrame and current_day is a dictionary

    percentage_deviation = float(((overall_consumption - target) / overall_consumption) * 100)


    # target_consumption=f"{target_consumption:.2f} kWh"
    # target_cost=f"{target_cost:.2f} $"
    # target_emission=f"{target_emission:.2f} tCO2e"
    sav_plot= json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder)) 

    return sav_plot, total_yesterday_consumption,target_consumption,target_cost,target_emission, percentage_deviation,total_today_consumption_so_far, today_total, rate_of_change_hour,emission_yesterday,emission_today_so_far,emission_today_predicted,estimated_cost_yesterday,estimated_cost_today_so_far,estimated_cost_today_predicted
