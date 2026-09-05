# Chapter 15 — DeepEval

Evaluating LLM output with [DeepEval](https://deepeval.com/), a pytest-native
framework for LLM evaluation.

Chapter 14 argues *why* traditional QA breaks on LLM-powered systems. This
chapter is the hands-on answer: you write assertions against non-deterministic
output, and a second LLM — the **judge** — scores them.

---

## The core idea

A normal assertion compares two values:

```python
assert response == "4"
```

That fails the moment the model answers `"The answer is 4."` — which is
correct. LLM output is non-deterministic, so equality is the wrong tool.

DeepEval replaces the comparison with a **metric**: a judge LLM scores the
output 0.0–1.0 against a rubric, and you assert on a threshold.

```python
metric = AnswerRelevancyMetric(threshold=0.9)
assert_test(test_case, [metric])
```

The consequences are the whole chapter:

- **Every assertion is a paid API call.** A 500-case suite is 500 calls per run.
- **The judge is itself an LLM**, so it can be wrong. Pin `temperature=0` and
  read the `reason` string it returns, don't just trust the number.
- **Thresholds are a design decision.** `0.9` is strict, `0.5` waves almost
  anything through. There is no default that is right for every metric.

---

## Verification status

Last verified **2026-09-05**, Windows 11 + CPython 3.14.4, judge
`openai/gpt-oss-120b` via OpenRouter:

| Check | Result |
| --- | --- |
| `pip install -r requirements.txt` | resolves clean |
| `pip check` | no broken requirements |
| `deepeval test run test_01_Anwser_Relevancy.py` | 1 passed, 100% |
| Score returned | 1.0 (threshold 0.9) |
| Run time / cost | ~15s / $0.00016 USD |

Not verified, and not claimed: macOS/Linux, the OpenAI and Groq provider paths
below, and any Python older than 3.14.

---

## Prerequisites

- Python 3.11+ (verified on 3.14.4)
- Working pytest knowledge — DeepEval *is* pytest, with extra metrics
- An API key for a judge LLM. Paid options: OpenRouter, OpenAI, Anthropic.
  Cheap/free tiers: Groq, NVIDIA NIM, AMD.

---

## Install

**Windows (PowerShell):**

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify:

```bash
python -c "import deepeval, requests; print(deepeval.__version__, requests.__version__)"
```

Deactivate when done: `deactivate`

> Install from `requirements.txt`, not `pip install -U deepeval`. The plain
> install omits `portalocker[win32]`, which every Windows run needs — see
> Troubleshooting.

---

## Configure the judge

DeepEval defaults to OpenAI and fails at run time if no provider is set. Pick
one, once per machine.

**OpenRouter** — what this chapter is configured for:

```powershell
deepeval set-openrouter -m "openai/gpt-oss-120b" -t 0 --save "dotenv:.env"
```

Reads `OPENROUTER_API_KEY` from `.env`. `-t 0` pins temperature to 0 so the
judge scores reproducibly across runs.

**OpenAI:**

```powershell
deepeval set-openai --model gpt-4o-mini      # needs OPENAI_API_KEY
```

**Groq** — speaks the OpenAI API, so register it as a *local model*:

```powershell
deepeval set-local-model --model openai/gpt-oss-120b `
  --base-url "https://api.groq.com/openai/v1" --format json --prompt-api-key
```

> `deepeval set-grok` is **xAI's Grok**, not Groq.com. Different vendor.

Check what actually won:

```powershell
deepeval diagnose
```

It prints the resolved model and the source precedence: process env →
`.env.local` → `.env` → `.deepeval/` → built-in defaults. Reach for this first
whenever a run behaves unexpectedly.

Undo with the matching `unset-` command (`deepeval unset-openrouter`).

---

## Run

```powershell
$env:PYTHONUTF8="1"
deepeval test run test_01_Anwser_Relevancy.py
```

Useful flags:

| Flag | Effect |
| --- | --- |
| `-v` | verbose — full judge reasoning per case |
| `-c` | use cached results, skips repeat API calls |
| `-n 4` | run 4 cases in parallel |
| `-r 3` | repeat each case 3x — exposes a flaky judge |
| `-d failing` | show only failures in the summary table |

Plain `pytest test_01_Anwser_Relevancy.py` also works, but prints no score
table and no token cost.

---

## Files

| File | Purpose |
| --- | --- |
| `test_01_Anwser_Relevancy.py` | Lab 1 — Answer Relevancy on a trivial Q&A pair |
| `requirements.txt` | Pinned deps + the Windows landmines, documented |
| `Notes.md` | Original class notes |
| `MyNotes.txt` | Step-by-step setup transcript |
| `.env` | API key + judge config. **Gitignored.** |
| `.deepeval/` | DeepEval keystore and run cache. **Gitignored.** |

---

## Troubleshooting

Three failures you will hit on Windows, in the order you hit them.

### 1. `AttributeError: 'NoneType' object has no attribute 'test_cases_lookup_map'`

Preceded by:

```
Warning: Could not load test run from disk: Shared locks on Windows require
the win32 extra (pywin32); msvcrt provides no true shared lock.
```

**The metric passed.** The results table says `PASSED` while pytest reports
`FAILED` — the crash is in the *cache write* after scoring.

`portalocker` without `pywin32` falls back to `msvcrt`, which cannot take a
shared lock. The lock fails, `get_cached_test_run()` returns `None`, and
DeepEval dereferences it without a null guard. Upstream bug, Windows only.

```powershell
pip install "portalocker[win32]"
```

### 2. `UnicodeEncodeError` inside a `rich` traceback

`deepeval diagnose` and the results table print box-drawing characters that a
cp1252 console cannot encode. The real error is buried under a wall of
`rich/console.py` frames.

```powershell
$env:PYTHONUTF8="1"                                              # this session
[Environment]::SetEnvironmentVariable("PYTHONUTF8","1","User")   # permanent
```

### 3. `Invalid value for --save: Unsupported --save option`

The syntax is `--save=dotenv[:path]`, not a bare path:

```powershell
deepeval set-openrouter -m "openai/gpt-oss-120b" --save "dotenv:.env"   # correct
deepeval set-openrouter -m "openai/gpt-oss-120b" --save .env            # errors
```

### 4. `OpenAI API key is not configured`

No judge provider set — DeepEval fell back to its OpenAI default. Run
`deepeval diagnose`, then the `set-` command for your provider.

---

## Watch out

- **Every metric assertion is a paid LLM call.** Keep golden datasets small.
  Use `-c` to reuse cached scores while iterating on test structure.
- **The judge is non-deterministic** unless you pin `-t 0`. Even then, scores
  drift across model versions — a suite that passes today can fail after a
  provider-side update with no change to your code.
- **Never commit a key.** `.env`, `.env.local`, `.deepeval/` and `.venv/` are
  gitignored at the repo root. Only `.env.example`-style templates belong in
  git.

---

## Known gaps

`test_01_Anwser_Relevancy.py` is incomplete as a teaching lab:

- Header promises "the two most fundamental metrics" and "Hallucination
  Detection", but only `AnswerRelevancyMetric` is implemented.
- `context=[...]` on the test case is ignored by `AnswerRelevancyMetric` —
  it feeds `HallucinationMetric` / `FaithfulnessMetric`.
- Only a **passing** case exists. Threshold tuning cannot be taught without a
  failing one (e.g. `actual_output="Paris is the capital of France"` against
  `input="What is 2+2?"` scores near 0).
