
"""

This module contains functions for generating figures for workweek  data visualization.

"""
import json
from datetime import datetime, timedelta

import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz
import plotly.graph_objects as go
import pandas as pd
import pytz
from datetime import datetime, timedelta

# Define your timezone


def workweek_fig(next_week_end,fin,dz_day,historical_data_workweek,forecast_data_bar_workweek,forecast_data_workweek_cal, start_date,current_week_start, cost_per_hr,current_time,tz):
        
    fin=fin.set_index('ds').resample('D').sum().reset_index()

    tz = pytz.timezone('Asia/Kolkata')

    # Ensure timestamps are localized or converted appropriately
    dz_day["ds"] = pd.to_datetime(dz_day["ds"])
    if dz_day["ds"].dt.tz is None:
        dz_day["ds"] = dz_day["ds"].dt.tz_localize(tz)
    else:
        dz_day["ds"] = dz_day["ds"].dt.tz_convert(tz)

    current_time = datetime.now(tz)
    current_date = pd.Timestamp.now(tz=tz)

    # Calculate the start and end dates of the previous work week, current work week, and next work week
    current_weekday = current_date.weekday()
    start_of_current_week = current_date - timedelta(days=current_weekday)
    end_of_current_week = start_of_current_week + timedelta(days=4)

    start_of_previous_week = start_of_current_week - timedelta(days=7)
    end_of_previous_week = start_of_previous_week + timedelta(days=4)

    start_of_next_week = end_of_current_week + timedelta(days=3)
    end_of_next_week = start_of_next_week + timedelta(days=4)

    # Historical data for the current work week and previous work week
    historical_data_week = fin[
        (fin["ds"].dt.date >= start_of_previous_week.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ]

    # Determine the end date of the historical data
    end_date_historical_data = historical_data_week["ds"].max()

    # Ensure end_date_historical_data is timezone-aware
    if end_date_historical_data.tzinfo is None:
        end_date_historical_data = end_date_historical_data.tz_localize(tz)
    else:
        end_date_historical_data = end_date_historical_data.tz_convert(tz)

    # Filter the forecasted data to include dates from the end of the historical data to the end of the next work week
    forecasted_bar_data_weekly = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_week)
    ]

    # Ensure current_time is timezone-aware
    current_time = pd.Timestamp.now(tz)

    # Now you can use it in your filter
    forecasted_data_currentweek_end = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_current_week)
    ]
    before_current_time1 = dz_day[
        (dz_day["ds"].dt.date >= start_of_previous_week.date()) &
        (dz_day["ds"].dt.date <= current_time.date())
    ]
    after_current_time1 = dz_day[
        (dz_day["ds"] > end_date_historical_data) &
        (dz_day["ds"] <= end_of_next_week)
    ]
    total_day = pd.concat([historical_data_week, forecasted_data_currentweek_end])
    max_value = int(total_day["y"].max())
    max_date = total_day.loc[total_day["y"].idxmax(), "ds"].strftime("%d %b %y")
    min_value = int(total_day["y"].min())
    min_date = total_day.loc[total_day["y"].idxmin(), "ds"].strftime("%d %b %y")
    total_average = round(total_day["y"].mean())

    cleaning_forecast_weekly = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_week)
    ]
    cleaning_history_weekly = fin[
        (fin["ds"].dt.date >= start_of_previous_week.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ]

    # Create hourly plot
    fig_weekly = go.Figure()
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values_history = cleaning_history_weekly[cleaning_history_weekly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_week[historical_data_week["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values = cleaning_forecast_weekly[cleaning_forecast_weekly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_week[historical_data_week["ds"] == row["ds"]]["y"].values[0] + adjustment
        if row["ds"] in historical_data_week["ds"].values else forecasted_bar_data_weekly[forecasted_bar_data_weekly["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )

    # Calculate the start and end dates for the last workweek and the current workweek
    def get_workweek_dates(current_time):
        # Calculate the start of the current workweek (Monday)
        start_of_current_workweek = current_time - timedelta(days=current_time.weekday())
        # Calculate the end of the current workweek (Friday)
        end_of_current_workweek = start_of_current_workweek + timedelta(days=4)
        # Calculate the start of the last workweek (Monday)
        start_of_last_workweek = start_of_current_workweek - timedelta(days=7)
        # Calculate the end of the last workweek (Friday)
        end_of_last_workweek = start_of_last_workweek + timedelta(days=4)
        return start_of_last_workweek, end_of_last_workweek, start_of_current_workweek, end_of_current_workweek

    start_of_last_workweek, end_of_last_workweek, start_of_current_workweek, end_of_current_workweek = get_workweek_dates(current_time)
    current_workweek_data = fin[(fin['ds'].dt.date >= start_of_current_workweek.date()) & (fin['ds'].dt.date <= end_of_current_workweek.date())]
    current_workweek_data_upto_current_day = current_workweek_data[current_workweek_data['ds'].dt.date <= current_time.date()]
    so_far_workweek_work_orders=int(current_workweek_data_upto_current_day['cleaning_schedule'].sum())
    tot_this_workweek_work=int(current_workweek_data['cleaning_schedule'].sum())

    fig_weekly.add_trace(
        go.Bar(
            x=historical_data_week["ds"],
            y=historical_data_week["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y} <br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data_week["y"] * cost_per_hr,
            name=" Actual Footfalls",
            marker=dict(color="#2275e0"),
        )
    )

    fig_weekly.add_trace(
        go.Bar(
            x=forecasted_bar_data_weekly["ds"],
            y=forecasted_bar_data_weekly["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y}<br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecasted_bar_data_weekly["y"] * cost_per_hr,
            showlegend=False,
            name="Forecasted Footfalls",
            marker=dict(color="#2275e0", opacity=0.4),
        )
    )

    fig_weekly.add_trace(
        go.Scatter(
            x=before_current_time1["ds"],
            y=before_current_time1["y"],
            mode="lines+markers",
            name=" Air Quality Index ",
            showlegend=True,
            legendgroup="IAQZ",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in before_current_time1["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )

    fig_weekly.add_trace(
        go.Scatter(
            x=after_current_time1["ds"],
            y=after_current_time1["y"],
            mode="lines+markers",
            name=" Air Quality Index ",
            showlegend=False,
            legendgroup="IAQZ",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            opacity=0.6,
            connectgaps=True,
            text=[f"{temp:.2f}" for temp in after_current_time1["y"]],
            hovertemplate="Air Quality Index: %{text}<extra></extra>"
        )
    )

    last_point_trace_1 = dict(
        x=before_current_time1["ds"].iloc[-1],
        y=before_current_time1["y"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=after_current_time1["ds"].iloc[0],
        y=after_current_time1["y"].iloc[0],
    )

    fig_weekly.add_trace(
        go.Scatter(
            x=[last_point_trace_1["x"], first_point_trace_2["x"]],
            y=[last_point_trace_1["y"], first_point_trace_2["y"]],
            mode="lines+markers",
            showlegend=False,
            legendgroup="IAQZ",
            yaxis="y2",
            line=dict(color="#FFA500", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            hoverinfo="skip",
        )
    )

    # Add scatter trace for forecasted alerts with data labels (lighter colors)
    fig_weekly.add_trace(
        go.Scatter(
            x=cleaning_forecast_weekly[cleaning_forecast_weekly["cleaning_schedule"] != 0]["ds"],
            y=cleaning_y_values,
            name="Cleaning Alert",
            mode='markers+text',
            marker=dict(
                size=20,
                color='red',
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                ),
                opacity=0.6,
            ),
            text=cleaning_forecast_weekly[cleaning_forecast_weekly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='#000000'
            ),
            showlegend=False,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_forecast_weekly[cleaning_forecast_weekly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    fig_weekly.add_trace(
        go.Scatter(
            x=cleaning_history_weekly[cleaning_history_weekly["cleaning_schedule"] != 0]["ds"],
            y=cleaning_y_values_history,
            name="Cleaning Alert",
            mode='markers+text',
            marker=dict(
                size=20,
                color='red',
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                )
            ),
            text=cleaning_history_weekly[cleaning_history_weekly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='white'
            ),
            showlegend=True,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_history_weekly[cleaning_history_weekly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )

    # Add annotations for Previous Work Week, Current Work Week, and Next Work Week
    annotations = [
        dict(
            x=start_of_previous_week,
            y=0,
            xref="x",
            yref="y",
            text="Previous Workweek",
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
            text="Current Workweek",
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
            text="Next Workweek",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]

    fig_weekly.update_layout(
        template="plotly_dark",
        yaxis_title=" Footfalls ",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
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
                text=f'<span style="text-align:left;font-family:Mulish;"><b>Max</b></span>: {max_value} ({max_date})<br><span style="text-align:left;font-family:Mulish;"><b>Min</b></span>: {min_value} ({min_date})<br> <span style="text-align:left;font-family:Mulish;"><b>Avg</b></span>: {total_average} ',
                font=dict(size=15, family="Mulish"),
                align="left",
                showarrow=False,
                borderwidth=1,
                bordercolor="gray",
            )
        ] ,  # Add the new annotations
    )
    fig_weekly.update_xaxes(showgrid=False)
    fig_weekly.update_yaxes(showgrid=False)
    workweek_plot = json.loads(
        json.dumps(
            fig_weekly,
            cls=plotly.utils.PlotlyJSONEncoder))
    return workweek_plot,so_far_workweek_work_orders,tot_this_workweek_work