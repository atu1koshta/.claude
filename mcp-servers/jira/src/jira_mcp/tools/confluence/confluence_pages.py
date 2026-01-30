from jira_mcp.tools.base import ConfluenceBaseTool


class GetPage(ConfluenceBaseTool):
    name = "confluence_get_page"
    description = "Get a Confluence page by its ID. Returns title, body (storage format), and version info."
    input_schema = {
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "The Confluence page ID",
            },
            "body_format": {
                "type": "string",
                "description": "Body format to return: storage, atlas_doc_format, or view (default: storage)",
                "enum": ["storage", "atlas_doc_format", "view"],
            },
        },
        "required": ["page_id"],
    }

    async def execute(self, args: dict) -> dict:
        page_id = args["page_id"]
        body_format = args.get("body_format", "storage")
        return await self.client.get(
            f"/pages/{page_id}", params={"body-format": body_format}
        )


class ListPages(ConfluenceBaseTool):
    name = "confluence_list_pages"
    description = "List pages in a Confluence space."
    input_schema = {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The Confluence space ID",
            },
            "limit": {
                "type": "integer",
                "description": "Max number of pages to return (default 25, max 250)",
            },
            "cursor": {
                "type": "string",
                "description": "Pagination cursor from a previous response",
            },
        },
        "required": ["space_id"],
    }

    async def execute(self, args: dict) -> dict:
        space_id = args["space_id"]
        params: dict = {}
        if "limit" in args:
            params["limit"] = args["limit"]
        if "cursor" in args:
            params["cursor"] = args["cursor"]
        return await self.client.get(f"/spaces/{space_id}/pages", params=params or None)


class SearchPages(ConfluenceBaseTool):
    name = "confluence_search_pages"
    description = "Search Confluence pages by title, optionally filtered by space."
    input_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Page title to search for",
            },
            "space_id": {
                "type": "string",
                "description": "Optional space ID to filter results",
            },
            "limit": {
                "type": "integer",
                "description": "Max number of results (default 25)",
            },
        },
        "required": ["title"],
    }

    async def execute(self, args: dict) -> dict:
        params: dict = {"title": args["title"]}
        if "space_id" in args:
            params["space-id"] = args["space_id"]
        if "limit" in args:
            params["limit"] = args["limit"]
        return await self.client.get("/pages", params=params)


class CreatePage(ConfluenceBaseTool):
    name = "confluence_create_page"
    description = "Create a new Confluence page with storage-format body."
    input_schema = {
        "type": "object",
        "properties": {
            "space_id": {
                "type": "string",
                "description": "The space ID to create the page in",
            },
            "title": {
                "type": "string",
                "description": "Page title",
            },
            "body": {
                "type": "string",
                "description": "Page body in Confluence storage format (XHTML)",
            },
            "parent_id": {
                "type": "string",
                "description": "Optional parent page ID",
            },
            "status": {
                "type": "string",
                "description": "Page status: current or draft (default: current)",
                "enum": ["current", "draft"],
            },
        },
        "required": ["space_id", "title", "body"],
    }

    async def execute(self, args: dict) -> dict:
        payload: dict = {
            "spaceId": args["space_id"],
            "status": args.get("status", "current"),
            "title": args["title"],
            "body": {
                "representation": "storage",
                "value": args["body"],
            },
        }
        if "parent_id" in args:
            payload["parentId"] = args["parent_id"]
        return await self.client.post("/pages", json=payload)


class UpdatePage(ConfluenceBaseTool):
    name = "confluence_update_page"
    description = "Update an existing Confluence page. Requires the current version number."
    input_schema = {
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "The page ID to update",
            },
            "title": {
                "type": "string",
                "description": "New page title",
            },
            "body": {
                "type": "string",
                "description": "New page body in Confluence storage format (XHTML)",
            },
            "version_number": {
                "type": "integer",
                "description": "Current version number of the page (will be incremented). Get this from confluence_get_page.",
            },
            "status": {
                "type": "string",
                "description": "Page status: current or draft (default: current)",
                "enum": ["current", "draft"],
            },
        },
        "required": ["page_id", "title", "body", "version_number"],
    }

    async def execute(self, args: dict) -> dict:
        page_id = args["page_id"]
        payload: dict = {
            "id": page_id,
            "status": args.get("status", "current"),
            "title": args["title"],
            "body": {
                "representation": "storage",
                "value": args["body"],
            },
            "version": {
                "number": args["version_number"] + 1,
                "message": "Updated via MCP",
            },
        }
        return await self.client.put(f"/pages/{page_id}", json=payload)


class DeletePage(ConfluenceBaseTool):
    name = "confluence_delete_page"
    description = "Delete a Confluence page by ID."
    input_schema = {
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "The page ID to delete",
            },
        },
        "required": ["page_id"],
    }

    async def execute(self, args: dict) -> dict:
        return await self.client.delete(f"/pages/{args['page_id']}")
