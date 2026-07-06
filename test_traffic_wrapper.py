from dotenv import load_dotenv

load_dotenv()

from agents.traffic_agent import TrafficAgent


def main() -> None:

    agent = TrafficAgent()

    response = agent.run(
        """
        Calculate the best driving route from Bengaluru to Mysuru.
        Report:

        - Distance
        - Estimated travel time
        - Route summary
        """
    )

    print(response)


if __name__ == "__main__":
    main()