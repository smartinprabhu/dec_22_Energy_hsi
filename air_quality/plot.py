"""
Module for Psychrometric Chart
"""

import base64
import os
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import psychrolib as psy
from matplotlib.patches import FancyArrowPatch, Polygon

psy.SetUnitSystem(psy.SI)

def generate_psychrometric_chart(
        indoor_temperature,
        indoor_humidity,
        indoor_pressure):

    color_scheme_1 = {
        "facecolor": "#282828",
        "edgecolor": "#282828",
        "contour_color": "white",
        "comfort_color": "lightyellow",
        "zone_color": "lightyellow",
        "text_color": "white",
        "label_color": "#949495",
        "tick_color": "#949495",
        "filename": "psychrometric_chart"
    }

    color_scheme_2 = {
        "facecolor": "#ffffff",
        "edgecolor": "#ffffff",
        "contour_color": "black",
        "comfort_color": "yellow",
        "zone_color": "yellow",
        "text_color": "black",
        "label_color": "#000000",
        "tick_color": "#000000",
        "filename": "psychrometric_chart1"
    }

    # Use the Agg backend for non-interactive environments
    plt.switch_backend("Agg")

    # Define the range for dry-bulb temperature (°C) and specific humidity
    # ratio (kg water/kg dry air)
    dbt_range = np.linspace(0, 45, 100)  # Dry-bulb temperature range
    hr_range = np.linspace(0, 0.03, 100)  # Humidity ratio range (kg/kg)

    # Create a meshgrid for Dry Bulb Temperature (DBT) and Humidity Ratio (HR)
    DBT, HR = np.meshgrid(dbt_range, hr_range)

    # Initialize arrays for Relative Humidity (RH), Wet Bulb Temperature
    # (WBT), Vapor Pressure (VP), Enthalpy (Enth), and Dew Point (DP)
    RH = np.zeros_like(DBT)
    WBT = np.zeros_like(DBT)
    VP = np.zeros_like(DBT)  # Vapor Pressure in Pascals
    Enth = np.zeros_like(DBT)  # Enthalpy in kJ/kg dry air
    DP = np.zeros_like(DBT)  # Dew Point in °C
    SH = np.zeros_like(DBT)  # Specific Humidity in g/kg

    # Air pressure (standard)
    pressure = 101325  # in Pascals

    # Calculate psychrometric properties
    for i in range(DBT.shape[0]):
        for j in range(DBT.shape[1]):
            RH[i, j] = (
                psy.GetRelHumFromHumRatio(DBT[i, j], HR[i, j], pressure) * 100
            )  # RH in percentage
            WBT[i, j] = psy.GetTWetBulbFromHumRatio(
                DBT[i, j], HR[i, j], pressure
            )  # Wet Bulb Temperature in °C
            VP[i, j] = psy.GetVapPresFromHumRatio(
                HR[i, j], pressure
            )  # Vapor Pressure in Pascals
            Enth[i, j] = (
                psy.GetMoistAirEnthalpy(DBT[i, j], HR[i, j]) / 1000
            )  # Enthalpy in kJ/kg
            DP[i, j] = psy.GetTDewPointFromHumRatio(
                DBT[i, j], HR[i, j], pressure
            )  # Dew Point in °C
            SH[i, j] = HR[i, j] * 1000  # Convert kg/kg to g/kg

    # Mask values where RH is greater than 100%
    RH_masked = np.ma.masked_where(RH > 110, RH)
    WBT_masked = np.ma.masked_where(RH > 100, WBT)
    SH_masked = np.ma.masked_where(RH > 100, SH)
    DBT_masked = np.ma.masked_where(RH > 100, DBT)

    specific_temp = indoor_temperature  # °C
    specific_rh = indoor_humidity

    # Calculate specific properties at the specified temperature and humidity
    specific_hr = psy.GetHumRatioFromRelHum(
        specific_temp, specific_rh / 100, pressure
    )  # Specific humidity
    specific_sh = specific_hr * 1000  # Convert kg/kg to g/kg
    specific_vp = psy.GetVapPresFromHumRatio(
        specific_hr, pressure)  # Vapor Pressure
    specific_enthalpy = (
        psy.GetMoistAirEnthalpy(specific_temp, specific_hr) / 1000
    )  # Enthalpy in kJ/kg
    specific_dp = psy.GetTDewPointFromHumRatio(
        specific_temp, specific_hr, pressure
    )  # Dew Point in °C
    specific_wbt = psy.GetTWetBulbFromHumRatio(
        specific_temp, specific_hr, pressure
    )  # Wet Bulb Temperature

    # Calculate coordinates for the specific point
    specific_point_x = specific_temp  # DBT
    specific_point_y = specific_hr  # HR

    # Define comfort zone vertices and other zones
    comfort_zone_vertices = [
        (20, 0.005),
        (29, 0.010),  # Updated to 29°C
        (29, 0.015),  # Updated to 29°C
        (23, 0.015),
        (18, 0.010),
    ]
    passive_solar_vertices = [(0, 0.003), (5, 0.005), (10, 0.007), (5, 0.002)]
    active_solar_vertices = [(0, 0.002), (5, 0.002), (5, 0.003), (0, 0.003)]
    humidification_vertices = [
        (18, 0.002), (23, 0.002), (23, 0.005), (18, 0.005)]
    internal_gains_vertices = [
        (15, 0.005), (20, 0.005), (20, 0.007), (15, 0.007)]
    air_conditioning_dehumidification_vertices = [
        (30, 0.010),
        (35, 0.015),
        (45, 0.020),
        (45, 0.010),
    ]
    natural_ventilation_vertices = [
        (20, 0.005), (30, 0.008), (30, 0.015), (25, 0.010)]
    evaporative_cooling_vertices = [
        (35, 0.008), (45, 0.012), (45, 0.018), (35, 0.015)]
    mass_cooling_vertices = [(30, 0.010), (35, 0.014),
                             (45, 0.020), (40, 0.010)]
    mass_cooling_night_ventilation_vertices = [
        (30, 0.015),
        (35, 0.020),
        (45, 0.025),
        (35, 0.018),
    ]
    winter_vertices = [(0, 0.002), (5, 0.003), (10, 0.005), (5, 0.001)]

    # Define zone actions
    def get_action_items(zone_label):
        actions = {
            "COMFORT ZONE": "No action needed, conditions are comfortable.",
            "PASSIVE SOLAR HEATING": "Increase solar exposure for natural heating.",
            "ACTIVE SOLAR HEATING": "Activate solar heating systems.",
            "HUMIDIFICATION": "Increase humidity using a humidifier.",
            "INTERNAL GAINS": "Utilize internal heat sources.",
            "AIR-CONDITIONING & DEHUMIDIFICATION": "Activate air-conditioning and dehumidification systems.",
            "NATURAL VENTILATION": "Open windows for natural ventilation.",
            "EVAPORATIVE COOLING": "Utilize evaporative cooling techniques.",
            "MASS COOLING": "Consider mass cooling systems.",
            "MASS COOLING & NIGHT VENTILATION": "Use mass cooling with night ventilation.",
            "WINTER HEATING": "Use heating systems to maintain comfort.",
        }
        return actions.get(zone_label, "No specific action required.")

    # Check which zone the specific point falls into
    def check_zone(x, y):
        if Polygon(comfort_zone_vertices).contains_point((x, y)):
            return "COMFORT ZONE", comfort_zone_vertices
        if Polygon(passive_solar_vertices).contains_point((x, y)):
            return "PASSIVE SOLAR HEATING", passive_solar_vertices
        if Polygon(active_solar_vertices).contains_point((x, y)):
            return "ACTIVE SOLAR HEATING", active_solar_vertices
        if Polygon(humidification_vertices).contains_point((x, y)):
            return "HUMIDIFICATION", humidification_vertices
        if Polygon(internal_gains_vertices).contains_point((x, y)):
            return "INTERNAL GAINS", internal_gains_vertices
        if Polygon(air_conditioning_dehumidification_vertices).contains_point(
                (x, y)):
            return (
                "AIR-CONDITIONING & DEHUMIDIFICATION",
                air_conditioning_dehumidification_vertices,
            )
        if Polygon(natural_ventilation_vertices).contains_point((x, y)):
            return "NATURAL VENTILATION", natural_ventilation_vertices
        if Polygon(evaporative_cooling_vertices).contains_point((x, y)):
            return "EVAPORATIVE COOLING", evaporative_cooling_vertices
        if Polygon(mass_cooling_vertices).contains_point((x, y)):
            return "MASS COOLING", mass_cooling_vertices
        if Polygon(mass_cooling_night_ventilation_vertices).contains_point(
                (x, y)):
            return (
                "MASS COOLING & NIGHT VENTILATION",
                mass_cooling_night_ventilation_vertices,
            )
        if Polygon(winter_vertices).contains_point((x, y)):
            return "WINTER HEATING", winter_vertices
        return "AIR-CONDITIONING & DEHUMIDIFICATION", None

    # Get the zone and action items for the specific point
    zone_label, zone_vertices = check_zone(specific_point_x, specific_point_y)
    action_items = get_action_items(zone_label)

    # Plotting the psychrometric chart for color scheme 1
    fig, ax1 = plt.subplots(
        figsize=(
            12, 10), facecolor=color_scheme_1["facecolor"], edgecolor=color_scheme_1["edgecolor"])

    # Set background color
    ax1.set_facecolor(color_scheme_1["facecolor"])

    # Add contour lines for Specific Humidity (SH) only below 100% RH
    CS_SH = plt.contour(
        DBT,
        HR,
        SH_masked,
        levels=np.arange(0, 31, 5),
        colors=color_scheme_1["contour_color"],
        linestyles="dotted",
        alpha=0.5,
    )
    plt.clabel(
        CS_SH,
        inline=True,
        fontsize=8,
        fmt="%1.0f g/kg SH",
        colors=color_scheme_1["contour_color"])

    # Add contour lines for Wet-Bulb Temperature (WBT) only below 100% RH
    CS_WBT = plt.contour(
        DBT,
        HR,
        WBT_masked,
        levels=np.arange(0, 31, 5),
        colors=color_scheme_1["contour_color"],
        linestyles="solid",
        alpha=0.5,
    )
    plt.clabel(
        CS_WBT,
        inline=True,
        fontsize=8,
        fmt="%1.0f°C WBT",
        colors=color_scheme_1["contour_color"])

    # Add contour lines for relative humidity (RH)
    CS_RH_100 = ax1.contour(
        DBT,
        HR,
        RH_masked,
        levels=[100],
        colors=color_scheme_1["contour_color"],
        linestyles="solid",
        alpha=1.0)  # 100% RH solid
    ax1.clabel(
        CS_RH_100,
        inline=True,
        fontsize=10,
        fmt="%1.0f%% RH",
        colors=color_scheme_1["contour_color"])
    CS_RH = ax1.contour(
        DBT,
        HR,
        RH_masked,
        levels=np.arange(10, 100, 10),
        colors=color_scheme_1["contour_color"],
        linestyles="dashed",
        alpha=0.5,
    )  # RH < 100 dashed
    ax1.clabel(CS_RH, inline=True, fontsize=10, fmt="%.0f%%", colors=color_scheme_1["contour_color"])

    # Add contour lines for Dry Bulb Temperature (DBT) only below 100% RH
    CS_DBT = plt.contour(
        DBT,
        HR,
        DBT_masked,
        levels=np.arange(0, 46, 5),
        colors=color_scheme_1["contour_color"],
        linestyles="solid",
        alpha=0.5,
    )
    plt.clabel(
        CS_DBT,
        inline=True,
        fontsize=8,
        fmt="%1.0f°C DBT",
        colors=color_scheme_1["contour_color"])

    # Always fill the comfort zone with light green
    comfort_polygon = Polygon(
        comfort_zone_vertices, closed=True, color=color_scheme_1["comfort_color"], alpha=0.4
    )  # Light green color for comfort zone
    ax1.add_patch(comfort_polygon)

    # Display the comfort zone label in the center of the filled zone
    x_coords, y_coords = zip(*comfort_zone_vertices)
    ax1.text(
        np.mean(x_coords),
        np.mean(y_coords),
        "COMFORT ZONE",
        ha="center",
        va="center",
        fontsize=9,
        color=color_scheme_1["text_color"],
        weight="bold",
    )

    # Fill the zone that the point falls into with light yellow
    if zone_vertices and zone_label != "COMFORT ZONE":
        polygon = Polygon(
            zone_vertices, closed=True, color=color_scheme_1["zone_color"], alpha=0.5
        )  # Light color that adapts well with green
        ax1.add_patch(polygon)

        # Display the zone label in the center of the filled zone
        x_coords, y_coords = zip(*zone_vertices)
        ax1.text(
            np.mean(x_coords),
            np.mean(y_coords),
            zone_label,
            ha="center",
            va="center",
            fontsize=10,
            color=color_scheme_1["text_color"],
            weight="bold",
        )

    # Plot the specific point (only showing DBT temperature)
    point_color = "palegreen" if zone_label == "COMFORT ZONE" else "red"
    ax1.plot(
        specific_point_x,
        specific_hr,
        "o",
        markersize=14,
        color=point_color,
        zorder=30)

    # Add four side dotted arrow marks around the specific point in red color
    arrow_length = 0.0015  # Length of the arrow in the same units as the plot
    arrow_props = dict(
        arrowstyle="->", color=point_color, linestyle="dotted", linewidth=3
    )

    # Top arrow
    ax1.add_patch(
        FancyArrowPatch(
            posA=(specific_point_x, specific_hr),
            posB=(specific_point_x, specific_hr + arrow_length),
            **arrow_props,
        )
    )

    # Bottom arrow
    ax1.add_patch(
        FancyArrowPatch(
            posA=(specific_point_x, specific_hr),
            posB=(specific_point_x, specific_hr - arrow_length),
            **arrow_props,
        )
    )

    # Update annotation text in the top left corner (keeping it the same)
    annotation_text = (
        f"Specific Point Calculations:\n"
        f"Temperature: {specific_temp} °C\n"
        f"Relative Humidity: {specific_rh} %\n"
        f"Specific Humidity: {specific_sh:.2f} g/kg\n"
        f"Vapor Pressure: {specific_vp:.2f} Pa\n"
        f"Enthalpy: {specific_enthalpy:.2f} kJ/kg\n"
        f"Dew Point: {specific_dp:.2f} °C\n"
        f"Wet Bulb Temperature: {specific_wbt:.2f} °C\n"
        f"Zone: {zone_label}\n"
        f"Action: {action_items}"
    )
    # Add action items text box
    # textstr = "\n".join(
    #     [
    #         f"{key}: {value}"
    #         for key, value in {
    #             "Temperature (°C)": f"{specific_temp:.0f}",
    #             "Relative Humidity": f"{specific_rh:.0f} %",
    #             "Absolute Humidity (g/kg)": f"{specific_sh:.2f}",
    #             "Wet Bulb Temp (°C)": f"{specific_wbt:.2f}",
    #             "Dew Point (°C)": f"{specific_dp:.2f}",
    #             "Vapor Pressure (Pa)": f"{specific_vp:.2f}",
    #             "Enthalpy (kJ/kg)": f"{specific_enthalpy:.2f}",
    #             "Zone": zone_label,
    #             "Action": action_items,
    #         }.items()
    #     ]
    # )

    # Update the text box to remove the outline or change the background color
    # ax1.text(
    #     0.02,
    #     0.95,
    #     textstr,
    #     transform=ax1.transAxes,
    #     fontsize=12,
    #     verticalalignment="top",
    #     bbox=dict(boxstyle="round,pad=0.5", facecolor="#282828", alpha=0.99, edgecolor="#282828"),  # No outline
    #     color='white'
    # )
    # Add labels and title
    # ax1.set_title("Psychrometric Chart ", fontsize=20, color='white')
    ax1.set_xlabel(
        "Dry Bulb Temperature (°C)", fontsize=14, color=color_scheme_1["label_color"], labelpad=10
    )
    ax1.set_ylabel(
        "Humidity Ratio (kg water/kg dry air)",
        fontsize=14,
        color=color_scheme_1["label_color"],
        labelpad=10,
    )
    ax1.set_xlim(0, 45)
    ax1.set_ylim(0, 0.03)

    # Set the color of the x-axis and y-axis values to white
    # Add padding to x-axis ticks
    ax1.tick_params(axis="x", colors=color_scheme_1["tick_color"], pad=25)
    # Add padding to y-axis ticks
    ax1.tick_params(axis="y", colors=color_scheme_1["tick_color"], pad=25)

    # Create a secondary y-axis for Specific Humidity
    ax2 = ax1.twinx()
    ax2.set_ylabel(
        "Specific Humidity (g/kg)", fontsize=14, color=color_scheme_1["label_color"], labelpad=10
    )  # Label for the secondary y-axis
    ax2.tick_params(
        axis="y", labelcolor=color_scheme_1["tick_color"], pad=25
    )  # Add padding to secondary y-axis ticks

    # Create the folder if it doesn't exist
    plot_folder = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(plot_folder, exist_ok=True)

    # Define the paths for the PNG and SVG files
    png_path = os.path.join(plot_folder, f"{color_scheme_1['filename']}.png")
    svg_path = os.path.join(plot_folder, f"{color_scheme_1['filename']}.svg")

    # Debug print statements
    print(f"Saving chart1 to PNG: {png_path}")
    print(f"Saving chart1 to SVG: {svg_path}")

    # Remove the existing SVG file if it exists
    if os.path.exists(svg_path):
        os.remove(svg_path)

    # Save the plot as PNG and SVG
    plt.savefig(png_path, facecolor=color_scheme_1["facecolor"], edgecolor=color_scheme_1["edgecolor"])
    plt.savefig(svg_path, facecolor=color_scheme_1["facecolor"], edgecolor=color_scheme_1["edgecolor"])

    # Convert the plot to a base64-encoded PNG image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64_1 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    # Create a JSON object with the base64-encoded image and annotations
    plot_json_1 = {"image": image_base64_1, "annotations": annotation_text}

    # Plotting the psychrometric chart for color scheme 2
    fig, ax1 = plt.subplots(
        figsize=(
            12, 10), facecolor=color_scheme_2["facecolor"], edgecolor=color_scheme_2["edgecolor"])

    # Set background color
    ax1.set_facecolor(color_scheme_2["facecolor"])

    # Add contour lines for Specific Humidity (SH) only below 100% RH
    CS_SH = plt.contour(
        DBT,
        HR,
        SH_masked,
        levels=np.arange(0, 31, 5),
        colors=color_scheme_2["contour_color"],
        linestyles="dotted",
        alpha=0.5,
    )
    plt.clabel(
        CS_SH,
        inline=True,
        fontsize=8,
        fmt="%1.0f g/kg SH",
        colors=color_scheme_2["contour_color"])

    # Add contour lines for Wet-Bulb Temperature (WBT) only below 100% RH
    CS_WBT = plt.contour(
        DBT,
        HR,
        WBT_masked,
        levels=np.arange(0, 31, 5),
        colors=color_scheme_2["contour_color"],
        linestyles="solid",
        alpha=0.5,
    )
    plt.clabel(
        CS_WBT,
        inline=True,
        fontsize=8,
        fmt="%1.0f°C WBT",
        colors=color_scheme_2["contour_color"])

    # Add contour lines for relative humidity (RH)
    CS_RH_100 = ax1.contour(
        DBT,
        HR,
        RH_masked,
        levels=[100],
        colors=color_scheme_2["contour_color"],
        linestyles="solid",
        alpha=1.0)  # 100% RH solid
    ax1.clabel(
        CS_RH_100,
        inline=True,
        fontsize=10,
        fmt="%1.0f%% RH",
        colors=color_scheme_2["contour_color"])
    CS_RH = ax1.contour(
        DBT,
        HR,
        RH_masked,
        levels=np.arange(10, 100, 10),
        colors=color_scheme_2["contour_color"],
        linestyles="dashed",
        alpha=0.5,
    )  # RH < 100 dashed
    ax1.clabel(CS_RH, inline=True, fontsize=10, fmt="%.0f%%", colors=color_scheme_2["contour_color"])

    # Add contour lines for Dry Bulb Temperature (DBT) only below 100% RH
    CS_DBT = plt.contour(
        DBT,
        HR,
        DBT_masked,
        levels=np.arange(0, 46, 5),
        colors=color_scheme_2["contour_color"],
        linestyles="solid",
        alpha=0.5,
    )
    plt.clabel(
        CS_DBT,
        inline=True,
        fontsize=8,
        fmt="%1.0f°C DBT",
        colors=color_scheme_2["contour_color"])

    # Always fill the comfort zone with light green
    comfort_polygon = Polygon(
        comfort_zone_vertices, closed=True, color=color_scheme_2["comfort_color"], alpha=0.4
    )  # Light green color for comfort zone
    ax1.add_patch(comfort_polygon)

    # Display the comfort zone label in the center of the filled zone
    x_coords, y_coords = zip(*comfort_zone_vertices)
    ax1.text(
        np.mean(x_coords),
        np.mean(y_coords),
        "COMFORT ZONE",
        ha="center",
        va="center",
        fontsize=9,
        color=color_scheme_2["text_color"],
        weight="bold",
    )

    # Fill the zone that the point falls into with light yellow
    if zone_vertices and zone_label != "COMFORT ZONE":
        polygon = Polygon(
            zone_vertices, closed=True, color=color_scheme_2["zone_color"], alpha=0.5
        )  # Light color that adapts well with green
        ax1.add_patch(polygon)

        # Display the zone label in the center of the filled zone
        x_coords, y_coords = zip(*zone_vertices)
        ax1.text(
            np.mean(x_coords),
            np.mean(y_coords),
            zone_label,
            ha="center",
            va="center",
            fontsize=10,
            color=color_scheme_2["text_color"],
            weight="bold",
        )

    # Plot the specific point (only showing DBT temperature)
    point_color = "palegreen" if zone_label == "COMFORT ZONE" else "red"
    ax1.plot(
        specific_point_x,
        specific_hr,
        "o",
        markersize=14,
        color=point_color,
        zorder=30)

    # Add four side dotted arrow marks around the specific point in red color
    arrow_length = 0.0015  # Length of the arrow in the same units as the plot
    arrow_props = dict(
        arrowstyle="->", color=point_color, linestyle="dotted", linewidth=3
    )

    # Top arrow
    ax1.add_patch(
        FancyArrowPatch(
            posA=(specific_point_x, specific_hr),
            posB=(specific_point_x, specific_hr + arrow_length),
            **arrow_props,
        )
    )

    # Bottom arrow
    ax1.add_patch(
        FancyArrowPatch(
            posA=(specific_point_x, specific_hr),
            posB=(specific_point_x, specific_hr - arrow_length),
            **arrow_props,
        )
    )

    # Update annotation text in the top left corner (keeping it the same)
    annotation_text = (
        f"Specific Point Calculations:\n"
        f"Temperature: {specific_temp} °C\n"
        f"Relative Humidity: {specific_rh} %\n"
        f"Specific Humidity: {specific_sh:.2f} g/kg\n"
        f"Vapor Pressure: {specific_vp:.2f} Pa\n"
        f"Enthalpy: {specific_enthalpy:.2f} kJ/kg\n"
        f"Dew Point: {specific_dp:.2f} °C\n"
        f"Wet Bulb Temperature: {specific_wbt:.2f} °C\n"
        f"Zone: {zone_label}\n"
        f"Action: {action_items}"
    )
    # Add action items text box
    # textstr = "\n".join(
    #     [
    #         f"{key}: {value}"
    #         for key, value in {
    #             "Temperature (°C)": f"{specific_temp:.0f}",
    #             "Relative Humidity": f"{specific_rh:.0f} %",
    #             "Absolute Humidity (g/kg)": f"{specific_sh:.2f}",
    #             "Wet Bulb Temp (°C)": f"{specific_wbt:.2f}",
    #             "Dew Point (°C)": f"{specific_dp:.2f}",
    #             "Vapor Pressure (Pa)": f"{specific_vp:.2f}",
    #             "Enthalpy (kJ/kg)": f"{specific_enthalpy:.2f}",
    #             "Zone": zone_label,
    #             "Action": action_items,
    #         }.items()
    #     ]
    # )

    # Update the text box to remove the outline or change the background color
    # ax1.text(
    #     0.02,
    #     0.95,
    #     textstr,
    #     transform=ax1.transAxes,
    #     fontsize=12,
    #     verticalalignment="top",
    #     bbox=dict(boxstyle="round,pad=0.5", facecolor="#282828", alpha=0.99, edgecolor="#282828"),  # No outline
    #     color='white'
    # )
    # Add labels and title
    # ax1.set_title("Psychrometric Chart ", fontsize=20, color='white')
    ax1.set_xlabel(
        "Dry Bulb Temperature (°C)", fontsize=14, color=color_scheme_2["label_color"], labelpad=10
    )
    ax1.set_ylabel(
        "Humidity Ratio (kg water/kg dry air)",
        fontsize=14,
        color=color_scheme_2["label_color"],
        labelpad=10,
    )
    ax1.set_xlim(0, 45)
    ax1.set_ylim(0, 0.03)

    # Set the color of the x-axis and y-axis values to white
    # Add padding to x-axis ticks
    ax1.tick_params(axis="x", colors=color_scheme_2["tick_color"], pad=25)
    # Add padding to y-axis ticks
    ax1.tick_params(axis="y", colors=color_scheme_2["tick_color"], pad=25)

    # Create a secondary y-axis for Specific Humidity
    ax2 = ax1.twinx()
    ax2.set_ylabel(
        "Specific Humidity (g/kg)", fontsize=14, color=color_scheme_2["label_color"], labelpad=10
    )  # Label for the secondary y-axis
    ax2.tick_params(
        axis="y", labelcolor=color_scheme_2["tick_color"], pad=25
    )  # Add padding to secondary y-axis ticks

    # Create the folder if it doesn't exist
    plot_folder = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(plot_folder, exist_ok=True)

    # Define the paths for the PNG and SVG files
    png_path = os.path.join(plot_folder, f"{color_scheme_2['filename']}.png")
    svg_path = os.path.join(plot_folder, f"{color_scheme_2['filename']}.svg")
    plt.savefig(png_path)
    plt.savefig(svg_path)

    # Convert the plot to a base64-encoded PNG image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64_2 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    # Create a JSON object with the base64-encoded image and annotations
    plot_json = {"image": image_base64_2, "annotations": annotation_text}

    # Return the JSON object if needed
    return plot_json, zone_label, action_items