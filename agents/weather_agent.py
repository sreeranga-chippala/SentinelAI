"""
SentinelAI Weather ADK Agent

Uses the Weather MCP Server through Google ADK.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.genai import types

from mcp_servers.weather.client import (
    get_weather_connection,
)

# --------------------------------------------------------
# Create ONE MCP Toolset for the application's lifetime
# --------------------------------------------------------

weather_toolset = McpToolset(
    connection_params=get_weather_connection(),
)

# --------------------------------------------------------

root_agent = LlmAgent(

    name="weather_agent",

    model="gemini-2.5-flash-lite",

    instruction="""
You are SentinelAI's Weather Intelligence Agent.

Always use the Weather MCP tool.

Never answer using your own knowledge.

Return only:

- Weather Condition
- Temperature
- Feels Like
- Humidity
- Wind Speed

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
        weather_toolset,
    ],

)