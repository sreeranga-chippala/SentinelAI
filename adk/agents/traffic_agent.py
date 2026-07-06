"""
SentinelAI Traffic ADK Agent

Uses the Traffic MCP Server through Google ADK.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.genai import types

from mcp_servers.traffic.client import (
    get_traffic_connection,
)

# --------------------------------------------------------
# Create ONE MCP Toolset for the application's lifetime
# --------------------------------------------------------

traffic_toolset = McpToolset(
    connection_params=get_traffic_connection(),
)

# --------------------------------------------------------

root_agent = LlmAgent(

    name="traffic_agent",

    model="gemini-2.5-flash-lite",

    instruction="""
You are SentinelAI's Traffic Intelligence Agent.

Always use the Traffic MCP tools.

Never guess routes.

Return only:

- Route
- Distance
- Duration
- Road Status

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
        traffic_toolset,
    ],

)