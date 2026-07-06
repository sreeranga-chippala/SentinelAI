"""
SentinelAI Decision Agent
"""

from google.adk.agents import LlmAgent

from google.adk.tools.mcp_tool import McpToolset

from mcp_servers.decision.client import (
    get_decision_connection,
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="decision_agent",
    description="Generates emergency decisions from all upstream agents.",
    instruction="""
You are the Decision Agent of SentinelAI.

You receive:

• Weather analysis
• Traffic analysis
• Hospital availability
• Population density

Your responsibilities:

1. Analyze all available information.
2. Determine emergency severity.
3. Recommend response priority.
4. Produce concise actionable recommendations.

Always use the Decision MCP tool.

Never invent data.
""",
    tools=[
        McpToolset(
            connection_params=get_decision_connection(),
        )
    ],
)