from dotenv import load_dotenv

load_dotenv()

from agents.communication_agent import CommunicationAgent


def main():

    agent = CommunicationAgent()

    response = agent.run(
        """
Generate a high severity emergency alert.

Incident : Flood

Location : Bengaluru

Instructions :
Evacuate immediately.
Avoid low lying areas.
Follow district administration instructions.
"""
    )

    print(response)


if __name__ == "__main__":
    main()