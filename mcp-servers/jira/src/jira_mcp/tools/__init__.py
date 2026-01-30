from __future__ import annotations

import importlib
import pkgutil
from typing import Any

from mcp.types import Tool, TextContent

from jira_mcp.client import JiraClient
from jira_mcp.confluence_client import ConfluenceClient
from jira_mcp.tools.base import BaseTool, ConfluenceBaseTool


class ToolRegistry:
    def __init__(self, jira_client: JiraClient, confluence_client: ConfluenceClient) -> None:
        self._tools: dict[str, BaseTool | ConfluenceBaseTool] = {}
        self._discover(jira_client, confluence_client)

    def _discover(self, jira_client: JiraClient, confluence_client: ConfluenceClient) -> None:
        for pkg_name in ("jira_mcp.tools.jira", "jira_mcp.tools.confluence"):
            package = importlib.import_module(pkg_name)
            for _importer, modname, _ispkg in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{pkg_name}.{modname}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if not (isinstance(attr, type) and hasattr(attr, "name")):
                        continue
                    if issubclass(attr, ConfluenceBaseTool) and attr is not ConfluenceBaseTool:
                        instance = attr(confluence_client)
                        self._tools[instance.name] = instance
                    elif issubclass(attr, BaseTool) and attr is not BaseTool:
                        instance = attr(jira_client)
                        self._tools[instance.name] = instance

    def list_tools(self) -> list[Tool]:
        return [
            Tool(
                name=t.name,
                description=t.description,
                inputSchema=t.input_schema,
            )
            for t in self._tools.values()
        ]

    async def call_tool(self, name: str, args: dict[str, Any]) -> list[TextContent]:
        tool = self._tools.get(name)
        if not tool:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            result = await tool.execute(args)
            import json
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]
