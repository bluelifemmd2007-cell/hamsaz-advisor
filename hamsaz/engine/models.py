"""Core data structures shared across the recommendation engine.

Keeping these as plain dataclasses (rather than framework-specific models)
means the engine can be tested and reused completely independently of Flask.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import List


#: Valid budget tier keys, ordered from least to most financial headroom.
BUDGET_TIERS = ("budget", "balanced", "comfortable", "premium")

#: Valid air quality descriptors used throughout the engine.
AIR_QUALITY_LEVELS = ("good", "moderate", "poor")

#: Valid electrical grid reliability descriptors.
GRID_RELIABILITY_LEVELS = ("stable", "variable", "unstable")

#: Valid computer/device use cases.
USE_CASES = (
    "general",
    "office",
    "student",
    "gaming",
    "creative",
    "programming",
    "data_science",
    "engineering",
)


@dataclass
class UserProfile:
    """Everything the engine knows about the person asking for advice.

    ``location_key`` is either a key into ``hamsaz.data.locations.LOCATIONS``
    or the literal string ``"custom"`` when the visitor described their own
    location manually instead of picking one from the list.
    """

    location_key: str
    location_name: str
    climate_key: str
    budget_tier: str
    use_case: str = "general"
    household_size: int = 1
    has_children: bool = False
    coastal: bool = False
    storm_risk: bool = False
    seismic_risk: bool = False
    air_quality: str = "moderate"
    grid_reliability: str = "stable"
    cost_of_living_index: float = 100.0
    highland: bool = False

    def __post_init__(self) -> None:
        if self.budget_tier not in BUDGET_TIERS:
            raise ValueError(f"Unknown budget tier: {self.budget_tier!r}")
        if self.use_case not in USE_CASES:
            raise ValueError(f"Unknown use case: {self.use_case!r}")
        if self.air_quality not in AIR_QUALITY_LEVELS:
            raise ValueError(f"Unknown air quality level: {self.air_quality!r}")
        if self.grid_reliability not in GRID_RELIABILITY_LEVELS:
            raise ValueError(
                f"Unknown grid reliability level: {self.grid_reliability!r}"
            )
        if self.household_size < 1:
            raise ValueError("household_size must be at least 1")


@dataclass
class Recommendation:
    """A single structured recommendation block for one life category."""

    category: str
    headline: str
    summary: str
    picks: List[str] = field(default_factory=list)
    avoid: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class FullReport:
    """The complete, five-category advisory report for one user profile."""

    profile: UserProfile
    clothing: Recommendation
    vehicle: Recommendation
    housing: Recommendation
    devices: Recommendation
    computer: Recommendation

    def as_dict(self) -> dict:
        return {
            "profile": asdict(self.profile),
            "clothing": self.clothing.as_dict(),
            "vehicle": self.vehicle.as_dict(),
            "housing": self.housing.as_dict(),
            "devices": self.devices.as_dict(),
            "computer": self.computer.as_dict(),
        }
