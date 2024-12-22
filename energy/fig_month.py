import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime, time, timedelta
import pytz
import plotly
def fig_month(tz, historical_data_month,cost_per_kw, forecasted_data_month_end,next_month_end, forecasted_bar_data_monthly, dz_day):
    
    total_day = pd.concat([historical_data_month, forecasted_data_month_end])
    max_value = total_day["y"].max()
    max_date = total_day.loc[total_day["y"].idxmax(),
                            "ds"].strftime("%d %b %Y")
    min_value = total_day["y"].min()
    min_date = total_day.loc[total_day["y"].idxmin(),
                            "ds"].strftime("%d %b %Y")
    total_average = total_day["y"].mean()
    
    # Ensure timestamps are localized or converted appropriately
    dz_day["ds"] = pd.to_datetime(dz_day["ds"])
    if dz_day["ds"].dt.tz is None:
        dz_day["ds"] = dz_day["ds"].dt.tz_localize(tz)
    else:
        dz_day["ds"] = dz_day["ds"].dt.tz_convert(tz)
    start_time = pd.Timestamp.today(tz) - pd.Timedelta(days=59)
    end_time = next_month_end
    combined_temp_data_11 = dz_day[(dz_day["ds"] >= start_time) & (dz_day["ds"] <= end_time)]
    before_current_time1 = combined_temp_data_11[combined_temp_data_11["ds"] <= pd.Timestamp.today(tz)]
    after_current_time1 = combined_temp_data_11[combined_temp_data_11["ds"] > pd.Timestamp.today(tz)]


    # Create hourly plot
    fig_monthly = go.Figure()

    fig_monthly.add_trace(
    go.Bar(
        x=historical_data_month["ds"],
        y=historical_data_month["y"],
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh<br><b>Cost</b>: %{customdata:.2f}',
        customdata=historical_data_month["y"]*cost_per_kw,
        name="Actual Consumption",
        marker=dict(color="#2275e0"),
    )
    )

    fig_monthly.add_trace(
    go.Bar(
        x=forecasted_bar_data_monthly["ds"],
        y=forecasted_bar_data_monthly["y"],
        hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh<br><b>Cost</b>: %{customdata:.2f}',
        customdata=forecasted_bar_data_monthly["y"]* cost_per_kw,
        name="Forecasted Consumption",
        marker=dict(color="#2275e0",opacity=0.4),
    )
    )

    fig_monthly.add_trace(
    go.Scatter(
        x=before_current_time1["ds"],
        y=before_current_time1["y"],
        mode="lines+markers",
        name=" Temperature •C",
        showlegend=True,
        legendgroup="CA",
        yaxis="y2",
        line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
        marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
        connectgaps=True,
        text=[f"{y:.2f}" for y in before_current_time1["y"]],
        hovertemplate="Temp: %{text}°C<extra></extra>"
    )
    )

    fig_monthly.add_trace(
    go.Scatter(
        x=after_current_time1["ds"],
        y=after_current_time1["y"],
        mode="lines+markers",
        name=" Temperature •C",
        showlegend=False,
        legendgroup="CA",
        yaxis="y2",
        line=dict(color="#FF7F50", width=3, dash="solid", shape="spline"),
        marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
        connectgaps=True,
        opacity=0.6,
        text=[f"{y:.2f}" for y in after_current_time1["y"]],
        hovertemplate="Temp: %{text}°C<extra></extra>"
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
        legendgroup="CA",
        yaxis="y2",
        line=dict(color="#FFA500", width=3, dash="solid", shape="spline"),
        marker=dict(color="#FFFF00", size=4, line=dict(color="black", width=1)),
        hoverinfo="skip",
    )
    )

    # Update layout of the figure
    fig_monthly.update_layout(
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
        # range=[10,35]
        

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
    fig_monthly.update_xaxes(showgrid=False)
    fig_monthly.update_yaxes(showgrid=False)
    month_plot = json.loads(
        json.dumps(
            fig_monthly,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return month_plot