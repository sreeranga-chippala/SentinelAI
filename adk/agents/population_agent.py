"""
SentinelAI Population ADK Agent

Uses the Population MCP Server through Google ADK.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.genai import types

from mcp_servers.population.client import (
    get_population_connection,
)

# --------------------------------------------------------
# Create ONE MCP Toolset for the application's lifetime
# --------------------------------------------------------

population_toolset = McpToolset(
    connection_params=get_population_connection(),
)

# --------------------------------------------------------

root_agent = LlmAgent(

    name="population_agent",

    model="gemini-2.5-flash-lite",

    instruction="""
You are SentinelAI's Population Intelligence Agent.

Always use the Population MCP tool.

Never estimate population.

Return only:

- Population
- Administrative Region (if available)
- Relevant demographic information

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
        population_toolset,
    ],

)