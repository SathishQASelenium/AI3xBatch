"""Local RAG over the team's existing test-case library.

Loads rag_corpus/tta_testcases.json and returns the most similar cases for a
query using a simple token-overlap (BM25-ish) scorer. No external vector DB:
good enough to demonstrate "ground the plan in what already exists".
"""

import json
import math
import re
from collections import Counter
from pathlib import Path

_CORPUS = Path(__file__).parent / "rag_corpus" / "tta_testcases.json"


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class TestCaseRAG:
    """Minimal in-memory RAG: tokenize the corpus, score by TF-IDF overlap."""

    def __init__(self, corpus_path: Path | None = None) -> None:
        path = corpus_path or _CORPUS
        self.cases = json.loads(path.read_text(encoding="utf-8"))
        self.backend = f"local-tfidf ({path.name})"
        # Pre-tokenize each case once.
        self._docs = [
            _tokens(f"{c['title']} {c['area']} {' '.join(c['tags'])} "
                    f"{' '.join(c['steps'])} {c['expected']}")
            for c in self.cases
        ]
        self._idf = self._build_idf()

    def _build_idf(self) -> dict[str, float]:
        n = len(self._docs)
        df: Counter = Counter()
        for doc in self._docs:
            df.update(set(doc))
        return {term: math.log((1 + n) / (1 + count)) + 1.0
                for term, count in df.items()}

    def search(self, query: str, k: int = 5) -> list[tuple[float, dict]]:
        q = Counter(_tokens(query))
        scored = []
        for doc, case in zip(self._docs, self.cases):
            # .get() -> 0.0 for query tokens absent from the corpus, so a
            # token like "end" that never appears cannot raise a KeyError.
            qd = sum(self._idf.get(t, 0.0) * min(q[t], doc.count(t)) for t in q)
            scored.append((qd, case))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]


def format_for_prompt(hits: list[tuple[float, dict]]) -> str:
    """Render retrieved cases as a compact block the planner can read."""
    lines = []
    for score, c in hits:
        lines.append(
            f"- {c['id']} [{c['type']}] {c['title']} (score {score:.3f})\n"
            f"    steps: {' | '.join(c['steps'])}\n"
            f"    expected: {c['expected']}\n"
            f"    tags: {', '.join(c['tags'])}"
        )
    return "\n".join(lines) if lines else "(no similar cases found)"