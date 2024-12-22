import json
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import pytz

def format(percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend):
    if percentage_deviation >= 0:
        percentage_deviation = f"▲ +{percentage_deviation:.2f} %  "
    else:
        percentage_deviation = f"▼ {percentage_deviation:.2f} % "
    if percentage_deviation1 >= 0:
        percentage_deviation1 = f"▲ +{percentage_deviation1:.2f} %  "
    else:
        percentage_deviation1 = f"▼ {percentage_deviation1:.2f} % "
        
    if percentage_deviation2 >= 0:
        percentage_deviation2 = f"▲ +{percentage_deviation2:.2f} %  "
    else:
        percentage_deviation2 = f"▼ {percentage_deviation2:.2f} % "
    if percentage_deviation3 >= 0:
        percentage_deviation3 = f"▲ +{percentage_deviation3:.2f} %  "
    else:
        percentage_deviation3 = f"▼ {percentage_deviation3:.2f} % "
    if percentage_deviation4 >= 0:
        percentage_deviation4 = f"▲ +{percentage_deviation4:.2f} %  "
    else:
        percentage_deviation4 = f"▼ {percentage_deviation4:.2f} % "
        
    if percentage_deviation5 >= 0:
        percentage_deviation5 = f"▲ +{percentage_deviation5:.2f} %  "
    else:
        percentage_deviation5 = f"▼ {percentage_deviation5:.2f} % "
    if rate_of_change_hour >= 0:
        rate_of_change_hour = f"▲ +{rate_of_change_hour:.2f} %   "
    else:
        rate_of_change_hour = f"▼ {rate_of_change_hour:.2f} %  "

    if rate_of_change_year >= 0:
        rate_of_change_year = f"▲ +{rate_of_change_year:.2f} %   "
    else:
        rate_of_change_year = f"▼ {rate_of_change_year:.2f} %   "

    if rate_of_change_month >= 0:
        rate_of_change_month = f"▲ +{rate_of_change_month:.2f} %  "
    else:
        rate_of_change_month = f"▼ {rate_of_change_month:.2f} %   "

    if rate_of_change_week >= 0:
        rate_of_change_week = f"▲ +{rate_of_change_week:.2f} %  "
    else:
        rate_of_change_week = f"▼ {rate_of_change_week:.2f} %   "

    if rate_of_change_workweek >= 0:
        rate_of_change_workweek = f"▲ +{rate_of_change_workweek:.2f} %   "
    else:
        rate_of_change_workweek = f"▼ {rate_of_change_workweek:.2f} %   "

    if rate_of_change_weekend >= 0:
        rate_of_change_weekend = f"▲ +{rate_of_change_weekend:.2f} %   "
    else:
        rate_of_change_weekend = f"▼ {rate_of_change_weekend:.2f} %  "
    return percentage_deviation,percentage_deviation1,percentage_deviation2,percentage_deviation3,percentage_deviation4,percentage_deviation5,rate_of_change_hour,rate_of_change_year,rate_of_change_month,rate_of_change_week,rate_of_change_workweek,rate_of_change_weekend
