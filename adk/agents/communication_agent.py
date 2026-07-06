"""
SentinelAI Communication ADK Agent
"""

from google.adk.agents import LlmAgent

from mcp_servers.communication.client import (
    get_communication_connection,
)


root_agent = LlmAgent(
    name="communication_agent",
    model="gemini-2.5-flash",
    instruction="""
You are SentinelAI's Communication Intelligence Agent.

Responsibilities:
- Generate emergency alerts.
- Generate public safety messages.
- Broadcast emergency communications.

Always use the Communication MCP tools.

Never hallucinate information.
Return concise structured communication messages.
""",
    tools=[
        get_communication_connection(),
    ],
)