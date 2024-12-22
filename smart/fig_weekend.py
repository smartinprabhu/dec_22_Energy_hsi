
"""

This module contains functions for generating figures for weekend,  data visualization.

"""
import json
from datetime import timedelta

import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.graph_objects as go
import pandas as pd

from datetime import datetime, timedelta
import pytz

def weekend_fig( fin,current_weekend_start,forecast_data_bar_weekend,historical_data_weekend,dz_day,next_weekend_start,next_weekend_end,forecast_data_weekend_cal,current_weekend_end,current_time,cost_per_hr,tz):
    fin=fin.set_index('ds').resample('D').sum().reset_index()

    # Define your timezone
    tz = pytz.timezone('Asia/Kolkata')

    # Ensure timestamps are localized or converted appropriately
    dz_day["ds"] = pd.to_datetime(dz_day["ds"])
    if dz_day["ds"].dt.tz is None:
        dz_day["ds"] = dz_day["ds"].dt.tz_localize(tz)
    else:
        dz_day["ds"] = dz_day["ds"].dt.tz_convert(tz)

    current_time = datetime.now(tz)
    current_date = pd.Timestamp.now(tz=tz)

    # Calculate the start and end dates of the previous weekend, current weekend, and next weekend
    current_weekday = current_date.weekday()
    start_of_current_weekend = current_date - timedelta(days=current_weekday + 2)  # Saturday
    end_of_current_weekend = start_of_current_weekend + timedelta(days=1)  # Sunday

    start_of_previous_weekend = start_of_current_weekend - timedelta(days=7)
    end_of_previous_weekend = start_of_previous_weekend + timedelta(days=1)

    start_of_next_weekend = end_of_current_weekend + timedelta(days=6)
    end_of_next_weekend = start_of_next_weekend + timedelta(days=1)

    # Filter the data for weekends only
    def filter_weekend_data(df):
        return df[(df["ds"].dt.weekday == 5) | (df["ds"].dt.weekday == 6)]

    # Historical data for the current weekend and previous weekend
    historical_data_weekend = filter_weekend_data(fin[
        (fin["ds"].dt.date >= start_of_previous_weekend.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ])

    # Determine the end date of the historical data
    end_date_historical_data = historical_data_weekend["ds"].max()

    # Ensure end_date_historical_data is timezone-aware
    if end_date_historical_data.tzinfo is None:
        end_date_historical_data = end_date_historical_data.tz_localize(tz)
    else:
        end_date_historical_data = end_date_historical_data.tz_convert(tz)

    # Filter the forecasted data to include dates from the end of the historical data to the end of the next weekend
    forecasted_bar_data_weekend = filter_weekend_data(fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_weekend)
    ])

    # Ensure current_time is timezone-aware
    current_time = pd.Timestamp.now(tz)

    # Now you can use it in your filter
    forecasted_data_currentweekend_end = filter_weekend_data(fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_current_weekend)
    ])
    before_current_time1 = filter_weekend_data(dz_day[
        (dz_day["ds"].dt.date >= start_of_previous_weekend.date()) &
        (dz_day["ds"].dt.date <= current_time.date())
    ])
    after_current_time1 = filter_weekend_data(dz_day[
        (dz_day["ds"] > end_date_historical_data) &
        (dz_day["ds"] <= end_of_next_weekend)
    ])
    total_day = pd.concat([historical_data_weekend, forecasted_data_currentweekend_end])
    max_value = int(total_day["y"].max())
    max_date = total_day.loc[total_day["y"].idxmax(), "ds"].strftime("%d %b %y")
    min_value = int(total_day["y"].min())
    min_date = total_day.loc[total_day["y"].idxmin(), "ds"].strftime("%d %b %y")
    total_average = round(total_day["y"].mean())

    cleaning_forecast_weekend = filter_weekend_data(fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_weekend)
    ])
    cleaning_history_weekend = filter_weekend_data(fin[
        (fin["ds"].dt.date >= start_of_previous_weekend.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ])

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
    current_weekend_data = fin[(fin['ds'].dt.date >= start_of_current_weekend.date()) & (fin['ds'].dt.date <= end_of_current_weekend.date())]
    current_weekend_data_upto_current_day = current_weekend_data[current_weekend_data['ds'].dt.date <= current_time.date()]
    so_far_weekend_work_orders=int(current_weekend_data_upto_current_day['cleaning_schedule'].sum())
    tot_this_weekend_work=int(current_weekend_data['cleaning_schedule'].sum())

    # Create hourly plot
    fig_weekend = go.Figure()
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values_history = cleaning_history_weekend[cleaning_history_weekend["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_weekend[historical_data_weekend["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values = cleaning_forecast_weekend[cleaning_forecast_weekend["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_weekend[historical_data_weekend["ds"] == row["ds"]]["y"].values[0] + adjustment
        if row["ds"] in historical_data_weekend["ds"].values else forecasted_bar_data_weekend[forecasted_bar_data_weekend["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )

    fig_weekend.add_trace(
        go.Bar(
            x=historical_data_weekend["ds"],
            y=historical_data_weekend["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y} <br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data_weekend["y"] * cost_per_hr,
            name=" Actual Footfalls",
            marker=dict(color="#2275e0"),
        )
    )

    fig_weekend.add_trace(
        go.Bar(
            x=forecasted_bar_data_weekend["ds"],
            y=forecasted_bar_data_weekend["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y}<br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecasted_bar_data_weekend["y"] * cost_per_hr,
            showlegend=False,
            name="Forecasted Footfalls",
            marker=dict(color="#2275e0", opacity=0.4),
        )
    )

    fig_weekend.add_trace(
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

    fig_weekend.add_trace(
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

    fig_weekend.add_trace(
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
    fig_weekend.add_trace(
        go.Scatter(
            x=cleaning_forecast_weekend[cleaning_forecast_weekend["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_forecast_weekend[cleaning_forecast_weekend["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='#000000'
            ),
            showlegend=False,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_forecast_weekend[cleaning_forecast_weekend["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    fig_weekend.add_trace(
        go.Scatter(
            x=cleaning_history_weekend[cleaning_history_weekend["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_history_weekend[cleaning_history_weekend["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='white'
            ),
            showlegend=True,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_history_weekend[cleaning_history_weekend["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )

    # Add annotations for Previous Weekend, Current Weekend, and Next Weekend
    annotations = [
        dict(
            x=start_of_previous_weekend,
            y=0,
            xref="x",
            yref="y",
            text="Previous Weekend",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_current_weekend,
            y=0,
            xref="x",
            yref="y",
            text="Current Weekend",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_next_weekend,
            y=0,
            xref="x",
            yref="y",
            text="Next Weekend",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]

    fig_weekend.update_layout(
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
    fig_weekend.update_xaxes(showgrid=False)
    fig_weekend.update_yaxes(showgrid=False)

    weekend_plot = json.loads(
        json.dumps(
            fig_weekend,
            cls=plotly.utils.PlotlyJSONEncoder))

    
    return weekend_plot,so_far_weekend_work_orders,tot_this_weekend_work