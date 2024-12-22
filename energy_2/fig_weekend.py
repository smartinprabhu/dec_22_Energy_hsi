import json
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz

def sav_plot_weekend(data, current_time, current_time_dt641, cost_per_kw):
    # Example of resampling with different aggregation functions for different columns
    data_daily = (
        data.set_index('ds')
        .resample('D')
        .agg({'y': 'sum','savings':'sum','consumption':'sum', 'temperature': 'first','final_target':'sum'})
        .reset_index()
    )

    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)

    # Calculate the date range for last weekend, this weekend, and next weekend
    last_weekend_start = current_time_dt64 - timedelta(days=current_time_dt64.weekday() + 7)
    last_weekend_end = last_weekend_start + timedelta(days=6)
    this_weekend_start = current_time_dt64 - timedelta(days=current_time_dt64.weekday())
    this_weekend_end = this_weekend_start + timedelta(days=6)
    next_weekend_start = this_weekend_start + timedelta(days=7)
    next_weekend_end = next_weekend_start + timedelta(days=6)

    # Filter the data to include only these three weekends
    filtered_data = data_daily[(data_daily['ds'] >= last_weekend_start) & (data_daily['ds'] <= next_weekend_end)]
    filtered_data['consumption'] = filtered_data['final_target']
    actual_data = filtered_data[filtered_data['ds'] <= current_time_dt64]
    forecasted_data = filtered_data[filtered_data['ds'] > current_time_dt64]

    # Filter for weekend (Saturday and Sunday)
    weekend_filter = filtered_data['ds'].dt.weekday >= 5
    filtered_data = filtered_data[weekend_filter]
    actual_data = actual_data[weekend_filter]
    forecasted_data = forecasted_data[weekend_filter]

    # Calculate consumption and savings
    data_daily['consumption'] = np.where(data_daily['y'] <= data_daily['final_target'], data_daily['y'], data_daily['final_target'])
    data_daily['savings'] = np.where(data_daily['y'] > data_daily['final_target'], data_daily['y'] - data_daily['final_target'], 0)

    # Get the current weekend's data
    current_weekend_data = data_daily[(data_daily['ds'] >= this_weekend_start) & (data_daily['ds'] <= this_weekend_end)]
    current_weekend_data = current_weekend_data[current_weekend_data['ds'].dt.weekday >= 5]  # Filter for weekend
    this_weekend_total = current_weekend_data['y'].sum()
    this_weekend_savings = current_weekend_data['savings'].sum()
    target_reduction_this_weekend = this_weekend_savings
    current_datetime = datetime.now()
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    # Calculate the start of the current weekend (Saturday) with timezone info
    start_of_weekend = current_date - timedelta(days=current_date.weekday())
    start_of_weekend = start_of_weekend.replace(hour=0, minute=0, second=0, microsecond=0)

    # The end date is today with the current time
    end_of_today = current_date

    # Filter the DataFrame for the current weekend's data up to today
    current_weekend_data_up_to_today = data_daily[(data_daily['ds'] >= start_of_weekend) & (data_daily['ds'] <= end_of_today)]
    current_weekend_data_up_to_today = current_weekend_data_up_to_today[current_weekend_data_up_to_today['ds'].dt.weekday >= 5]  # Filter for weekend
    total_current_weekend_consumption_so_far = float(current_weekend_data_up_to_today['y'].sum())

    # Get last weekend's data
    last_weekend_data = data_daily[(data_daily['ds'] >= last_weekend_start) & (data_daily['ds'] <= last_weekend_end)]
    last_weekend_data = last_weekend_data[last_weekend_data['ds'].dt.weekday >= 5]  # Filter for weekend
    total_last_weekend_consumption = last_weekend_data['y'].sum()

    # Calculate metrics
    emission_factor = 0.87
    emission_last_weekend = float(total_last_weekend_consumption * emission_factor)
    emission_this_weekend_so_far = float(total_current_weekend_consumption_so_far * emission_factor)
    emission_this_weekend_predicted = float(this_weekend_total * emission_factor)
    target_reduction_this_weekend_emission = float(target_reduction_this_weekend * emission_factor)
    estimated_cost_last_weekend = float(total_last_weekend_consumption * cost_per_kw)
    estimated_cost_this_weekend_so_far = float(total_current_weekend_consumption_so_far * cost_per_kw)
    estimated_cost_this_weekend_predicted = float(this_weekend_total * cost_per_kw)
    rate_of_change_weekend = ((this_weekend_total - total_last_weekend_consumption) / total_last_weekend_consumption) * 100
    rate_of_change_weekend2 = ((emission_this_weekend_predicted - emission_last_weekend) / emission_this_weekend_predicted) * 100
    rate_of_change_weekend1 = ((emission_this_weekend_predicted - emission_last_weekend) / emission_this_weekend_predicted) * 100
    target_reduction_this_weekend_cost = float(target_reduction_this_weekend * cost_per_kw)

    fig = go.Figure()

    # Plot actual consumption up to the target level (no breach)
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
            marker=dict(color="#c1deda", opacity=0.4),
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
        hovertemplate="Temp: %{text}°C<extra></extra>",
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
            traceorder="normal",
            font=dict(size=10)
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
            side='right',
            anchor="x",
            position=0.05,
            range=[5, 25]
        ),
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
    # Calculate Target_percent

    target_consumption_weekend = float(current_weekend_data['consumption'].sum())
    target_cost_weekend=float(target_consumption_weekend * cost_per_kw)
    target_emission_weekend=float(target_consumption_weekend * emission_factor)


    overall_consumption = current_weekend_data['y'].sum()
    target = current_weekend_data['consumption'].sum()
    # Assuming current_day_data is a DataFrame and current_day is a dictionary

    percentage_deviation5 = float(((overall_consumption - target) / overall_consumption) * 100)


    sav_weekend = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))

    return sav_weekend, total_last_weekend_consumption, target_consumption_weekend, target_cost_weekend, target_emission_weekend, total_current_weekend_consumption_so_far, this_weekend_total, rate_of_change_weekend, emission_last_weekend, emission_this_weekend_so_far, emission_this_weekend_predicted, rate_of_change_weekend2, estimated_cost_last_weekend, estimated_cost_this_weekend_so_far, estimated_cost_this_weekend_predicted, rate_of_change_weekend1, percentage_deviation5
