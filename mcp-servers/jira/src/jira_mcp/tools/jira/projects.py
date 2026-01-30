from jira_mcp.tools.base import BaseTool


class ListProjects(BaseTool):
    name = "jira_list_projects"
    description = "List all JIRA projects accessible to the authenticated user."
    input_schema = {
        "type": "object",
        "properties": {},
    }

    async def execute(self, args: dict) -> dict:
        projects = await self.client.get("/project")
        return {"projects": projects}


class GetProject(BaseTool):
    name = "jira_get_project"
    description = "Get detailed information about a specific JIRA project."
    input_schema = {
        "type": "object",
        "properties": {
            "project_key": {
                "type": "string",
                "description": "The project key, e.g. PROJ",
            },
        },
        "required": ["project_key"],
    }

    async def execute(self, args: dict) -> dict:
        return await self.client.get(f"/project/{args['project_key']}")
