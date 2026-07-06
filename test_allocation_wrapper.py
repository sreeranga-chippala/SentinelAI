from dotenv import load_dotenv

load_dotenv()

from agents.allocation_agent import AllocationAgent


def main() -> None:

    agent = AllocationAgent()

    response = agent.run(
        """
        Allocate disaster resources.

        Disaster Type: Flood
        Severity: High
        Affected People: 25000

        Available Resources:

        Ambulances: 18
        Medical Teams: 10
        Fire Trucks: 6
        Boats: 8
        Helicopters: 2
        Food Packets: 5000
        Water Liters: 12000

        Return:

        - Priority
        - Resource Allocation
        - Remaining Resources
        - Operational Recommendations
        """
    )

    print(response)


if __name__ == "__main__":
    main()