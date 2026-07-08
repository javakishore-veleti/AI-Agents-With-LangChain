import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

FILE_EXTRACTION_PROMPT = """
You are a medical data extraction assistant.
You are given text that may contain blood work or lab results for a patient.
Extract every lab test you can find from the text.

Patient report:
{rag_text}

Rules:
- Return ONLY valid JSON. Do not include markdown, code fences, or explanation text.
- If the text is not a blood work or lab report, return: {{"blood_work_results": []}}
- Use an empty string for test_value when a value is missing.
- Include section_name when the report groups tests into sections.

Required JSON format:
{{
    "blood_work_results": [
        {{
            "section_name": "section_name",
            "test_name": "test_name",
            "test_value": "test_value"
        }}
    ]
}}
"""


def extract_json(text: str) -> dict:
    """Parse JSON from raw LLM output, including markdown code fences."""
    if not text or not text.strip():
        raise ValueError("The model returned an empty response.")

    cleaned = text.strip()

    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if fenced_match:
        cleaned = fenced_match.group(1)
    else:
        object_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if object_match:
            cleaned = object_match.group(0)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        preview = text.strip()[:300]
        raise ValueError(
            "The model did not return valid JSON. "
            "Try pasting a blood work report or use the sample report."
            f"\n\nModel response preview:\n{preview}"
        ) from exc


def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )


def extract_blood_work(report_text: str) -> dict:
    llm = get_llm()
    response = llm.invoke(FILE_EXTRACTION_PROMPT.format(rag_text=report_text))
    return extract_json(response.content)
