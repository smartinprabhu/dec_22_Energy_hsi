"""
This module contains functions for generating figures for hourly, daily and weekly data visualization.
"""

import datetime
import json
from datetime import datetime, timedelta
from datetime import timedelta
import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz


def fig_week(tz,fin1,fin,current_time,next_7_days_end,current_time_dt64,forecasted_data_week_end,cost_per_hr,forecasted_bar_data_daily,historical_data_daily):

    cumulative_count = 0
    cumulative_counts = []
    cleaning_schedule = []

    # Calculate cumulative counts and determine cleaning schedule based on answer_value
    for value in fin['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        cleaning_schedule.append(1 if cumulative_count >= 50 else 0)
        if cumulative_count >= 50:
            cumulative_count = 0


    # Assign results to DataFrame
    fin['cumulative_count'] = cumulative_counts
    fin['cleaning_schedule'] = cleaning_schedule


    end_of_week = current_time + timedelta(days=(6 - current_time.weekday()))
    next_7_days_end = end_of_week + timedelta(days=7)
    next_7_days_end = pd.Timestamp(next_7_days_end.replace(hour=23, minute=59, second=59, microsecond=999999)).tz_convert(tz)
    fin=fin.set_index('ds').resample('D').sum().reset_index()
    dz_day=fin1[['ds','y']].set_index('ds').resample('D').mean().reset_index()
    
    forecasted_bar_data_daily = fin[
        (fin["ds"] > current_time_dt64) & (fin["ds"] <= next_7_days_end)
    ]

    historical_data_daily = fin[
        (fin["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (fin["ds"].dt.date <= current_time.date())
    ]
    before_current_time1 = dz_day[
        (dz_day["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (dz_day["ds"].dt.date <= current_time.date())
    ]
    after_current_time1 = dz_day[
        (dz_day["ds"] > current_time_dt64) & (dz_day["ds"] <= next_7_days_end)
    ]
    forecasted_data_week_end = fin[
        (fin["ds"] > current_time_dt64) & (fin["ds"] <= end_of_week)]
    total_day = pd.concat([historical_data_daily, forecasted_data_week_end])
    max_value = int(total_day["y"].max())
    max_date = total_day.loc[total_day["y"].idxmax(),
                            "ds"].strftime("%d %b %y")
    min_value = int(total_day["y"].min())
    min_date = total_day.loc[total_day["y"].idxmin(),
                            "ds"].strftime("%d %b %y")
    total_average = round(total_day["y"].mean())


    cleaning_forecast_daily = fin[
        (fin["ds"] > current_time_dt64) & (fin["ds"] <= next_7_days_end)
    ]
    cleaning_history_daily = fin[
        (fin["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (fin["ds"].dt.date <= current_time.date())
    ]

    # Calculate adjusted y-values for historical circles
    adjustment = 15 # Change this value to adjust the position
    cleaning_y_values_history = cleaning_history_daily[cleaning_history_daily["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_daily[historical_data_daily["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1)
    start_of_this_week = current_time_dt64 - timedelta(days=current_time_dt64.weekday())
    end_of_this_week = start_of_this_week + timedelta(days=6)
    this_week_data = fin[(fin['ds'].dt.date >= start_of_this_week.date()) & (fin['ds'].dt.date <= end_of_this_week.date())]
    tot_this_week_work=this_week_data['cleaning_schedule'].sum()
    this_week_data_upto_current_day = this_week_data[this_week_data['ds'].dt.date <= current_time_dt64.date()]
    so_far_week_work_orders=this_week_data_upto_current_day['cleaning_schedule'].sum()
    so_far_week_work_orders=int(so_far_week_work_orders)
    tot_this_week_work=int(tot_this_week_work)
    # Create hourly plot
    fig_daily = go.Figure()

    # Add actual footfall bar trace
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily["ds"],
            y=historical_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y:.0f}  <br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data_daily["y"] * cost_per_hr,
            name="Actual Footfalls",
            marker=dict(color="#2275e0"),

        )
    )

    # Add forecasted footfall bar trace
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily["ds"],
            y=forecasted_bar_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y:.0f}  <br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecasted_bar_data_daily["y"] * cost_per_hr,
            showlegend=False,
            name="Forecasted Footfalls",
            marker=dict(color="#2275e0",opacity=0.4),

        )
    )
    fig_daily.add_trace(
        go.Scatter(
            x=before_current_time1["ds"],
            y=before_current_time1["y"],
            mode="lines+markers",
            name="Air Quality Index",
            showlegend=True,
            legendgroup="IAQ",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in before_current_time1["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )

    # Add air quality index after current time
    fig_daily.add_trace(
        go.Scatter(
            x=after_current_time1["ds"],
            y=after_current_time1["y"],
            mode="lines+markers",
            name="Air Quality Index",
            showlegend=False,
            legendgroup="IAQ",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            opacity=0.6,
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in after_current_time1["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )
    # Add line to connect last point of before_current_time1 and first point of after_current_time1
    last_point_trace_1 = dict(
        x=before_current_time1["ds"].iloc[-1],
        y=before_current_time1["y"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=after_current_time1["ds"].iloc[0],
        y=after_current_time1["y"].iloc[0],
    )

    fig_daily.add_trace(
        go.Scatter(
            x=[last_point_trace_1["x"], first_point_trace_2["x"]],
            y=[last_point_trace_1["y"], first_point_trace_2["y"]],
            mode="lines+markers",
            showlegend=False,
            legendgroup="IAQ",
            yaxis="y2",
            line=dict(color="#FFA500", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            hoverinfo="skip",
        )
    )
    # Adjust y-values to position circles above the bars
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values = cleaning_forecast_daily[cleaning_forecast_daily["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_daily[historical_data_daily["ds"] == row["ds"]]["y"].values[0] + adjustment
        if row["ds"] in historical_data_daily["ds"].values else forecasted_bar_data_daily[forecasted_bar_data_daily["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )

    # Add scatter trace for forecasted alerts with data labels (lighter colors)
    fig_daily.add_trace(
        go.Scatter(
            x=cleaning_forecast_daily[cleaning_forecast_daily["cleaning_schedule"] != 0]["ds"],
            y=cleaning_y_values,
            name="Cleaning Alert",
            mode='markers+text',
            marker=dict(
                size=30,
                color='red',
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                )
            ),
            text=cleaning_forecast_daily[cleaning_forecast_daily["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='#000000'
            ),
            showlegend=True,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_forecast_daily[cleaning_forecast_daily["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    # Add scatter trace for historical alerts with data labels (lighter colors)
    fig_daily.add_trace(
        go.Scatter(
            x=cleaning_history_daily[cleaning_history_daily["cleaning_schedule"] != 0]["ds"],
            y=cleaning_y_values_history,
            name="Cleaning Alert",
            mode='markers+text',
            marker=dict(
                size=30,
                color='red',
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                )
            ),
            text=cleaning_history_daily[cleaning_history_daily["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='white'
            ),
            showlegend=False,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_history_daily[cleaning_history_daily["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
        
    # Define your timezone
    tz = pytz.timezone('Asia/Kolkata')

    # Calculate the start and end dates of the previous week, current week, and next week
    current_time = pd.Timestamp.now().normalize().tz_localize(tz)
    start_of_current_week = current_time - pd.Timedelta(days=current_time.dayofweek)
    end_of_current_week = start_of_current_week + pd.Timedelta(days=6)

    start_of_previous_week = start_of_current_week - pd.Timedelta(days=7)
    start_of_next_week = end_of_current_week + pd.Timedelta(days=1)

    # Add annotations for Previous Week, Current Week, and Next Week
    annotations = [
        dict(
            x=start_of_previous_week,
            y=0,
            xref="x",
            yref="y",
            text="Previous Week",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_current_week,
            y=0,
            xref="x",
            yref="y",
            text="Current Week",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_next_week,
            y=0,
            xref="x",
            yref="y",
            text="Next Week",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]

    # Update layout of the figure
    fig_daily.update_layout(
        template="plotly_dark",  # Use plotly_dark template
        yaxis_title="Footfalls",
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5
        ),
        yaxis2=dict(
            title="Air Quality Index",
            titlefont_color="orange",
            tickfont_color="orange",
            overlaying="y",
            side="right",
            anchor="x",
            position=0.05,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor='#2C2C2F',  # Black background for hover labels
            font=dict(color='white'),  # Font color
            font_family='Mulish'
        ),
        xaxis=dict(),
        font=dict(
            family="Mulish",
        ),
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.98,
                y=1.15,
                xanchor="right",
                yanchor="top",
                text=f'<span style="text-align:left;font-family:Mulish;"><b>Max</b></span>: {max_value} ({max_date})<br><span style="text-align:left;font-family:Mulish;"><b>Min</b></span>: {min_value} ({min_date})<br> <span style="text-align:left;font-family:Mulish;"><b>Avg</b></span>: {total_average} ',
                font=dict(size=15, family="Mulish"),
                align="left",
                showarrow=False,
                borderwidth=1,
                bordercolor="gray",
            )
        ] ,  # Add the new annotations
    )
    fig_daily.update_xaxes(showgrid=False)
    fig_daily.update_yaxes(showgrid=False)
    week_plot = json.loads(
        json.dumps(
            fig_daily,
            cls=plotly.utils.PlotlyJSONEncoder))
    return dz_day,week_plot,tot_this_week_work,so_far_week_work_orders