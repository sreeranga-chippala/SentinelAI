"""
SentinelAI - Allocation ADK Agent

Google ADK Allocation Agent backed by the Allocation MCP Server.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from mcp_servers.allocation.client import (
    get_allocation_connection,
)


root_agent = LlmAgent(
    name="allocation_agent",
    model="gemini-2.5-flash",
    instruction="""
You are SentinelAI's Resource Allocation Intelligence Agent.

Your responsibilities are:

- Analyze disaster severity.
- Determine disaster priority.
- Allocate available emergency resources.
- Generate operational recommendations.
- Never perform manual calculations.
- Always use the Allocation MCP tools.
- Never hallucinate allocation results.
- Return concise structured responses.
""",
    tools=[
        McpToolset(
            connection_params=get_allocation_connection(),
        ),
    ],
)