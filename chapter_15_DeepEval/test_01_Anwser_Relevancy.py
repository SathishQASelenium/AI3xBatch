# Exercise 1 (Basic): Answer Relevancy
# Level Basic : chatbot anwsers

# Goal:
#     Learn the two most fundamental LLM evaluation metrics:
#     1. Answer Relevancy  — Does the chatbot answer the question asked?

# Setup: DeepEval needs a "judge" LLM to score the output. This chapter uses
# OpenRouter. Install first:  pip install -r requirements.txt
#
#   OpenRouter (what this chapter is configured for):
#     deepeval set-openrouter -m "openai/gpt-oss-120b" -t 0 --save "dotenv:.env"
#     Reads OPENROUTER_API_KEY from .env. Note the --save syntax: it is
#     --save="dotenv[:path]", NOT --save .env (that errors).
#
#   OpenAI (alternative):
#     deepeval set-openai --model gpt-4o-mini    # needs OPENAI_API_KEY in .env
#
#   Groq (alternative; OpenAI-compatible endpoint -> register as a local model):
#     deepeval set-local-model --model openai/gpt-oss-120b \
#         --base-url "https://api.groq.com/openai/v1" --format json --prompt-api-key
#     `deepeval set-grok` is xAI's Grok, NOT Groq.com. Different vendor.
#
# -t 0 pins temperature=0 so the judge scores reproducibly across runs.
# `deepeval diagnose` shows which provider actually won and from which file.
#
# Run (PowerShell):
#     $env:PYTHONUTF8="1"     # else rich's box-drawing chars crash a cp1252 console
#     deepeval test run test_01_Anwser_Relevancy.py
#
# Plain `pytest test_01_Anwser_Relevancy.py` also works, but prints no score
# table and no token cost.


from deepeval.test_case import LLMTestCase
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric

def test_hello_world():

    test = LLMTestCase(
        input="What is 2+2?",
        actual_output="4",
        expected_output="4",
        context=["Basic arithmetice perform and give result"]
    )
    metric = [AnswerRelevancyMetric(threshold=0.9)]
    assert_test(test, metric)