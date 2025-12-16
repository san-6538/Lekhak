

# 📚 Lekhak — Essence-Preserving Story Reimagination Engine

Lekhak is a **multi-stage AI storytelling system** that reimagines stories across entirely new universes while preserving only their **abstract narrative essence**—not plot, characters, or structure.

Unlike prompt-only rewriting tools, Lekhak enforces originality, coherence, and explainability through a **structured semantic pipeline**.

---

## 🚀 What Problem Does Lekhak Solve?

Most AI writing tools:

* Rewrite text directly
* Risk imitation or plagiarism
* Collapse into summaries at low temperature
* Lose coherence at high temperature

**Lekhak solves this by design**, not by instruction.

It transforms:

```
Story → Meaning → World Logic → New Story
```

This guarantees:

* Conceptual distance from the source
* Strong narrative coherence
* Ethical and defensible AI-generated content

---

## 🧠 Core Idea

> **Preserve narrative essence, not narrative form**

Lekhak discards:

* Plot
* Characters
* Events
* Symbols

And preserves only:

* Themes
* Central conflict
* Moral tension
* Emotional arc
* Power dynamics
* Resolution ethos

---

## 🏗️ Architecture Overview

### Pipeline Stages

```
Input Story
   ↓
Normalization
   ↓
Narrative Essence Extraction
   ↓
World Remapping
   ↓
Constrained Story Generation
   ↓
Schema Validation
   ↓
Final Output
```

Each stage acts as a **guardrail**, preventing common LLM failure modes.

---

## 📂 Project Structure

```
lekhak/
│
├── api.py               # FastAPI orchestrator
├── understand.py        # Extracts abstract narrative essence
├── world.py             # Remaps essence into new world logic
├── reimagine.py         # Generates original story
├── schema.py            # Validates output structure
├── frontend.py          # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 🔐 Guardrails (By Design)

Lekhak uses **layered guardrails**, not a single safety filter.

| Layer                 | File            | Purpose                    |
| --------------------- | --------------- | -------------------------- |
| Input validation      | `api.py`        | Prevent malformed requests |
| Semantic abstraction  | `understand.py` | Prevent plot copying       |
| Logical constraints   | `world.py`      | Prevent deus ex machina    |
| Creative control      | `reimagine.py`  | Prevent format drift       |
| Structural validation | `schema.py`     | Prevent broken output      |

Originality is **structural**, not requested.

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **LLM:** OpenAI (via new SDK client)
* **Language:** Python 3.9+
* **Config:** `.env` via python-dotenv

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
LLM_MODE=openai
```

To run without API calls (mock mode):

```env
LLM_MODE=mock
```

---

## ▶️ How to Run

### 1️⃣ Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start backend

```bash
python api.py
```

Backend runs at:

```
http://localhost:8000
```

### 4️⃣ Start frontend

```bash
streamlit run frontend.py
```

---

## 🧪 Mock Mode vs Real LLM Mode

| Mode     | Purpose                             |
| -------- | ----------------------------------- |
| `mock`   | UI + pipeline testing, no API calls |
| `openai` | Real story generation               |

Switch using `.env` only — no code changes needed.

---

## ✍️ Output Format

Lekhak returns **structured JSON**, not raw text:

```json
{
  "outline": { "act_1": "...", "act_2": "...", "act_3": "..." },
  "characters": [...],
  "themes": [...],
  "narrative_arc": "...",
  "final_story": "1500–2000 word original story"
}
```

This makes the system:

* API-friendly
* Evaluatable
* Extendable

---

## 🧠 Why This Is Novel

* Separates **understanding** from **generation**
* Enforces originality **before** writing
* Allows higher creativity without chaos
* Produces explainable outputs
* Model-agnostic by design

This is **AI system design**, not prompt engineering.

---

## 🧩 Future Improvements

* Automated evaluation (coherence, novelty)
* RAG-based theme grounding
* Multi-act adaptive temperature
* Agent-based critique loop
* Publishing workflow integration

---

## 📜 License & Ethics

Lekhak is designed to:

* Avoid copyrighted reproduction
* Preserve only abstract narrative meaning
* Be transparent about AI usage

It is suitable for:

* Education
* Creative tooling
* Research
* Ethical AI demonstrations

---

## 🧑‍💻 Author

Sachin Kumar
