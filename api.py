from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os
from dotenv import load_dotenv
import wikipedia

from understand import extract_essence
from world import remap_world
from reimagine import generate_story
from schema import validate_story

# ---------------- Startup ----------------

load_dotenv()

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()
if LLM_MODE not in {"mock", "openai"}:
    raise RuntimeError("Invalid LLM_MODE")

print("LLM_MODE =", LLM_MODE)

app = FastAPI(title="Lekhak API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Schemas ----------------

class StoryInput(BaseModel):
    type: Literal["popular", "raw"]
    name: Optional[str] = None
    text: Optional[str] = None


class NormalizeRequest(BaseModel):
    story: StoryInput


class NormalizeResponse(BaseModel):
    normalized_text: str


class ReimagineRequest(BaseModel):
    normalized_text: str
    universe: str
    tone: str
    genre: str
    temperature: float = Field(0.7, ge=0.0, le=1.0)


class ReimagineResponse(BaseModel):
    essence: dict
    world: dict
    story: dict

# ---------------- Endpoints ----------------

@app.get("/")
def health():
    return {"status": "ok", "llm_mode": LLM_MODE}


@app.post("/normalize", response_model=NormalizeResponse)
def normalize(req: NormalizeRequest):
    s = req.story

    if s.type == "popular":
        if not s.name:
            raise HTTPException(400, "Story name required")
        try:
            text = wikipedia.page(s.name).summary
        except Exception:
            text = f"High-level description of the story {s.name}."
    else:
        if not s.text:
            raise HTTPException(400, "Story text required")
        text = s.text

    return NormalizeResponse(normalized_text=text)


@app.post("/reimagine", response_model=ReimagineResponse)
def reimagine(req: ReimagineRequest):
    try:
        essence = extract_essence(req.normalized_text)
        world = remap_world(
            essence=essence,
            universe=req.universe,
            tone=req.tone,
            genre=req.genre
        )
        story = generate_story(
            essence=essence,
            world=world,
            temperature=req.temperature
        )

        validate_story(story)

        return ReimagineResponse(
            essence=essence,
            world=world,
            story=story
        )

    except Exception as e:
        raise HTTPException(500, str(e))
