"""
SentinelAI Weather ADK Agent

Uses the Weather MCP Server through Google ADK.
"""

from __future__ import annotations

import sys
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from google.genai import types

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

    name="weather_agent",

    model="gemini-2.5-flash-lite",

    instruction="""
You are SentinelAI's Weather Intelligence Agent.

Always use the Weather MCP tool.

Never answer from your own knowledge.

Return only concise weather observations.
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