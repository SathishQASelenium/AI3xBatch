"""Dummy Slack MCP tools for the reporter agent.

Nothing is actually sent to Slack. The tool records the message so the run can
show what WOULD have been posted. Swap in a real Slack MCP later by replacing
SLACK_TOOLS with the real tool list.
"""

from langchain.tools import tool

_sent: list[str] = []


class _DummySlackMCP:
    """Stand-in for the Slack MCP server connection."""

    @staticmethod
    def connect() -> str:
        return "[DUMMY Slack MCP] connected (nothing will be sent)"


@tool
def slack_post_message(channel: str, text: str) -> str:
    """Post a message to a Slack channel. Returns a confirmation string.

    Args:
        channel: the channel to post to, e.g. #qa-automation
        text: the message body (Slack mrkdwn)
    """
    _sent.append(f"#{channel.lstrip('#')}: {text}")
    return f"Message recorded for {channel} (DUMMY - not actually sent)"


SLACK_TOOLS = [slack_post_message]


def sent_messages() -> list[str]:
    """Return the messages recorded so far (for the run summary)."""
    return list(_sent)