"""
This module contains functions for generating figures for hourly, daily and weekly data visualization.
"""
# Air Quality Index
import datetime
import json
from datetime import datetime, timedelta
from datetime import timedelta
import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz


def fig_month(tz,fin,historical_data_month,forecasted_bar_data_monthly,dz_day,current_time_dt64,next_month_end,current_time,cost_per_hr):
    
    fin=fin.set_index('ds').resample('D').sum().reset_index()

    # Ensure timestamps are localized or converted appropriately
    dz_day["ds"] = pd.to_datetime(dz_day["ds"])
    if dz_day["ds"].dt.tz is None:
        dz_day["ds"] = dz_day["ds"].dt.tz_localize(tz)
    else:
        dz_day["ds"] = dz_day["ds"].dt.tz_convert(tz)
        


    current_time = datetime.now(tz)
    current_date = pd.Timestamp.now(tz=tz)

    # Get the first day of the current month
    first_day_current_month = current_date.replace(day=1)

    # Get the last day of the previous month
    last_day_previous_month = first_day_current_month - timedelta(days=1)

    # Get the first day of the previous month
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Historical data for the current month and last month
    historical_data_month = fin[
        (fin["ds"].dt.date >= first_day_previous_month.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ]

    # Determine the end date of the historical data
    end_date_historical_data = historical_data_month["ds"].max()

    # Ensure end_date_historical_data is timezone-aware
    if end_date_historical_data.tzinfo is None:
        end_date_historical_data = end_date_historical_data.tz_localize(tz)
    else:
        end_date_historical_data = end_date_historical_data.tz_convert(tz)

    # Calculate the first day of the next month
    first_day_next_month = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)

    # Calculate the last day of the next month
    last_day_next_month = (first_day_next_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Filter the forecasted data to include dates from the end of the historical data to the last day of the next month
    forecasted_bar_data_monthly = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= last_day_next_month)
    ]

    # Ensure current_time is timezone-aware
    current_time = pd.Timestamp.now(tz)

    # Find the last day of the current month
    last_day_current_month = current_date + pd.offsets.MonthEnd(0)

    # Now you can use it in your filter
    forecasted_data_curentmonth_end = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= last_day_current_month)
    ]
    before_current_time1= dz_day[
        (dz_day["ds"].dt.date >= first_day_previous_month.date()) &
        (dz_day["ds"].dt.date <= current_time.date())
    ]
    after_current_time1=dz_day[
        (dz_day["ds"] > end_date_historical_data) &
        (dz_day["ds"] <= last_day_next_month)
    ]
    total_day = pd.concat([historical_data_month, forecasted_data_curentmonth_end])
    max_value = int(total_day["y"].max())
    max_date = total_day.loc[total_day["y"].idxmax(), "ds"].strftime("%d %b %y")
    min_value = int(total_day["y"].min())
    min_date = total_day.loc[total_day["y"].idxmin(), "ds"].strftime("%d %b %y")
    total_average = round(total_day["y"].mean())


    cleaning_forecast_monthly = fin[
    (fin["ds"] > end_date_historical_data) &
    (fin["ds"] <= last_day_next_month)
]
    cleaning_history_monthly =fin[
    (fin["ds"].dt.date >= first_day_previous_month.date()) &
    (fin["ds"].dt.date <= current_time.date())
]
    # Create hourly plot
    fig_monthly = go.Figure()
    adjustment = 15 # Change this value to adjust the position
    cleaning_y_values_history = cleaning_history_monthly[cleaning_history_monthly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_month[historical_data_month["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values = cleaning_forecast_monthly[cleaning_forecast_monthly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_month[historical_data_month["ds"] == row["ds"]]["y"].values[0] + adjustment
        if row["ds"] in historical_data_month["ds"].values else forecasted_bar_data_monthly[forecasted_bar_data_monthly["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )
    start_of_this_month = current_time_dt64.replace(day=1)
    end_of_this_month = (start_of_this_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    this_month_data = fin[(fin['ds'].dt.date >= start_of_this_month.date()) & (fin['ds'].dt.date <= end_of_this_month.date())]
    this_month_data_upto_current_day = this_month_data[this_month_data['ds'].dt.date <= current_time.date()]

    tot_this_month_work=int(this_month_data['cleaning_schedule'].sum())
    so_far_month_work_orders=int(this_month_data_upto_current_day['cleaning_schedule'].sum())
    fig_monthly.add_trace(
    go.Bar(
        x=historical_data_month["ds"],
        y=historical_data_month["y"],
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y} <br><b>Cost</b>: %{customdata:.2f}',
        customdata=historical_data_month["y"]*cost_per_hr,
        name=" Actual Footfalls",
        marker=dict(color="#2275e0"),
    )
    )

    fig_monthly.add_trace(
    go.Bar(
        x=forecasted_bar_data_monthly["ds"],
        y=forecasted_bar_data_monthly["y"],
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y}<br><b>Cost</b>: %{customdata:.2f}',
        customdata=forecasted_bar_data_monthly["y"]* cost_per_hr,
        showlegend=False,
        name="Forecasted Footfalls",
        marker=dict(color="#2275e0",opacity=0.4),
    )
    )

    fig_monthly.add_trace(
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

    fig_monthly.add_trace(
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

    fig_monthly.add_trace(
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
    fig_monthly.add_trace(
        go.Scatter(
            x=cleaning_forecast_monthly[cleaning_forecast_monthly["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_forecast_monthly[cleaning_forecast_monthly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='#000000'
            ),
            showlegend=False,
            legendgroup="CA", 
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_forecast_monthly[cleaning_forecast_monthly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    fig_monthly.add_trace(
        go.Scatter(
            x=cleaning_history_monthly[cleaning_history_monthly["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_history_monthly[cleaning_history_monthly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='white'
            ),
            showlegend=True,
            legendgroup="CA", 
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_history_monthly[cleaning_history_monthly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    tz = pytz.timezone('Asia/Kolkata')

    # Calculate the start and end dates of the previous month, current month, and next month
    current_time = pd.Timestamp.now().normalize().tz_localize(tz)
    start_of_current_month = current_time.replace(day=1)
    end_of_current_month = (start_of_current_month + pd.DateOffset(months=1)) - pd.Timedelta(days=1)

    start_of_previous_month = (start_of_current_month - pd.DateOffset(months=1)).replace(day=1)
    start_of_next_month = end_of_current_month + pd.Timedelta(days=1)
    annotations = [
        dict(
            x=start_of_previous_month,
            y=0,
            xref="x",
            yref="y",
            text="Previous Month",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_current_month,
            y=0,
            xref="x",
            yref="y",
            text="Current Month",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_next_month,
            y=0,
            xref="x",
            yref="y",
            text="Next Month",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]
    fig_monthly.update_layout(
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
    ],
    )
    fig_monthly.update_xaxes(showgrid=False)
    fig_monthly.update_yaxes(showgrid=False)
    month_plot = json.loads(
    json.dumps(
        fig_monthly,
        cls=plotly.utils.PlotlyJSONEncoder))
    return month_plot,tot_this_month_work,so_far_month_work_orders