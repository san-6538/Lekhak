import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()


def extract_essence(text: str) -> dict:
    """
    Extract abstract narrative essence from story text.
    No plot, no characters, no events.
    """

    if LLM_MODE == "mock":
        return {
            "themes": ["dignity", "power"],
            "central_conflict": "individual vs system",
            "moral_tension": "survival vs integrity",
            "emotional_arc": "hope → pressure → refusal",
            "power_dynamics": "asymmetric authority",
            "stakes": "identity and self-respect",
            "resolution_ethos": "quiet resistance"
        }

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
Analyze the following story and extract its abstract narrative essence.

DO NOT summarize the plot.
DO NOT reuse characters, events, or symbols.

Return STRICT JSON:

{{
  "themes": [],
  "central_conflict": "",
  "moral_tension": "",
  "emotional_arc": "",
  "power_dynamics": "",
  "stakes": "",
  "resolution_ethos": ""
}}

STORY:
{text}
"""

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You extract abstract narrative essence as strict JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    content = resp.choices[0].message.content
    start, end = content.find("{"), content.rfind("}")
    return json.loads(content[start:end+1])
