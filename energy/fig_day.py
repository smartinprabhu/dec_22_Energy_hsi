
    

import json
from datetime import datetime, time, timedelta

import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz
def fig_day(historical_data,forecasted_data_today,forecasted_bar_data,dz_hour,current_time,current_time_dt641,cost_per_kw):
    total_df = pd.concat([historical_data, forecasted_data_today])
    max_value = total_df["y"].max()
    max_date = total_df.loc[total_df["y"].idxmax(), "ds"].strftime("%d %b %Y, %I %p")
    min_value = total_df["y"].min()
    min_date = total_df.loc[total_df["y"].idxmin(), "ds"].strftime("%d %b %Y, %I %p")
    total_average = total_df["y"].mean()
    dz_hour["ds"] = pd.to_datetime(dz_hour["ds"])
    start_time = current_time - pd.Timedelta(days=2)
    end_time = current_time.replace(hour=23, minute=59, second=59) + pd.Timedelta(hours=24)
    combined_temp_data = dz_hour[(dz_hour["ds"] >= start_time) & (dz_hour["ds"] <= end_time)]
    before_current_time = combined_temp_data[combined_temp_data["ds"] <= current_time]
    after_current_time = combined_temp_data[combined_temp_data["ds"] > current_time]

    fig_hourly = go.Figure()

    fig_hourly.add_trace(
        go.Bar(
            x=historical_data["ds"],
            y=historical_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh <br><b>Cost</b>: %{customdata:.2f}',
            customdata=historical_data["y"]*cost_per_kw,
            name="Actual Consumption",
            marker=dict(color="#2275e0"),
        )
    )

    fig_hourly.add_trace(
        go.Bar(
            x=forecasted_bar_data["ds"],
            y=forecasted_bar_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh <br><b>Cost</b>: %{customdata:.2f}',
            customdata=forecasted_bar_data["y"]*cost_per_kw,
            name="Forecasted Consumption",
            marker=dict(color="#2275e0",opacity=0.4),
        )
    )
    

    fig_hourly.add_trace(
        go.Scatter(
            x=before_current_time["ds"],
            y=before_current_time["y"],
            mode="lines+markers",
            name=" Temperature •C",
            showlegend=True,
            legendgroup="CA",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            text=[f"{y:.2f}" for y in before_current_time["y"]],
            hovertemplate="Temp: %{text}°C<extra></extra>"
        )
    )
    
    fig_hourly.add_trace(
        go.Scatter(
            x=after_current_time["ds"],
            y=after_current_time["y"],
            mode="lines+markers",
            name=" Temperature •C",
            showlegend=False,
            legendgroup="CA",
            yaxis="y2",
            line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
            marker=dict(color="#FFFF00",size=4, line=dict(color="black", width=1)),
            connectgaps=True,
            opacity=0.6,
            text=[f"{y:.2f}" for y in after_current_time["y"]],
            hovertemplate="Temp: %{text}°C<extra></extra>"
        )
    )

    last_point_trace_1 = dict(
        x=before_current_time["ds"].iloc[-1],
        y=before_current_time["y"].iloc[-1],
    )
    first_point_trace_2 = dict(
        x=after_current_time["ds"].iloc[0],
        y=after_current_time["y"].iloc[0],
    )

    fig_hourly.add_trace(
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

    # Update layout of the figure
    fig_hourly.update_layout(
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

    # Remove gridlines
    fig_hourly.update_xaxes(showgrid=False)
    fig_hourly.update_yaxes(showgrid=False)

    day_plot = json.loads(
        json.dumps(
            fig_hourly,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return day_plot
