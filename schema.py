def validate_story(output: dict):
    required = ["outline", "characters", "themes", "narrative_arc", "final_story"]
    for key in required:
        if key not in output:
            raise ValueError(f"Missing required field: {key}")

    if not isinstance(output["characters"], list):
        raise ValueError("Characters must be a list")
