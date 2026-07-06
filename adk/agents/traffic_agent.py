"""
SentinelAI - Traffic ADK Agent

Google ADK Traffic Agent backed by the Traffic MCP Server.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from mcp_servers.traffic.client import get_traffic_connection


root_agent = LlmAgent(
    name="traffic_agent",
    model="gemini-2.5-flash",
    instruction="""
You are SentinelAI's Traffic Intelligence Agent.

Your responsibilities are:

- Analyze road conditions.
- Calculate driving routes.
- Estimate travel distance.
- Estimate travel duration.
- Always use the Traffic MCP tools.
- Never hallucinate traffic information.
- Return concise structured traffic observations.
""",
    tools=[
        McpToolset(
            connection_params=get_traffic_connection(),
        ),
    ],
)