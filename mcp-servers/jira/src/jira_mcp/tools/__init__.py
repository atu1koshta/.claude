from __future__ import annotations

import importlib
import pkgutil
from typing import Any

from mcp.types import Tool, TextContent

from jira_mcp.client import JiraClient
from jira_mcp.tools.base import BaseTool


class ToolRegistry:
    def __init__(self, client: JiraClient) -> None:
        self._tools: dict[str, BaseTool] = {}
        self._discover(client)

    def _discover(self, client: JiraClient) -> None:
        package = importlib.import_module("jira_mcp.tools")
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if modname in ("base", "__init__"):
                continue
            module = importlib.import_module(f"jira_mcp.tools.{modname}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseTool)
                    and attr is not BaseTool
                    and hasattr(attr, "name")
                ):
                    instance = attr(client)
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
