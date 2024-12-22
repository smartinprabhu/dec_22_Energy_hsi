
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime, time, timedelta
import pytz
import plotly





def fig_yearly(tz,after_current_time,before_current_time1,forecast_data_until_end_of_year_cal,historical_data_monthly, forecast_data_monthly,cost_per_kw):
    # Assuming historical_data_monthly and forecast_data_monthly are already defined
    min_date = historical_data_monthly["ds"].min()
    max_date = forecast_data_monthly["ds"].max()

    if before_current_time1["ds"].dt.tz is None:
        before_current_time1["ds"] = before_current_time1["ds"].dt.tz_localize('Asia/Kolkata')
    else:
        before_current_time1["ds"] = before_current_time1["ds"].dt.tz_convert('Asia/Kolkata')

    if after_current_time["ds"].dt.tz is None:
        after_current_time["ds"] = after_current_time["ds"].dt.tz_localize('Asia/Kolkata')
    else:
        after_current_time["ds"] = after_current_time["ds"].dt.tz_convert('Asia/Kolkata')

    # Convert min_date and max_date to Asia/Kolkata timezone if they are timezone-naive
    if min_date.tzinfo is None:
        min_date = min_date.tz_localize('Asia/Kolkata')
    else:
        min_date = min_date.tz_convert('Asia/Kolkata')

    if max_date.tzinfo is None:
        max_date = max_date.tz_localize('Asia/Kolkata')
    else:
        max_date = max_date.tz_convert('Asia/Kolkata')

    # Now you can filter the data
    filtered_before_current_time1 = before_current_time1[
        (before_current_time1["ds"] >= min_date) & (before_current_time1["ds"] <= max_date)
    ]
    filtered_after_current_time = after_current_time[
        (after_current_time["ds"] >= min_date) & (after_current_time["ds"] <= max_date)
    ]


    # Create hourly plot
    fig_year = go.Figure()

    fig_year.add_trace(
        go.Bar(
            x=historical_data_monthly["ds"],
            y=historical_data_monthly["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x| %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh<br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data_monthly["y"] * cost_per_kw,
            name="Actual Consumption",
            marker=dict(color="#2275e0"),
        )
    )

    fig_year.add_trace(
        go.Bar(
            x=forecast_data_monthly["ds"],
            y=forecast_data_monthly["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x| %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh<br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecast_data_monthly["y"] * cost_per_kw,
            name="Forecasted Consumption",
            marker=dict(color="#2275e0",opacity=0.4),
        )
    )

    fig_year.add_trace(
        go.Scatter(
            x=filtered_before_current_time1["ds"],
            y=filtered_before_current_time1["y"],
            mode="lines+markers",
            name="Temperature •C",
            showlegend=True,
            legendgroup="CA",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            text=[f"{y:.2f}" for y in filtered_before_current_time1["y"]],
            hovertemplate="Temp: %{text}°C<extra></extra>"
        )
    )

    fig_year.add_trace(
        go.Scatter(
            x=filtered_after_current_time["ds"],
            y=filtered_after_current_time["y"],
            mode="lines+markers",
            name="Temperature •C",
            showlegend=False,
            legendgroup="CA",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            opacity=0.6,
            text=[f"{y:.2f}" for y in filtered_after_current_time["y"]],
            hovertemplate="Temp: %{text}°C<extra></extra>"
        )
    )

    last_point_trace_1 = dict(
        x=filtered_before_current_time1["ds"].iloc[-1],
        y=filtered_before_current_time1["y"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=filtered_after_current_time["ds"].iloc[0],
        y=filtered_after_current_time["y"].iloc[0],
    )

    fig_year.add_trace(
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
        )
    )

    total_day = pd.merge(historical_data_monthly, forecast_data_until_end_of_year_cal, how='outer')
    max_value = total_day["y"].max()
    min_value = total_day["y"].min()
    min_date = total_day.loc[total_day["y"].idxmin(), "ds"].strftime(" %b %Y")
    max_date = total_day.loc[total_day["y"].idxmax(), "ds"].strftime(" %b %Y")
    total_average = total_day["y"].mean()

    # Update layout of the figure
    fig_year.update_layout(
        template="plotly_dark",
        yaxis_title="Consumption (kWh)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        yaxis2=dict(
            title="Temperature (°C)",
            titlefont_color="orange",
            tickfont_color="orange",
            overlaying="y",
            side="right",
            anchor="x",
            position=0.05,
            range=[10,35]
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
                y=1.08,
                xanchor="right",
                yanchor="top",
                text=f'<span style="text-align:left;font-family:Mulish;"><b>Max</b></span>: {max_value:.2f} kWh ({max_date})<br><span style="text-align:left;font-family:Mulish;"><b>Min</b></span>: {min_value:.2f} kWh ({min_date})<br><span style="text-align:left;font-family:Mulish;"><b>Avg</b></span>: {total_average:.2f} kWh',
                font=dict(size=15, family="Mulish"),
                align="left",
                showarrow=False,
                borderwidth=1,
                bordercolor="gray",
            )
        ],
    )
    fig_year.update_xaxes(showgrid=False)
    fig_year.update_yaxes(showgrid=False)
    # Update x-axis to show only month and year in hover mode
    fig_year.update_xaxes(tickformat="%b %Y")
    year_plot = json.loads(
    json.dumps(
        fig_year,
        cls=plotly.utils.PlotlyJSONEncoder)) 


    return year_plot
