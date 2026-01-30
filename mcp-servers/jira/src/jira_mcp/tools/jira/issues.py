from jira_mcp.tools.base import BaseTool


class SearchIssues(BaseTool):
    name = "jira_search_issues"
    description = "Search JIRA issues using JQL (JIRA Query Language). Returns matching issues with key fields."
    input_schema = {
        "type": "object",
        "properties": {
            "jql": {
                "type": "string",
                "description": "JQL query string, e.g. 'project = PROJ AND status = Open'",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum results to return (default 50, max 100)",
                "default": 50,
            },
            "fields": {
                "type": "string",
                "description": "Comma-separated list of fields to return (default: summary,status,assignee,priority,issuetype)",
            },
        },
        "required": ["jql"],
    }

    async def execute(self, args: dict) -> dict:
        fields_str = args.get("fields", "summary,status,assignee,priority,issuetype")
        fields_list = [f.strip() for f in fields_str.split(",")]
        body = {
            "jql": args["jql"],
            "maxResults": min(args.get("max_results", 50), 100),
            "fields": fields_list,
        }
        return await self.client.post("/search/jql", json=body)


class GetIssue(BaseTool):
    name = "jira_get_issue"
    description = "Get detailed information about a specific JIRA issue by its key (e.g. PROJ-123)."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "fields": {
                "type": "string",
                "description": "Comma-separated fields to include (omit for all fields)",
            },
        },
        "required": ["issue_key"],
    }

    async def execute(self, args: dict) -> dict:
        params = {}
        if "fields" in args:
            params["fields"] = args["fields"]
        return await self.client.get(f"/issue/{args['issue_key']}", params=params or None)


class CreateIssue(BaseTool):
    name = "jira_create_issue"
    description = "Create a new JIRA issue. Requires project key, summary, and issue type at minimum."
    input_schema = {
        "type": "object",
        "properties": {
            "project_key": {
                "type": "string",
                "description": "Project key, e.g. PROJ",
            },
            "summary": {
                "type": "string",
                "description": "Issue summary/title",
            },
            "issue_type": {
                "type": "string",
                "description": "Issue type name, e.g. Task, Bug, Story",
            },
            "description": {
                "type": "string",
                "description": "Issue description (plain text, will be converted to ADF)",
            },
            "assignee_account_id": {
                "type": "string",
                "description": "Atlassian account ID of the assignee",
            },
            "priority": {
                "type": "string",
                "description": "Priority name, e.g. High, Medium, Low",
            },
            "labels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Labels to apply",
            },
            "parent_key": {
                "type": "string",
                "description": "Parent issue key for subtasks",
            },
        },
        "required": ["project_key", "summary", "issue_type"],
    }

    async def execute(self, args: dict) -> dict:
        fields: dict = {
            "project": {"key": args["project_key"]},
            "summary": args["summary"],
            "issuetype": {"name": args["issue_type"]},
        }
        if "description" in args:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": args["description"]}],
                    }
                ],
            }
        if "assignee_account_id" in args:
            fields["assignee"] = {"accountId": args["assignee_account_id"]}
        if "priority" in args:
            fields["priority"] = {"name": args["priority"]}
        if "labels" in args:
            fields["labels"] = args["labels"]
        if "parent_key" in args:
            fields["parent"] = {"key": args["parent_key"]}
        return await self.client.post("/issue", json={"fields": fields})


class UpdateIssue(BaseTool):
    name = "jira_update_issue"
    description = "Update fields on an existing JIRA issue."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key, e.g. PROJ-123",
            },
            "summary": {"type": "string", "description": "New summary"},
            "description": {"type": "string", "description": "New description (plain text)"},
            "assignee_account_id": {"type": "string", "description": "New assignee account ID"},
            "priority": {"type": "string", "description": "New priority name"},
            "labels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "New labels (replaces existing)",
            },
        },
        "required": ["issue_key"],
    }

    async def execute(self, args: dict) -> dict:
        fields: dict = {}
        if "summary" in args:
            fields["summary"] = args["summary"]
        if "description" in args:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": args["description"]}],
                    }
                ],
            }
        if "assignee_account_id" in args:
            fields["assignee"] = {"accountId": args["assignee_account_id"]}
        if "priority" in args:
            fields["priority"] = {"name": args["priority"]}
        if "labels" in args:
            fields["labels"] = args["labels"]
        await self.client.put(f"/issue/{args['issue_key']}", json={"fields": fields})
        return {"status": "updated", "key": args["issue_key"]}


class DeleteIssue(BaseTool):
    name = "jira_delete_issue"
    description = "Delete a JIRA issue. Use with caution."
    input_schema = {
        "type": "object",
        "properties": {
            "issue_key": {
                "type": "string",
                "description": "The issue key to delete, e.g. PROJ-123",
            },
        },
        "required": ["issue_key"],
    }

    async def execute(self, args: dict) -> dict:
        await self.client.delete(f"/issue/{args['issue_key']}")
        return {"status": "deleted", "key": args["issue_key"]}
