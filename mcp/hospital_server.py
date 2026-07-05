"""
mcp/hospital_server.py
"""

import pandas as pd

from models.hospital import Hospital


class HospitalServer:

    def __init__(self, csv_path="data/hospitals.csv"):

        self.csv_path = csv_path

        self.hospitals = {}

        self.load()

    # ---------------------------------------------------------

    def load(self):

        df = pd.read_csv(self.csv_path)

        self.hospitals.clear()

        for _, row in df.iterrows():

            hospital = Hospital(

                hospital_id=row["hospital_id"],

                name=row["name"],

                area_id=row["area_id"],

                latitude=float(row["latitude"]),

                longitude=float(row["longitude"]),

                total_beds=int(row["total_beds"]),

                available_beds=int(row["available_beds"]),

                icu_beds=int(row["icu_beds"]),

                emergency_capacity=int(row["emergency_capacity"])

            )

            self.hospitals.setdefault(
                row["area_id"],
                []
            ).append(hospital)

    # ---------------------------------------------------------

    def get_hospitals(self, area_id):

        return self.hospitals.get(area_id, [])

    # ---------------------------------------------------------

    def get_all_hospitals(self):

        return self.hospitals

    # ---------------------------------------------------------

    def update_available_beds(
        self,
        hospital_id,
        beds
    ):

        for hospitals in self.hospitals.values():

            for hospital in hospitals:

                if hospital.hospital_id == hospital_id:

                    hospital.available_beds = beds

                    return True

        return False

    # ---------------------------------------------------------

    def reserve_beds(
        self,
        hospital_id,
        beds
    ):

        for hospitals in self.hospitals.values():

            for hospital in hospitals:

                if hospital.hospital_id == hospital_id:

                    if hospital.available_beds < beds:

                        return False

                    hospital.available_beds -= beds

                    return True

        return False

    # ---------------------------------------------------------

    def release_beds(
        self,
        hospital_id,
        beds
    ):

        for hospitals in self.hospitals.values():

            for hospital in hospitals:

                if hospital.hospital_id == hospital_id:

                    hospital.available_beds = min(
                        hospital.total_beds,
                        hospital.available_beds + beds
                    )

                    return True

        return False

    # ---------------------------------------------------------

    def save(self):

        rows = []

        for hospitals in self.hospitals.values():

            for hospital in hospitals:

                rows.append({

                    "hospital_id": hospital.hospital_id,

                    "name": hospital.name,

                    "area_id": hospital.area_id,

                    "latitude": hospital.latitude,

                    "longitude": hospital.longitude,

                    "total_beds": hospital.total_beds,

                    "available_beds": hospital.available_beds,

                    "icu_beds": hospital.icu_beds,

                    "emergency_capacity": hospital.emergency_capacity

                })

        pd.DataFrame(rows).to_csv(
            self.csv_path,
            index=False
        )