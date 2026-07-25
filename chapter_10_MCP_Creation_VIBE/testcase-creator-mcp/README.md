# vwo-testcases MCP server

FastMCP server exposing a local export of VWO manual test cases
(`../resource/vwo_5000_test_cases.csv`) as MCP tools, resources, and prompts.
Transport: stdio.

## Install

```bash
uv sync
```

## Run

```bash
uv run server.py
```

Optional CSV override:

```bash
VWO_CSV_PATH=/path/to/other.csv uv run server.py
```

## Open in MCP Inspector

```bash
uv run fastmcp dev server.py
```

This launches the Inspector in your browser, connected to the server over stdio.

## Verify each primitive in the Inspector

- **Tools tab**: run `get_test_case` with `issue_key="VWO-1001"`; run `search_test_cases`
  with `query="login"`; run `test_case_stats` with `group_by="priority"`.
- **Resources tab**: read `testcases://schema`, `testcases://all`, and the templated
  `testcases://module/Reports`.
- **Prompts tab**: render `review_test_case` with an `issue_key`, and
  `generate_regression_suite` with a `module` name (e.g. `Reports`).
- Confirm error paths return a readable MCP error, not a stack trace: an unknown
  `issue_key`, an unknown `module`, or an invalid `group_by`.

## Register with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vwo-testcases": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/testcase-creator-mcp1",
        "run",
        "server.py"
      ]
    }
  }
}
```

Replace the `--directory` path with this project's absolute path on your machine.
