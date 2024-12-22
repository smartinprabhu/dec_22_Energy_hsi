import pytz
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import plotly.utils

def calculate_and_plot_energy_consumption(h_assets, l_assets, c_assets,total,total1,total2,total3):
    # Define the timezone
    timezone = pytz.timezone("Asia/Kolkata")

    # Get the current date, week, month, and year in the specified timezone
    current_date = pd.Timestamp.now(timezone)
    current_week = pd.Timestamp.now(tz=timezone).isocalendar().week
    current_month = pd.Timestamp.now(tz=timezone).month
    current_year = pd.Timestamp.now(tz=timezone).year

    # Dictionary to store the results for h_assets
    h_asset_totals = {
        'current_date': {},
        'current_week': {},
        'current_month': {},
        'current_year': {}
    }

    # Dictionary to store the results for l_assets
    l_asset_totals = {
        'current_date': {},
        'current_week': {},
        'current_month': {},
        'current_year': {}
    }

    # Dictionary to store the results for c_assets
    c_asset_totals = {
        'current_date': {},
        'current_week': {},
        'current_month': {},
        'current_year': {}
    }

    # List of assets to transform
    assets_to_transform = [
        'c5_asset', 'c6_asset', 'c7_asset',
        'h12_asset', 'h13_asset', 'h14_asset',
        'l6_asset', 'c2_asset', 'c3_asset',
        'c4_asset', 'l1_asset', 'l2_asset',
        'l3_asset', 'h1_asset', 'h2_asset',
        'h3_asset', 'h4_asset', 'h5_asset',
        'h11_asset'
    ]

    # Function to process assets
    def process_assets(assets, asset_totals, category):
        transformed_assets = []
        for i, asset in enumerate(assets, start=1):
            # Ensure 'ds' is of datetime type
            asset['ds'] = pd.to_datetime(asset['ds'])

            # Check if the asset needs to be transformed
            asset_name = f'{category}{i}_asset'
            if asset_name in assets_to_transform:
                # Reset the y values if already transformed
                if 'original_y' not in asset.columns:
                    asset['original_y'] = asset['y']  # Store original y values
                # Transform the asset by multiplying 'y' by the given 10
                asset['y'] = asset['original_y'] * 10
            else:
                # If not transformed, just ensure original_y is set
                if 'original_y' not in asset.columns:
                    asset['original_y'] = asset['y']  # Store original y values

            # Add the (possibly transformed) asset to the list
            transformed_assets.append(asset)
            filtered_data = asset[(asset['ds'].dt.date == current_date.date()) & 
                                (asset['ds'].dt.hour <= current_date.hour)]
            # print(filtered_data)
            if not filtered_data.empty:
                total_date = filtered_data['y'].sum()
            else:
                total_date = 0  # or handle it accordingly
            # print(filtered_data)
            if not filtered_data.empty:
                total_date = filtered_data['y'].sum()
            else:
                total_date = 0  # or handle it accordingly

            # Calculate the totals on the transformed asset
            total_date = asset[(asset['ds'].dt.date == current_date.date()) &
                               (asset['ds'].dt.hour <= current_date.hour)]['y'].sum()
            asset_totals['current_date'][f'asset{i}'] = total_date

            total_week = asset[(asset['ds'].dt.isocalendar().week == current_week) &
                               (asset['ds'].dt.date <= current_date.date())]['y'].sum()
            asset_totals['current_week'][f'asset{i}'] = total_week

            total_month = asset[(asset['ds'].dt.month == current_month) &
                                (asset['ds'].dt.year == current_date.year) &
                                (asset['ds'].dt.date <= current_date.date())]['y'].sum()
            asset_totals['current_month'][f'asset{i}'] = total_month

            total_year = asset[(asset['ds'].dt.year == current_year) &
                               (asset['ds'].dt.month <= current_date.month)]['y'].sum()
            asset_totals['current_year'][f'asset{i}'] = total_year

        return transformed_assets

    # Process h_assets
    h_assets = process_assets(h_assets, h_asset_totals, 'h')

    # Process l_assets
    l_assets = process_assets(l_assets, l_asset_totals, 'l')

    # Process c_assets
    c_assets = process_assets(c_assets, c_asset_totals, 'c')

    # Calculate the total sum of all h_assets for each time period
    h_total = sum(h_asset_totals['current_date'].values())
    h_total_week = sum(h_asset_totals['current_week'].values())
    h_total_month = sum(h_asset_totals['current_month'].values())
    h_total_year = sum(h_asset_totals['current_year'].values())

    # Calculate the total sum of all l_assets for each time period
    l_total = sum(l_asset_totals['current_date'].values())
    l_total_week = sum(l_asset_totals['current_week'].values())
    l_total_month = sum(l_asset_totals['current_month'].values())
    l_total_year = sum(l_asset_totals['current_year'].values())

    # Calculate the total sum of all c_assets for each time period
    c_total = sum(c_asset_totals['current_date'].values())
    c_total_week = sum(c_asset_totals['current_week'].values())
    c_total_month = sum(c_asset_totals['current_month'].values())
    c_total_year = sum(c_asset_totals['current_year'].values())

    # Data
    categories = ['HVAC   ', 'Compressor   ', 'Lighting   ']
    def reduce_values(values, total):
        sum_values = sum(values)
        if sum_values > total:
            reduction_ratio = total / sum_values
            reduced_values = [value * reduction_ratio for value in values]
            return reduced_values
        return values

    # Reduce values if necessary
    values_today = [h_total, c_total, l_total]
    values_today = reduce_values(values_today, total)

    values_week = [h_total_week, c_total_week, l_total_week]
    values_week = reduce_values(values_week, total1)

    values_month = [h_total_month, c_total_month, l_total_month]
    values_month = reduce_values(values_month, total2)

    values_year = [h_total_year, c_total_year, l_total_year]
    values_year = reduce_values(values_year, total3)

    # Update the original variables with the reduced values
    h_total, c_total, l_total = values_today
    h_total_week, c_total_week, l_total_week = values_week
    h_total_month, c_total_month, l_total_month = values_month
    h_total_year, c_total_year, l_total_year = values_year

    # Calculate the combined values
    t_c = (h_total / 2 + c_total / 2 + l_total)
    w_c = (h_total_week / 2.5 + c_total_week / 2.5 + l_total_week / 2.5)
    m_c = (h_total_month / 2.5 + c_total_month / 3.5 + l_total_month / 2.5)
    y_c = (h_total_year + c_total_year + l_total_year)

    # Format the values
    formatted_values_today = [f'{h_total} kWh', f'{l_total} kWh', f'{c_total} kWh']

    # Calculate the percentage change for today
    percent_chnage_today = ((t_c - total) / total)

    percent_chnage_week=(w_c-total1)/total1
    # Function to format values based on size
    percent_chnage_month=(m_c-total2)/total2
    percent_chnage_year=(y_c-total3)/total3

    def format_value(val):
        return f"{val:.2f}"

    # Format values for labels
    formatted_values_today = [format_value(val) for val in values_today]
    formatted_values_week = [format_value(val) for val in values_week]
    formatted_values_month = [format_value(val) for val in values_month]
    formatted_values_year = [format_value(val) for val in values_year]

    # Function to sort values and categories by descending order
    def sort_data(values, categories, formatted_values):
        sorted_indices = np.argsort(values)  # Sort indices in descending order
        sorted_values = np.array(values)[sorted_indices]
        sorted_categories = np.array(categories)[sorted_indices]
        sorted_formatted_values = np.array(formatted_values)[sorted_indices]
        return sorted_values, sorted_categories, sorted_formatted_values

    # Sort data for each time period in descending order
    values_today, categories_today, formatted_values_today = sort_data(values_today, categories, formatted_values_today)
    values_week, categories_week, formatted_values_week = sort_data(values_week, categories, formatted_values_week)
    values_month, categories_month, formatted_values_month = sort_data(values_month, categories, formatted_values_month)
    values_year, categories_year, formatted_values_year = sort_data(values_year, categories, formatted_values_year)
    fig_today = go.Figure(go.Bar(
        x=values_today,
        y=categories_today,
        orientation='h',
        marker=dict(
            color='#1f77b4'  # Use blue as per the image color scheme
        ),
        hovertemplate='<b>%{y}</b><br> %{x:.2f} kWh<extra></extra>',
        text=formatted_values_today,  # Add formatted data labels
        textposition='outside',  # Automatically position labels
    ))



    symbol = '▲' if percent_chnage_today > 0 else '▼'
    color = 'green' if percent_chnage_today > 0 else 'red'
    # Add annotation for percentage change
    fig_today.add_annotation(
        x=1, y=categories_today,
        text=f"<span style=' font-size:17px; font-family:Mulish;'> <span style='color:{color}; font-size:17px; font-family:Mulish;'>{symbol} <b>{abs(percent_chnage_today):.2f}%</b> </span><br> Energy Loss</span> ",
        showarrow=False,
        font=dict(size=17),
        xshift=350,  # Adjust for placement
        yshift=-135,  # Adjust for placement
    )

    # Update layout for today's plot
    fig_today.update_layout(
        title='Active Appliances',
        xaxis_title='Energy Consumption (kWh)',
        yaxis_title='',

        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font=dict(color='white', family='Mulish', size=14),  # White font color, Mulish font family, size 14
        margin=dict(l=10,  r=20, t=50, b=50),
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish', size=14)
        ),
        showlegend=False,
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False),  # Remove y-axis gridlines
        hovermode='x unified',  # Set hover mode to x unified
        autosize=False,
        width=800  # Set the width  the plot to 800 pixels
    )
    # Create the bar chart for the current week
    fig_week = go.Figure(go.Bar(
        x=values_week,
        y=categories_week,
        orientation='h',
        marker=dict(
            color='#1f77b4'  # Use the specific blue color
        ),
        hovertemplate='<b>%{y}</b><br> %{x:.2f} kWh<extra></extra>',

        text=formatted_values_week,  # Add formatted data labels
        textposition='outside'  # Position labels outside the bars
    ))
    
    symbol = '▲' if percent_chnage_week > 0 else '▼'
    color = 'green' if percent_chnage_week > 0 else 'red'
    # Add annotation for percentage change
    fig_week.add_annotation(
        x=1, y=categories_week,
        text=f"<span style=' font-size:17px; font-family:Mulish;'> <span style='color:{color}; font-size:17px; font-family:Mulish;'>{symbol} <b>{abs(percent_chnage_week):.2f}%</b> </span><br>Energy Loss</span> ",

        showarrow=False,
        font=dict(size=17),
        xshift=350,  # Adjust for placement
        yshift=-135,  # Adjust for placement
    )
        # Add annotation for percentage change

    # Update layout for the week's plot
    fig_week.update_layout(
        title='',
        xaxis_title='Energy Consumption (kWh)',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font=dict(color='white', family='Mulish', size=14),  # White font color, Mulish font family, size 14
        margin=dict(l=10,  r=30, t=50, b=50),
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish', size=14)
        ),
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False),  # Remove y-axis gridlines
        showlegend=False,
        hovermode='x unified'  # Set hover mode to x unified
    )

    # Create the bar chart for the current month
    fig_month = go.Figure(go.Bar(
        x=values_month,
        y=categories_month,
        orientation='h',
        marker=dict(
            color='#1f77b4'  # Use the specific blue color
        ),
        hovertemplate='<b>%{y}</b><br> %{x:.2f} kWh<extra></extra>',

        text=formatted_values_month,  # Add formatted data labels
        textposition='outside'  # Position labels outside the bars
    ))
    symbol = '▲' if percent_chnage_month > 0 else '▼'
    color = 'green' if percent_chnage_month > 0 else 'red'
    # Add annotation for percentage change
    fig_month.add_annotation(
        x=1, y=categories_month,
        text=f"<span style=' font-size:17px; font-family:Mulish;'> <span style='color:{color}; font-size:17px; font-family:Mulish;'>{symbol} <b>{abs(percent_chnage_month):.2f}%</b> </span><br> Energy Loss</span> ",

        showarrow=False,
        font=dict(size=17),
        xshift=350,  # Adjust for placement
        yshift=-135,  # Adjust for placement
    )

    # Update layout for the month's plot
    fig_month.update_layout(
        title='',
        xaxis_title='Energy Consumption (kWh)',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font=dict(color='white', family='Mulish', size=14),  # White font color, Mulish font family, size 14
        margin=dict(l=10,  r=30, t=50, b=50),
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish', size=14)
        ),
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False),  # Remove y-axis gridlines
        showlegend=False,
        hovermode='x unified'  # Set hover mode to x unified
    )

    # Create the bar chart for the current year
    fig_year = go.Figure(go.Bar(
        x=values_year,
        y=categories_year,
        orientation='h',
        marker=dict(
            color='#1f77b4'  # Use the specific blue color
        ),
        hovertemplate='<b>%{y}</b><br> %{x:.2f} kWh<extra></extra>',

        text=formatted_values_year,  # Add formatted data labels
        textposition='outside'  # Position labels outside the bars
    ))
    symbol = '▲' if percent_chnage_year > 0 else '▼'
    color = 'green' if percent_chnage_year > 0 else 'red'
    # Add annotation for percentage change
    fig_year.add_annotation(
        x=1, y=categories_year,
        text=f"<span style=' font-size:17px; font-family:Mulish;'>  <span style='color:{color}; font-size:17px; font-family:Mulish;'>{symbol} <b>{abs(percent_chnage_year):.2f}%</b> </span><br>Energy Loss</span> ",

        showarrow=False,
        font=dict(size=17),
        xshift=350,  # Adjust for placement
        yshift=-135,  # Adjust for placement
    )
    # Update layout for the year's plot
    fig_year.update_layout(
        title='',
        xaxis_title='Energy Consumption (kWh)',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        font=dict(color='white', family='Mulish', size=14),  # White font color, Mulish font family, size 14
        margin=dict(l=10,  r=30, t=50, b=50),
        hoverlabel=dict(
            bgcolor='#2C2C2F',
            font=dict(color='white', family='Mulish', size=14)
        ),
        xaxis=dict(showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(showgrid=False),  # Remove y-axis gridlines
        showlegend=False,
        hovermode='x unified'  # Set hover mode to x unified
    )



    fig_today = json.loads(
        json.dumps(
            fig_today,
            cls=plotly.utils.PlotlyJSONEncoder))
    fig_month = json.loads(
        json.dumps(
            fig_month,
            cls=plotly.utils.PlotlyJSONEncoder))
    fig_year = json.loads(
        json.dumps(
            fig_year,
            cls=plotly.utils.PlotlyJSONEncoder))
    fig_week = json.loads(
        json.dumps(
            fig_week,
            cls=plotly.utils.PlotlyJSONEncoder))
    # Return the figures
    return fig_today, fig_week, fig_month, fig_year
