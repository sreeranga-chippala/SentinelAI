"""
mcp/resource_server.py
"""

import pandas as pd

from models.resource import Resource


class ResourceServer:

    def __init__(self, csv_path="data/resources.csv"):

        self.csv_path = csv_path

        self.resources = self._load()

    # ---------------------------------------------------------

    def _load(self):

        df = pd.read_csv(self.csv_path)

        row = df.iloc[0]

        return Resource(

            rescue_teams=int(row["rescue_teams"]),

            boats=int(row["boats"]),

            ambulances=int(row["ambulances"]),

            helicopters=int(row["helicopters"]),

            food_packets=int(row["food_packets"]),

            medical_kits=int(row["medical_kits"])

        )

    # ---------------------------------------------------------

    def get_resources(self):

        return self.resources

    # ---------------------------------------------------------

    def allocate(

        self,

        rescue_teams,

        boats,

        ambulances,

        helicopters,

        food_packets,

        medical_kits

    ):

        if (

            rescue_teams > self.resources.rescue_teams

            or boats > self.resources.boats

            or ambulances > self.resources.ambulances

            or helicopters > self.resources.helicopters

            or food_packets > self.resources.food_packets

            or medical_kits > self.resources.medical_kits

        ):

            return False

        self.resources.rescue_teams -= rescue_teams

        self.resources.boats -= boats

        self.resources.ambulances -= ambulances

        self.resources.helicopters -= helicopters

        self.resources.food_packets -= food_packets

        self.resources.medical_kits -= medical_kits

        return True

    # ---------------------------------------------------------

    def release(

        self,

        rescue_teams,

        boats,

        ambulances,

        helicopters,

        food_packets,

        medical_kits

    ):

        self.resources.rescue_teams += rescue_teams

        self.resources.boats += boats

        self.resources.ambulances += ambulances

        self.resources.helicopters += helicopters

        self.resources.food_packets += food_packets

        self.resources.medical_kits += medical_kits

    # ---------------------------------------------------------

    def save(self):

        df = pd.DataFrame([{

            "rescue_teams": self.resources.rescue_teams,

            "boats": self.resources.boats,

            "ambulances": self.resources.ambulances,

            "helicopters": self.resources.helicopters,

            "food_packets": self.resources.food_packets,

            "medical_kits": self.resources.medical_kits

        }])

        df.to_csv(

            self.csv_path,

            index=False

        )

    # ---------------------------------------------------------

    def reset(self):

        self.resources = self._load()