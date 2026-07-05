"""
mcp/traffic_server.py
"""

import pandas as pd

from models.road import Road


class TrafficServer:

    def __init__(self, csv_path="data/roads.csv"):

        self.csv_path = csv_path

        self.roads = {}

        self.load()

    # ---------------------------------------------------------

    def load(self):

        df = pd.read_csv(self.csv_path)

        self.roads.clear()

        for _, row in df.iterrows():

            road = Road(

                road_id=row["road_id"],

                road_name=row["road_name"],

                area_id=row["area_id"],

                start_area=row["start_area"],

                end_area=row["end_area"],

                traffic_level=row["traffic_level"],

                water_level=float(row["water_level"]),

                is_blocked=bool(row["is_blocked"]),

                travel_time=int(row["travel_time"])

            )

            self.roads.setdefault(
                row["area_id"],
                []
            ).append(road)

    # ---------------------------------------------------------

    def get_roads(self, area_id):

        return self.roads.get(area_id, [])

    # ---------------------------------------------------------

    def get_all_roads(self):

        return self.roads

    # ---------------------------------------------------------

    def update_traffic(
        self,
        road_id,
        traffic_level=None,
        water_level=None,
        is_blocked=None,
        travel_time=None
    ):

        for roads in self.roads.values():

            for road in roads:

                if road.road_id == road_id:

                    if traffic_level is not None:
                        road.traffic_level = traffic_level

                    if water_level is not None:
                        road.water_level = water_level

                    if is_blocked is not None:
                        road.is_blocked = is_blocked

                    if travel_time is not None:
                        road.travel_time = travel_time

                    return True

        return False

    # ---------------------------------------------------------

    def get_blocked_roads(self):

        blocked = []

        for roads in self.roads.values():

            for road in roads:

                if road.is_blocked:

                    blocked.append(road)

        return blocked

    # ---------------------------------------------------------

    def save(self):

        rows = []

        for roads in self.roads.values():

            for road in roads:

                rows.append({

                    "road_id": road.road_id,

                    "road_name": road.road_name,

                    "area_id": road.area_id,

                    "start_area": road.start_area,

                    "end_area": road.end_area,

                    "traffic_level": road.traffic_level,

                    "water_level": road.water_level,

                    "is_blocked": road.is_blocked,

                    "travel_time": road.travel_time

                })

        pd.DataFrame(rows).to_csv(
            self.csv_path,
            index=False
        )