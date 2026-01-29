import asyncio

from dotenv import load_dotenv

load_dotenv()

from mcp.server import Server
from mcp.server.stdio import stdio_server

from jira_mcp.client import JiraClient
from jira_mcp.tools import ToolRegistry


def create_server() -> tuple[Server, JiraClient]:
    app = Server("jira-mcp")
    client = JiraClient()
    registry = ToolRegistry(client)

    @app.list_tools()
    async def list_tools():
        return registry.list_tools()

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        return await registry.call_tool(name, arguments)

    return app, client


async def main() -> None:
    app, client = create_server()
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
