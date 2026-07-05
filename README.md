# SentinelAI

AI-powered Multi-Agent Emergency Command Center.

Built with:

- Google ADK
- Gemini
- MCP
- Streamlit

| Agent               | Reads           | Writes                       |
| ------------------- | --------------- | ---------------------------- |
| Weather Agent       | Input.weather   | Knowledge.risk_scores        |
| Hospital Agent      | Input.hospitals | Knowledge.hospital_capacity  |
| Traffic Agent       | Input.roads     | Knowledge.safe_routes        |
| Population Agent    | Input.areas     | Knowledge.population_stats   |
| Priority Agent      | Knowledge       | Knowledge.priority_scores    |
| Allocation Agent    | Knowledge       | Decision.resource_allocation |
| Communication Agent | Decision        | Decision.public_alerts       |
| Decision Agent      | Everything      | Decision.missions            |


🚧 Under Development

