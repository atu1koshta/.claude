import httpx
from base64 import b64encode

from jira_mcp.config import settings


class JiraClient:
    def __init__(self) -> None:
        credentials = b64encode(
            f"{settings.jira_email}:{settings.jira_api_token}".encode()
        ).decode()
        self._headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._base_url = settings.jira_url.rstrip("/")
        self._client = httpx.AsyncClient(
            headers=self._headers, timeout=30.0
        )

    def _url(self, path: str, agile: bool = False) -> str:
        prefix = "/rest/agile/1.0" if agile else "/rest/api/3"
        return f"{self._base_url}{prefix}{path}"

    async def get(self, path: str, params: dict | None = None, agile: bool = False) -> dict:
        resp = await self._client.get(self._url(path, agile), params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, json: dict | None = None, agile: bool = False) -> dict:
        resp = await self._client.post(self._url(path, agile), json=json)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def put(self, path: str, json: dict | None = None, agile: bool = False) -> dict:
        resp = await self._client.put(self._url(path, agile), json=json)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def delete(self, path: str, agile: bool = False) -> dict:
        resp = await self._client.delete(self._url(path, agile))
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def post_multipart(self, path: str, files: dict) -> dict:
        headers = {**self._headers, "X-Atlassian-Token": "no-check"}
        headers.pop("Content-Type", None)
        resp = await self._client.post(
            self._url(path), files=files, headers=headers
        )
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def close(self) -> None:
        await self._client.aclose()
