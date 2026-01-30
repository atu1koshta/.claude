from jira_mcp.tools.base import BaseTool


class ListTransitions(BaseTool):
    name = "jira_list_transitions"
    description = "List available status transitions for a JIRA issue. Use this to find valid transition IDs before transitioning."
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
        return await self.client.get(f"/issue/{args['issue_key']}/transitions")


class TransitionIssue(BaseTool):
    name = "jira_transition_issue"
    description = "Transition a JIRA issue to a new status. Use jira_list_transitions first to get valid transition IDs."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "transition_id": {
                "type": "string",
                "description": "The transition ID (from jira_list_transitions)",
            },
            "comment": {
                "type": "string",
                "description": "Optional comment to add with the transition",
            },
        },
        "required": ["issue_key", "transition_id"],
    }

    async def execute(self, args: dict) -> dict:
        payload: dict = {"transition": {"id": args["transition_id"]}}
        if "comment" in args:
            payload["update"] = {
                "comment": [
                    {
                        "add": {
                            "body": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [{"type": "text", "text": args["comment"]}],
                                    }
                                ],
                            }
                        }
                    }
                ]
            }
        await self.client.post(f"/issue/{args['issue_key']}/transitions", json=payload)
        return {"status": "transitioned", "key": args["issue_key"], "transition_id": args["transition_id"]}
