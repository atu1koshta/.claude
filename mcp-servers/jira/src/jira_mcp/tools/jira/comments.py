from jira_mcp.tools.base import BaseTool


class GetComments(BaseTool):
    name = "jira_get_comments"
    description = "Get all comments on a JIRA issue."
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
        return await self.client.get(f"/issue/{args['issue_key']}/comment")


class AddComment(BaseTool):
    name = "jira_add_comment"
    description = "Add a comment to a JIRA issue."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "body": {
                "type": "string",
                "description": "Comment text (plain text, will be converted to ADF)",
            },
        },
        "required": ["issue_key", "body"],
    }

    async def execute(self, args: dict) -> dict:
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": args["body"]}],
                    }
                ],
            }
        }
        return await self.client.post(f"/issue/{args['issue_key']}/comment", json=payload)
