import pandas as pd
import plotly.graph_objects as go
import json
import plotly

def emission_cal(DG_hour, EB_hour, solar_hour, tz, current_datetime):
    DG_hour['emission'] = DG_hour['y'] * 2.25
    EB_hour['emission'] = EB_hour['y'] * 0.71

    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)

    current_date = current_datetime.date()

    # Filter the DataFrame for the entire current date (from 0th hour to 23rd hour)
    filtered_data_dg = DG_hour[DG_hour['ds'].dt.date == current_date]
    filtered_data_eb = EB_hour[EB_hour['ds'].dt.date == current_date]

    # Sum the consumption for the entire day
    today_emmision_dg = filtered_data_dg['emission'].sum()
    today_emmision_eb = filtered_data_eb['emission'].sum()

    # print(f"Total consumption for {current_date} is {today_emmision_dg:.2f} tCO2e")
    # print(f"Total consumption for {current_date} is {today_emmision_eb:.2f} tCO2e")

    current_hour = current_datetime.hour

    # Filter the DataFrame for the entire current date from 0th hour to the current hour
    filtered_data_today_dg = DG_hour[(DG_hour['ds'].dt.date == current_date) &
                                     (DG_hour['ds'].dt.hour <= current_hour)]
    filtered_data_today_eb = EB_hour[(EB_hour['ds'].dt.date == current_date) &
                                     (EB_hour['ds'].dt.hour <= current_hour)]

    # Sum the consumption or emissions up to the current hour
    today_so_far_emission_dg = filtered_data_today_dg['emission'].sum()
    today_so_far_emission_eb = filtered_data_today_eb['emission'].sum()

    # print(f"Total emission for {current_date} up to hour {current_hour} is {today_so_far_emission_dg:.2f} tCO2e")
    # print(f"Total emission for {current_date} up to hour {current_hour} is {today_so_far_emission_eb:.2f} tCO2e")

    # Filter data for the current date
    filtered_data_solar = solar_hour[solar_hour['ds'].dt.date == current_date]

    # Calculate total emissions
    today_emission_solar = filtered_data_solar['y'].sum()

    # Calculate emissions up to the current hour
    filtered_data_today_solar = solar_hour[(solar_hour['ds'].dt.date == current_date) & (solar_hour['ds'].dt.hour <= current_hour)]

    today_so_far_solar = filtered_data_today_solar['y'].sum()

    def solar_plot(today_so_far_solar):
        till_date_value = today_so_far_solar
        predicted_emission_value = 3000

        # Calculate the remaining predicted emission
        remaining_predicted = predicted_emission_value - till_date_value

        # Create the figure
        fig_solar = go.Figure()

        fig_solar.add_trace(go.Bar(
            x=[till_date_value],
            y=['Green Energy Generated'],
            orientation='h',
            marker_color='lightgreen',
            name='Till Date',
            hovertemplate='<b>Till now Consumption</b>: %{x:.2f} kWh<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_solar.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Green Energy Generated'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} kWh<extra></extra>'
            ))

        fig_solar.add_annotation(
            x=0.2,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{till_date_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Goal',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xref='x',
            xshift=-1,
            xanchor='right',
            yref='paper'
        )

        fig_solar.update_layout(
            template="plotly_dark",
            title='<br><b>Green Energy Generated</b><br>',
            title_y=0.98,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        solar_tco2_plot = json.loads(
            json.dumps(
                fig_solar,
                cls=plotly.utils.PlotlyJSONEncoder))
        return solar_tco2_plot

    def eb_plot(today_so_far_emission_eb, today_emmision_eb):
        till_date_value = today_so_far_emission_eb
        predicted_emission_value = today_emmision_eb

        remaining_predicted = predicted_emission_value - till_date_value

        fig_eb = go.Figure()

        fig_eb.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#1f77b4',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_eb.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_eb.add_annotation(
            x=2.6,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=2.6,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xanchor='right',
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_eb.add_annotation(
            x=midpoint,
            y=1.8,
            text='EB',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_eb.update_layout(
            template="plotly_dark",
            title='<b>Emission -EB </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        eb_tco2_plot = json.loads(
            json.dumps(
                fig_eb,
                cls=plotly.utils.PlotlyJSONEncoder))
        return eb_tco2_plot

    def dg_plot(today_so_far_emission_dg, today_emmision_dg):
        
        till_date_value = today_so_far_emission_dg
        predicted_emission_value = today_emmision_dg

        if predicted_emission_value == 0:
            predicted_emission_value = 100
        remaining_predicted = predicted_emission_value - till_date_value

        fig_dg = go.Figure()

        fig_dg.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#ff7f0e',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_dg.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_dg.add_annotation(
            x=0.2,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xanchor="right",
            yanchor="bottom",
            xshift=-0.5,
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_dg.add_annotation(
            x=midpoint,
            y=1.8,
            text='DG',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_dg.update_layout(
            template="plotly_dark",
            title='<b>Emission -DG </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        dg_tco2_plot = json.loads(
            json.dumps(
                fig_dg,
                cls=plotly.utils.PlotlyJSONEncoder))
        return dg_tco2_plot

    dg_tco2_plot = dg_plot(today_so_far_emission_dg, today_emmision_dg)
    eb_tco2_plot = eb_plot(today_so_far_emission_eb, today_emmision_eb)
    solar_tco2_plot = solar_plot(today_so_far_solar)

    return eb_tco2_plot, dg_tco2_plot, solar_tco2_plot

def emission_cal1(DG_hour, EB_hour, solar_hour, tz, current_datetime,solar_value):
    EB_hour = EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour = DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour = solar_hour.set_index('ds').resample('D').sum().reset_index()
    current_date = current_datetime.date()
    start_date = current_date - pd.Timedelta(days=current_date.weekday())
    end_date = start_date + pd.Timedelta(days=6)

    # Filter data for the current week
    DG_week = DG_hour[(DG_hour['ds'].dt.date >= start_date) & (DG_hour['ds'].dt.date <= end_date)]
    EB_week = EB_hour[(EB_hour['ds'].dt.date >= start_date) & (EB_hour['ds'].dt.date <= end_date)]
    solar_week = solar_hour[(solar_hour['ds'].dt.date >= start_date) & (solar_hour['ds'].dt.date <= end_date)]

    weekly_emmision_dg = DG_week['emission'].sum()
    weekly_emmision_eb = EB_week['emission'].sum()
    weekly_emission_solar = solar_week['y'].sum()
    DG_week_today = DG_week[DG_week['ds'].dt.date <= current_date]
    EB_week_today = EB_week[EB_week['ds'].dt.date <= current_date]
    solar_week_today = solar_week[solar_week['ds'].dt.date <= current_date]

    weekly_so_far_emission_dg = DG_week_today['emission'].sum()
    weekly_so_far_emission_eb = EB_week_today['emission'].sum()
    weekly_so_far_solar = solar_week_today['y'].sum()
    till_date_value = weekly_so_far_solar
    predicted_emission_value = 7*3000

    remaining_predicted = predicted_emission_value - solar_value

    def solar_plot():
        fig_solar = go.Figure()

        fig_solar.add_trace(go.Bar(
            x=[solar_value],
            y=['Green Energy Generated'],
            orientation='h',
            marker_color='lightgreen',
            name='Till Date',
            hovertemplate='<b>Till now Consumption</b>: %{x:.2f} kWh<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_solar.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Green Energy Generated'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} kWh<extra></extra>'
            ))

        fig_solar.add_annotation(
            x=0.2,
            y=1.7,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{solar_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=1.7,
            text='Goal',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xref='x',
            xshift=-1,
            xanchor='right',
            yref='paper'
        )

        fig_solar.update_layout(
            template="plotly_dark",
            title='<br><b>Green Energy Generated</b><br>',
            title_y=0.98,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        solar_tco2_plot = json.loads(
            json.dumps(
                fig_solar,
                cls=plotly.utils.PlotlyJSONEncoder))
        return solar_tco2_plot

    def eb_plot():
        till_date_value = weekly_so_far_emission_eb
        predicted_emission_value = weekly_emmision_eb

        remaining_predicted = predicted_emission_value - till_date_value

        fig_eb = go.Figure()

        fig_eb.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#1f77b4',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_eb.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_eb.add_annotation(
            x=2.6,
            y=1.7,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=1.7,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=2.6,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xanchor='right',
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_eb.add_annotation(
            x=midpoint,
            y=1.8,
            text='EB',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_eb.update_layout(
            template="plotly_dark",
            title='<b>Emission -EB </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        eb_tco2_plot = json.loads(
            json.dumps(
                fig_eb,
                cls=plotly.utils.PlotlyJSONEncoder))
        return eb_tco2_plot

    def dg_plot():
        till_date_value = weekly_so_far_emission_dg
        predicted_emission_value = weekly_emmision_dg

        if predicted_emission_value == 0:
            predicted_emission_value = 100
        remaining_predicted = predicted_emission_value - till_date_value

        fig_dg = go.Figure()

        fig_dg.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#ff7f0e',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_dg.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_dg.add_annotation(
            x=0.2,
            y=1.7,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=1.7,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xanchor="right",
            yanchor="bottom",
            xshift=-0.5,
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_dg.add_annotation(
            x=midpoint,
            y=1.8,
            text='DG',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_dg.update_layout(
            template="plotly_dark",
            title='<b>Emission -DG </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        dg_tco2_plot = json.loads(
            json.dumps(
                fig_dg,
                cls=plotly.utils.PlotlyJSONEncoder))
        return dg_tco2_plot

    solar_tco2_plot_week = solar_plot()
    eb_tco2_plot_week = eb_plot()
    dg_tco2_plot_week = dg_plot()
    return solar_tco2_plot_week, eb_tco2_plot_week, dg_tco2_plot_week
def emission_cal2(DG_hour, EB_hour, solar_hour, tz, current_datetime,solar_value1):
    EB_hour = EB_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour = DG_hour.set_index('ds').resample('D').sum().reset_index()
    solar_hour = solar_hour.set_index('ds').resample('D').sum().reset_index()
    DG_hour['emission'] = DG_hour['y'] * 2.25
    EB_hour['emission'] = EB_hour['y'] * 0.71

    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)

    current_date = pd.Timestamp.now().date()
    start_date = pd.Timestamp(current_date.replace(day=1))
    end_date = pd.Timestamp((start_date + pd.DateOffset(months=1)) - pd.Timedelta(days=1))

    # Filter data for the current month
    DG_month = DG_hour[(DG_hour['ds'].dt.date >= start_date.date()) & (DG_hour['ds'].dt.date <= end_date.date())]
    EB_month = EB_hour[(EB_hour['ds'].dt.date >= start_date.date()) & (EB_hour['ds'].dt.date <= end_date.date())]
    solar_month = solar_hour[(solar_hour['ds'].dt.date >= start_date.date()) & (solar_hour['ds'].dt.date <= end_date.date())]

    # Calculate total emissions for the month
    monthly_emmision_dg = DG_month['emission'].sum()
    monthly_emmision_eb = EB_month['emission'].sum()
    DG_month_today = DG_month[DG_month['ds'].dt.date <= current_date]
    EB_month_today = EB_month[EB_month['ds'].dt.date <= current_date]
    solar_month_today = solar_month[solar_month['ds'].dt.date <= current_date]

    monthly_so_far_emission_dg = DG_month_today['emission'].sum()
    monthly_so_far_emission_eb = EB_month_today['emission'].sum()
    monthly_so_far_solar = solar_month_today['y'].sum()

    till_date_value = monthly_so_far_solar
    predicted_emission_value = 30 * 3000

    remaining_predicted = predicted_emission_value - solar_value1

    def solar_plot():
        fig_solar = go.Figure()

        fig_solar.add_trace(go.Bar(
            x=[solar_value1],
            y=['Green Energy Generated'],
            orientation='h',
            marker_color='lightgreen',
            name='Till Date',
            hovertemplate='<b>Till now Consumption</b>: %{x:.2f} kWh<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_solar.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Green Energy Generated'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} kWh<extra></extra>'
            ))

        fig_solar.add_annotation(
            x=0.2,
            y=1.7,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{solar_value1:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=1.7,
            text='Goal',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xref='x',
            xshift=-1,
            xanchor='right',
            yref='paper'
        )

        fig_solar.update_layout(
            template="plotly_dark",
            title='<br><b>Green Energy Generated</b><br>',
            title_y=0.98,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig_solar

    def eb_plot():
        till_date_value = monthly_so_far_emission_eb
        predicted_emission_value = monthly_emmision_eb

        remaining_predicted = predicted_emission_value - till_date_value

        fig_eb = go.Figure()

        fig_eb.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#1f77b4',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_eb.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_eb.add_annotation(
            x=2.6,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=2.6,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xanchor='right',
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_eb.add_annotation(
            x=midpoint,
            y=1.8,
            text='EB',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_eb.update_layout(
            template="plotly_dark",
            title='<b>Emission -EB </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        eb_tco2_plot = json.loads(
            json.dumps(
                fig_eb,
                cls=plotly.utils.PlotlyJSONEncoder))
        return eb_tco2_plot

    def dg_plot():
        till_date_value = monthly_so_far_emission_dg
        predicted_emission_value = monthly_emmision_dg

        if predicted_emission_value == 0:
            predicted_emission_value = 100
        remaining_predicted = predicted_emission_value - till_date_value

        fig_dg = go.Figure()

        fig_dg.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#ff7f0e',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_dg.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_dg.add_annotation(
            x=0.2,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xanchor="right",
            yanchor="bottom",
            xshift=-0.5,
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_dg.add_annotation(
            x=midpoint,
            y=1.8,
            text='DG',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_dg.update_layout(
            template="plotly_dark",
            title='<b>Emission -DG </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        dg_tco2_plot = json.loads(
            json.dumps(
                fig_dg,
                cls=plotly.utils.PlotlyJSONEncoder))
        return dg_tco2_plot

    fig_solar = solar_plot()
    fig_eb = eb_plot()
    fig_dg = dg_plot()
    solar_tco2_plot_month = json.loads(
        json.dumps(
            fig_solar,
            cls=plotly.utils.PlotlyJSONEncoder))
    eb_tco2_plot_month = json.loads(
        json.dumps(
            fig_eb,
            cls=plotly.utils.PlotlyJSONEncoder))
    dg_tco2_plot_month = json.loads(
        json.dumps(
            fig_dg,
            cls=plotly.utils.PlotlyJSONEncoder))

    return solar_tco2_plot_month, eb_tco2_plot_month, dg_tco2_plot_month

def emission_cal3(DG_hour,EB_hour,solar_hour,tz,current_datetime,solar_value2):
    EB_hour=EB_hour.set_index('ds').resample('M').sum().reset_index()
    DG_hour=DG_hour.set_index('ds').resample('M').sum().reset_index()  
    solar_hour=solar_hour.set_index('ds').resample('M').sum().reset_index()      
    EB_hour['y'] = EB_hour['y'].apply(lambda x: '{:,.2f}'.format(x))
    EB_hour['y'] = EB_hour['y'].str.replace(',', '').astype(float)

    emission_factor_dg=2.25
    emission_factor_eb=0.71


    DG_hour["ds"] = pd.to_datetime(DG_hour["ds"])
    if DG_hour["ds"].dt.tz is None:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_localize(tz)
    else:
        DG_hour["ds"] = DG_hour["ds"].dt.tz_convert(tz)

    if EB_hour["ds"].dt.tz is None:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_localize(tz)
    else:
        EB_hour["ds"] = EB_hour["ds"].dt.tz_convert(tz)
    current_date = current_datetime.date()
    start_date = current_date.replace(month=1, day=1)
    end_date = current_date.replace(month=12, day=31)

    # Filter data for the current year
    DG_year = DG_hour[(DG_hour['ds'].dt.date >= start_date) & (DG_hour['ds'].dt.date <= end_date)]
    EB_year = EB_hour[(EB_hour['ds'].dt.date >= start_date) & (EB_hour['ds'].dt.date <= end_date)]
    solar_year = solar_hour[(solar_hour['ds'].dt.date >= start_date) & (solar_hour['ds'].dt.date <= end_date)]

    # Calculate total emissions for the year
    yearly_emmision_dg = DG_year['y'].sum()*emission_factor_dg
    yearly_emmision_eb = EB_year['y'].sum()*emission_factor_eb
    yearly_emission_solar = solar_year['y'].sum()

    # Calculate emissions up to the current date
    DG_year_today = DG_year[DG_year['ds'].dt.date <= current_date]
    EB_year_today = EB_year[EB_year['ds'].dt.date <= current_date]
    solar_year_today = solar_year[solar_year['ds'].dt.date <= current_date]

    yearly_so_far_emission_dg = DG_year_today['y'].sum()*emission_factor_dg
    yearly_so_far_emission_eb = EB_year_today['y'].sum()*emission_factor_eb
    yearly_so_far_solar = solar_year_today['y'].sum()
        
    def solar_plot():
        till_date_value = yearly_so_far_solar
        predicted_emission_value = 365*3000

        remaining_predicted = predicted_emission_value - solar_value2

        fig_solar = go.Figure()

        fig_solar.add_trace(go.Bar(
            x=[solar_value2],
            y=['Green Energy Generated'],
            orientation='h',
            marker_color='lightgreen',
            name='Till Date',
            hovertemplate='<b>Till now Consumption</b>: %{x:.2f} kWh<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_solar.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Green Energy Generated'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} kWh<extra></extra>'
            ))

        fig_solar.add_annotation(
            x=0.2,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{solar_value2:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Goal',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_solar.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} kWh',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xref='x',
            xshift=-1,
            xanchor='right',
            yref='paper'
        )

        fig_solar.update_layout(
            template="plotly_dark",
            title='<br><b>Green Energy Generated</b><br>',
            title_y=0.98,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig_solar
    def eb_plot():
        till_date_value = yearly_so_far_emission_eb
        predicted_emission_value = yearly_emmision_eb

        remaining_predicted = predicted_emission_value - till_date_value

        fig_eb = go.Figure()

        fig_eb.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#1f77b4',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_eb.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_eb.add_annotation(
            x=2.6,
            y=1.7,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=2.6,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_eb.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xanchor='right',
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_eb.add_annotation(
            x=midpoint,
            y=1.8,
            text='EB',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_eb.update_layout(
            template="plotly_dark",
            title='<b></b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig_eb

    def dg_plot():
        till_date_value = yearly_so_far_emission_dg
        predicted_emission_value = yearly_emmision_dg

        if predicted_emission_value == 0:
            predicted_emission_value = 100
        remaining_predicted = predicted_emission_value - till_date_value

        fig_dg = go.Figure()

        fig_dg.add_trace(go.Bar(
            x=[till_date_value],
            y=['Carbon Emission'],
            orientation='h',
            marker_color='#ff7f0e',
            name='Till Date',
            hovertemplate='<b>Till Now Emitted</b>: %{x:.2f} tCO2e<extra></extra>'
        ))

        if remaining_predicted > 0:
            fig_dg.add_trace(go.Bar(
                x=[remaining_predicted],
                y=['Carbon Emission'],
                orientation='h',
                marker_color='gray',
                name='Remaining',
                hovertemplate='<b>Remaining</b>: %{x:.2f} tCO2e<extra></extra>'
            ))

        fig_dg.add_annotation(
            x=0.2,
            y=1.70,
            text='Till Now',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=1.70,
            text='Predicted',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xshift=-1,
            xref='x',
            xanchor='right',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=0.2,
            y=-0.58,
            text=f'{till_date_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="left",
            xanchor="left",
            xshift=1,
            xref='x',
            yref='paper'
        )

        fig_dg.add_annotation(
            x=predicted_emission_value,
            y=-0.58,
            text=f'{predicted_emission_value:.2f} tCO2e',
            showarrow=False,
            font=dict(color="white", size=10),
            align="right",
            xanchor="right",
            yanchor="bottom",
            xshift=-0.5,
            xref='x',
            yref='paper'
        )

        midpoint = (0 + predicted_emission_value) / 2
        fig_dg.add_annotation(
            x=midpoint,
            y=1.8,
            text='DG',
            showarrow=False,
            font=dict(color="white", size=14),
            xref='x',
            yref='paper'
        )

        fig_dg.update_layout(
            template="plotly_dark",
            title='<b>Emission -DG </b><br>',
            title_y=0.8,
            title_x=0.02881,
            height=100,
            autosize=True,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis_title='',
            yaxis=dict(showticklabels=False),
            barmode='stack',
            bargap=0.2,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig_dg
    fig_eb=eb_plot()
    fig_dg=dg_plot()
    fig_solar=solar_plot()
    dg_tco2_plot_year = json.loads(
        json.dumps(
            fig_dg,
            cls=plotly.utils.PlotlyJSONEncoder))
    eb_tco2_plot_year = json.loads(
        json.dumps(
            fig_eb,
            cls=plotly.utils.PlotlyJSONEncoder))
    solar_tco2_plot_year = json.loads(
        json.dumps(
            fig_solar,
            cls=plotly.utils.PlotlyJSONEncoder))
    return dg_tco2_plot_year,eb_tco2_plot_year,solar_tco2_plot_year