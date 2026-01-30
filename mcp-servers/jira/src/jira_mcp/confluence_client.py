import httpx
from base64 import b64encode

from jira_mcp.config import settings


class ConfluenceClient:
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

    def _url(self, path: str) -> str:
        return f"{self._base_url}/wiki/api/v2{path}"

    async def get(self, path: str, params: dict | None = None) -> dict:
        resp = await self._client.get(self._url(path), params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, json: dict | None = None) -> dict:
        resp = await self._client.post(self._url(path), json=json)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def put(self, path: str, json: dict | None = None) -> dict:
        resp = await self._client.put(self._url(path), json=json)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def delete(self, path: str) -> dict:
        resp = await self._client.delete(self._url(path))
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def close(self) -> None:
        await self._client.aclose()
