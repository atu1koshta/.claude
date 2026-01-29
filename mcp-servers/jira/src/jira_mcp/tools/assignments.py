from jira_mcp.tools.base import BaseTool


class AssignIssue(BaseTool):
    name = "jira_assign_issue"
    description = "Assign a JIRA issue to a user. Pass null account_id to unassign."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "account_id": {
                "type": ["string", "null"],
                "description": "Atlassian account ID of the assignee, or null to unassign",
            },
        },
        "required": ["issue_key", "account_id"],
    }

    async def execute(self, args: dict) -> dict:
        await self.client.put(
            f"/issue/{args['issue_key']}/assignee",
            json={"accountId": args["account_id"]},
        )
        return {"status": "assigned", "key": args["issue_key"], "account_id": args["account_id"]}
