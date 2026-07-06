from dotenv import load_dotenv

load_dotenv()

from agents.weather_agent import WeatherAgent

agent = WeatherAgent()

print(
    agent.run(
        "What is the weather in Bengaluru?"
    )
)