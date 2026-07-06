from dotenv import load_dotenv

load_dotenv()

from agents.priority_agent import PriorityAgent


def main():

    agent = PriorityAgent()

    response = agent.run(
        """
Evaluate this disaster.

Severity: 9
Affected People: 750
Critical Injuries: 35
Distance: 8 km
Weather: Heavy Rain
Road Access: Difficult

Determine the disaster priority and explain why.
"""
    )

    print(response)


if __name__ == "__main__":
    main()