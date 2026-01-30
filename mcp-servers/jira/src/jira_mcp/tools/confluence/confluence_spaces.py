from jira_mcp.tools.base import ConfluenceBaseTool


class ListSpaces(ConfluenceBaseTool):
    name = "confluence_list_spaces"
    description = "List all Confluence spaces accessible to the authenticated user."
    input_schema = {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Max number of spaces to return (default 25, max 250)",
            },
            "cursor": {
                "type": "string",
                "description": "Pagination cursor from a previous response",
            },
        },
    }

    async def execute(self, args: dict) -> dict:
        params: dict = {}
        if "limit" in args:
            params["limit"] = args["limit"]
        if "cursor" in args:
            params["cursor"] = args["cursor"]
        return await self.client.get("/spaces", params=params or None)


class GetSpace(ConfluenceBaseTool):
    name = "confluence_get_space"
    description = "Get details of a specific Confluence space."
    input_schema = {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The space ID",
            },
        },
        "required": ["space_id"],
    }

    async def execute(self, args: dict) -> dict:
        return await self.client.get(f"/spaces/{args['space_id']}")
