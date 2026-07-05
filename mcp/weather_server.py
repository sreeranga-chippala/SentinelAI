"""
mcp/weather_server.py
"""

import pandas as pd

from models.area import Area


class WeatherServer:

    def __init__(self, csv_path="data/weather.csv"):

        self.csv_path = csv_path

        self.weather = {}

        self.load()

    # ---------------------------------------------------------

    def load(self):

        df = pd.read_csv(self.csv_path)

        self.weather.clear()

        for _, row in df.iterrows():

            self.weather[row["area_id"]] = {

                "area": row["area"],

                "rainfall": float(row["rainfall"]),

                "river_level": float(row["river_level"]),

                "humidity": float(row["humidity"]),

                "forecast": row["forecast"]

            }

    # ---------------------------------------------------------

    def get_weather(self, area_id):

        return self.weather.get(area_id)

    # ---------------------------------------------------------

    def get_all_weather(self):

        return self.weather

    # ---------------------------------------------------------

    def update_weather(
        self,
        area_id,
        rainfall,
        river_level,
        humidity,
        forecast
    ):

        if area_id not in self.weather:
            return

        self.weather[area_id]["rainfall"] = rainfall
        self.weather[area_id]["river_level"] = river_level
        self.weather[area_id]["humidity"] = humidity
        self.weather[area_id]["forecast"] = forecast

    # ---------------------------------------------------------

    def save(self):

        rows = []

        for area_id, data in self.weather.items():

            rows.append({

                "area_id": area_id,

                "area": data["area"],

                "rainfall": data["rainfall"],

                "river_level": data["river_level"],

                "humidity": data["humidity"],

                "forecast": data["forecast"]

            })

        pd.DataFrame(rows).to_csv(
            self.csv_path,
            index=False
        )