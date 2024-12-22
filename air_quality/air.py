"""
Flask API for Indoor Air Quality (IAQ) Data
"""

import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import certifi
import requests
from cachetools import TTLCache, cached
from dotenv import load_dotenv
from flask import Flask, Response, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from plot import generate_psychrometric_chart

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Get the API base URL and token from the environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")

# Construct the full API URL
API_URL = f"{API_BASE_URL}?token={API_TOKEN}"

# Create a cache with a TTL of 5 minutes
cache = TTLCache(maxsize=100, ttl=300)

# Create a thread pool executor for concurrent tasks
executor = ThreadPoolExecutor(max_workers=5)


def load_db_config(
    config_file="./config.js",
):
    """
    Load database configuration from a JSON file.
    """
    with open(config_file, "r") as file:
        config = json.load(file)
    return config["database"]


def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using SSL.
    """
    config = load_db_config()
    user = config["user"]
    password = config["password"]
    host = config["host"]
    port = config["port"]
    dbname = config["dbname"]

    # Construct the connection string with SSL mode enabled
    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"

    try:
        engine = create_engine(
            connection_string,
            pool_size=10,
            max_overflow=20)
        connection = engine.connect()
        return connection
    except SQLAlchemyError as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None


@cached(cache)
def fetch_indoor_air_quality():
    """
    Fetch indoor air quality data from the PostgreSQL database.
    """
    connection = get_db_connection()
    if not connection:
        return None

    query = text(
        """
        SELECT reading_name, answer_value, updated_on
        FROM public.dw_reading_latest
        WHERE device_id = '3030'
        AND reading_name IN ('bmet_c', 'bmeh','bmep','senpm1p0', 'senpm2p5','o3','co','bmeiaq')
    """
    )

    try:
        result = connection.execute(query)
        readings = result.fetchall()

        temperature = None
        humidity = None
        pm1 = None
        pm25 = None
        o3 = None
        co = None
        iaq = None
        updated_on = None

        for reading in readings:
            if reading[0] == "bmet_c":
                temperature = reading[1]
                updated_on = reading[2]
            elif reading[0] == "bmeh":
                humidity = reading[1]
                updated_on = reading[2]
            elif reading[0] == "bmep":
                bmep = reading[1]
                updated_on = reading[2]
            elif reading[0] == "senpm1p0":
                pm1 = reading[1]
                updated_on = reading[2]
            elif reading[0] == "senpm2p5":
                pm25 = reading[1]
                updated_on = reading[2]
            elif reading[0] == "o3":
                o3 = reading[1]
                updated_on = reading[2]
            elif reading[0] == "co":
                co = reading[1]
                updated_on = reading[2]
            elif reading[0] == "bmeiaq":
                iaq = reading[1]
                updated_on = reading[2]

        bmep = round(bmep / 1000, 2)

        # Convert updated_on to IST
        if updated_on:
            updated_on_ist = updated_on + timedelta(hours=5, minutes=30)
            updated_on_str = updated_on_ist.strftime("%H:%M:%S")
        else:
            updated_on_str = None

        response = {
            "temperature": round(
                temperature,
                2) if temperature is not None else None,
            "humidity": round(
                humidity,
                2) if humidity is not None else None,
            "pressure": bmep if bmep is not None else None,
            "pm1": round(
                pm1,
                2) if pm1 is not None else None,
            "pm25": round(
                pm25,
                2) if pm25 is not None else None,
            "o3": round(
                o3,
                2) if o3 is not None else None,
            "co": round(
                co,
                2) if co is not None else None,
            "aqi": round(
                iaq,
                2) if iaq is not None else None,
            "updated_on": updated_on_str,
        }

        return response

    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        connection.close()


@cached(cache)
def fetch_air_quality_data(api_url):
    """
    Fetch air quality data from the WAQI API with caching.
    """
    try:
        with requests.Session() as session:
            response = session.get(api_url, verify=certifi.where())
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def parse_air_quality_data(data):
    """
    Parse the air quality data from the JSON response.
    """
    if data["status"] != "ok":
        print("Error: API status is not 'ok'")
        return None

    try:
        aqi = data["data"]["aqi"]
        temp = data["data"]["iaqi"]["t"]["v"]
        humidity = data["data"]["iaqi"]["h"]["v"]
        pressure = data["data"]["iaqi"]["p"]["v"]
        pm1 = data["data"]["iaqi"]["pm10"]["v"]
        pm25 = data["data"]["iaqi"]["pm25"]["v"]
        co = data["data"]["iaqi"]["co"]["v"]
        o3 = data["data"]["iaqi"]["o3"]["v"]
        city_name = data["data"]["city"]["name"]

        return {
            "city": city_name,
            "aqi": round(aqi, 2) if aqi is not None else None,
            "temperature": round(temp, 2) if temp is not None else None,
            "pressure": round(pressure, 2) if pressure is not None else None,
            "humidity": round(humidity, 2) if humidity is not None else None,
            "pm1": round(pm1, 2) if pm1 is not None else None,
            "pm25": round(pm25, 2) if pm25 is not None else None,
            "co": round(co, 2) if co is not None else None,
            "o3": round(o3, 2) if o3 is not None else None,
        }
    except KeyError as e:
        print(f"Error parsing data: Missing key {e}")
        return None


async def get_air_quality_async():
    """
    Asynchronous function to fetch and return air quality data as a JSON response.
    """
    loop = asyncio.get_event_loop()

    indoor_data = await loop.run_in_executor(executor, fetch_indoor_air_quality)
    if indoor_data is None:
        return jsonify(
            {"error": "Failed to fetch indoor air quality data"}), 500

    indoor_temperature = indoor_data.get("temperature")
    indoor_humidity = indoor_data.get("humidity")
    indoor_pressure = indoor_data.get(
        "pressure") * 1000  # Convert to correct unit

    try:
        plot_json, zone_label, action_items = await loop.run_in_executor(
            executor,
            generate_psychrometric_chart,
            indoor_temperature,
            indoor_humidity,
            indoor_pressure,
        )
    except Exception as e:
        print(f"Error generating psychrometric chart: {e}")
        return jsonify(
            {"error": "Failed to generate psychrometric chart"}), 500

    outdoor_data = await loop.run_in_executor(executor, fetch_air_quality_data, API_URL)
    if outdoor_data is not None:
        air_quality_data = parse_air_quality_data(outdoor_data)
        if air_quality_data is not None:
            response = [
                ("Indoor", indoor_data),
                (
                    "Outdoor",
                    {
                        "city": air_quality_data["city"],
                        "aqi": air_quality_data["aqi"],
                        "temperature": air_quality_data["temperature"],
                        "pressure": air_quality_data["pressure"],
                        "humidity": air_quality_data["humidity"],
                        "pm1": air_quality_data["pm1"],
                        "pm25": air_quality_data["pm25"],
                        "co": air_quality_data["co"],
                        "o3": air_quality_data["o3"],
                        "zone": zone_label,
                        "image": plot_json,
                        "action": action_items,
                    },
                ),
            ]
            response_json = json.dumps(response)
            return Response(response_json, content_type="application/json")
        else:
            return jsonify(
                {"error": "Failed to parse outdoor air quality data"}), 500
    else:
        return jsonify(
            {"error": "Failed to fetch outdoor air quality data"}), 500


@app.route("/air-quality", methods=["GET"])
async def get_air_quality():
    """
    Flask route to fetch and return air quality data as a JSON response.
    """
    return await get_air_quality_async()


if __name__ == "__main__":
    app.run(port=5010, debug=True)
