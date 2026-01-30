from abc import ABC, abstractmethod

from jira_mcp.client import JiraClient
from jira_mcp.confluence_client import ConfluenceClient


class BaseTool(ABC):
    name: str
    description: str
    input_schema: dict

    def __init__(self, client: JiraClient) -> None:
        self.client = client

    @abstractmethod
    async def execute(self, args: dict) -> dict:
        ...


class ConfluenceBaseTool(ABC):
    name: str
    description: str
    input_schema: dict

    def __init__(self, client: ConfluenceClient) -> None:
        self.client = client

    @abstractmethod
    async def execute(self, args: dict) -> dict:
        ...
