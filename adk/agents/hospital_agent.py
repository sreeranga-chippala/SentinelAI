"""
SentinelAI Hospital ADK Agent

Uses the Hospital MCP Server through Google ADK.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.genai import types

from mcp_servers.hospital.client import (
    get_hospital_connection,
)

# --------------------------------------------------------
# Create ONE toolset for the lifetime of the application
# --------------------------------------------------------

hospital_toolset = McpToolset(
    connection_params=get_hospital_connection(),
)

# --------------------------------------------------------

root_agent = LlmAgent(

    name="hospital_agent",

    model="gemini-2.5-flash-lite",

    instruction="""
You are SentinelAI Hospital Intelligence Agent.

Always use the Hospital MCP tool.

Never ask for coordinates.

Return ONLY:

- Hospital Name
- Emergency Facility
- Phone Number
- Coordinates

Never invent hospitals.

Keep the response concise.
""",

    generate_content_config=types.GenerateContentConfig(

        temperature=0,

        http_options=types.HttpOptions(

            retry_options=types.HttpRetryOptions(

                initial_delay=2,

                attempts=5,

            ),

        ),

    ),

    tools=[
        hospital_toolset,
    ],
)