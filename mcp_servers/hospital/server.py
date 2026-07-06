from mcp.server.fastmcp import FastMCP

from mcp_servers.hospital.tools import (
    find_nearby_hospitals,
    health_check,
)

mcp = FastMCP("Hospital MCP")

mcp.tool()(find_nearby_hospitals)
mcp.tool()(health_check)

if __name__ == "__main__":
    mcp.run()