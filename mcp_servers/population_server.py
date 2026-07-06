"""
mcp/population_server.py
"""

import pandas as pd

from models.area import Area


class PopulationServer:

    def __init__(self, csv_path="data/population.csv"):

        self.csv_path = csv_path

        self.areas = {}

        self.load()

    # ---------------------------------------------------------

    def load(self):

        df = pd.read_csv(self.csv_path)

        self.areas.clear()

        for _, row in df.iterrows():

            area = Area(

                area_id=row["area_id"],

                name=row["area"],

                population=int(row["population"]),

                children=int(row["children"]),

                adults=int(row["adults"]),

                elderly=int(row["elderly"]),

                disabled=int(row["disabled"]),

                rescue_requests=int(row["rescue_requests"]),

                latitude=float(row["latitude"]),

                longitude=float(row["longitude"])

            )

            self.areas[area.area_id] = area

    # ---------------------------------------------------------

    def get_population(self, area_id):

        return self.areas.get(area_id)

    # ---------------------------------------------------------

    def get_all_population(self):

        return self.areas

    # ---------------------------------------------------------

    def update_rescue_requests(
        self,
        area_id,
        requests
    ):

        if area_id in self.areas:

            self.areas[area_id].rescue_requests = requests

            return True

        return False

    # ---------------------------------------------------------

    def increment_rescue_requests(
        self,
        area_id,
        count=1
    ):

        if area_id in self.areas:

            self.areas[area_id].rescue_requests += count

            return True

        return False

    # ---------------------------------------------------------

    def save(self):

        rows = []

        for area in self.areas.values():

            rows.append({

                "area_id": area.area_id,

                "area": area.name,

                "population": area.population,

                "children": area.children,

                "adults": area.adults,

                "elderly": area.elderly,

                "disabled": area.disabled,

                "rescue_requests": area.rescue_requests,

                "latitude": area.latitude,

                "longitude": area.longitude

            })

        pd.DataFrame(rows).to_csv(
            self.csv_path,
            index=False
        )