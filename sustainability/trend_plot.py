import pandas as pd
import plotly.graph_objects as go
import json
import plotly
from datetime import datetime, timedelta
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
def trend_plotting(DG_hour,EB_hour,solar_hour,tz,current_datetime):
    
    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)


    # Extract hour from datetime
    EB_hour['hour'] = EB_hour['ds'].dt.hour



    # Define a function to adjust consumption based on the time of day
    def adjust_consumption(hour, consumption):
        if 6 <= hour < 10:  # Morning peak
            return consumption * 1.1
        elif 10 <= hour < 16:  # Daytime
            return consumption * 1.05
        elif 16 <= hour < 20:  # Evening peak
            return consumption * 1.1
        else:  # Nighttime
            return consumption * 0.95

    # Apply the adjustment function
    # EB_hour['y'] = EB_hour.apply(lambda row: adjust_consumption(row['hour'], row['y']), axis=1)

    # Drop the hour column as it's no longer needed
    EB_hour.drop(columns=['hour'], inplace=True)


    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    current_time_dt641=current_time_dt64+ pd.Timedelta(hours=1)
    # Get the date for the previous day
    previous_day = current_time_dt64.date() - timedelta(days=1)

    # Create the start and end timestamps for the previous day
    start_time = pd.Timestamp(previous_day, tz=tz)


    historical_data = EB_hour[(EB_hour["ds"] >= start_time) & (EB_hour["ds"] <= current_time_dt641)]
    historical_data1 = DG_hour[(DG_hour["ds"] >= start_time) & (DG_hour["ds"] <= current_time_dt641)]
    historical_data2 = solar_hour[(solar_hour["ds"] >= start_time) & (solar_hour["ds"] <= current_time_dt641)]





    # Get the end of the next 24 hours
    next_24_hours_end = current_datetime + timedelta(days=1)
    next_24_hours_end = pd.Timestamp(next_24_hours_end.replace(hour=23, minute=59, second=59, microsecond=999999)).tz_convert(tz)

    forecasted_bar_data = EB_hour[
        (EB_hour["ds"] > current_time_dt641) & (EB_hour["ds"] <= next_24_hours_end)
    ]

    forecasted_bar_data1 = DG_hour[
        (DG_hour["ds"] > current_time_dt641) & (DG_hour["ds"] <= next_24_hours_end)
    ]

    forecasted_bar_data2 = solar_hour[
        (solar_hour["ds"] > current_time_dt641) & (solar_hour["ds"] <= next_24_hours_end)
    ]
    fig_hourly = go.Figure()
    cost_per_kw = 6.09

    # Add historical EB
    fig_hourly.add_trace(
        go.Bar(
            x=historical_data["ds"],
            y=historical_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh  ',

            name="EB ",
            marker=dict(color="#1f77b4"),  
            showlegend=True,
            legendgroup="EB",
            offsetgroup=0,  # Group all EB bars together
        )
    )

    # Add forecasted EB
    fig_hourly.add_trace(
        go.Bar(
            x=forecasted_bar_data["ds"],
            y=forecasted_bar_data["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="EB (Forecasted)",
            marker=dict(color="#1f77b4", opacity=0.4),
            showlegend=False,
            legendgroup="EB",
            offsetgroup=0,  # Same group as historical EB
        )
    )

    # Add historical DG
    fig_hourly.add_trace(
        go.Bar(
            x=historical_data1["ds"],
            y=historical_data1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG ",
            marker=dict(color="#ff7f0e"),   
            showlegend=True,
            legendgroup="DG",
            offsetgroup=1,  # Group all DG bars together
        )
    )

    # Add forecasted DG
    fig_hourly.add_trace(
        go.Bar(
            x=forecasted_bar_data1["ds"],
            y=forecasted_bar_data1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG (Forecasted)",
            showlegend=False,
            legendgroup="DG",
            marker=dict(color="#ff7f0e", opacity=0.4),
            offsetgroup=1,  # Same group as historical DG
        )
    )

    # Add historical Solar
    fig_hourly.add_trace(
        go.Bar(
            x=historical_data2["ds"],
            y=historical_data2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar ",
            showlegend=True,
            legendgroup="SA",
            marker=dict(color="#2ca02c"),
            offsetgroup=2,  # Group all Solar bars together
        )
    )

    # Add forecasted Solar
    fig_hourly.add_trace(
        go.Bar(
            x=forecasted_bar_data2["ds"],
            y=forecasted_bar_data2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}, %{x|%I %p}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar (Forecasted)",
            showlegend=False,
            legendgroup="SA",
            marker=dict(color="#2ca02c", opacity=0.4),
            offsetgroup=2,  # Same group as historical Solar
        )
    )

        

    # Get the current date
    current_date = pd.Timestamp.now(tz).normalize()

    # Define the range (first hour and last hour of the current day)
    range_start = current_date  # First hour of the current day
    range_end = current_date + pd.Timedelta(hours=23, minutes=59)  # Last hour of the current day

    fig_hourly.update_layout(
        title='Energy Trend By Sources',
        template="plotly_dark",
        yaxis_title="Consumption (kWh)",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.65,
            xanchor="center",
            x=0.5,
            font=dict(size=10),  # Adjust legend font size for mobile
        ),
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
            font=dict(color='white', size=10),  # Adjust hover font size for mobile
            font_family='Mulish'
        ),
        bargap=0.1,  # Adjust space between groups
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date",
            range=[range_start, range_end]  # Dynamic range based on the end of the first trace
        ),
        margin=dict(l=10, r=10, t=50, b=40), 
        
        autosize=False,  # Enable autosizing
        width=None,
        height=None,
    )

    # Set responsive attributes
    fig_hourly.update_layout(
        autosize=False,
        # responsive=True,
        width=None,  # Auto-adjust width
        height=None,  # Auto-adjust height
        margin=dict(
            l=10, r=10, t=70, b=40  # Smaller margins for better mobile view
        ),
    )

    # Adjust font sizes and other attributes for better responsiveness
    fig_hourly.update_layout(
        font=dict(
            size=12,  # General font size
            color="white"
        ),
        legend=dict(
            font=dict(size=10),  # Smaller legend font for mobile
            itemclick="toggleothers"  # Improve interaction on mobile
        )
    )

    # Optional: Adjust hover and legend for specific devices
    fig_hourly.update_traces(
        hoverlabel=dict(
            font_size=10  # Smaller hover font for better mobile display
        ),
        selector=dict(type='bar')
    )

    trend_plot = json.loads(
        json.dumps(
            fig_hourly,
            cls=plotly.utils.PlotlyJSONEncoder)) 
    return trend_plot
def trend_plotting1(DG_hour,EB_hour,solar_hour,tz,current_datetime):
    current_time = datetime.now(tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)
    EB_hour=EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour=DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour=solar_hour.set_index('ds').resample('D').sum().reset_index()

    historical_data_daily = EB_hour[
        (EB_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (EB_hour["ds"].dt.date <= current_time.date())
    ]
    next_7_days_end = current_time + timedelta(days=7)
    next_7_days_end = pd.Timestamp(next_7_days_end.replace(hour=23, minute=59, second=59, microsecond=999999)).tz_convert(tz)
    forecasted_bar_data_daily = EB_hour[
        (EB_hour["ds"] > current_time_dt64) & (EB_hour["ds"] <= next_7_days_end)
    ]

        
    end_of_week = current_time + timedelta(days=(6 - current_time.weekday()))


    next_7_days_end = end_of_week + timedelta(days=7)

    forecasted_bar_data_daily = EB_hour[
        (EB_hour["ds"] > current_time_dt64) & (EB_hour["ds"] <= next_7_days_end)
    ]
    historical_data_daily2 = solar_hour[
        (solar_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (solar_hour["ds"].dt.date <= current_time.date())
    ]

    forecasted_bar_data_daily2 = solar_hour[
        (solar_hour["ds"] > current_time_dt64) & (solar_hour["ds"] <= next_7_days_end)
    ]


    forecasted_bar_data_daily2 = solar_hour[
        (solar_hour["ds"] > current_time_dt64) & (solar_hour["ds"] <= next_7_days_end)
    ]
    historical_data_daily1 = DG_hour[
        (DG_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=13)).date())
        & (DG_hour["ds"].dt.date <= current_time.date())
    ]

    forecasted_bar_data_daily1 = DG_hour[
        (DG_hour["ds"] > current_time_dt64) & (DG_hour["ds"] <= next_7_days_end)
    ]



    forecasted_bar_data_daily1 = DG_hour[
        (DG_hour["ds"] > current_time_dt64) & (DG_hour["ds"] <= next_7_days_end)
    ]

    # Add historical EB
    fig_daily = go.Figure()
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily["ds"],
            y=historical_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  ',

            name="EB",
            marker=dict(color="#1f77b4"),  
            showlegend=True,
            legendgroup="EB",
            offsetgroup=0,  # Group all EB bars together
        )
    )
        # Add forecasted EB
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily["ds"],
            y=forecasted_bar_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="EB",
            marker=dict(color="#1f77b4", opacity=0.4),
            showlegend=False,
            legendgroup="EB",
            offsetgroup=0,  # Same group as historical EB
        )
    )
    # Add historical DG
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily1["ds"],
            y=historical_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            marker=dict(color="#ff7f0e"),   
            showlegend=True,
            legendgroup="DG",
            offsetgroup=1,  # Group all DG bars together
        )
    )

    # Add forecasted DG
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily1["ds"],
            y=forecasted_bar_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            showlegend=False,
            legendgroup="DG",
            marker=dict(color="#ff7f0e", opacity=0.4),
            offsetgroup=1,  # Same group as historical DG
        )
    )

    # Add historical Solar
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily2["ds"],
            y=historical_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=True,
            legendgroup="SA",
            marker=dict(color="#2ca02c"),
            offsetgroup=2,  # Group all Solar bars together
        )
    )

    # Add forecasted Solar
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily2["ds"],
            y=forecasted_bar_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=False,
            legendgroup="SA",
            marker=dict(color="#2ca02c", opacity=0.4),
            offsetgroup=2,  # Same group as historical Solar
        )
    )
    


    current_date = pd.Timestamp.now()

    # Define the range (first day and last day of the current week)
    range_start = current_date - pd.Timedelta(days=current_date.weekday())  # First day of the current week (Monday)
    range_end = range_start + pd.Timedelta(days=6)  # Last day of the current week (Sunday)



    fig_daily.update_layout(
        title='Energy Trend By Sources',
        template="plotly_dark",
        yaxis_title="",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.65,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),

        hovermode="x unified",
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', size=10),
            font_family='Mulish'
        ),
        bargap=0.05,
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date",
            range=[range_start.date(), range_end.date()],  # Ensure this covers the full week
        tickmode='linear',
        tick0=range_start.date(),
        dtick=86400000.0 
        ),


        autosize=False,
        width=None,
        height=None,
    )


    # Adjust font sizes and other attributes for better responsiveness
    fig_daily.update_layout(
        font=dict(
            size=12,  # General font size
            color="white"
        ),
        legend=dict(
            font=dict(size=10),  # Smaller legend font for mobile
            itemclick="toggleothers"  # Improve interaction on mobile
        )
    )

    # Optional: Adjust hover and legend for specific devices
    fig_daily.update_traces(
        
        hoverlabel=dict(
            font_size=10  # Smaller hover font for better mobile display
        ),
        selector=dict(type='bar')
    )
    fig_daily.update_layout(
    barmode='group',  # Use 'group' to place bars side by side, or 'overlay' for stacking
    )

    trend_plot1 = json.loads(
        json.dumps(
            fig_daily,
            cls=plotly.utils.PlotlyJSONEncoder))     
    return trend_plot1
def trend_plotting2(DG_hour,EB_hour,solar_hour,tz):
    current_time = datetime.now(tz)
    current_date = pd.Timestamp.now(tz=tz)
    current_time_dt64 = pd.Timestamp(current_time).tz_convert(tz)
    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)
    EB_hour=EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour=DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour=solar_hour.set_index('ds').resample('D').sum().reset_index()

    historical_data_daily = EB_hour[
        (EB_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=59)).date())
        & (EB_hour["ds"].dt.date <= current_time.date())
    ]
    historical_data_daily1 = DG_hour[
        (DG_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=59)).date())
        & (DG_hour["ds"].dt.date <= current_time.date())
    ]
    historical_data_daily2 = solar_hour[
        (solar_hour["ds"].dt.date >= (current_time - pd.Timedelta(days=59)).date())
        & (solar_hour["ds"].dt.date <= current_time.date())
    ]

    # Get the end of the current month
    # current_month_end = pd.Timestamp(current_date.year, current_date.month + 1, 1) - pd.Timedelta(days=1)
    # current_month_end = current_month_end.tz_localize(tz)
    # Get the end of the next month
    current_date = pd.Timestamp.now()  # Example current date
    next_month = (current_date.month + 1) % 12 + 1
    next_year = current_date.year + (current_date.month + 1) // 12 
    next_month_end = pd.Timestamp(next_year, next_month, 1) - pd.Timedelta(days=1)
    next_month_end = next_month_end.tz_localize(tz)
    # Filter the dataframe
    forecasted_bar_data_daily = EB_hour[
        (EB_hour["ds"] > current_time_dt64) & (EB_hour["ds"] <= next_month_end)
    ]
    forecasted_bar_data_daily1 = DG_hour[
        (DG_hour["ds"] > current_time_dt64) & (DG_hour["ds"] <= next_month_end)
    ]
    forecasted_bar_data_daily2 = solar_hour[
        (solar_hour["ds"] > current_time_dt64) & (solar_hour["ds"] <= next_month_end)
    ]

    # Add historical EB
    fig_daily = go.Figure()
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily["ds"],
            y=historical_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  ',

            name="EB",
            marker=dict(color="#1f77b4"),  
            showlegend=True,
            legendgroup="EB",
            offsetgroup=0,  # Group all EB bars together
        )
    )
        # Add forecasted EB
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily["ds"],
            y=forecasted_bar_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="EB",
            marker=dict(color="#1f77b4", opacity=0.4),
            showlegend=False,
            legendgroup="EB",
            offsetgroup=0,  # Same group as historical EB
        )
    )
    # Add historical DG
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily1["ds"],
            y=historical_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            marker=dict(color="#ff7f0e"),   
            showlegend=True,
            legendgroup="DG",
            offsetgroup=1,  # Group all DG bars together
        )
    )

    # Add forecasted DG
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily1["ds"],
            y=forecasted_bar_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            showlegend=False,
            legendgroup="DG",
            marker=dict(color="#ff7f0e", opacity=0.4),
            offsetgroup=1,  # Same group as historical DG
        )
    )

    # Add historical Solar
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily2["ds"],
            y=historical_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=True,
            legendgroup="SA",
            marker=dict(color="#2ca02c"),
            offsetgroup=2,  # Group all Solar bars together
        )
    )

    # Add forecasted Solar
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily2["ds"],
            y=forecasted_bar_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=False,
            legendgroup="SA",
            marker=dict(color="#2ca02c", opacity=0.4),
            offsetgroup=2,  # Same group as historical Solar
        )
    )
    


    current_date = pd.Timestamp.now()

    # Define the range (start of the current month and end of the current month)
    range_start = current_date.replace(day=1)  # Start of the current month
    range_end = (current_date + pd.offsets.MonthEnd(0)).replace(hour=23, minute=59, second=59)  # End of the current month

    fig_daily.update_layout(
        title='Energy Trend By Sources',
        template="plotly_dark",
        yaxis_title="Consumption (kWh)",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.65,
            xanchor="center",
            x=0.5,
            font=dict(size=10),  # Adjust legend font size for mobile
        ),
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
            font=dict(color='white', size=10),  # Adjust hover font size for mobile
            font_family='Mulish'
        ),
        bargap=0.1,  # Adjust space between groups
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date",
            range=[range_start, range_end]  # Dynamic range based on the end of the first trace
        ),
        margin=dict(l=10, r=10, t=50, b=40),  # Adjust margins for mobile
        autosize=False,  # Enable autosizing
        width=None,
        height=None,
    )

    # Set responsive attributes
    fig_daily.update_layout(
        autosize=False,
        # responsive=True,
        width=None,  # Auto-adjust width
        height=None,  # Auto-adjust height
        margin=dict(
            l=10, r=10, t=80, b=0  # Smaller margins for better mobile view
        ),
    )

    # Adjust font sizes and other attributes for better responsiveness
    fig_daily.update_layout(
        font=dict(
            size=12,  # General font size
            color="white"
        ),
        legend=dict(
            font=dict(size=10),  # Smaller legend font for mobile
            itemclick="toggleothers"  # Improve interaction on mobile
        )
    )

    # Optional: Adjust hover and legend for specific devices
    fig_daily.update_traces(
        hoverlabel=dict(
            font_size=10  # Smaller hover font for better mobile display
        ),
        selector=dict(type='bar')
    )
    
    trend_plot2 = json.loads(
        json.dumps(
            fig_daily,
            cls=plotly.utils.PlotlyJSONEncoder))     
    return trend_plot2
def trend_plotting3(DG_hour,EB_hour,solar_hour,tz):
    current_time = datetime.now(tz)

    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
        
    if solar_hour["ds"].dt.tz is None:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_localize(tz)
    else:
        solar_hour["ds"] = solar_hour["ds"].dt.tz_convert(tz)
    EB_hour=EB_hour.set_index('ds').resample('M').sum().reset_index()

    DG_hour=DG_hour.set_index('ds').resample('M').sum().reset_index()
    solar_hour=solar_hour.set_index('ds').resample('M').sum().reset_index()

    # Define the end of the current month
    end_of_current_month = (current_time + relativedelta(day=31)).date()

    # Filter data up to the end of the current month
    historical_data_daily = EB_hour[
        (EB_hour["ds"].dt.date >= (current_time - relativedelta(years=2)).date()) &
        (EB_hour["ds"].dt.date <= end_of_current_month)
    ]
    historical_data_daily1 = DG_hour[
        (DG_hour["ds"].dt.date >= (current_time - relativedelta(years=2)).date()) &
        (DG_hour["ds"].dt.date <= end_of_current_month)
    ]
    historical_data_daily2 = solar_hour[
        (solar_hour["ds"].dt.date >= (current_time - relativedelta(years=2)).date()) &
        (solar_hour["ds"].dt.date <= end_of_current_month)
    ]
    # Define the start of the month after the current month
    start_of_next_month = (current_time + relativedelta(day=1, months=1)).date()

    # Define the end of the next year
    end_of_next_year = (current_time + relativedelta(years=2, day=31, month=12)).date()

    # Filter the data for the period after the current month up to the end of next year
    forecasted_bar_data_daily = EB_hour[
        (EB_hour["ds"].dt.date >= start_of_next_month) &
        (EB_hour["ds"].dt.date <= end_of_next_year)
    ]
    forecasted_bar_data_daily1 = DG_hour[
        (DG_hour["ds"].dt.date >= start_of_next_month) &
        (DG_hour["ds"].dt.date <= end_of_next_year)
    ]
    forecasted_bar_data_daily2 = solar_hour[
        (solar_hour["ds"].dt.date >= start_of_next_month) &
        (solar_hour["ds"].dt.date <= end_of_next_year)
    ]

    # Add historical EB
    fig_daily = go.Figure()
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily["ds"],
            y=historical_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  ',

            name="EB",
            marker=dict(color="#1f77b4"),  
            showlegend=True,
            legendgroup="EB",
            offsetgroup=0,  # Group all EB bars together
        )
    )
        # Add forecasted EB
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily["ds"],
            y=forecasted_bar_data_daily["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="EB",
            marker=dict(color="#1f77b4", opacity=0.4),
            showlegend=False,
            legendgroup="EB",
            offsetgroup=0,  # Same group as historical EB
        )
    )
    # Add historical DG
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily1["ds"],
            y=historical_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            marker=dict(color="#ff7f0e"),   
            showlegend=True,
            legendgroup="DG",
            offsetgroup=1,  # Group all DG bars together
        )
    )

    # Add forecasted DG
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily1["ds"],
            y=forecasted_bar_data_daily1["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh ',

            name="DG",
            showlegend=False,
            legendgroup="DG",
            marker=dict(color="#ff7f0e", opacity=0.4),
            offsetgroup=1,  # Same group as historical DG
        )
    )

    # Add historical Solar
    fig_daily.add_trace(
        go.Bar(
            x=historical_data_daily2["ds"],
            y=historical_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=True,
            legendgroup="SA",
            marker=dict(color="#2ca02c"),
            offsetgroup=2,  # Group all Solar bars together
        )
    )

    # Add forecasted Solar
    fig_daily.add_trace(
        go.Bar(
            x=forecasted_bar_data_daily2["ds"],
            y=forecasted_bar_data_daily2["y"],
            hovertemplate='<span style="text-align:left;font-family:Mulish;"></span><br><b>Date: </b>%{x|%d %b %Y}<br><b>Consumption </b>: %{y:.2f} kWh  <br>',

            name="Solar",
            showlegend=False,
            legendgroup="SA",
            marker=dict(color="#2ca02c", opacity=0.4),
            offsetgroup=2,  # Same group as historical Solar
        )
    )
    


    current_date = pd.Timestamp.now()

    # Define the range (first month and last month of the current year)
    range_start = current_date.replace(month=1, day=1)  # First month of the current year (January)
    range_end = current_date.replace(month=12, day=31, hour=23, minute=59, second=59)  # Last month of the current year (December)


    fig_daily.update_layout(
        title='Energy Trend By Sources',
        template="plotly_dark",
        yaxis_title="Consumption (kWh)",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.65,
            xanchor="center",
            x=0.5,
            font=dict(size=10),  # Adjust legend font size for mobile
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', size=10),  # Adjust hover font size for mobile
            font_family='Mulish'
        ),
        bargap=0.1,  # Adjust space between groups
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date",
            range=[range_start, range_end]  # Dynamic range based on the end of the first trace
        ),

        autosize=False,  # Enable autosizing
        width=None,
        height=None,
    )

    # Set responsive attributes
    fig_daily.update_layout(
        autosize=False,
        # responsive=True,
        width=None,  # Auto-adjust width
        height=None,  # Auto-adjust height
        margin=dict(
            l=10, r=10, t=80, b=0  # Smaller margins for better mobile view
        ),
    )

    # Adjust font sizes and other attributes for better responsiveness
    fig_daily.update_layout(
        font=dict(
            size=12,  # General font size
            color="white"
        ),
        legend=dict(
            font=dict(size=10),  # Smaller legend font for mobile
            itemclick="toggleothers"  # Improve interaction on mobile
        )
    )

    # Optional: Adjust hover and legend for specific devices
    fig_daily.update_traces(
        hoverlabel=dict(
            font_size=10  # Smaller hover font for better mobile display
        ),
        selector=dict(type='bar')
    )
    trend_plot3 = json.loads(
        json.dumps(
            fig_daily,
            cls=plotly.utils.PlotlyJSONEncoder))     
    return trend_plot3