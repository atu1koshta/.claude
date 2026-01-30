from jira_mcp.tools.base import BaseTool


class ListSprints(BaseTool):
    name = "jira_list_sprints"
    description = "List sprints for a JIRA board. Optionally filter by state (active, closed, future)."
    input_schema = {
        "type": "object",
        "properties": {
            "board_id": {
                "type": "integer",
                "description": "The board ID",
            },
            "state": {
                "type": "string",
                "description": "Filter by sprint state: active, closed, future (comma-separated for multiple)",
            },
        },
        "required": ["board_id"],
    }

    async def execute(self, args: dict) -> dict:
        params: dict = {}
        if "state" in args:
            params["state"] = args["state"]
        return await self.client.get(
            f"/board/{args['board_id']}/sprint", params=params or None, agile=True
        )


class GetSprintIssues(BaseTool):
    name = "jira_get_sprint_issues"
    description = "Get all issues in a specific sprint."
    input_schema = {
        "type": "object",
        "properties": {
            "sprint_id": {
                "type": "integer",
                "description": "The sprint ID",
            },
            "fields": {
                "type": "string",
                "description": "Comma-separated fields to return",
            },
        },
        "required": ["sprint_id"],
    }

    async def execute(self, args: dict) -> dict:
        params: dict = {}
        if "fields" in args:
            params["fields"] = args["fields"]
        return await self.client.get(
            f"/sprint/{args['sprint_id']}/issue", params=params or None, agile=True
        )


class MoveToSprint(BaseTool):
    name = "jira_move_to_sprint"
    description = "Move one or more issues to a sprint."
    input_schema = {
        "type": "object",
        "properties": {
            "sprint_id": {
                "type": "integer",
                "description": "Target sprint ID",
            },
            "issue_keys": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of issue keys to move, e.g. ['PROJ-1', 'PROJ-2']",
            },
        },
        "required": ["sprint_id", "issue_keys"],
    }

    async def execute(self, args: dict) -> dict:
        await self.client.post(
            f"/sprint/{args['sprint_id']}/issue",
            json={"issues": args["issue_keys"]},
            agile=True,
        )
        return {"status": "moved", "sprint_id": args["sprint_id"], "issues": args["issue_keys"]}
