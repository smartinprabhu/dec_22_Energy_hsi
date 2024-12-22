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
from datetime import datetime
from dateutil.relativedelta import relativedelta

def fig_year(fin,start_of_next_month,dz_day,end_of_next_year,current_time,end_of_current_month,forecast_data_monthly,historical_data_monthly,before_current_time1,forecast_data_until_end_of_year_cal,after_current_time,cost_per_hr):

    # Define your timezone
    tz = pytz.timezone('Asia/Kolkata')
    
    # Ensure timestamps are localized or converted appropriately
    dz_day["ds"] = pd.to_datetime(dz_day["ds"])
    if dz_day["ds"].dt.tz is None:
        dz_day["ds"] = dz_day["ds"].dt.tz_localize(tz)
    else:
        dz_day["ds"] = dz_day["ds"].dt.tz_convert(tz)

    dz_month=dz_day[['ds','y']].set_index('ds').resample('M').mean().reset_index()
    
    
    fin=fin.set_index('ds').resample('M').sum().reset_index()
    current_time = datetime.now(tz)
    current_date = pd.Timestamp.now(tz=tz)

    # Calculate the start and end dates of the previous year, current year, and next year
    start_of_current_year = current_date.replace(month=1, day=1)
    end_of_current_year = start_of_current_year + pd.DateOffset(years=1) - pd.Timedelta(days=1)

    start_of_previous_year = start_of_current_year - pd.DateOffset(years=1)
    end_of_previous_year = start_of_current_year - pd.Timedelta(days=1)

    start_of_next_year = end_of_current_year + pd.Timedelta(days=1)
    end_of_next_year = start_of_next_year + pd.DateOffset(years=1) - pd.Timedelta(days=1)

    # Historical data for the current year and previous year
    historical_data_year = fin[
        (fin["ds"].dt.date >= start_of_previous_year.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ]

    # Determine the end date of the historical data
    end_date_historical_data = historical_data_year["ds"].max()

    # Ensure end_date_historical_data is timezone-aware
    if end_date_historical_data.tzinfo is None:
        end_date_historical_data = end_date_historical_data.tz_localize(tz)
    else:
        end_date_historical_data = end_date_historical_data.tz_convert(tz)

    # Filter the forecasted data to include dates from the end of the historical data to the end of the next year
    forecasted_bar_data_yearly = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_year)
    ]

    # Ensure current_time is timezone-aware
    current_time = pd.Timestamp.now(tz)

    # Now you can use it in your filter
    forecasted_data_currentyear_end = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_current_year)
    ]
    before_current_time1 = dz_month[
        (dz_month["ds"].dt.date >= start_of_previous_year.date()) &
        (dz_month["ds"].dt.date <= current_time.date())
    ]
    after_current_time1 = dz_month[
        (dz_month["ds"] > end_date_historical_data) &
        (dz_month["ds"] <= end_of_next_year)
    ]
    total_day = pd.concat([historical_data_year, forecasted_data_currentyear_end])
    max_value = int(total_day["y"].max())
    max_date = total_day.loc[total_day["y"].idxmax(), "ds"].strftime("%d %b %y")
    min_value = int(total_day["y"].min())
    min_date = total_day.loc[total_day["y"].idxmin(), "ds"].strftime("%d %b %y")
    total_average = round(total_day["y"].mean())

    cleaning_forecast_yearly = fin[
        (fin["ds"] > end_date_historical_data) &
        (fin["ds"] <= end_of_next_year)
    ]
    cleaning_history_yearly = fin[
        (fin["ds"].dt.date >= start_of_previous_year.date()) &
        (fin["ds"].dt.date <= current_time.date())
    ]
    def get_year_dates(current_time):
        # Calculate the start of the current year
        start_of_current_year = datetime(current_time.year, 1, 1)
        # Calculate the end of the current year
        end_of_current_year = datetime(current_time.year, 12, 31)
        # Calculate the start of the last year
        start_of_last_year = datetime(current_time.year - 1, 1, 1)
        # Calculate the end of the last year
        end_of_last_year = datetime(current_time.year - 1, 12, 31)
        return start_of_last_year, end_of_last_year, start_of_current_year, end_of_current_year

    start_of_last_year, end_of_last_year, start_of_current_year, end_of_current_year = get_year_dates(current_time)

    current_year_data = fin[(fin['ds'].dt.date >= start_of_current_year.date()) & (fin['ds'].dt.date <= end_of_current_year.date())]
    current_year_data_upto_current_day = current_year_data[current_year_data['ds'].dt.date <= current_time.date()]
    tot_this_year_work=int(current_year_data['cleaning_schedule'].sum())
    so_far_year_work_orders=int(current_year_data_upto_current_day['cleaning_schedule'].sum())

    # Create yearly plot
    fig_yearly = go.Figure()
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values_history = cleaning_history_yearly[cleaning_history_yearly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_year[historical_data_year["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )
    adjustment = 15  # Change this value to adjust the position
    cleaning_y_values = cleaning_forecast_yearly[cleaning_forecast_yearly["cleaning_schedule"] != 0].apply(
        lambda row: historical_data_year[historical_data_year["ds"] == row["ds"]]["y"].values[0] + adjustment
        if row["ds"] in historical_data_year["ds"].values else forecasted_bar_data_yearly[forecasted_bar_data_yearly["ds"] == row["ds"]]["y"].values[0] + adjustment,
        axis=1
    )

    fig_yearly.add_trace(
        go.Bar(
            x=historical_data_year["ds"],
            y=historical_data_year["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y} <br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data_year["y"] * cost_per_hr,
            name=" Actual Footfalls",
            marker=dict(color="#2275e0"),
        )
    )

    fig_yearly.add_trace(
        go.Bar(
            x=forecasted_bar_data_yearly["ds"],
            y=forecasted_bar_data_yearly["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %y}<br><b>Footfalls </b>: %{y}<br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecasted_bar_data_yearly["y"] * cost_per_hr,
            showlegend=False,
            name="Forecasted Footfalls",
            marker=dict(color="#2275e0", opacity=0.4),
        )
    )

    fig_yearly.add_trace(
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

    fig_yearly.add_trace(
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

    fig_yearly.add_trace(
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
    fig_yearly.add_trace(
        go.Scatter(
            x=cleaning_forecast_yearly[cleaning_forecast_yearly["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_forecast_yearly[cleaning_forecast_yearly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='#000000'
            ),
            showlegend=False,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_forecast_yearly[cleaning_forecast_yearly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )
    fig_yearly.add_trace(
        go.Scatter(
            x=cleaning_history_yearly[cleaning_history_yearly["cleaning_schedule"] != 0]["ds"],
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
            text=cleaning_history_yearly[cleaning_history_yearly["cleaning_schedule"] != 0]["cleaning_schedule"],
            textposition='middle center',
            textfont=dict(
                color='white'
            ),
            showlegend=True,
            legendgroup="CA",
            hovertemplate='<b>Cleaning Alert:</b> %{text}<extra></extra>',
            hoverinfo='skip',
            customdata=cleaning_history_yearly[cleaning_history_yearly["cleaning_schedule"] != 0]["cleaning_schedule"]
        )
    )

    # Add annotations for Previous Year, Current Year, and Next Year
    annotations = [
        dict(
            x=start_of_previous_year,
            y=0,
            xref="x",
            yref="y",
            text="Previous Year",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_current_year,
            y=0,
            xref="x",
            yref="y",
            text="Current Year",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
        dict(
            x=start_of_next_year,
            y=0,
            xref="x",
            yref="y",
            text="Next Year",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0, 0, 0, 0.5)",
        ),
    ]

    fig_yearly.update_layout(
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
    fig_yearly.update_xaxes(showgrid=False)
    fig_yearly.update_yaxes(showgrid=False)
    year_plot = json.loads(
        json.dumps(
            fig_yearly,
            cls=plotly.utils.PlotlyJSONEncoder))
    return year_plot,so_far_year_work_orders,tot_this_year_work