

import json
from datetime import datetime, time, timedelta

import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz


def fig_day(fin, current_time,fin1,tz, historical_data,cost_per_hr, forecasted_data_today,current_time_dt641,next_24_hours_end, forecasted_bar_data):

    fin1= fin1[['ds','y']].set_index("ds").resample('H').mean().reset_index()
    current_time_dt64_plus_one_hour = current_time_dt641 
    # Get the date for the previous day
    previous_day = current_time_dt64_plus_one_hour.date() - timedelta(days=1)

    # Create the start and end timestamps for the previous day
    start_time = pd.Timestamp(previous_day, tz=tz)
    before_current_time = fin1[(fin1["ds"] >= start_time) & (fin1["ds"] <= current_time_dt64_plus_one_hour)]
    after_current_time=fin1[
            (fin1["ds"] > current_time_dt64_plus_one_hour) & (fin1["ds"] <= next_24_hours_end)
        ]
    common_columns = historical_data.columns.intersection(forecasted_bar_data.columns)
    historical_data = historical_data[common_columns]
    forecasted_bar_data = forecasted_bar_data[common_columns]

    total_df = pd.concat([historical_data, forecasted_bar_data], ignore_index=True)

    max_value = int(total_df["y"].max())
    max_date = total_df.loc[total_df["y"].idxmax(), "ds"].strftime("%d %b %y, %I %p")
    min_value = int(total_df["y"].min())
    min_date = total_df.loc[total_df["y"].idxmin(), "ds"].strftime("%d %b %y, %I %p")
    total_average = round(total_df["y"].mean())

    # Initialize cumulative count and cleaning schedule
    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    # Calculate cumulative counts and determine cleaning schedule based on answer_value
    for value in total_df['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0


    # Assign results to DataFrame
    total_df['cumulative_count'] = cumulative_counts
    total_df['cleaning_schedule'] = cleaning_schedule

    historical_data1 = total_df[(total_df["ds"] >= start_time) & (total_df["ds"] <= current_time_dt64_plus_one_hour)]

    forecasted_data1 = total_df[
        (total_df["ds"] > current_time_dt64_plus_one_hour) & (total_df["ds"] <= next_24_hours_end)
    ]

    # Filter and concatenate the datasets
    historical_alerts = historical_data1[historical_data1["cleaning_schedule"] != 0]
    forecasted_alerts = forecasted_data1[forecasted_data1["cleaning_schedule"] != 0]

    combined_alerts = pd.concat([historical_alerts, forecasted_alerts])
    today = current_time_dt64_plus_one_hour.date()
    current_hour = current_time_dt64_plus_one_hour.hour
    today_data = total_df[total_df['ds'].dt.date == today]
    today_data_upto_current_hour = today_data[today_data['ds'].dt.hour <= current_hour]
    so_far_work_orders =today_data_upto_current_hour['cleaning_schedule'].sum()
    total_today_work_orders=today_data['cleaning_schedule'].sum()
    total_today_work_orders = int(total_today_work_orders)
    so_far_work_orders = int(so_far_work_orders)
   

    fig_hourly = go.Figure()

    fig_hourly.add_trace(
        go.Bar(
            x=historical_data["ds"],
            y=historical_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}, %{x|%I %p}<br><b>Footfalls </b>: %{y:.0f}',
            customdata=historical_data["y"] * cost_per_hr,
            name="Actual Footfalls",
            marker=dict(color="#2275e0"),
        )
    )
    fig_hourly.add_trace(
        go.Bar(
            x=forecasted_bar_data["ds"],
            y=forecasted_bar_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}, %{x|%I %p}<br><b>Footfalls </b>: %{y:.0f}',
            customdata=forecasted_bar_data["y"] * cost_per_hr,
            showlegend=False,
            name="Forecasted Footfalls",
            marker=dict(color="#2275e0", opacity=0.4),
        )
    )

    # Ensure before_current_time starts after historical_data starts
    before_current_time_filtered = before_current_time[before_current_time["ds"] >= historical_data["ds"].min()]

    # Ensure after_current_time ends when forecasted_bar_data ends
    after_current_time_filtered = after_current_time[after_current_time["ds"] <= forecasted_bar_data["ds"].max()]

    # Create the AQI trace for before current time
    fig_hourly.add_trace(
        go.Scatter(
            x=before_current_time_filtered["ds"],
            y=before_current_time_filtered["y"],
            mode="lines+markers",
            name="Air Quality Index",
            showlegend=True,
            legendgroup="AQI",  # Group with after_current_time trace
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in before_current_time_filtered["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )
    # Create the AQI trace for after current time
    fig_hourly.add_trace(
        go.Scatter(
            x=after_current_time_filtered["ds"],
            y=after_current_time_filtered["y"],
            mode="lines+markers",
            name="Air Quality Index",
            showlegend=False,  # Hide this legend entry
            legendgroup="AQI",  # Group with before_current_time trace
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            opacity=0.6,
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in after_current_time_filtered["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )

    last_point_trace_1 = dict(
        x=before_current_time_filtered["ds"].iloc[-1],
        y=before_current_time_filtered["y"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=after_current_time_filtered["ds"].iloc[0],
        y=after_current_time_filtered["y"].iloc[0],
    )



    fig_hourly.add_trace(
        go.Scatter(
            x=[last_point_trace_1["x"], first_point_trace_2["x"]],
            y=[last_point_trace_1["y"], first_point_trace_2["y"]],
            mode="lines+markers",
            showlegend=False,  # Hide this legend entry
            legendgroup="AQI",  # Group with before_current_time trace
            yaxis="y2",
            line=dict(color="#FFA500", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            opacity=0.6,
            hoverinfo="skip",
        )
    )
    # Assign colors based on historical or forecasted data
    colors = ['rgba(255, 0, 0, 1)' if idx < len(historical_alerts) else 'rgba(255, 0, 0, 0.6)' for idx in range(len(combined_alerts))]
    fig_hourly.add_trace(
        go.Scatter(
            x=[combined_alerts["ds"].min(), combined_alerts["ds"].max()],
            y=[50, 50],
            mode="lines",
            name="Threshold limit",
            line=dict(color="#529513", width=2, dash="dot"),
            showlegend=True,
            hoverinfo="skip"
        )
    )

    # Create the single trace
    fig_hourly.add_trace(
        go.Scatter(
            x=combined_alerts["ds"],
            y=combined_alerts["y"] + 1.1,  # Adjust the offset here
            mode='markers',
            name="Cleaning Alert",
            marker=dict(
                size=15,
                color=colors,  # Use the combined color array
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                )
            ),
            showlegend=True,
            hovertemplate='<b>Cleaning Alert</b><extra></extra>',  # Hover template
            customdata=combined_alerts["cleaning_schedule"]
        )
    )

    # Calculate positions for Yesterday, Today, and Tomorrow
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Add annotations for Yesterday, Today, and Tomorrow
    annotations = [
        dict(
            x=yesterday,
            y=0,
            xref="x",
            yref="y",
            text="Yesterday",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=today,
            y=0,
            xref="x",
            yref="y",
            text="Today",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=tomorrow,
            y=0,
            xref="x",
            yref="y",
            text="Tomorrow",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]

    # Update layout of the figure
    fig_hourly.update_layout(
        template="plotly_dark",
        yaxis_title="Footfalls",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
        yaxis2=dict(
            title="Air Quality Index ",
            titlefont_color="orange",
            tickfont_color="orange",
            overlaying="y",
            side="right",
            anchor="x",
            position=0.05,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white'),
            font_family='Mulish'
        ),
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.98,
                y=1.15,
                xanchor="right",
                yanchor="top",
                text=f'<span style="text-align:left;font-family:Mulish;"><b>Max</b></span>: {max_value}  ({max_date})<br><span style="text-align:left;font-family:Mulish;"><b>Min</b></span>:  {min_value}   ({min_date})<br><span style="text-align:left;font-family:Mulish;"><b>Avg</b></span>: {total_average}  ',
                font=dict(size=15, family="Mulish"),
                align="left",
                showarrow=False,
                borderwidth=1,
                bordercolor="gray",
            )
        ]   # Add the new annotations
    )
    fig_hourly.update_xaxes(showgrid=False)
    fig_hourly.update_yaxes(showgrid=False)
    day_plot = json.loads(
        json.dumps(
            fig_hourly,
            cls=plotly.utils.PlotlyJSONEncoder))
    return day_plot,total_today_work_orders,so_far_work_orders