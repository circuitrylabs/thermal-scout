import re

from thermal_scout.search import estimate_thermal_cost

test_cases = [
    ("model-100m", "Low"),
    ("model-350m", "Low"),
    ("model-1b", "Medium"),
    ("model-7b", "High"),
    ("model-13b", "High"),
]

for model_id, expected in test_cases:
    model_info = {"modelId": model_id, "tags": []}
    result = estimate_thermal_cost(model_info)

    # Debug parameter matching
    patterns = [
        (r"(?:^ < /dev/null | -)(\d{2,})b(?:$|-)", 4),
        (r"(?:^|-)([7-9])b(?:$|-)", 3),
        (r"(?:^|-)([4-6])b(?:$|-)", 3),
        (r"(?:^|-)([1-3])b(?:$|-)", 2),
        (r"(?:^|-)(\d+)b(?:$|-)", 3),
        (r"(?:^|-)(\d+)m(?:$|-)", 1),
    ]

    matched = False
    for pattern, score in patterns:
        if re.search(pattern, model_id):
            print(f"{model_id}: matched pattern {pattern} with score {score}")
            matched = True
            break

    if not matched:
        print(f"{model_id}: no pattern matched")

    print(
        f"  Expected: {expected}, Got: {result}, {'✓' if result == expected else '✗'}"
    )
    print()
