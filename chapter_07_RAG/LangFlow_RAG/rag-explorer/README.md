# Langflow RAG Explorer

Thin chat UI over a Langflow-hosted Naive RAG pipeline for an e-commerce test case
repository. All retrieval and generation happens **inside Langflow** — this app
never touches chunking, embeddings, or the vector store; it only calls Langflow's
REST API and renders the answer.

```
File → Parser → Split Text → Mistral Embeddings → ChromaDB (top 10)
     → Prompt Template → Groq llama-3.3-70b-versatile → Chat Output
```

![Langflow RAG Explorer UI](../../Langflow-Task-Testcases-Mistral-Groq-UI-Results.png)

*Real answer returned through the app: user question → Vite proxy → Langflow → Groq → chat bubble, rendered as Markdown.*

## How it works

1. User picks a suggestion chip or types a question.
2. The browser `fetch`es same-origin `POST /api/chat` with
   `{ output_type: "chat", input_type: "chat", input_value, session_id }`.
3. Vite's dev proxy (`vite.config.js`) rewrites that to
   `POST http://localhost:7860/api/v1/run/<flowId>?stream=false` and attaches the
   `x-api-key` header **server-side** — the key is read from `.env` at Vite boot
   and never appears in a browser network call.
4. Langflow runs the flow end-to-end (retrieval + Groq) and returns its response
   envelope.
5. `src/lib/api.js` defensively extracts
   `outputs[0].outputs[0].results.message.text`. If that path doesn't exist (flow
   changed, error payload, etc.), the bubble falls back to a collapsible **Raw
   response** block instead of showing blank.
6. A `session_id` (`ui-session-<timestamp>`) is generated once per browser tab via
   `sessionStorage` and reused for every message, so Langflow keeps one chat
   history thread per session.

## Setup

```bash
npm install
cp .env.example .env
```

| Variable | Purpose |
|---|---|
| `VITE_LANGFLOW_BASE_URL` | Langflow instance URL, e.g. `http://localhost:7860` |
| `VITE_LANGFLOW_FLOW_ID` | Flow UUID from Langflow's `Publish → API access` panel |
| `VITE_LANGFLOW_API_KEY` | Key from Langflow UI → Settings (gear) → **Langflow API Keys** |

These are only read server-side by `vite.config.js` (Node), not bundled into the
client, so the API key never ships to the browser despite the `VITE_` prefix.

Before running the UI: Langflow must be up on `:7860` with one of the
`../*.json` flow exports imported, its **File** component pointed at a CSV from
`../data/`, and ingestion already run inside Langflow so ChromaDB is populated.

## Run

```bash
npm run dev
```

Opens at `http://localhost:5176` (Vite bumps the port if it's taken — check the
terminal output). Click a suggestion chip or type a question about the test case
repository.

## Project layout

```
src/
  main.jsx                    entry point
  App.jsx                     chat state, send/receive, composer
  styles.css                  dark chat theme
  lib/api.js                  session id, fetch, defensive parse, error mapping
  components/
    PipelineBanner.jsx        static "File → ... → Answer" banner
    SuggestionChips.jsx       3 one-click sample questions
    ChatBubble.jsx            markdown answer bubble + raw-JSON fallback
vite.config.js                 /api/chat proxy + server-side x-api-key injection
```

## Error handling

| Condition | Message shown in chat |
|---|---|
| Network error / Langflow not running | "Langflow backend is not reachable. Please make sure Langflow is running on port 7860." |
| `401` / `403` | "Invalid or missing Langflow API key — check your .env file." |
| Other `4xx`/`5xx` | Langflow's own `detail`/`message`, or a generic status line |
| Response shape mismatch | Raw JSON in a collapsible "Raw response" block (never a blank bubble) |

**Seen a 401/403?** The key is invalid or expired — regenerate it in Langflow's
Settings, update `.env`, then restart `npm run dev` (env vars are only read at
server boot, so editing `.env` alone doesn't take effect until restart).

## Notes

- No database, no embedding libraries, no LLM SDKs in this app — Langflow is the
  entire RAG backend. The only external runtime dependency is a running Langflow
  instance.
- Stack kept minimal on purpose: Vite + React + `react-markdown`/`remark-gfm`
  for rendering the flow's formatted test-case lists (TID, Priority, Description).
