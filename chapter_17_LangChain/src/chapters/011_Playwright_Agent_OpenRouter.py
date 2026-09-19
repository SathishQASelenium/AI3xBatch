import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from playwright_tools import PLAYWRIGHT_TOOLS
import os

load_dotenv()


class SequentialToolsMiddleware(AgentMiddleware):
    """Force one tool call per model turn.

    Playwright tools share module-level browser state (_page, _browser), so
    running several at once on the same event loop races: one tool's action
    closes the page while the others are mid-flight. Keeping only the first
    tool call from each model response makes execution strictly sequential.
    """

    def after_model(self, state, runtime):
        messages = state.get("messages", [])
        if not messages:
            return None
        last = messages[-1]
        if isinstance(last, AIMessage) and last.tool_calls and len(last.tool_calls) > 1:
            # Keep only the first tool call; drop the rest so they run next turn.
            last.tool_calls = last.tool_calls[:1]
        return None


sequential_tools = SequentialToolsMiddleware()

# OpenRouter speaks the OpenAI API, so ChatOpenAI works unchanged:
# just point base_url at OpenRouter and use the OpenRouter key.
llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_LLM_MODEL", "deepseek/deepseek-chat"),
    api_key=os.getenv("OPENROUTER_LLM_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    # temperature=0 keeps tool calling deterministic. DeepSeek via OpenRouter
    # intermittently emits tool calls as markdown text at higher temperatures,
    # which the agent cannot execute.
    temperature=0,
)

SYSTEM_PROMPT = """
You are an automation testing agent that controls a real browser using Playwright.

Rules:
1. Always start by launching the browser before performing any action.
2. Perform the actions in the order they are requested.
3. Use clear CSS selectors to interact with elements on the page.
4. Take a screenshot before closing the browser to capture the final state.
5. At the end, report every step you took and whether the test PASSED or FAILED."""

TASK = """ Test the login functionality on https://app.thetestingacademy.com/playwright/ttacart/
1. Launch the browser
2. Navigate to the login page
3. Enter the username "standard_user"
4. Enter the password "tta_secret"
5. Click the login button
6. Close the browser
"""

async def main():
    agent = create_agent(
        model=llm,
        tools=PLAYWRIGHT_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        # Playwright tools share module-level browser state, so they must run
        # one at a time. Parallel tool calls race on the same event loop and
        # close the page mid-flight.
        middleware=[sequential_tools],
    )

    # Playwright's async API needs ainvoke: every tool call runs on the same event loop
    result = await agent.ainvoke({"messages": [{"role": "user", "content": TASK}]})

    # Show each tool call and what the browser answered
    print("\n===== Steps taken =====")
    for msg in result["messages"]:
        if msg.type == "ai" and msg.tool_calls:
            for call in msg.tool_calls:
                print(f"-> {call['name']}({call['args']})")
        elif msg.type == "tool":
            print(f"   {msg.content}")

    print("\n===== Final Result =====")
    print(result["messages"][-1].text)   # .text joins the reply's text blocks


asyncio.run(main())