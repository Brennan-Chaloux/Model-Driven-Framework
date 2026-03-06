"""MDF MCP server — FastMCP entry point."""
from fastmcp import FastMCP
from mdf_server.tools.model_io import list_domains, read_model, write_model

mcp = FastMCP("mdf")

mcp.tool(list_domains)
mcp.tool(read_model)
mcp.tool(write_model)


def main() -> None:
    """Start the MDF MCP server with stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
