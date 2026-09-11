#Flow:
# 1. Send "What is 2+2?" to the subject model (Qwen via OpenRouter).
# 2. Capture the raw answer.
# 3. Hand input + answer + context to DeepEval.
# 4. openai/gpt-oss-120b as judge -> scores AnswerRelevancy + Hallucination.
#    Subject != judge on purpose: a judge scoring its own family inflates scores.

import os

from dotenv import load_dotenv
from openai import OpenAI

from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval import assert_test

load_dotenv()

# Subject model = the thing under test. Both subject and judge go through
# OpenRouter here, which is fine: the "subject != judge" rule is about model
# family, not provider. qwen (subject) is still scored by gpt-oss (judge).
# The model ID must be a real OpenRouter slug, e.g. qwen/qwen3-32b.
SUBJECT_MODEL = os.getenv("SUBJECT_MODEL_NAME", "qwen/qwen3-32b")
JUDGE_MODEL = os.getenv("OPENROUTER_MODEL_NAME", "openai/gpt-oss-120b")

# OpenRouter speaks the OpenAI API, so the official openai SDK works
# unchanged: just point base_url at OpenRouter and use OPENROUTER_API_KEY.
# NOTE: deepeval's own OpenRouter path (the judge below) never reads
# OPENAI_API_KEY -- that var still holds the old gsk_... Groq key. Don't
# overwrite it with the OpenRouter key or any Groq client you keep around
# will start failing auth.
subject = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def llm_response(question):
    """Ask SUBJECT_MODEL one question and return its raw answer text."""
    response = subject.chat.completions.create(
        model=SUBJECT_MODEL,
        messages=[{"role": "user", "content": question}],
        # temperature=0 keeps the answer stable so the score below is
        # reproducible. The judge is still non-deterministic; this only
        # pins the thing under test.
        temperature=0,
    )
    return response.choices[0].message.content.strip()

question = "What is 2+2? Reply with just the number."
answer = llm_response(question)
print(f"\n[OpenRouter {SUBJECT_MODEL}] → {answer!r}\n")



def test_qwen_with_judge_gpt120b():
    case = LLMTestCase(
        input=question,
        actual_output=answer,
        expected_output="4",
        # HallucinationMetric scores actual_output against this grounding text.
        context=["Basic arithmetic fact: 2 + 2 = 4"],
    )

    metrics = [
        AnswerRelevancyMetric(threshold=0.8, model=JUDGE_MODEL),
        HallucinationMetric(threshold=0.3, model=JUDGE_MODEL),
    ]
    assert_test(case, metrics)