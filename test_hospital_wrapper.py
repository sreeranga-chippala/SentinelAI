from dotenv import load_dotenv

load_dotenv()

from agents.hospital_agent import HospitalAgent


def main():

    agent = HospitalAgent()

    response = agent.run("""
Search hospitals.

Location = Bengaluru

Return nearest hospitals.
""")

    print(response)


if __name__ == "__main__":
    main()