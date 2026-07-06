from dotenv import load_dotenv

load_dotenv()

from agents.decision_agent import DecisionAgent


def main():

    agent = DecisionAgent()

    response = agent.run(
        """
Weather Report:

Heavy rainfall has been reported in Bengaluru.
Wind speed is 18 km/h.

Traffic Report:

Heavy congestion on NH-275.
Average delay is 25 minutes.

Hospital Report:

3 hospitals are available.

ICU Beds:
57

General Beds:
112

Population Report:

High population density.

Estimated affected population:
15,000 people.

Generate:

1. Situation summary

2. Emergency priority

3. Recommended response

4. Immediate actions
"""
    )

    print(response)


if __name__ == "__main__":
    main()