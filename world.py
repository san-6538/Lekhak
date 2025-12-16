import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()


def remap_world(essence: dict, universe: str, tone: str, genre: str) -> dict:
    """
    Translate abstract narrative forces into world-specific constraints.
    """

    if LLM_MODE == "mock":
        return {
            "world_setting": universe,
            "translated_conflict": f"{essence['central_conflict']} in {universe}",
            "translated_stakes": essence["stakes"],
            "power_structure": essence["power_dynamics"],
            "allowed_resolutions": ["refusal", "exit", "symbolic defiance"]
        }

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
Translate the following narrative essence into a new world.

ESSENCE:
{json.dumps(essence, indent=2)}

TARGET WORLD:
- Setting: {universe}
- Tone: {tone}
- Genre: {genre}

Return STRICT JSON:

{{
  "world_setting": "",
  "translated_conflict": "",
  "translated_stakes": "",
  "power_structure": "",
  "allowed_resolutions": []
}}
"""

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You translate narrative forces into world logic as strict JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1200,
    )

    content = resp.choices[0].message.content
    start, end = content.find("{"), content.rfind("}")
    return json.loads(content[start:end+1])
