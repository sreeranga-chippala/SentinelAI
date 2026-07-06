"""
SentinelAI
Weather ADK Agent

This agent connects to the Weather MCP Server using the
official Google ADK McpToolset.
"""

from __future__ import annotations

import sys
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)

from mcp import StdioServerParameters


SERVER_PATH = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "mcp_servers"
    / "weather"
    / "server.py"
)


root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="weather_agent",
    instruction="""
You are SentinelAI's Weather Intelligence Agent.

Always use the Weather MCP tools.

Never hallucinate weather information.

Return structured and concise weather observations.
""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
    command=sys.executable,
    args=[
        "-m",
        "mcp_servers.weather.server",
    ],
),
                timeout=30,
            ),
        ),
    ],
)