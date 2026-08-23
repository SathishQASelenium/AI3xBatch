# Test Strategy Builder Agent
#
# Creates customized test strategies aligned with project scope,
# tech stack, and release goals — reducing strategy creation time
# from days to minutes.
#
# Multi-agent workflow:
#   1. Strategy Analyst  — analyzes project metadata, scope, risks
#   2. Tool Recommender  — suggests tools based on tech stack
#   3. Strategy Writer   — assembles full ISTQB-aligned strategy doc

from crewai import Agent, Task, Crew, Process
from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

groq_llm = LLM(
    model=f"openai/{os.getenv('GROQ_MODEL')}",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL"),
)

# ── Agent 1: Strategy Analyst ──────────────────────────────────────────
strategy_analyst = Agent(
    role="Senior Test Strategy Analyst",
    goal=(
        "Analyze project metadata, tech stack, team composition, and "
        "release timeline to define test scope, risk areas, and quality gates."
    ),
    backstory=(
        "You are a seasoned test strategy consultant with 18+ years in "
        "enterprise QA. You've designed test strategies for 200+ projects "
        "across fintech, healthcare, e-commerce, and SaaS. You excel at "
        "identifying risk areas, defining test levels, and scoping effort "
        "based on team capacity and release deadlines."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False,
)

# ── Agent 2: Tool Recommender ──────────────────────────────────────────
tool_recommender = Agent(
    role="QA Tool Stack Architect",
    goal=(
        "Recommend the optimal test automation tools, frameworks, and "
        "infrastructure based on the project's tech stack and constraints."
    ),
    backstory=(
        "You are a test automation architect who has evaluated 100+ tools "
        "across web, mobile, API, performance, and security domains. You "
        "know exactly which tool fits which stack — Playwright for modern "
        "web apps, Appium for mobile, k6 for performance, OWASP ZAP for "
        "security, and so on. You also consider team skill level and "
        "budget when making recommendations."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False,
)

# ── Agent 3: Strategy Writer ───────────────────────────────────────────
strategy_writer = Agent(
    role="Test Strategy Document Author",
    goal=(
        "Synthesize analysis and tool recommendations into a comprehensive, "
        "well-structured test strategy document following ISTQB standards."
    ),
    backstory=(
        "You are a technical writer and QA lead who has authored test "
        "strategies for Fortune 500 companies. Your documents are known for "
        "being thorough, actionable, and easy for both technical and "
        "business stakeholders to understand. You follow the ISTQB test "
        "strategy template covering all key components."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False,
)

# ── Task 1: Analyze project scope & risks ──────────────────────────────
analysis_task = Task(
    description=(
        """Analyze the following project metadata and produce a structured analysis:

Project Name: {project_name}
Tech Stack: {tech_stack}
Team Size: {team_size}
Release Timeline: {release_timeline}
Compliance Requirements: {compliance}
Additional Context: {additional_context}

Your analysis MUST cover:
1. **Scope Definition** — What's in scope vs out of scope for testing
2. **Risk Assessment** — Top 5-7 risk areas with severity (High/Medium/Low)
3. **Test Levels** — Which ISTQB test levels apply (unit, integration, system, acceptance)
4. **Quality Gates** — Entry and exit criteria for each phase
5. **Environment Requirements** — What test environments are needed
6. **Team Capacity Assessment** — Can the team deliver with given timeline?
"""
    ),
    expected_output=(
        "A structured JSON-like analysis with sections: scope_definition, "
        "risk_assessment (list of risks with severity), test_levels, "
        "quality_gates, environment_requirements, and team_capacity_assessment."
    ),
    agent=strategy_analyst,
)

# ── Task 2: Recommend tools ────────────────────────────────────────────
tool_task = Task(
    description=(
        """Based on the tech stack and project context below, recommend tools:

Tech Stack: {tech_stack}
Project Name: {project_name}
Team Size: {team_size}
Compliance: {compliance}

For each testing category, recommend a specific tool with rationale:
1. **Functional / UI Automation** — e.g., Playwright, Selenium, Cypress
2. **API / Contract Testing** — e.g., REST Assured, Postman, Pact
3. **Performance / Load Testing** — e.g., k6, JMeter, Gatling
4. **Security Testing** — e.g., OWASP ZAP, Burp Suite, SonarQube
5. **Mobile Testing** (if applicable) — e.g., Appium, Detox, XCUITest
6. **Test Management** — e.g., Jira/Xray, TestRail, Zephyr
7. **CI/CD Integration** — how tests fit into the pipeline

Consider team skill level, open-source vs commercial, and community support.
"""
    ),
    expected_output=(
        "A categorized list of tool recommendations with tool name, "
        "category, rationale, and estimated learning curve for each."
    ),
    agent=tool_recommender,
)

# ── Task 3: Write the full strategy document ───────────────────────────
strategy_task = Task(
    description=(
        """Using the analysis from the Strategy Analyst and recommendations "
        "from the Tool Architect, write a complete test strategy document.

Project Name: {project_name}
Tech Stack: {tech_stack}
Team Size: {team_size}
Release Timeline: {release_timeline}
Compliance Requirements: {compliance}
Additional Context: {additional_context}

The document MUST include ALL of these sections:

1. **Executive Summary** — Brief overview of strategy
2. **Scope & Objectives** — What will be tested and why
3. **Risk Assessment & Mitigation** — Key risks and how to address them
4. **Test Levels & Types** — Unit, integration, system, acceptance, and non-functional
5. **Test Environment Strategy** — Environments, data, and configurations
6. **Tool & Framework Recommendations** — With rationale
7. **Entry & Exit Criteria** — Quality gates for each phase
8. **Test Deliverables** — What artifacts will be produced
9. **Roles & Responsibilities** — Who does what
10. **Defect Management Process** — How bugs are tracked and triaged
11. **Measurement & Metrics** — How quality is measured
12. **Phased Execution Plan** — Timeline broken into phases
13. **Appendices** — References, glossary, templates

Format the output in clean Markdown with proper headings (##, ###).
"""
    ),
    expected_output=(
        "A complete test strategy document in Markdown format with all 13 "
        "sections, ready to be exported to Confluence, Notion, or Google Docs."
    ),
    agent=strategy_writer,
    output_file="test_strategy_output.md",
)

# ── Crew ───────────────────────────────────────────────────────────────
crew = Crew(
    agents=[strategy_analyst, tool_recommender, strategy_writer],
    tasks=[analysis_task, tool_task, strategy_task],
    process=Process.sequential,  # Analyst → Tool Recommender → Writer
    verbose=True,
)

# ── Entry point ────────────────────────────────────────────────────────
if __name__ == "__main__":
    inputs = {
        "project_name": input("Project name: ").strip() or "E-Commerce Platform Redesign",
        "tech_stack": input("Tech stack (e.g., React, Node.js, PostgreSQL): ").strip()
                     or "React, Node.js, PostgreSQL, AWS",
        "team_size": input("Team size: ").strip() or "5 QA engineers, 10 devs",
        "release_timeline": input("Release timeline: ").strip() or "3 months (12 sprints)",
        "compliance": input("Compliance requirements (or 'None'): ").strip()
                      or "GDPR, WCAG 2.1 AA",
        "additional_context": input("Additional context (or press Enter to skip): ").strip()
                              or "",
    }

    result = crew.kickoff(inputs=inputs)
    print("\n" + "=" * 60)
    print("TEST STRATEGY GENERATED")
    print("=" * 60)
    print(result)

    # Also save a timestamped copy
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    copy_path = f"test_strategy_{ts}.md"
    with open(copy_path, "w", encoding="utf-8") as f:
        f.write(str(result))
    print(f"\nSaved to: {copy_path}")