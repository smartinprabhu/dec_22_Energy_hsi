

"""Energy-Analyzer Flask API"""
import json
from datetime import datetime, time, timedelta
import plotly.graph_objects as go
import pandas as pd
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
# from DG import processing
# from EB import processing_eb
from utility_plot import calculate_and_plot_energy_consumption
from emission import emission_cal,emission_cal1,emission_cal2,emission_cal3
from EUI_EOI import calcualte,calcualte1,calculate2,calculate3
from flask import Flask, Response
from flask_cors import CORS
# from utility import utility_process
from load_data import load_and_process_data
# from solar import processing_solar
from total_con import total_consumption,tot_con_week,tot_con_month,tot_con_year
from trend_plot import trend_plotting,trend_plotting1,trend_plotting2,trend_plotting3
from pie import pie,pie1,pie2,pie3
app = Flask(__name__)
CORS(app)
cost_per_kw = 6.09
num_days = 180


( DG_hour,  EB_hour, solar_hour,
        h_asset1, h_asset2, h_asset3, h_asset4, h_asset5, h_asset6,
        h_asset7, h_asset8, h_asset9, h_asset10, h_asset11,h_asset12,h_asset13,h_asset14,
        l_asset1, l_asset2, l_asset3, l_asset4, l_asset5, l_asset6,
        c_asset1, c_asset2, c_asset3, c_asset4, c_asset5, c_asset6,c_asset7
    )=load_and_process_data()
h_assets = [h_asset1, h_asset2, h_asset3, h_asset4, h_asset5, h_asset6,h_asset7, h_asset8, h_asset9, h_asset10, h_asset11,h_asset12,h_asset13,h_asset14,]
l_assets = [l_asset1, l_asset2, l_asset3, l_asset4, l_asset5, l_asset6]
c_assets = [c_asset1, c_asset2, c_asset3, c_asset4, c_asset5, c_asset6,c_asset7]

@app.route("/forecast", methods=["POST"])

def get_energy_data():

    tz = pytz.timezone("Asia/Kolkata")
    current_datetime = pd.Timestamp.now(tz)
    current_date = pd.Timestamp.today().date()
    energy_data_all,building_area,population,EIO,EUI=calcualte(DG_hour,EB_hour,solar_hour,current_date)

    energy_data_all['ds'] = pd.to_datetime(energy_data_all['ds'])


    energy_data_all["ds"] = pd.to_datetime(energy_data_all["ds"])
    if energy_data_all["ds"].dt.tz is None:
        energy_data_all["ds"] = energy_data_all["ds"].dt.tz_localize(tz)
    else:
        energy_data_all["ds"] = energy_data_all["ds"].dt.tz_convert(tz)
    consumption_plot = total_consumption(energy_data_all, current_datetime)
    df_daily=energy_data_all.set_index('ds').resample('D').sum().reset_index()
    consumption_plot_week=tot_con_week(df_daily)
    consumption_plot_month=tot_con_month(df_daily,current_datetime)
    consumption_plot_year=tot_con_year(df_daily, current_datetime)
    # Get the current date
    current_date = pd.Timestamp.today().date()

    # Convert the 'ds' column to datetime
    DG_hour['ds'] = pd.to_datetime(DG_hour['ds'])
    EB_hour['ds'] = pd.to_datetime(EB_hour['ds'])
    solar_hour['ds'] = pd.to_datetime(solar_hour['ds'])

    pie_plot,total=pie(DG_hour,EB_hour,solar_hour,current_datetime)
    pie_plot1,total1,solar_value=pie1(DG_hour,EB_hour,solar_hour,current_date)
    pie_plot2,total2,solar_value1=pie2(DG_hour,EB_hour,solar_hour,current_date)
    
    pie_plot3,total3,solar_value2=pie3(DG_hour,EB_hour,solar_hour,current_date)
    EIO1,EUI1=calcualte1(energy_data_all,current_date)
    EIO2,EUI2=calculate2(energy_data_all,current_date)
    EIO3,EUI3=calculate3(energy_data_all,current_date)
    eb_tco2_plot,dg_tco2_plot,solar_tco2_plot=emission_cal(DG_hour,EB_hour,solar_hour,tz,current_datetime)
    solar_tco2_plot_week,eb_tco2_plot_week,dg_tco2_plot_week=emission_cal1(DG_hour,EB_hour,solar_hour,tz,current_datetime,solar_value)
    solar_tco2_plot_month,eb_tco2_plot_month,dg_tco2_plot_month=emission_cal2(DG_hour,EB_hour,solar_hour,tz,current_datetime,solar_value1)
    dg_tco2_plot_year,eb_tco2_plot_year,solar_tco2_plot_year=emission_cal3(DG_hour,EB_hour,solar_hour,tz,current_datetime,solar_value2)
    fig_today, fig_week, fig_month, fig_year=calculate_and_plot_energy_consumption(h_assets, l_assets, c_assets,total,total1,total2,total3)
    trend_plot= trend_plotting(DG_hour,EB_hour,solar_hour,tz,current_datetime)
    trend_plot1= trend_plotting1(DG_hour,EB_hour,solar_hour,tz,current_datetime)
    trend_plot2=trend_plotting2(DG_hour,EB_hour,solar_hour,tz)
    trend_plot3=trend_plotting3(DG_hour,EB_hour,solar_hour,tz)

    
    
    response = ([
                    ('Today', {
        'eb_tco2_plot': eb_tco2_plot,
        'dg_tco2_plot': dg_tco2_plot,
        'solar_energy_plot': solar_tco2_plot,
        'trend_plot': trend_plot,
        'pie':pie_plot,
        'total':total,
        'utility_plot':fig_today,
        'consumption_plot':consumption_plot,
        'EIO':EIO,
        'EUI':EUI,


                }),

                    ('Week', {
        'eb_tco2_plot': eb_tco2_plot_week,
        'dg_tco2_plot': dg_tco2_plot_week,
        'solar_energy_plot': solar_tco2_plot_week,
        'trend_plot': trend_plot1,
        'pie':pie_plot1,
        'utility_plot':fig_week,
        'total':total,
        'consumption_plot':consumption_plot_week,
        'EIO':EIO1,
        'EUI':EUI1,


                }),


                    ('Month', {
        'eb_tco2_plot': eb_tco2_plot_month,
        'dg_tco2_plot': dg_tco2_plot_month,
        'solar_energy_plot': solar_tco2_plot_month,
        'trend_plot': trend_plot2,
        'pie':pie_plot2,
        'utility_plot':fig_month,
        'total':total,
        'consumption_plot':consumption_plot_month,
        'EIO':EIO2,
        'EUI':EUI2, 

                }),
                    ('Year', {

        'eb_tco2_plot': eb_tco2_plot_year,
        'dg_tco2_plot': dg_tco2_plot_year,
        'solar_energy_plot': solar_tco2_plot_year,
        'trend_plot': trend_plot3,
        'pie':pie_plot3,
        'utility_plot':fig_year,
        'total':total,
        'consumption_plot':consumption_plot_year,
        'EIO':EIO3,
        'EUI':EUI3,


                }),
        ])
    response_json = json.dumps(response)
    return Response(response_json, content_type='application/json')

if __name__ == "__main__":
    app.run(port=5003,
            debug=True)

