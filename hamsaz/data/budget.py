from __future__ import annotations

from collections import OrderedDict

BUDGET_TIERS = OrderedDict(
    [
        (
            "budget",
            {
                "label": "Tight / budget-conscious",
                "description": (
                    "You need maximum value for money. Buying used, "
                    "refurbished, or entry-level is completely fine."
                ),
            },
        ),
        (
            "balanced",
            {
                "label": "Balanced / mid-range",
                "description": (
                    "You can afford solid, mainstream quality but still "
                    "want to avoid overpaying."
                ),
            },
        ),
        (
            "comfortable",
            {
                "label": "Comfortable",
                "description": (
                    "You can prioritize comfort, reliability, and extra "
                    "features over squeezing out the lowest price."
                ),
            },
        ),
        (
            "premium",
            {
                "label": "Premium / no real constraint",
                "description": (
                    "You want the option that best fits your needs, "
                    "largely independent of price."
                ),
            },
        ),
    ]
)

USE_CASES = OrderedDict(
    [
        ("general", "General use - browsing, email, streaming, documents"),
        ("office", "Office & business productivity, spreadsheets, video calls"),
        ("student", "Studying, note-taking, research, light multitasking"),
        ("gaming", "PC gaming at good settings and frame rates"),
        ("creative", "Photo/video editing, graphic design, music production"),
        ("programming", "Software development, local servers, containers, VMs"),
        ("data_science", "Data science, machine learning, large datasets"),
        ("engineering", "CAD, 3D modeling, simulation, engineering software"),
    ]
)
