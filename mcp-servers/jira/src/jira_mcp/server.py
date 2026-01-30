import asyncio

from dotenv import load_dotenv

load_dotenv()

from mcp.server import Server
from mcp.server.stdio import stdio_server

from jira_mcp.client import JiraClient
from jira_mcp.confluence_client import ConfluenceClient
from jira_mcp.tools import ToolRegistry


def create_server() -> tuple[Server, JiraClient, ConfluenceClient]:
    app = Server("jira-mcp")
    jira_client = JiraClient()
    confluence_client = ConfluenceClient()
    registry = ToolRegistry(jira_client, confluence_client)

    @app.list_tools()
    async def list_tools():
        return registry.list_tools()

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        return await registry.call_tool(name, arguments)

    return app, jira_client, confluence_client


async def main() -> None:
    app, jira_client, confluence_client = create_server()
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    finally:
        await jira_client.close()
        await confluence_client.close()


if __name__ == "__main__":
    asyncio.run(main())
