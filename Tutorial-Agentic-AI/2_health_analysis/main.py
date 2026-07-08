"""
Blood Work Analysis
"""
import json
from pathlib import Path

from extractor import extract_blood_work

rag_text = (Path(__file__).parent / "rag.txt").read_text()
blood_work_results = extract_blood_work(rag_text)

print(json.dumps(blood_work_results, indent=2))
