import datetime
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import pytz

def waste_day(fin):
    current_date = datetime.datetime.now().date()
    yesterday_date = current_date - datetime.timedelta(days=1)

    current_day_data = fin[fin['ds'].dt.date == current_date]
    yesterday_data = fin[fin['ds'].dt.date == yesterday_date]

    today_total = round(current_day_data['y'].sum())
    total_yesterday_consumption = round(yesterday_data['y'].sum())

    rate_of_change_hour = (
        (today_total - total_yesterday_consumption) / total_yesterday_consumption
    ) * 100
    rate_of_change_hour = f"{rate_of_change_hour:.2f} % {'▴' if rate_of_change_hour >= 0 else '▼'}"

    num_people_per_tissue_roll = 200
    handwashing_solution_per_person = 0.05
    waste_generated_per_person = 0.00055

    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    for value in fin['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    fin['cumulative_count_tissue'] = cumulative_counts
    fin['tissue_roll_count'] = tissue_roll_counts
    fin['handwashing_solution_used'] = handwashing_solution_used
    fin['waste_generated'] = waste_generated

    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(tz)
    end_of_day = current_time.replace(hour=23, minute=59, second=59)
    today = current_time.date()
    today_data = fin[fin['ds'].dt.date == today]
    remaining_hours_data = today_data[(today_data['ds'] > current_time) & (today_data['ds'] <= end_of_day)]
    today_waste_generated = remaining_hours_data['waste_generated'].sum()
    today_handwash = remaining_hours_data['handwashing_solution_used'].sum()
    today_tissue = remaining_hours_data['tissue_roll_count'].sum()

    tomorrow = current_time.date() + datetime.timedelta(days=1)
    tomorrow_data = fin[fin['ds'].dt.date == tomorrow]
    tomorrow_waste_generated = tomorrow_data['waste_generated'].sum()
    tomorrow_handwash = tomorrow_data['handwashing_solution_used'].sum()
    tomorrow_tissue = tomorrow_data['tissue_roll_count'].sum()

    predicted_waste = round(today_waste_generated + tomorrow_waste_generated, 2)
    predicted_handwash = round(today_handwash + tomorrow_handwash, 2)
    predicted_tissue = round(today_tissue + tomorrow_tissue, 2)

    current_datetime = datetime.datetime.now()
    current_hour = current_datetime.hour
    filtered_data_so_far = fin[(fin['ds'].dt.date == current_date) & (fin['ds'].dt.hour <= current_hour)]
    today_so_far_waste = filtered_data_so_far['waste_generated'].sum()
    today_so_far_tissue = filtered_data_so_far['tissue_roll_count'].sum()
    today_so_far_handwash = filtered_data_so_far['handwashing_solution_used'].sum()

    remaining_data = fin[(fin['ds'].dt.date == current_date) & (fin['ds'].dt.hour > current_hour)]
    remaining_waste = remaining_data['waste_generated'].sum()
    remaining_tissue = remaining_data['tissue_roll_count'].sum()
    remaining_handwash = remaining_data['handwashing_solution_used'].sum()

    times = filtered_data_so_far['ds']
    usage_till_now = filtered_data_so_far['waste_generated'].cumsum()
    times_remaining_adjusted = pd.concat([pd.Series([times.iloc[-1]]), remaining_data['ds']])
    predicted_usage = pd.concat([pd.Series([usage_till_now.iloc[-1]]), remaining_data['waste_generated'].cumsum() + usage_till_now.iloc[-1]])

    current_time = datetime.datetime.now()
    current_hour = current_time.replace(minute=0, second=0, microsecond=0)
    if current_time.minute > 0:
        current_hour += datetime.timedelta(hours=1)

    trace1 = go.Scatter(
        x=times,
        y=usage_till_now,
        mode='lines+markers',
        fill='tozeroy',
        name='Till Now',
        marker=dict(color='red'),
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='<b>Till Now</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    trace2 = go.Scatter(
        x=times_remaining_adjusted,
        y=predicted_usage,
        mode='lines+markers',
        fill='tozeroy',
        name='Predicted',
        marker=dict(color='#2275e0'),
        line=dict(width=0),
        fillcolor='rgba(34, 117, 224, 0.2)',
        hovertemplate='<b>Predicted</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    layout = go.Layout(
        title='Estimated Waste',
        title_x=0.05,
        title_y=0.92,
        yaxis=dict(title=''),
        hovermode='x unified',
        template="plotly_dark",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        annotations=[
            dict(
                x=times.iloc[-1],
                y=usage_till_now.iloc[-1],
                xref='x',
                yref='y',
                text=f'Till Now<br> {usage_till_now.iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=times_remaining_adjusted.iloc[-1],
                y=predicted_usage.iloc[-1],
                xref='x',
                yref='y',
                text=f'Predicted<br> {predicted_usage.iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=current_time,
                y=1,
                xref='x',
                yref='paper',
                text='',
                showarrow=False,
                arrowhead=7,
                ax=0,
                ay=-40,
                font=dict(size=12, color='Yellow')
            )
        ],
        shapes=[
            dict(
                type='line',
                x0=times.iloc[-1],
                y0=0,
                x1=times.iloc[-1],
                y1=usage_till_now.iloc[-1],
                line=dict(
                    color='White',
                    width=1,
                    dash='dot',
                ),
            ),
            dict(
                type='line',
                x0=times.iloc[-1],
                y0=0,
                x1=times.iloc[-1],
                y1=1,
                line=dict(
                    color='rgba(128, 128, 128, 0.5)',
                    width=2,
                    dash='dot',
                ),
                xref='x',
                yref='paper'
            )
        ],
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=1
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_layout(
        autosize=False,
        height=300,
        width=380,
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=5, r=90, t=50, b=40),
    )

    waste_plot = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return waste_plot

def waste_week(fin):
    fin = fin.set_index('ds').resample('D').sum().reset_index()
    current_time = datetime.datetime.now()
    start_of_current_week = current_time - datetime.timedelta(days=current_time.weekday())
    end_of_current_week = start_of_current_week + datetime.timedelta(days=6)
    current_week_data = fin[(fin['ds'].dt.date >= start_of_current_week.date()) & (fin['ds'].dt.date <= end_of_current_week.date())]

    num_people_per_tissue_roll = 200
    handwashing_solution_per_person = 0.05
    waste_generated_per_person = 0.00055

    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    for value in current_week_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    current_week_data['cumulative_count_tissue'] = cumulative_counts
    current_week_data['tissue_roll_count'] = tissue_roll_counts
    current_week_data['handwashing_solution_used'] = handwashing_solution_used
    current_week_data['waste_generated'] = waste_generated

    current_week_data_upto_current_day = current_week_data[current_week_data['ds'].dt.date <= current_time.date()]
    current_week_upto_current_day_waste = current_week_data_upto_current_day['waste_generated'].sum()
    current_week_upto_current_day_tissue = current_week_data_upto_current_day['tissue_roll_count'].sum()
    current_week_upto_current_day_handwash = current_week_data_upto_current_day['handwashing_solution_used'].sum()

    remaining_week_data = current_week_data[current_week_data['ds'].dt.date > current_time.date()]
    remaining_week_waste = remaining_week_data['waste_generated'].sum()
    remaining_week_tissue = remaining_week_data['tissue_roll_count'].sum()
    remaining_week_handwash = remaining_week_data['handwashing_solution_used'].sum()

    total_current_week_waste = current_week_data['waste_generated'].sum()
    total_current_week_tissue = current_week_data['tissue_roll_count'].sum()
    total_current_week_handwash = current_week_data['handwashing_solution_used'].sum()

    data = {
        'Category': ['Waste Generated', 'Handwashing Solution Used', 'Tissue Roll Count'],
        'Total This Week': [total_current_week_waste, total_current_week_handwash, total_current_week_tissue],
        'Up to Current Day': [current_week_upto_current_day_waste, current_week_upto_current_day_handwash, current_week_upto_current_day_tissue],
        'Remaining': [remaining_week_waste, remaining_week_handwash, remaining_week_tissue]
    }

    trace1 = go.Scatter(
        x=current_week_data_upto_current_day['ds'],
        y=current_week_data_upto_current_day['waste_generated'].cumsum(),
        mode='lines+markers',
        fill='tozeroy',
        name='Till Now',
        marker=dict(color='red'),
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='<b>Till Now</b><br>Date: %{x|%d %b %y}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    trace2 = go.Scatter(
        x=pd.concat([pd.Series([current_week_data_upto_current_day['ds'].iloc[-1]]), remaining_week_data['ds']]),
        y=pd.concat([pd.Series([current_week_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]), remaining_week_data['waste_generated'].cumsum() + current_week_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]),
        mode='lines+markers',
        fill='tozeroy',
        name='Predicted',
        marker=dict(color='#2275e0'),
        line=dict(width=0),
        fillcolor='rgba(34, 117, 224, 0.2)',
        hovertemplate='<b>Predicted</b><br>Date: %{x|%d %b %y}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    layout = go.Layout(
        title='Estimated Waste ',
        title_x=0.05,
        title_y=0.92,
        yaxis=dict(title=''),
        hovermode='x unified',
        template="plotly_dark",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        annotations=[
            dict(
                x=current_week_data_upto_current_day['ds'].iloc[-1],
                y=current_week_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Till Now<br> {current_week_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=remaining_week_data['ds'].iloc[-1],
                y=remaining_week_data['waste_generated'].cumsum().iloc[-1] + current_week_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Predicted<br> {remaining_week_data["waste_generated"].cumsum().iloc[-1] + current_week_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=current_time,
                y=1,
                xref='x',
                yref='paper',
                text='',
                showarrow=False,
                arrowhead=7,
                ax=0,
                ay=-40,
                font=dict(size=12, color='Yellow')
            )
        ],
        shapes=[
            dict(
                type='line',
                x0=current_week_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_week_data_upto_current_day['ds'].iloc[-1],
                y1=current_week_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                line=dict(
                    color='White',
                    width=1,
                    dash='dot',
                ),
            ),
            dict(
                type='line',
                x0=current_week_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_week_data_upto_current_day['ds'].iloc[-1],
                y1=1,
                line=dict(
                    color='rgba(128, 128, 128, 0.5)',
                    width=2,
                    dash='dot',
                ),
                xref='x',
                yref='paper'
            )
        ],
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=1
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_layout(
        autosize=False,
        height=300,
        width=380,
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=5, r=90, t=50, b=40),
    )

    waste_plot1 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return waste_plot1

def waste_workweek(fin):
    current_time = datetime.datetime.now()
    fin = fin.set_index('ds').resample('D').sum().reset_index()

    def get_workweek_dates(current_time):
        start_of_current_workweek = current_time - datetime.timedelta(days=current_time.weekday())
        end_of_current_workweek = start_of_current_workweek + datetime.timedelta(days=4)
        return start_of_current_workweek, end_of_current_workweek

    start_of_current_workweek, end_of_current_workweek = get_workweek_dates(current_time)
    current_workweek_data = fin[(fin['ds'].dt.date >= start_of_current_workweek.date()) & (fin['ds'].dt.date <= end_of_current_workweek.date())]

    num_people_per_tissue_roll = 200
    handwashing_solution_per_person = 0.05
    waste_generated_per_person = 0.00055

    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    for value in current_workweek_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    current_workweek_data['cumulative_count_tissue'] = cumulative_counts
    current_workweek_data['tissue_roll_count'] = tissue_roll_counts
    current_workweek_data['handwashing_solution_used'] = handwashing_solution_used
    current_workweek_data['waste_generated'] = waste_generated

    current_workweek_data_upto_current_day = current_workweek_data[current_workweek_data['ds'].dt.date <= current_time.date()]
    current_workweek_upto_current_day_waste = current_workweek_data_upto_current_day['waste_generated'].sum()
    current_workweek_upto_current_day_tissue = current_workweek_data_upto_current_day['tissue_roll_count'].sum()
    current_workweek_upto_current_day_handwash = current_workweek_data_upto_current_day['handwashing_solution_used'].sum()

    remaining_workweek_data = current_workweek_data[current_workweek_data['ds'].dt.date > current_time.date()]

    data = {
        'Category': ['Waste Generated', 'Handwashing Solution Used', 'Tissue Roll Count'],
        'Total This Workweek': [current_workweek_data['waste_generated'].sum(), current_workweek_data['handwashing_solution_used'].sum(), current_workweek_data['tissue_roll_count'].sum()],
        'Up to Current Day': [current_workweek_upto_current_day_waste, current_workweek_upto_current_day_handwash, current_workweek_upto_current_day_tissue],
        'Remaining': [remaining_workweek_data['waste_generated'].sum(), remaining_workweek_data['handwashing_solution_used'].sum(), remaining_workweek_data['tissue_roll_count'].sum()]
    }

    trace1 = go.Scatter(
        x=current_workweek_data_upto_current_day['ds'],
        y=current_workweek_data_upto_current_day['waste_generated'].cumsum(),
        mode='lines+markers',
        fill='tozeroy',
        name='Till Now',
        marker=dict(color='red'),
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='<b>Till Now</b><br>Date: %{x|%d %b %y}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    trace2 = go.Scatter(
        x=pd.concat([pd.Series([current_workweek_data_upto_current_day['ds'].iloc[-1]]), remaining_workweek_data['ds']]),
        y=pd.concat([pd.Series([current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]), remaining_workweek_data['waste_generated'].cumsum() + current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]),
        mode='lines+markers',
        fill='tozeroy',
        name='Predicted',
        marker=dict(color='#2275e0'),
        line=dict(width=0),
        fillcolor='rgba(34, 117, 224, 0.2)',
        hovertemplate='<b>Predicted</b><br>Date: %{x|%d %b %y}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    annotations = [
        dict(
            x=current_workweek_data_upto_current_day['ds'].iloc[-1],
            y=current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
            xref='x',
            yref='y',
            text=f'Till Now<br> {current_workweek_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        ),
        dict(
            x=current_time,
            y=1,
            xref='x',
            yref='paper',
            text='',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font=dict(size=12, color='Yellow')
        )
    ]

    if not remaining_workweek_data.empty:
        x_value = remaining_workweek_data['ds'].iloc[-1]
        y_value = remaining_workweek_data['waste_generated'].cumsum().iloc[-1] + current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1]
        predicted_text = f'Predicted<br> {y_value:.1f} kg'
    else:
        x_value = current_workweek_data_upto_current_day['ds'].iloc[-1]
        y_value = current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1]
        predicted_text = ''

    annotations.append(
        dict(
            x=x_value,
            y=y_value,
            xref='x',
            yref='y',
            text=predicted_text,
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    )

    layout = go.Layout(
        title='Estimated Waste ',
        title_x=0.05,
        title_y=0.92,
        yaxis=dict(title=''),
        hovermode='x unified',
        template="plotly_dark",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        annotations=annotations,
        shapes=[
            dict(
                type='line',
                x0=current_workweek_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_workweek_data_upto_current_day['ds'].iloc[-1],
                y1=current_workweek_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                line=dict(color='White', width=1, dash='dot'),
            ),
            dict(
                type='line',
                x0=current_workweek_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_workweek_data_upto_current_day['ds'].iloc[-1],
                y1=1,
                line=dict(color='rgba(128, 128, 128, 0.5)', width=2, dash='dot'),
                xref='x',
                yref='paper'
            )
        ],
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=1
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_layout(
        autosize=False,
        height=300,
        width=380,
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=5, r=90, t=50, b=40)
    )

    waste_plot2 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return waste_plot2

def waste_month(fin):
    current_time = datetime.datetime.now()
    fin = fin.set_index('ds').resample('D').sum().reset_index()

    start_of_current_month = datetime.datetime(current_time.year, current_time.month, 1)
    end_of_current_month = (start_of_current_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    current_month_data = fin[(fin['ds'].dt.date >= start_of_current_month.date()) & (fin['ds'].dt.date <= end_of_current_month.date())]

    num_people_per_tissue_roll = 200
    handwashing_solution_per_person = 0.05
    waste_generated_per_person = 0.00055

    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    for value in current_month_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    current_month_data['cumulative_count_tissue'] = cumulative_counts
    current_month_data['tissue_roll_count'] = tissue_roll_counts
    current_month_data['handwashing_solution_used'] = handwashing_solution_used
    current_month_data['waste_generated'] = waste_generated

    current_month_data_upto_current_day = current_month_data[current_month_data['ds'].dt.date <= current_time.date()]
    current_month_upto_current_day_waste = current_month_data_upto_current_day['waste_generated'].sum()
    current_month_upto_current_day_tissue = current_month_data_upto_current_day['tissue_roll_count'].sum()
    current_month_upto_current_day_handwash = current_month_data_upto_current_day['handwashing_solution_used'].sum()

    remaining_month_data = current_month_data[current_month_data['ds'].dt.date > current_time.date()]
    remaining_month_waste = remaining_month_data['waste_generated'].sum()
    remaining_month_tissue = remaining_month_data['tissue_roll_count'].sum()
    remaining_month_handwash = remaining_month_data['handwashing_solution_used'].sum()

    total_current_month_waste = current_month_data['waste_generated'].sum()
    total_current_month_tissue = current_month_data['tissue_roll_count'].sum()
    total_current_month_handwash = current_month_data['handwashing_solution_used'].sum()

    data = {
        'Category': ['Waste Generated', 'Handwashing Solution Used', 'Tissue Roll Count'],
        'Total This Month': [total_current_month_waste, total_current_month_handwash, total_current_month_tissue],
        'Up to Current Day': [current_month_upto_current_day_waste, current_month_upto_current_day_handwash, current_month_upto_current_day_tissue],
        'Remaining': [remaining_month_waste, remaining_month_handwash, remaining_month_tissue]
    }

    trace1 = go.Scatter(
        x=current_month_data_upto_current_day['ds'],
        y=current_month_data_upto_current_day['waste_generated'].cumsum(),
        mode='lines+markers',
        fill='tozeroy',
        name='Till Now',
        marker=dict(color='red'),
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='<b>Till Now</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    trace2 = go.Scatter(
        x=pd.concat([pd.Series([current_month_data_upto_current_day['ds'].iloc[-1]]), remaining_month_data['ds']]),
        y=pd.concat([pd.Series([current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]), remaining_month_data['waste_generated'].cumsum() + current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]),
        mode='lines+markers',
        fill='tozeroy',
        name='Predicted',
        marker=dict(color='#2275e0'),
        line=dict(width=0),
        fillcolor='rgba(34, 117, 224, 0.2)',
        hovertemplate='<b>Predicted</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    layout = go.Layout(
        title='Estimated Waste',
        title_x=0.05,
        title_y=0.92,
        yaxis=dict(title=''),
        hovermode='x unified',
        template="plotly_dark",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        annotations=[
            dict(
                x=current_month_data_upto_current_day['ds'].iloc[-1],
                y=current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Till Now<br> {current_month_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=remaining_month_data['ds'].iloc[-1] if not remaining_month_data.empty else current_month_data_upto_current_day['ds'].iloc[-1],
                y=remaining_month_data['waste_generated'].cumsum().iloc[-1] + current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1] if not remaining_month_data.empty else current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Predicted<br> {remaining_month_data["waste_generated"].cumsum().iloc[-1] + current_month_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg' if not remaining_month_data.empty else f'Predicted<br> {current_month_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=current_time,
                y=1,
                xref='x',
                yref='paper',
                text='',
                showarrow=False,
                arrowhead=7,
                ax=0,
                ay=-40,
                font=dict(size=12, color='Yellow')
            )
        ],
        shapes=[
            dict(
                type='line',
                x0=current_month_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_month_data_upto_current_day['ds'].iloc[-1],
                y1=current_month_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                line=dict(
                    color='White',
                    width=1,
                    dash='dot',
                ),
            ),
            dict(
                type='line',
                x0=current_month_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_month_data_upto_current_day['ds'].iloc[-1],
                y1=1,
                line=dict(
                    color='rgba(128, 128, 128, 0.5)',
                    width=2,
                    dash='dot',
                ),
                xref='x',
                yref='paper'
            )
        ],
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=1
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_layout(
        autosize=False,
        height=300,
        width=380,
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=5, r=90, t=50, b=40),
    )

    waste_plot3 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return waste_plot3

def waste_year(fin):
    current_time = datetime.datetime.now()
    fin = fin.set_index('ds').resample('M').sum().reset_index()

    start_of_current_year = datetime.datetime(current_time.year, 1, 1)
    end_of_current_year = datetime.datetime(current_time.year, 12, 31)
    current_year_data = fin[(fin['ds'].dt.date >= start_of_current_year.date()) & (fin['ds'].dt.date <= end_of_current_year.date())]

    num_people_per_tissue_roll = 200
    handwashing_solution_per_person = 0.05
    waste_generated_per_person = 0.00055

    cumulative_count = 0
    cumulative_counts = []
    tissue_roll_counts = []
    handwashing_solution_used = []
    waste_generated = []

    for value in current_year_data['y']:
        cumulative_count += value
        cumulative_counts.append(cumulative_count)
        num_rolls_used = cumulative_count // num_people_per_tissue_roll
        tissue_roll_counts.append(num_rolls_used)
        if num_rolls_used > 0:
            cumulative_count = cumulative_count % num_people_per_tissue_roll
        solution_used = value * handwashing_solution_per_person
        handwashing_solution_used.append(solution_used)
        waste_gen = value * waste_generated_per_person
        waste_generated.append(waste_gen)

    current_year_data['cumulative_count_tissue'] = cumulative_counts
    current_year_data['tissue_roll_count'] = tissue_roll_counts
    current_year_data['handwashing_solution_used'] = handwashing_solution_used
    current_year_data['waste_generated'] = waste_generated

    current_year_data_upto_current_day = current_year_data[current_year_data['ds'].dt.date <= current_time.date()]
    current_year_upto_current_day_waste = current_year_data_upto_current_day['waste_generated'].sum()
    current_year_upto_current_day_tissue = current_year_data_upto_current_day['tissue_roll_count'].sum()
    current_year_upto_current_day_handwash = current_year_data_upto_current_day['handwashing_solution_used'].sum()

    remaining_year_data = current_year_data[current_year_data['ds'].dt.date > current_time.date()]
    remaining_year_waste = remaining_year_data['waste_generated'].sum()
    remaining_year_tissue = remaining_year_data['tissue_roll_count'].sum()
    remaining_year_handwash = remaining_year_data['handwashing_solution_used'].sum()

    total_current_year_waste = current_year_data['waste_generated'].sum()
    total_current_year_tissue = current_year_data['tissue_roll_count'].sum()
    total_current_year_handwash = current_year_data['handwashing_solution_used'].sum()

    data = {
        'Category': ['Waste Generated', 'Handwashing Solution Used', 'Tissue Roll Count'],
        'Total This Year': [total_current_year_waste, total_current_year_handwash, total_current_year_tissue],
        'Up to Current Day': [current_year_upto_current_day_waste, current_year_upto_current_day_handwash, current_year_upto_current_day_tissue],
        'Remaining': [remaining_year_waste, remaining_year_handwash, remaining_year_tissue]
    }

    trace1 = go.Scatter(
        x=current_year_data_upto_current_day['ds'],
        y=current_year_data_upto_current_day['waste_generated'].cumsum(),
        mode='lines+markers',
        fill='tozeroy',
        name='Till Now',
        marker=dict(color='red'),
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.2)',
        hovertemplate='<b>Till Now</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    trace2 = go.Scatter(
        x=pd.concat([pd.Series([current_year_data_upto_current_day['ds'].iloc[-1]]), remaining_year_data['ds']]),
        y=pd.concat([pd.Series([current_year_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]), remaining_year_data['waste_generated'].cumsum() + current_year_data_upto_current_day['waste_generated'].cumsum().iloc[-1]]),
        mode='lines+markers',
        fill='tozeroy',
        name='Predicted',
        marker=dict(color='#2275e0'),
        line=dict(width=0),
        fillcolor='rgba(34, 117, 224, 0.2)',
        hovertemplate='<b>Predicted</b><br>Date: %{x|%d %b %y, %I %p}<br>Waste: %{y:.2f} kg<extra></extra>'
    )

    layout = go.Layout(
        title='Estimated Waste for Current Year',
        title_x=0.05,
        title_y=0.92,
        yaxis=dict(title=''),
        hovermode='x unified',
        template="plotly_dark",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        annotations=[
            dict(
                x=current_year_data_upto_current_day['ds'].iloc[-1],
                y=current_year_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Till Now<br> {current_year_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=remaining_year_data['ds'].iloc[-1],
                y=remaining_year_data['waste_generated'].cumsum().iloc[-1] + current_year_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                xref='x',
                yref='y',
                text=f'Predicted<br> {remaining_year_data["waste_generated"].cumsum().iloc[-1] + current_year_data_upto_current_day["waste_generated"].cumsum().iloc[-1]:.1f} kg',
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ),
            dict(
                x=current_time,
                y=1,
                xref='x',
                yref='paper',
                text='',
                showarrow=False,
                arrowhead=7,
                ax=0,
                ay=-40,
                font=dict(size=12, color='Yellow')
            )
        ],
        shapes=[
            dict(
                type='line',
                x0=current_year_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_year_data_upto_current_day['ds'].iloc[-1],
                y1=current_year_data_upto_current_day['waste_generated'].cumsum().iloc[-1],
                line=dict(
                    color='White',
                    width=1,
                    dash='dot',
                ),
            ),
            dict(
                type='line',
                x0=current_year_data_upto_current_day['ds'].iloc[-1],
                y0=0,
                x1=current_year_data_upto_current_day['ds'].iloc[-1],
                y1=1,
                line=dict(
                    color='rgba(128, 128, 128, 0.5)',
                    width=2,
                    dash='dot',
                ),
                xref='x',
                yref='paper'
            )
        ],
        showlegend=False,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=1
        )
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_layout(
        autosize=False,
        height=300,
        width=380,
        template='plotly_dark',
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish')
        ),
        margin=dict(l=5, r=90, t=50, b=40),
    )

    waste_plot4 = json.loads(
        json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder))
    return waste_plot4
