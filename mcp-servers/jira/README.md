# JIRA MCP Server for Claude Code

## Setup

### 1. Copy MCP servers to Claude config

```bash
cp -r mcp-servers ~/.claude/mcp-servers
```

### 2. Install uv

```bash
brew install uv
```

### 3. Install dependencies

```bash
cd ~/.claude/mcp-servers/jira
pip install -e .
```

### 4. Set environment variables

Generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens

Then set the following environment variables:

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
```

### 5. Add the MCP server to Claude Code

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```
