from mcp_servers.allocation.tools import perform_allocation


def main() -> None:

    resources = {
        "ambulances": 18,
        "medical_teams": 10,
        "fire_trucks": 6,
        "boats": 8,
        "helicopters": 2,
        "food_packets": 5000,
        "water_liters": 12000,
    }

    result = perform_allocation(
        disaster_type="Flood",
        severity="High",
        affected_people=25000,
        available_resources=resources,
    )

    print(result)


if __name__ == "__main__":
    main()