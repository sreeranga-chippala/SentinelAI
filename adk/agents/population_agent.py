"""
SentinelAI - Population ADK Agent

Google ADK Population Agent backed by the Population MCP Server.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from mcp_servers.population.client import (
    get_population_connection,
)


root_agent = LlmAgent(
    name="population_agent",
    model="gemini-2.5-flash",
    instruction="""
You are SentinelAI's Population Intelligence Agent.

Your responsibilities are:

- Retrieve city population.
- Compare populations.
- Provide demographic context.
- Always use the Population MCP tools.
- Never hallucinate population information.
- Return concise structured observations.
""",
    tools=[
        McpToolset(
            connection_params=get_population_connection(),
        ),
    ],
)