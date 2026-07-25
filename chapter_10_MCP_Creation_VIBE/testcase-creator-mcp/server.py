"""VWO test-case MCP server: tools, resources, and prompts over a local CSV export."""

from __future__ import annotations

import csv
import logging
import os
import sys
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import PromptError, ResourceError, ToolError

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("vwo-testcases")

# --- Column names (verified against the real CSV header) ---
COL_ISSUE_TYPE = "Issue Type"
COL_ISSUE_KEY = "Issue Key"
COL_SUMMARY = "Summary"
COL_DESCRIPTION = "Description"
COL_PRIORITY = "Priority"
COL_COMPONENT = "Component"
COL_LABELS = "Labels"
COL_TEST_TYPE = "Test Type"
COL_PRECONDITIONS = "Preconditions"
COL_STEPS = "Steps"
COL_EXPECTED_RESULT = "Expected Result"
COL_BROWSER = "Browser"
COL_DEVICE = "Device"
COL_STATUS = "Status"

SCHEMA: dict[str, str] = {
    COL_ISSUE_TYPE: "str",
    COL_ISSUE_KEY: "str (unique id, e.g. VWO-1001)",
    COL_SUMMARY: "str",
    COL_DESCRIPTION: "str",
    COL_PRIORITY: "str enum (Low/Medium/High/Highest)",
    COL_COMPONENT: "str (module name)",
    COL_LABELS: "str (space-separated tags)",
    COL_TEST_TYPE: "str enum (Functional/UI-UX/Accessibility/Boundary/...)",
    COL_PRECONDITIONS: "str",
    COL_STEPS: "str (numbered, '|'-delimited)",
    COL_EXPECTED_RESULT: "str",
    COL_BROWSER: "str",
    COL_DEVICE: "str",
    COL_STATUS: "str enum (Draft/Ready/Automated/...)",
}

# group_by aliases exposed to callers -> actual CSV column
GROUPABLE_FIELDS: dict[str, str] = {
    "module": COL_COMPONENT,
    "component": COL_COMPONENT,
    "priority": COL_PRIORITY,
    "status": COL_STATUS,
    "type": COL_TEST_TYPE,
    "test_type": COL_TEST_TYPE,
}

DEFAULT_CSV_PATH = Path(__file__).resolve().parent.parent / "resource" / "vwo_5000_test_cases.csv"
CSV_PATH = Path(os.environ.get("VWO_CSV_PATH", str(DEFAULT_CSV_PATH)))


def _load_test_cases(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        logger.error("CSV not found at %s", path)
        raise FileNotFoundError(
            f"Test case CSV not found at '{path}'. "
            "Set VWO_CSV_PATH to override the default location."
        )
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    logger.info("Loaded %d test cases from %s", len(rows), path)
    return rows


# Load once at startup; reused by every tool/resource call below.
TEST_CASES: list[dict[str, str]] = _load_test_cases(CSV_PATH)
TEST_CASES_BY_KEY: dict[str, dict[str, str]] = {
    row[COL_ISSUE_KEY].strip().upper(): row for row in TEST_CASES if row.get(COL_ISSUE_KEY)
}

mcp = FastMCP("vwo-testcases")


# --- Tools ---


@mcp.tool
def search_test_cases(
    query: str, component: str | None = None, limit: int = 20
) -> list[dict[str, str]]:
    """Search test cases by substring match on summary/description/steps, optionally filtered by component."""
    needle = query.strip().lower()
    if not needle:
        raise ToolError("query must not be empty.")
    safe_limit = max(1, min(limit, 200))

    matches: list[dict[str, str]] = []
    for row in TEST_CASES:
        if component and row.get(COL_COMPONENT, "").strip().lower() != component.strip().lower():
            continue
        haystack = " ".join(
            row.get(col, "") for col in (COL_SUMMARY, COL_DESCRIPTION, COL_STEPS, COL_EXPECTED_RESULT)
        ).lower()
        if needle in haystack:
            matches.append(row)
        if len(matches) >= safe_limit:
            break
    return matches


@mcp.tool
def get_test_case(issue_key: str) -> dict[str, str]:
    """Return a single test case by its Issue Key (e.g. VWO-1001)."""
    row = TEST_CASES_BY_KEY.get(issue_key.strip().upper())
    if row is None:
        raise ToolError(f"No test case found with issue_key='{issue_key}'.")
    return row


@mcp.tool
def test_case_stats(group_by: str) -> dict[str, int]:
    """Return counts of test cases grouped by module, priority, status, or test_type."""
    key = group_by.strip().lower()
    column = GROUPABLE_FIELDS.get(key)
    if column is None:
        valid = ", ".join(sorted(set(GROUPABLE_FIELDS)))
        raise ToolError(f"Unknown group_by='{group_by}'. Valid options: {valid}.")

    counts: dict[str, int] = {}
    for row in TEST_CASES:
        value = row.get(column, "").strip() or "Unknown"
        counts[value] = counts.get(value, 0) + 1
    return counts


# --- Resources ---


@mcp.resource("testcases://schema")
def get_schema() -> dict[str, str]:
    """Return the detected CSV column names and their inferred types."""
    return SCHEMA


@mcp.resource("testcases://all")
def get_all_test_cases() -> list[dict[str, str]]:
    """Return the full test case dataset as JSON."""
    return TEST_CASES


@mcp.resource("testcases://module/{name}")
def get_test_cases_by_module(name: str) -> list[dict[str, str]]:
    """Return all test cases belonging to a given component/module."""
    rows = [row for row in TEST_CASES if row.get(COL_COMPONENT, "").strip().lower() == name.strip().lower()]
    if not rows:
        raise ResourceError(f"No test cases found for module='{name}'.")
    return rows


# --- Prompts ---


@mcp.prompt
def review_test_case(issue_key: str) -> str:
    """Prompt template that asks the model to critique one test case's coverage and clarity."""
    row = TEST_CASES_BY_KEY.get(issue_key.strip().upper())
    if row is None:
        raise PromptError(f"No test case found with issue_key='{issue_key}'.")
    return (
        f"Review test case {row[COL_ISSUE_KEY]} ({row[COL_SUMMARY]}).\n\n"
        f"Preconditions: {row.get(COL_PRECONDITIONS, '')}\n"
        f"Steps: {row.get(COL_STEPS, '')}\n"
        f"Expected Result: {row.get(COL_EXPECTED_RESULT, '')}\n\n"
        "Critique this test case for coverage gaps (missing negative/boundary/edge scenarios) "
        "and clarity (ambiguous steps or expected results). Suggest concrete improvements."
    )


@mcp.prompt
def generate_regression_suite(module: str) -> str:
    """Prompt template that builds a regression suite from one module's test cases."""
    rows = [row for row in TEST_CASES if row.get(COL_COMPONENT, "").strip().lower() == module.strip().lower()]
    if not rows:
        raise PromptError(f"No test cases found for module='{module}'.")

    case_lines = "\n".join(
        f"- {row[COL_ISSUE_KEY]} [{row.get(COL_PRIORITY, '')}] {row[COL_SUMMARY]}" for row in rows
    )
    return (
        f"Build a regression test suite for the '{module}' module from these {len(rows)} test cases:\n\n"
        f"{case_lines}\n\n"
        "Group them by priority, flag any duplicate or overlapping coverage, and propose an "
        "execution order that surfaces high-risk failures first."
    )


if __name__ == "__main__":
    mcp.run()
