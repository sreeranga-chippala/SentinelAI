"""
SentinelAI - Priority ADK Agent

Google ADK Priority Agent backed by the Priority MCP Server.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from mcp_servers.priority.client import get_priority_connection


root_agent = LlmAgent(
    name="priority_agent",
    model="gemini-2.5-flash",
    instruction="""
You are SentinelAI's Priority Intelligence Agent.

Your responsibilities are:

- Evaluate disaster severity.
- Determine response priority.
- Explain the priority level.
- Always use the Priority MCP tool.
- Never hallucinate priority values.
- Return concise structured results.
""",
    tools=[
        McpToolset(
            connection_params=get_priority_connection(),
        ),
    ],
)