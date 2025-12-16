"""
Streamlit frontend for Lekhak story reimagination
Compatible with essence → world → story pipeline
"""

import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Lekhak – Story Reimagination",
    layout="wide"
)

st.title("Lekhak – Story Reimagination")
st.caption("Reimagine stories across universes while preserving narrative essence")

# ---------------- Session State ----------------

if "normalized_text" not in st.session_state:
    st.session_state.normalized_text = None

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- Sidebar ----------------

with st.sidebar:
    st.header("Backend Status")
    try:
        r = requests.get(f"{API_URL}/", timeout=2)
        if r.status_code == 200:
            st.success("API Connected")
        else:
            st.error("API Error")
    except Exception:
        st.error("API Not Running")
        st.code("python api.py")

# ---------------- Step 1: Input ----------------

st.header("Step 1: Input Story")

col1, col2 = st.columns([1, 2])

with col1:
    story_type = st.radio(
        "Story Type",
        ["Popular Story", "Raw Story"]
    )

with col2:
    if story_type == "Popular Story":
        story_name = st.text_input(
            "Story Name",
            placeholder="Romeo and Juliet, Hamlet, The Great Gatsby"
        )
        story_payload = {"type": "popular", "name": story_name}
    else:
        story_text = st.text_area(
            "Raw Story Text",
            height=220,
            placeholder="Paste your story here"
        )
        story_payload = {"type": "raw", "text": story_text}

if st.button("Normalize Input", use_container_width=True):
    if story_type == "Popular Story" and not story_name:
        st.error("Story name is required")
    elif story_type == "Raw Story" and not story_text:
        st.error("Story text is required")
    else:
        with st.spinner("Normalizing input..."):
            try:
                res = requests.post(
                    f"{API_URL}/normalize",
                    json={"story": story_payload},
                    timeout=30
                )

                if res.status_code == 200:
                    data = res.json()
                    st.session_state.normalized_text = data["normalized_text"]
                    st.success("Input normalized")

                    with st.expander("View Normalized Text"):
                        st.write(st.session_state.normalized_text)
                else:
                    st.error(res.json().get("detail", "Unknown error"))

            except Exception as e:
                st.error(f"Request failed: {e}")

# ---------------- Step 2: Reimagination ----------------

st.divider()
st.header("Step 2: Reimagine Story")

if not st.session_state.normalized_text:
    st.warning("Please complete Step 1 first")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        universe = st.text_input(
            "Universe",
            placeholder="Cyberpunk Megacity, Bureaucratic State"
        )

    with col2:
        tone = st.text_input(
            "Tone",
            placeholder="dark, hopeful, tragic"
        )

    with col3:
        genre = st.text_input(
            "Genre",
            placeholder="sci-fi, drama, speculative"
        )

    temperature = st.slider(
        "Creativity Level",
        0.0, 1.0, 0.7, 0.1
    )

    if st.button("Generate Reimagined Story", use_container_width=True):
        if not universe or not tone or not genre:
            st.error("Universe, Tone, and Genre are required")
        else:
            with st.spinner("Reimagining story..."):
                try:
                    payload = {
                        "normalized_text": st.session_state.normalized_text,
                        "universe": universe,
                        "tone": tone,
                        "genre": genre,
                        "temperature": temperature
                    }

                    res = requests.post(
                        f"{API_URL}/reimagine",
                        json=payload,
                        timeout=120
                    )

                    if res.status_code == 200:
                        st.session_state.result = res.json()
                        st.success("Story generated")
                    else:
                        st.error(res.json().get("detail", "Unknown error"))

                except Exception as e:
                    st.error(f"Request failed: {e}")

# ---------------- Output ----------------

if st.session_state.result:
    result = st.session_state.result

    essence = result["essence"]
    world = result["world"]
    story = result["story"]

    st.divider()
    st.header("Narrative Essence")

    st.json(essence)

    st.header("World Translation")
    st.json(world)

    st.header("Reimagined Story")

    if "outline" in story:
        with st.expander("Outline"):
            for k, v in story["outline"].items():
                st.write(f"**{k.replace('_', ' ').title()}** — {v}")

    if "characters" in story:
        with st.expander("Characters"):
            for c in story["characters"]:
                st.markdown(f"**{c['name']}** ({c['role']})")
                st.caption(f"Motivation: {c['motivation']}")
                st.caption(f"Trait: {c['trait']}")

    if "themes" in story:
        st.markdown("**Themes:** " + ", ".join(story["themes"]))

    if "final_story" in story:
        st.subheader("Complete Story")
        st.write(story["final_story"])

    st.download_button(
        "Download JSON",
        json.dumps(result, indent=2),
        file_name="reimagined_story.json",
        mime="application/json"
    )
