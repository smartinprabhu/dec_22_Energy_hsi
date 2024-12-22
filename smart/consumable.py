import datetime
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta

def consum(fin):

    # Constants
    num_people_per_tissue_roll = 200  # Number of people per tissue roll
    handwashing_solution_per_person = 0.005  # Amount of handwashing solution used per person (in liters)
    waste_generated_per_person = 0.005  # 50 g  Amount of waste generated per person (in kilograms)

    # Initialize cumulative count and tissue roll count
    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    current_datetime = datetime.now()
    fin = pd.DataFrame(fin)

    # Calculate cumulative counts and determine tissue roll usage
    for index, value in enumerate(fin['y'], start=1):
        cumulative_count += value
        cumulative_counts.append(cumulative_count)

        # Tissue roll usage
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll

        # Handwashing solution and waste generation
        handwashing_solution_used.append(value * handwashing_solution_per_person)
        waste_generated.append(value * waste_generated_per_person)

    # Assign calculated values to the DataFrame
    fin['cumulative_count_tissue'] = cumulative_counts
    fin['tissue_roll_count'] = tissue_roll_counts
    fin['handwashing_solution_used'] = handwashing_solution_used
    fin['waste_generated'] = waste_generated

    # Nested function to generate the daily consumption plot
    def day():
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_hour = current_datetime.hour

        # Filter data for the current date
        filtered_data = fin[fin['ds'].dt.date == current_date]

        # Calculate totals for the current day
        today_handwash = filtered_data['handwashing_solution_used'].sum()
        today_tissue = filtered_data['tissue_roll_count'].sum()

        # Calculate totals up to the current hour
        filtered_data_so_far = fin[(fin['ds'].dt.date == current_date) &
                                   (fin['ds'].dt.hour <= current_hour)]

        today_so_far_tissue = filtered_data_so_far['tissue_roll_count'].sum()
        today_so_far_handwash = filtered_data_so_far['handwashing_solution_used'].sum()

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        tissue_now = int(today_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(today_tissue)    # No decimals for tissue
        handwash_now = round(today_so_far_handwash, 2)
        handwash_predicted = round(today_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=7, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=7, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=8, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=8, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )
        con_plot = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot

    def week():
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Calculate the start and end dates for the current week
        start_of_current_week = current_datetime - timedelta(days=current_datetime.weekday())
        end_of_current_week = start_of_current_week + timedelta(days=6)

        # Filter data for the current week
        current_week_data = fin[(fin['ds'].dt.date >= start_of_current_week.date()) & (fin['ds'].dt.date <= end_of_current_week.date())]

        # Sum the consumption or emissions for the current week
        current_week_waste = current_week_data['waste_generated'].sum()
        current_week_handwash = current_week_data['handwashing_solution_used'].sum()
        current_week_tissue = current_week_data['tissue_roll_count'].sum()

        # Filter the DataFrame for the current week up to the current day
        current_week_data_upto_current_day = current_week_data[current_week_data['ds'].dt.date <= current_date]

        # Sum the consumption or emissions up to the current day
        current_week_so_far_waste = current_week_data_upto_current_day['waste_generated'].sum()
        current_week_so_far_tissue = current_week_data_upto_current_day['tissue_roll_count'].sum()
        current_week_so_far_handwash = current_week_data_upto_current_day['handwashing_solution_used'].sum()

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        # Prepare data for the plot
        tissue_now = int(current_week_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(current_week_tissue)    # No decimals for tissue
        handwash_now = round(current_week_so_far_handwash, 2)
        handwash_predicted = round(current_week_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=52, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=52, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=52, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=52, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables ',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )

        con_plot1 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot1

    def workweek():
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Calculate the start and end dates for the current workweek
        def get_workweek_dates(current_datetime):
            # Calculate the start of the current workweek (Monday)
            start_of_current_workweek = current_datetime - timedelta(days=current_datetime.weekday())
            # Calculate the end of the current workweek (Friday)
            end_of_current_workweek = start_of_current_workweek + timedelta(days=4)
            return start_of_current_workweek, end_of_current_workweek

        start_of_current_workweek, end_of_current_workweek = get_workweek_dates(current_datetime)

        # Filter data for the current workweek
        current_workweek_data = fin[(fin['ds'].dt.date >= start_of_current_workweek.date()) & (fin['ds'].dt.date <= end_of_current_workweek.date())]

        # Sum the consumption or emissions for the current workweek
        current_workweek_waste = current_workweek_data['waste_generated'].sum()
        current_workweek_handwash = current_workweek_data['handwashing_solution_used'].sum()
        current_workweek_tissue = current_workweek_data['tissue_roll_count'].sum()

        # Filter the DataFrame for the current workweek up to the current day
        current_workweek_data_upto_current_day = current_workweek_data[current_workweek_data['ds'].dt.date <= current_date]

        # Sum the consumption or emissions up to the current day
        current_workweek_so_far_waste = current_workweek_data_upto_current_day['waste_generated'].sum()
        current_workweek_so_far_tissue = current_workweek_data_upto_current_day['tissue_roll_count'].sum()
        current_workweek_so_far_handwash = current_workweek_data_upto_current_day['handwashing_solution_used'].sum()

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        # Prepare data for the plot
        tissue_now = int(current_workweek_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(current_workweek_tissue)    # No decimals for tissue
        handwash_now = round(current_workweek_so_far_handwash, 2)
        handwash_predicted = round(current_workweek_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=40, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=40, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=41, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=41, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )
        con_plot2 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot2

    def weekend():
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Calculate the start and end dates for the upcoming weekend
        def get_upcoming_weekend_dates(current_datetime):
            # Calculate the start of the upcoming weekend (Saturday)
            days_until_saturday = (5 - current_datetime.weekday()) % 7
            start_of_upcoming_weekend = current_datetime + timedelta(days=days_until_saturday)
            # Calculate the end of the upcoming weekend (Sunday)
            end_of_upcoming_weekend = start_of_upcoming_weekend + timedelta(days=1)
            return start_of_upcoming_weekend, end_of_upcoming_weekend

        start_of_upcoming_weekend, end_of_upcoming_weekend = get_upcoming_weekend_dates(current_datetime)

        # Filter data for the upcoming weekend
        upcoming_weekend_data = fin[(fin['ds'].dt.date >= start_of_upcoming_weekend.date()) & (fin['ds'].dt.date <= end_of_upcoming_weekend.date())]

        # Sum the consumption or emissions for the upcoming weekend
        upcoming_weekend_waste = upcoming_weekend_data['waste_generated'].sum()
        upcoming_weekend_handwash = upcoming_weekend_data['handwashing_solution_used'].sum()
        upcoming_weekend_tissue = upcoming_weekend_data['tissue_roll_count'].sum()

        # Filter the DataFrame for the upcoming weekend up to the current day (if the current day is within the weekend)
        if current_date >= start_of_upcoming_weekend.date() and current_date <= end_of_upcoming_weekend.date():
            upcoming_weekend_data_upto_current_day = upcoming_weekend_data[upcoming_weekend_data['ds'].dt.date <= current_date]

            # Sum the consumption or emissions up to the current day
            upcoming_weekend_so_far_waste = upcoming_weekend_data_upto_current_day['waste_generated'].sum()
            upcoming_weekend_so_far_tissue = upcoming_weekend_data_upto_current_day['tissue_roll_count'].sum()
            upcoming_weekend_so_far_handwash = upcoming_weekend_data_upto_current_day['handwashing_solution_used'].sum()
        else:
            upcoming_weekend_so_far_waste = 0
            upcoming_weekend_so_far_tissue = 0
            upcoming_weekend_so_far_handwash = 0

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        # Prepare data for the plot
        tissue_now = int(upcoming_weekend_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(upcoming_weekend_tissue)    # No decimals for tissue
        handwash_now = round(upcoming_weekend_so_far_handwash, 2)
        handwash_predicted = round(upcoming_weekend_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=12, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=12, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=12, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=12, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )
        con_plot3 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot3

    def year():
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Calculate the start and end dates for the current year
        def get_year_dates(current_datetime):
            # Calculate the start of the current year
            start_of_current_year = datetime(current_datetime.year, 1, 1)
            # Calculate the end of the current year
            end_of_current_year = datetime(current_datetime.year, 12, 31)
            return start_of_current_year, end_of_current_year

        start_of_current_year, end_of_current_year = get_year_dates(current_datetime)

        # Filter data for the current year
        current_year_data = fin[(fin['ds'].dt.date >= start_of_current_year.date()) & (fin['ds'].dt.date <= end_of_current_year.date())]

        # Sum the consumption or emissions for the current year
        current_year_waste = current_year_data['waste_generated'].sum()
        current_year_handwash = current_year_data['handwashing_solution_used'].sum()
        current_year_tissue = current_year_data['tissue_roll_count'].sum()

        # Filter the DataFrame for the current year up to the current day
        current_year_data_upto_current_day = current_year_data[current_year_data['ds'].dt.date <= current_date]

        # Sum the consumption or emissions up to the current day
        current_year_so_far_waste = current_year_data_upto_current_day['waste_generated'].sum()
        current_year_so_far_tissue = current_year_data_upto_current_day['tissue_roll_count'].sum()
        current_year_so_far_handwash = current_year_data_upto_current_day['handwashing_solution_used'].sum()

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        # Prepare data for the plot
        tissue_now = int(current_year_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(current_year_tissue)    # No decimals for tissue
        handwash_now = round(current_year_so_far_handwash, 2)
        handwash_predicted = round(current_year_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=1950, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=1950, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=1950, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=1950, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )
        con_plot4 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot4

    def month():
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        # Calculate the start and end dates for the current month
        def get_current_month_dates(current_datetime):
            # Calculate the start of the current month
            start_of_current_month = datetime(current_datetime.year, current_datetime.month, 1)
            # Calculate the end of the current month
            if current_datetime.month == 12:
                end_of_current_month = datetime(current_datetime.year, 12, 31)
            else:
                end_of_current_month = datetime(current_datetime.year, current_datetime.month + 1, 1) - timedelta(days=1)
            return start_of_current_month, end_of_current_month

        start_of_current_month, end_of_current_month = get_current_month_dates(current_datetime)

        # Filter data for the current month
        current_month_data = fin[(fin['ds'].dt.date >= start_of_current_month.date()) & (fin['ds'].dt.date <= end_of_current_month.date())]

        # Sum the consumption or emissions for the current month
        current_month_waste = current_month_data['waste_generated'].sum()
        current_month_handwash = current_month_data['handwashing_solution_used'].sum()
        current_month_tissue = current_month_data['tissue_roll_count'].sum()

        # Filter the DataFrame for the current month up to the current day
        current_month_data_upto_current_day = current_month_data[current_month_data['ds'].dt.date <= current_date]

        # Sum the consumption or emissions up to the current day
        current_month_so_far_waste = current_month_data_upto_current_day['waste_generated'].sum()
        current_month_so_far_tissue = current_month_data_upto_current_day['tissue_roll_count'].sum()
        current_month_so_far_handwash = current_month_data_upto_current_day['handwashing_solution_used'].sum()

        # Create a 2x2 subplot figure
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Tissue', 'Handwash'))

        # Prepare data for the plot
        tissue_now = int(current_month_so_far_tissue)  # No decimals for tissue
        tissue_predicted = int(current_month_tissue)    # No decimals for tissue
        handwash_now = round(current_month_so_far_handwash, 2)
        handwash_predicted = round(current_month_handwash, 2)

        # Add subplots separately with their annotations
        # Tissue subplot (1,1)
        fig.add_trace(go.Bar(
            x=[tissue_now], y=['Tissue'],
            orientation='h', marker_color='#ff7f0e', showlegend=False,
            hovertemplate=f'Till Now: {tissue_now} Rolls<extra></extra>'
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=[tissue_predicted - tissue_now], y=['Tissue'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {tissue_predicted} Rolls<extra></extra>'
        ), row=1, col=1)

        # Annotation for Tissue
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{tissue_now} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="left")
        fig.add_annotation(x=215, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")
        fig.add_annotation(x=215, y=-1, text=f'{tissue_predicted} Rolls', showarrow=False,
                        font=dict(color="white", size=12), xref="x1", yref="y1", xanchor="right")

        # Handwash subplot (2,1)
        fig.add_trace(go.Bar(
            x=[handwash_now], y=['Handwash'],
            orientation='h', marker_color='#2ca02c', showlegend=False,
            hovertemplate=f'Till Now: {handwash_now} Ltrs<extra></extra>'
        ), row=2, col=1)

        fig.add_trace(go.Bar(
            x=[handwash_predicted - handwash_now], y=['Handwash'],
            orientation='h', marker_color='gray', showlegend=False,
            hovertemplate=f'Predicted: {handwash_predicted} Ltrs<extra></extra>'
        ), row=2, col=1)

        # Annotation for Handwash
        fig.add_annotation(x=0, y=0.8, text=f'Till Now', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=0, y=-1, text=f'{handwash_now} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="left")
        fig.add_annotation(x=215, y=0.7, text=f'Predicted', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")
        fig.add_annotation(x=215, y=-1, text=f'{handwash_predicted} Ltrs', showarrow=False,
                        font=dict(color="white", size=12), xref="x2", yref="y2", xanchor="right")

        # Update layout for the entire figure
        fig.update_layout(
            template="plotly_dark",
            title='Estimated Consumables',
            title_y=0.92,
            title_x=0.03,
            height=300,
            width=300,
            showlegend=False,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor='#2C2C2F',
                font=dict(color='white', family='Mulish')
            ),
            barmode='stack',
            bargap=0.2,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            xaxis2=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(showticklabels=False),  # Hide y-axis labels for the first subplot
            yaxis2=dict(showticklabels=False),  # Hide y-axis labels for the second subplot
            margin=dict(l=30, r=30, t=100, b=50)
        )
        con_plot5 = json.loads(
            json.dumps(
                fig,
                cls=plotly.utils.PlotlyJSONEncoder))
        return con_plot5

    con_plot = day()
    con_plot1 = week()
    con_plot2 = workweek()
    con_plot3 = weekend()
    con_plot4 = year()
    con_plot5 = month()

    return con_plot, con_plot1, con_plot2, con_plot3, con_plot4, con_plot5

# Example usage:
# Assuming `fin` is a DataFrame with columns 'ds' (datetime) and 'y' (values)
# fin = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', periods=100, freq='D'), 'y': np.random.randint(1, 100, size=100)})
# con_plot, con_plot1, con_plot2, con_plot3, con_plot4, con_plot5 = consum(fin)
