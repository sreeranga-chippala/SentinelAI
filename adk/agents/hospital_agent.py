"""
SentinelAI - Hospital ADK Agent
"""

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from mcp_servers.hospital.client import (
    get_hospital_connection,
)

root_agent = LlmAgent(
    name="hospital_agent",
    model="gemini-flash-lite-latest",
    instruction="""
You are SentinelAI Hospital Intelligence Agent.

Always use the Hospital MCP tool.

The Hospital MCP accepts a location name.

Never ask the user for coordinates.

Examples:
- Bengaluru
- Whitefield
- Mysuru
- Kempegowda Airport

Return

- Hospital Name
- Emergency Facility
- Phone Number
- Coordinates

Never invent hospitals.
""",
    tools=[
        MCPToolset(
            connection_params=get_hospital_connection(),
        ),
    ],
)