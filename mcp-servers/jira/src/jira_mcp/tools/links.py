from jira_mcp.tools.base import BaseTool


class GetIssueLinks(BaseTool):
    name = "jira_get_issue_links"
    description = "Get all issue links for a JIRA issue (blocks, is blocked by, relates to, etc.)."
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
            f"/issue/{args['issue_key']}", params={"fields": "issuelinks"}
        )
        return {"links": result.get("fields", {}).get("issuelinks", [])}


class LinkIssues(BaseTool):
    name = "jira_link_issues"
    description = "Create a link between two JIRA issues (e.g. blocks, is blocked by, relates to, duplicates)."
    input_schema = {
        "type": "object",
        "properties": {
            "link_type": {
                "type": "string",
                "description": "Link type name, e.g. 'Blocks', 'Relates', 'Duplicate'",
            },
            "inward_issue_key": {
                "type": "string",
                "description": "Inward issue key (e.g. the issue that 'is blocked by')",
            },
            "outward_issue_key": {
                "type": "string",
                "description": "Outward issue key (e.g. the issue that 'blocks')",
            },
        },
        "required": ["link_type", "inward_issue_key", "outward_issue_key"],
    }

    async def execute(self, args: dict) -> dict:
        payload = {
            "type": {"name": args["link_type"]},
            "inwardIssue": {"key": args["inward_issue_key"]},
            "outwardIssue": {"key": args["outward_issue_key"]},
        }
        await self.client.post("/issueLink", json=payload)
        return {
            "status": "linked",
            "type": args["link_type"],
            "inward": args["inward_issue_key"],
            "outward": args["outward_issue_key"],
        }
