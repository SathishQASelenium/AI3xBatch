# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AI3x Batch: educational curriculum with 6 working sub-projects covering prompt engineering, Java test automation, and AI agent development. Each chapter/project is a self-contained sub-directory with its own dependencies.

## Sub-Project Commands

### Java Projects (Maven)

**Selenium Framework** (`chapter_02_Prompt_Eng/Project2_Selenium_Framework/AdvanceSeleniumFramework/`):
```bash
mvn clean test
mvn test -DsuiteXmlFile=testng-smoke.xml   # specific suite
```

**REST API Framework** (`Project_02_REST_API_Framework/RICEPOT_RESTASSURED_API_Project/`):
```bash
mvn test    # runs tests + generates Allure report artifacts
```

### Node.js / React Projects

**BLAST Jira AI Agent** (`chapter_03_BLAST_FW_JIRA_AI_AGENT/`):
```bash
npm run dev          # Vite + Express proxy — http://localhost:5173
npm run handshake    # verify Jira + Groq connectivity before full run
```

**ContentForge** (`chapter_04_AI_Agents_n8n/social_ai_agent/contentforge/`):
```bash
npm run dev          # Next.js dev server
npm run scheduler    # content generation cron job
npm run typecheck    # tsc --noEmit (only TypeScript gate in repo)
```

**Flaky Test Analyzer UI** (`chapter_05_AI_Agents_LangFlow/flaky_test_analyzer_ai_Agent/ui/`):
```bash
npm run dev    # Vite — proxies LangFlow at :7861
```

**Job Tracker AI** (`Project_Job_TRACKERAI/`):
```bash
npm run dev    # Vite — http://localhost:5173
```

## Environment Variables

**Chapter 03** (`.env` at `chapter_03_BLAST_FW_JIRA_AI_AGENT/`):
```
GROQ_KEY=
JIRA_EMAIL=
JIRA_API_TOKEN=
JIRA_URL=https://<domain>.atlassian.net
PORT=8787   # optional proxy override
```

**Chapter 04** (`.env.local` at `contentforge/`):
```
GROQ_API_KEY=
GEMINI_API_KEY=
```

## Framework Conventions

### Java / Selenium
- All pages extend `BasePage` — no exceptions
- `WebDriverWait` + `ExpectedConditions` only — no `Thread.sleep()`
- `ThreadLocal<WebDriver>` for parallel test safety
- Default: Chrome headless
- Locator priority: `data-testid` → ARIA roles → labels → text

### Prompt Engineering (RICE-POT / BLAST)
- All prompts include `ANTI_HALLUCINATION` block: model must report "Insufficient information" for unknowns rather than invent
- Pin `temperature=0` for reproducible test case generation
- RICE-POT structure: Role, Instructions, Context, Examples, Persona, Output format, Task
- BLAST coverage: Boundary, Logic, Action, State, Timing

## Key Gotchas

- **CORS proxy required**: Chapter 03 + 05 proxy Jira/LangFlow via Vite/Express (`/api → :8787`, `/langflow → :7861`). Direct browser calls to Jira Cloud are blocked.
- **Vercel read-only filesystem**: Chapter 03 "Save to server" is disabled on Vercel — users must use "Download .md" instead.
- **Job Tracker is local-only**: IndexedDB (idb library) with no backend. Don't suggest API calls or persistence layers.
- **LangFlow placeholder IDs**: Chapter 05 uses flow/component IDs like `File-daKW7` that must match the actual imported LangFlow instance — not constants.
- **n8n credentials**: Workflow JSONs use placeholder credential IDs injected at import time, not from source.

## CI / CD

- GitHub Actions: REST API project only (`.github/workflows/api-tests.yml`) — triggers on push to main, runs `mvn test`, uploads Allure artifacts.
- Vercel: Chapter 03 deploys to https://testplanbuddy.vercel.app — Groq/Jira env vars set in Vercel dashboard, not in repo.
