from jira_mcp.tools.base import BaseTool


class ListAttachments(BaseTool):
    name = "jira_list_attachments"
    description = "List all attachments on a JIRA issue."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
        },
        "required": ["issue_key"],
    }

    async def execute(self, args: dict) -> dict:
        result = await self.client.get(
            f"/issue/{args['issue_key']}", params={"fields": "attachment"}
        )
        return {"attachments": result.get("fields", {}).get("attachment", [])}


class AddAttachment(BaseTool):
    name = "jira_add_attachment"
    description = "Add a file attachment to a JIRA issue from a local file path."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "file_path": {
                "type": "string",
                "description": "Absolute path to the file to attach",
            },
        },
        "required": ["issue_key", "file_path"],
    }

    async def execute(self, args: dict) -> dict:
        import os

        file_path = args["file_path"]
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            return await self.client.post_multipart(
                f"/issue/{args['issue_key']}/attachments",
                files={"file": (filename, f)},
            )
