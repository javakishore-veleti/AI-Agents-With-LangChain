"""
Blood Work Analysis
"""
import json
import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def extract_json(text: str) -> dict:
    """Parse JSON from raw LLM output, including ```json code fences."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

rag_file = "2_health_analysis/rag.txt"
with open(rag_file, "r") as file:
    rag_text = file.read()

file_extraction_prompt = """
You are a medical data extraction assistant .
You are given a text file containing the blood work results of a patient.
Your task is to extract the blood work results from the text.
The text is in the following format:
{rag_text}
Return the blood work results in a JSON format.
The JSON format should be the following:
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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

response = llm.invoke(file_extraction_prompt.format(rag_text=rag_text))
blood_work_results = extract_json(response.content)

print(json.dumps(blood_work_results, indent=2))