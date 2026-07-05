"""
utils/hospital_analyzer.py

Analyzes the operational status of a hospital.
"""

from models.hospital_status import HospitalStatus


class HospitalAnalyzer:

    @staticmethod
    def analyze(hospital):

        occupied_beds = hospital.total_beds - hospital.available_beds

        occupancy_percentage = (
            occupied_beds / hospital.total_beds
        ) * 100

        if occupancy_percentage >= 95:
            status = "Full"

        elif occupancy_percentage >= 80:
            status = "Critical"

        elif occupancy_percentage >= 60:
            status = "Busy"

        else:
            status = "Available"

        return HospitalStatus(

            hospital_id=hospital.hospital_id,

            name=hospital.name,

            total_beds=hospital.total_beds,

            available_beds=hospital.available_beds,

            occupied_beds=occupied_beds,

            occupancy_percentage=round(
                occupancy_percentage,
                2
            ),

            icu_beds=hospital.icu_beds,

            emergency_capacity=hospital.emergency_capacity,

            status=status

        )