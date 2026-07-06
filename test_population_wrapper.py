from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

from agents.population_agent import PopulationAgent


def main() -> None:

    agent = PopulationAgent()

    response = agent.run(
        """
        What is the population of Bengaluru?

        Also compare it with Mysuru and tell me
        which city has the larger population.
        """
    )

    print(response)


if __name__ == "__main__":
    main()