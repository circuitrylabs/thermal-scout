"""
Thermal-aware search functionality for Hugging Face models
"""

import re
from typing import Any

from huggingface_hub import HfApi


def estimate_thermal_cost(model_info: dict[str, Any]) -> str:
    """
    Estimate the thermal cost of a model based on its characteristics

    Returns: "Low", "Medium", or "High"
    """
    # Extract model size indicators
    model_id = model_info.get("modelId", "").lower()
    tags = [tag.lower() for tag in model_info.get("tags", [])]

    # Size patterns
    size_patterns = {
        "tiny": 1,
        "small": 1,
        "base": 3,
        "large": 4,
        "xl": 5,
        "xxl": 6,
    }

    # Check for parameter counts (order matters - most specific first)
    param_patterns = [
        (r"(?:^|-)(\d{2,})b(?:$|-)", 5),  # 10B+
        (r"(?:^|-)([7-9])b(?:$|-)", 4),  # 7-9B
        (r"(?:^|-)([4-6])b(?:$|-)", 4),  # 4-6B
        (r"(?:^|-)([1-3])b(?:$|-)", 3),  # 1-3B
        (r"(?:^|-)(\d+)b(?:$|-)", 4),  # Any B
        (r"(?:^|-)(\d+)m(?:$|-)", 1),  # Millions
    ]

    thermal_score = 3  # Default medium

    # Check model ID for size indicators
    for pattern, score in size_patterns.items():
        if pattern in model_id:
            thermal_score = score
            break

    # Check for parameter count (overrides size patterns)
    for pattern, score in param_patterns:
        if re.search(pattern, model_id):
            thermal_score = score
            break

    # Adjust based on tags
    if any("tiny" in tag for tag in tags):
        thermal_score = 1
    elif any("efficient" in tag or "distil" in tag for tag in tags):
        thermal_score = max(1, thermal_score - 2)
    elif any("large" in tag or "xxl" in tag for tag in tags):
        thermal_score = max(thermal_score, 5)

    # Map to thermal categories
    if thermal_score <= 1:
        return "Low"
    elif thermal_score <= 3:
        return "Medium"
    else:
        return "High"


def thermal_search(
    query: str,
    limit: int = 10,
    model_type: str | None = None,
    thermal_aware: bool = True,
) -> list[dict[str, Any]]:
    """
    Search Hugging Face Hub for models with optional thermal awareness
    """
    api = HfApi()

    try:
        # Search models
        search_kwargs = {
            "search": query,
            "limit": limit * 2
            if thermal_aware
            else limit,  # Get extra for thermal filtering
            "sort": "downloads",
            "direction": -1,
        }

        if model_type:
            search_kwargs["task"] = model_type

        models = api.list_models(**search_kwargs)

        results = []
        for model in models:
            model_dict = {
                "modelId": model.id,
                "downloads": getattr(model, "downloads", 0),
                "likes": getattr(model, "likes", 0),
                "tags": getattr(model, "tags", []),
                "pipeline_tag": getattr(model, "pipeline_tag", None),
                "library_name": getattr(model, "library_name", None),
            }

            if thermal_aware:
                model_dict["thermal_cost"] = estimate_thermal_cost(model_dict)
            else:
                model_dict["thermal_cost"] = estimate_thermal_cost(model_dict)

            results.append(model_dict)

        # Sort by thermal cost if thermal aware
        if thermal_aware:
            # Define sort order
            thermal_order = {"Low": 0, "Medium": 1, "High": 2}
            results.sort(
                key=lambda x: (
                    thermal_order.get(x.get("thermal_cost", "High"), 3),
                    -x.get("downloads", 0),
                )
            )

        return results[:limit]

    except Exception as e:
        print(f"Error searching models: {e}")
        return []
