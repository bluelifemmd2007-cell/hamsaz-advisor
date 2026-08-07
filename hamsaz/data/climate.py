"""Simplified, Koeppen-inspired climate zone reference data.

Real climate classification has dozens of sub-types; this module collapses
them into eleven practically-distinct zones that are enough to drive real
buying decisions (clothing, vehicles, housing, devices) without pretending
to be a meteorological authority. Numbers are representative averages for
the zone, not a forecast for any single city.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ClimateZone:
    key: str
    name: str
    summer_high_c: float
    winter_low_c: float
    humidity: str  # "low", "medium", "high"
    rainfall: str
    uv_index: str  # "moderate", "high", "extreme"
    description: str
    example_cities: List[str]


CLIMATE_ZONES: Dict[str, ClimateZone] = {
    "tropical_humid": ClimateZone(
        key="tropical_humid",
        name="Tropical / Hot & Humid",
        summer_high_c=32,
        winter_low_c=22,
        humidity="high",
        rainfall="Heavy, often daily; little seasonal variation",
        uv_index="extreme",
        description=(
            "Hot and sticky all year round with barely any temperature swing "
            "between 'summer' and 'winter'. Rain arrives in sudden, heavy "
            "bursts rather than gentle showers."
        ),
        example_cities=["Singapore", "Kuala Lumpur", "Miami", "Mumbai", "Jakarta", "Bandar Abbas"],
    ),
    "tropical_savanna": ClimateZone(
        key="tropical_savanna",
        name="Tropical Savanna (Wet/Dry)",
        summer_high_c=33,
        winter_low_c=18,
        humidity="medium",
        rainfall="Distinct rainy season, long dry season",
        uv_index="extreme",
        description=(
            "Warm to hot year-round, but the year splits clearly into a wet "
            "season with dramatic downpours and a long, dusty dry season."
        ),
        example_cities=["Bangkok", "Lagos", "Rio de Janeiro", "Accra", "Bengaluru"],
    ),
    "hot_arid": ClimateZone(
        key="hot_arid",
        name="Hot Desert",
        summer_high_c=42,
        winter_low_c=8,
        humidity="low",
        rainfall="Minimal, under 250mm/year",
        uv_index="extreme",
        description=(
            "Scorching, bone-dry summers and mild, dry winters. Very large "
            "swings between daytime heat and nighttime cool, especially away "
            "from the coast."
        ),
        example_cities=["Dubai", "Riyadh", "Phoenix", "Las Vegas", "Cairo", "Yazd", "Ahvaz"],
    ),
    "hot_semi_arid": ClimateZone(
        key="hot_semi_arid",
        name="Hot Semi-Arid / Steppe",
        summer_high_c=38,
        winter_low_c=5,
        humidity="low",
        rainfall="Light and seasonal",
        uv_index="high",
        description=(
            "One notch wetter than true desert: hot, dry summers with a "
            "short, mild winter and occasional real rain."
        ),
        example_cities=["Jaipur", "Marrakech", "Karachi", "Shiraz", "Kerman"],
    ),
    "cold_semi_arid": ClimateZone(
        key="cold_semi_arid",
        name="Cold Semi-Arid / Steppe",
        summer_high_c=34,
        winter_low_c=-8,
        humidity="low",
        rainfall="Sparse year-round",
        uv_index="high",
        description=(
            "Hot, dry summers paired with genuinely cold winters and dry air "
            "in every season. Huge daily temperature swings are normal."
        ),
        example_cities=["Tehran", "Denver", "Ankara", "Madrid", "Tabriz", "Mashhad"],
    ),
    "mediterranean": ClimateZone(
        key="mediterranean",
        name="Mediterranean",
        summer_high_c=29,
        winter_low_c=6,
        humidity="medium",
        rainfall="Wet, mild winters; dry summers",
        uv_index="high",
        description=(
            "Widely considered one of the easiest climates to live in: warm, "
            "dry summers and mild, rainy winters with few extremes."
        ),
        example_cities=["Los Angeles", "Rome", "Athens", "Barcelona", "Lisbon", "Perth"],
    ),
    "humid_subtropical": ClimateZone(
        key="humid_subtropical",
        name="Humid Subtropical",
        summer_high_c=33,
        winter_low_c=2,
        humidity="high",
        rainfall="Abundant, spread through the year",
        uv_index="extreme",
        description=(
            "Hot, muggy summers and cool (rarely freezing) winters. Coastal "
            "versions of this zone see real hurricane/typhoon exposure."
        ),
        example_cities=["Tokyo", "Shanghai", "Sydney", "Atlanta", "Istanbul", "Houston", "Rasht"],
    ),
    "temperate_oceanic": ClimateZone(
        key="temperate_oceanic",
        name="Temperate Oceanic",
        summer_high_c=22,
        winter_low_c=3,
        humidity="high",
        rainfall="Frequent light rain, year-round",
        uv_index="moderate",
        description=(
            "Mild summers, cool winters, and grey, drizzly skies in every "
            "season. Rarely extreme in either direction, but rarely sunny."
        ),
        example_cities=["London", "Paris", "Amsterdam", "Vancouver", "Auckland", "Dublin", "Seattle"],
    ),
    "continental": ClimateZone(
        key="continental",
        name="Humid Continental",
        summer_high_c=28,
        winter_low_c=-10,
        humidity="medium",
        rainfall="Moderate, with real winter snow",
        uv_index="high",
        description=(
            "Warm-to-hot summers and cold, snowy winters, with a wide swing "
            "between the two. Four genuinely distinct seasons."
        ),
        example_cities=["Chicago", "Moscow", "Toronto", "Berlin", "Beijing", "New York", "Seoul"],
    ),
    "subarctic": ClimateZone(
        key="subarctic",
        name="Subarctic",
        summer_high_c=20,
        winter_low_c=-22,
        humidity="medium",
        rainfall="Light, mostly falling as snow",
        uv_index="moderate",
        description=(
            "Short, cool summers and long, brutally cold, dark winters. "
            "Cold-weather engineering stops being optional here."
        ),
        example_cities=["Anchorage", "Oulu", "Yellowknife", "Fairbanks", "Murmansk"],
    ),
    "highland": ClimateZone(
        key="highland",
        name="Tropical Highland",
        summer_high_c=22,
        winter_low_c=4,
        humidity="medium",
        rainfall="Moderate, often as afternoon showers",
        uv_index="extreme",
        description=(
            "Spring-like temperatures all year thanks to high elevation, but "
            "with intense, unfiltered sun and noticeably thin, dry air."
        ),
        example_cities=["Mexico City", "Bogota", "La Paz", "Addis Ababa", "Nairobi", "Quito"],
    ),
}


def get_climate(key: str) -> ClimateZone:
    try:
        return CLIMATE_ZONES[key]
    except KeyError as exc:
        raise KeyError(f"Unknown climate zone key: {key!r}") from exc
