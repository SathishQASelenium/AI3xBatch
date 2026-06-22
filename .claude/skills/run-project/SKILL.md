---
name: run-project
description: Start the dev server for whichever AI3x sub-project is currently active. Detects correct directory and command from context.
---

Identify which sub-project the user is working in and start its dev server.

Project → directory → command:
- BLAST Jira AI Agent → `chapter_03_BLAST_FW_JIRA_AI_AGENT/` → `npm run dev` (http://localhost:5173, Vite + Express proxy)
- ContentForge → `chapter_04_AI_Agents_n8n/social_ai_agent/contentforge/` → `npm run dev` (Next.js)
- Flaky Test Analyzer → `chapter_05_AI_Agents_LangFlow/flaky_test_analyzer_ai_Agent/ui/` → `npm run dev` (Vite, proxies LangFlow at :7861)
- Job Tracker AI → `Project_Job_TRACKERAI/` → `npm run dev` (http://localhost:5173)

Steps:
1. Identify sub-project from context (open files, user message, directory)
2. If ambiguous, ask which one
3. Check for `node_modules/` — run `npm install` first if missing
4. Start the dev server from the correct sub-directory
5. Report the URL
