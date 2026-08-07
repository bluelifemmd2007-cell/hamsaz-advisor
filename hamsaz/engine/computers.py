"""Comprehensive computer-buying advice by use case, budget, and climate.

This module is deliberately the most detailed one in the engine, because
"what computer should I buy" is rarely a single-axis question. It combines:

- use case (gaming, creative work, programming, data science, engineering...)
- budget tier
- desktop-vs-laptop factors (grid reliability, space, mobility)
- climate-specific operating/maintenance advice
"""
from __future__ import annotations

from .models import Recommendation, UserProfile

# Core spec guidance per use case, independent of budget tier. Budget tier
# scales *how much* to spend on each of these, not *which* components matter.
_USE_CASE_SPECS = {
    "general": {
        "summary": (
            "For browsing, email, streaming, and documents, almost any "
            "current mid-range machine is overkill in the best way - "
            "prioritize battery life, screen quality, and build quality "
            "over raw performance."
        ),
        "cpu": "Any current-generation mainstream CPU (mid-range Intel Core, AMD Ryzen, or Apple silicon)",
        "gpu": "Integrated graphics are sufficient - no dedicated GPU needed",
        "ram": "8-16 GB is comfortable for years of everyday multitasking",
        "storage": "256-512 GB SSD (NVMe preferred) - avoid mechanical hard drives entirely",
        "extra": "A comfortable keyboard and a sharp, matte-ish screen matter more here than benchmarks",
    },
    "office": {
        "summary": (
            "Office work rewards a machine that handles video calls, "
            "spreadsheets, and multiple browser tabs smoothly all day "
            "without becoming a laptop-vs-desk-space headache."
        ),
        "cpu": "Mid-range mainstream CPU is plenty; prioritize sustained performance over peak benchmarks",
        "gpu": "Integrated graphics are fine unless doing heavy design work",
        "ram": "16 GB is the sweet spot for many browser tabs plus office apps running together",
        "storage": "512 GB SSD, plus cloud or NAS backup for shared documents",
        "extra": "A good webcam and microphone (built-in or external) pay off constantly in video calls",
    },
    "student": {
        "summary": (
            "Students need portability and battery life first, enough "
            "power for occasional heavier apps second, and durability to "
            "survive years of daily transport."
        ),
        "cpu": "Mid-range mainstream CPU with efficient power draw for all-day battery life",
        "gpu": "Integrated graphics unless the field of study requires more (engineering, design, CS with local ML work)",
        "ram": "16 GB gives real headroom for multitasking between research, notes, and media",
        "storage": "512 GB SSD - course materials, media, and software add up faster than expected",
        "extra": "Weight and battery life matter more day-to-day than raw performance for most fields of study",
    },
    "gaming": {
        "summary": (
            "Gaming performance is GPU-led: spend disproportionately on the "
            "graphics card or GPU tier relative to everything else in the build."
        ),
        "cpu": "A current mid-to-high tier gaming CPU that won't bottleneck the GPU",
        "gpu": "The single most important component - buy the best dedicated GPU your budget allows",
        "ram": "16-32 GB, with 32 GB future-proofing newer titles",
        "storage": "1 TB NVMe SSD minimum - modern game install sizes are large",
        "extra": "A quality display (high refresh rate for competitive titles, color accuracy for immersive titles) and good cooling/airflow in the case",
    },
    "creative": {
        "summary": (
            "Creative work (photo/video editing, design, music production) "
            "is memory- and storage-hungry, and benefits heavily from a "
            "color-accurate display."
        ),
        "cpu": "A high core-count CPU for video encoding/rendering and multitasking",
        "gpu": "A dedicated GPU with strong video encode/decode support (matters a lot for video editing speed)",
        "ram": "32 GB is a realistic baseline for modern photo/video workflows",
        "storage": "1 TB+ fast NVMe SSD, plus external/NAS storage for project archives",
        "extra": "A color-accurate, ideally factory-calibrated display is often more impactful than extra CPU power",
    },
    "programming": {
        "summary": (
            "Development work rewards fast storage and enough RAM to run "
            "an IDE, containers, and local services simultaneously without slowdown."
        ),
        "cpu": "A strong multi-core CPU - compiling, containers, and local builds benefit directly from more cores",
        "gpu": "Integrated graphics are fine unless also doing ML/graphics work",
        "ram": "32 GB is comfortable for running an IDE, containers, and services together; 16 GB is a workable minimum",
        "storage": "1 TB NVMe SSD - fast storage noticeably speeds up builds, containers, and version control operations",
        "extra": "A second monitor is one of the highest-value upgrades for development productivity",
    },
    "data_science": {
        "summary": (
            "Local data science/ML work is RAM- and, for model training, "
            "GPU-hungry; for anything beyond small models, factor in cloud "
            "GPU rental instead of maxing out a laptop."
        ),
        "cpu": "A high core-count CPU for data processing pipelines",
        "gpu": "A dedicated GPU with ample VRAM if training models locally; otherwise integrated graphics plus cloud GPU access is more cost-effective",
        "ram": "32-64 GB - large datasets in memory are the most common local bottleneck",
        "storage": "1 TB+ fast NVMe SSD for datasets and model checkpoints",
        "extra": "For serious model training, budget for cloud GPU credits rather than an ultra-high-end local GPU that ages quickly",
    },
    "engineering": {
        "summary": (
            "CAD, 3D modeling, and simulation software are demanding on "
            "both CPU and a workstation-class GPU, and benefit from a "
            "larger, high-resolution display."
        ),
        "cpu": "A high-performance multi-core CPU, ideally validated against your specific CAD/simulation software's requirements",
        "gpu": "A workstation-class or high-VRAM GPU certified for your CAD software where possible",
        "ram": "32-64 GB for complex assemblies and simulations",
        "storage": "1 TB+ fast NVMe SSD - large assembly files and simulation outputs add up quickly",
        "extra": "Check your specific software vendor's certified hardware list before buying - CAD software is often picky about GPU drivers",
    },
}

_BUDGET_SCALING = {
    "budget": (
        "Buy one tier below what feels exciting on paper, and prioritize "
        "RAM and SSD storage over CPU/GPU speed bumps - a well-configured "
        "budget machine outperforms a poorly-configured expensive one for "
        "almost every real workload."
    ),
    "balanced": (
        "This tier gives real choice: spend on the component that matters "
        "most for your specific use case (GPU for gaming, RAM for "
        "programming/data work, display for creative work) and keep the "
        "rest mainstream."
    ),
    "comfortable": (
        "You can comfortably buy above the minimum spec for your use case, "
        "which buys meaningful longevity - expect 4-6 years of solid "
        "service before the machine feels dated."
    ),
    "premium": (
        "Buy the best-reviewed option for your exact use case rather than "
        "the most expensive one - beyond a certain point, extra spending "
        "buys marginal gains unless your workload specifically needs it."
    ),
}

_DESKTOP_VS_LAPTOP = {
    "stable": (
        "With a reliable power grid, choose freely between desktop and "
        "laptop based on mobility needs: desktops give more performance "
        "per dollar and easier upgrades, laptops give portability."
    ),
    "variable": (
        "With a somewhat unreliable grid, a laptop has a real practical "
        "advantage: its battery acts as automatic, built-in backup power "
        "during short outages that would otherwise crash a desktop mid-task."
    ),
    "unstable": (
        "With frequent power outages, strongly favor a laptop over a "
        "desktop for any primary/work machine - if you do need a desktop "
        "(for gaming or workstation power), pair it with a real UPS rated "
        "for at least 10-15 minutes of runtime."
    ),
}

_GLOSSARY = [
    "CPU (processor): handles general computation - more cores help multitasking and background tasks",
    "GPU (graphics card): handles graphics and, increasingly, AI workloads - critical for gaming and creative work",
    "RAM (memory): short-term working space - running out of RAM causes system-wide slowdowns, not just app crashes",
    "SSD/NVMe (storage): NVMe SSDs are dramatically faster than older SATA SSDs or mechanical hard drives for everyday responsiveness",
    "Refresh rate: how many times per second a display updates - matters most for gaming and fast-motion video",
]


def recommend(profile: UserProfile) -> Recommendation:
    spec = _USE_CASE_SPECS[profile.use_case]

    picks = [
        f"CPU: {spec['cpu']}",
        f"GPU: {spec['gpu']}",
        f"RAM: {spec['ram']}",
        f"Storage: {spec['storage']}",
        f"Also worth it: {spec['extra']}",
    ]

    avoid = [
        "A mechanical hard drive as your primary/boot drive - it will bottleneck everything else in the system",
        "Buying based on CPU clock speed or core count alone without checking real-world benchmarks for your use case",
    ]

    tips = [
        _BUDGET_SCALING[profile.budget_tier],
        _DESKTOP_VS_LAPTOP[profile.grid_reliability],
    ]

    if profile.climate_key in ("hot_arid", "hot_semi_arid", "cold_semi_arid"):
        tips.append(
            "Dusty, dry climates clog fans and heatsinks quickly - choose a "
            "case/laptop with easily removable dust filters and clean them "
            "every few months."
        )

    if profile.climate_key in ("tropical_humid", "tropical_savanna", "humid_subtropical"):
        tips.append(
            "In humid climates, favor good case airflow over silence-focused "
            "sealed designs, and keep the machine in air-conditioned or "
            "dehumidified space when possible to avoid internal condensation."
        )

    if profile.climate_key in ("continental", "subarctic"):
        tips.append(
            "If you carry a laptop between cold outdoor temperatures and a "
            "warm room, let it sit closed for 15-20 minutes to reach room "
            "temperature before powering it on - this avoids internal condensation."
        )

    if profile.highland:
        tips.append(
            "Thinner high-altitude air cools electronics less efficiently - "
            "favor a machine with strong independent reviews for thermal "
            "performance rather than the thinnest/lightest option available."
        )

    if profile.grid_reliability != "stable":
        picks.append("A UPS (uninterruptible power supply) for any desktop setup, sized for at least 10-15 minutes of runtime")

    tips.append("Glossary: " + "; ".join(_GLOSSARY))

    return Recommendation(
        category="computer",
        headline=f"Building or buying a computer for: {profile.use_case.replace('_', ' ')}",
        summary=spec["summary"],
        picks=picks,
        avoid=avoid,
        tips=tips,
    )
