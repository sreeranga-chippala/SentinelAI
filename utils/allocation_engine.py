"""
utils/allocation_engine.py
"""

from models.allocation_plan import AllocationPlan


class AllocationEngine:

    @staticmethod
    def allocate(
        priority,
        hospitals,
        resources,
    ):

        # -------------------------------------------------
        # Find best hospital (maximum available beds)
        # -------------------------------------------------

        available_hospitals = [

            hospital

            for hospital in hospitals

            if hospital.available_beds > 0

        ]

        if not available_hospitals:

            return AllocationPlan(

                area_id=priority.area_id,

                area_name=priority.area_name,

                assigned_hospital="None",

                beds_allocated=0,

                rescue_teams=0,

                boats=0,

                ambulances=0,

                helicopters=0,

                food_packets=0,

                medical_kits=0,

                success=False,

                message="No hospital beds available"

            )

        selected = max(

            available_hospitals,

            key=lambda hospital: hospital.available_beds

        )

        # -------------------------------------------------
        # Allocation Strategy
        # -------------------------------------------------

        level = priority.priority_level

        rescue = 1
        boats = 0
        ambulances = 1
        helicopters = 0
        beds = 5
        food = 20
        kits = 20

        if level == "Medium":

            rescue = 2
            boats = 1

        elif level == "High":

            rescue = 4
            boats = 2
            ambulances = 2
            beds = 10

        elif level == "Critical":

            rescue = 6
            boats = 3
            ambulances = 3
            helicopters = 1
            beds = 20
            food = 100
            kits = 50

        elif level == "Extreme":

            rescue = 10
            boats = 5
            ambulances = 5
            helicopters = 2
            beds = 40
            food = 300
            kits = 150

        # -------------------------------------------------
        # Respect available resources
        # -------------------------------------------------

        beds = min(

            beds,

            selected.available_beds

        )

        rescue = min(

            rescue,

            resources.rescue_teams

        )

        boats = min(

            boats,

            resources.boats

        )

        ambulances = min(

            ambulances,

            resources.ambulances

        )

        helicopters = min(

            helicopters,

            resources.helicopters

        )

        food = min(

            food,

            resources.food_packets

        )

        kits = min(

            kits,

            resources.medical_kits

        )

        # -------------------------------------------------
        # IMPORTANT
        # -------------------------------------------------
        # No mutation here.
        #
        # Coordinator will call:
        #
        # hospital_server.reserve_beds(...)
        # resource_server.allocate(...)
        # -------------------------------------------------

        return AllocationPlan(

            area_id=priority.area_id,

            area_name=priority.area_name,

            assigned_hospital=selected.name,

            beds_allocated=beds,

            rescue_teams=rescue,

            boats=boats,

            ambulances=ambulances,

            helicopters=helicopters,

            food_packets=food,

            medical_kits=kits,

            success=True,

            message="Allocation Successful"

        )