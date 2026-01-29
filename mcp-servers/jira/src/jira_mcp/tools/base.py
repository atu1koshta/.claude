from abc import ABC, abstractmethod

from jira_mcp.client import JiraClient


class BaseTool(ABC):
    name: str
    description: str
    input_schema: dict

    def __init__(self, client: JiraClient) -> None:
        self.client = client

    @abstractmethod
    async def execute(self, args: dict) -> dict:
        ...
