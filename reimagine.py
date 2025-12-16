import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()


def generate_story(essence: dict, world: dict, temperature: float) -> dict:
    """
    Generate full literary story from essence + world constraints.
    """

    if LLM_MODE == "mock":
        return {
            "outline": {
                "act_1": "Setup",
                "act_2": "Escalation",
                "act_3": "Resolution"
            },
            "characters": [],
            "themes": essence["themes"],
            "narrative_arc": essence["emotional_arc"],
            "final_story": "[MOCK STORY OUTPUT]"
        }

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
Write a complete original story of 1500–2000 words.

WORLD:
{json.dumps(world, indent=2)}

ESSENCE:
{json.dumps(essence, indent=2)}

Rules:
- No reference to the original story
- No reused characters
- Internally consistent world
- Resolution must follow resolution_ethos
- No deus ex machina

Return STRICT JSON:

{{
  "outline": {{
    "act_1": "",
    "act_2": "",
    "act_3": ""
  }},
  "characters": [
    {{
      "name": "",
      "role": "",
      "motivation": "",
      "trait": ""
    }}
  ],
  "themes": [],
  "narrative_arc": "",
  "final_story": ""
}}
"""

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a serious literary novelist producing strict JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=9000,
    )

    content = resp.choices[0].message.content
    start, end = content.find("{"), content.rfind("}")
    return json.loads(content[start:end+1])
