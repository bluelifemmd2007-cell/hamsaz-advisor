from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Location:
    key: str
    name: str
    country: str
    climate_key: str
    cost_of_living_index: float
    coastal: bool = False
    storm_risk: bool = False
    seismic_risk: bool = False
    air_quality: str = "moderate"
    grid_reliability: str = "stable"
    highland: bool = False


# key, name, country, climate_key, cost_of_living_index,
# coastal, storm_risk, seismic_risk, air_quality, grid_reliability, highland
_RAW: List[Tuple] = [
    
    ("tehran", "Tehran", "Iran", "cold_semi_arid", 34, False, False, True, "poor", "variable", True),
    ("mashhad", "Mashhad", "Iran", "cold_semi_arid", 29, False, False, True, "moderate", "variable", True),
    ("isfahan", "Isfahan", "Iran", "cold_semi_arid", 30, False, False, True, "moderate", "variable", True),
    ("shiraz", "Shiraz", "Iran", "hot_semi_arid", 32, False, False, True, "moderate", "variable", True),
    ("tabriz", "Tabriz", "Iran", "cold_semi_arid", 27, False, False, True, "moderate", "variable", True),
    ("ahvaz", "Ahvaz", "Iran", "hot_arid", 26, False, False, True, "poor", "variable", False),
    ("bandar_abbas", "Bandar Abbas", "Iran", "tropical_humid", 28, True, False, True, "moderate", "variable", False),
    ("rasht", "Rasht", "Iran", "humid_subtropical", 28, True, False, True, "moderate", "variable", False),
    ("kerman", "Kerman", "Iran", "hot_semi_arid", 24, False, False, True, "moderate", "variable", True),
    ("yazd", "Yazd", "Iran", "hot_arid", 24, False, False, True, "moderate", "variable", True),
    ("qom", "Qom", "Iran", "hot_arid", 26, False, False, True, "poor", "variable", False),
    ("karaj", "Karaj", "Iran", "cold_semi_arid", 32, False, False, True, "moderate", "variable", True),
    ("urmia", "Urmia", "Iran", "cold_semi_arid", 26, False, False, True, "moderate", "variable", True),
    ("sari", "Sari", "Iran", "humid_subtropical", 27, True, False, True, "moderate", "variable", False),

    
    ("singapore", "Singapore", "Singapore", "tropical_humid", 100, True, False, False, "moderate", "stable", False),
    ("kuala_lumpur", "Kuala Lumpur", "Malaysia", "tropical_humid", 55, True, False, False, "moderate", "stable", False),
    ("miami", "Miami", "United States", "tropical_humid", 90, True, True, False, "moderate", "stable", False),
    ("mumbai", "Mumbai", "India", "tropical_humid", 45, True, False, True, "poor", "variable", False),
    ("jakarta", "Jakarta", "Indonesia", "tropical_humid", 40, True, False, True, "poor", "variable", False),

    
    ("bangkok", "Bangkok", "Thailand", "tropical_savanna", 48, False, False, False, "poor", "stable", False),
    ("lagos", "Lagos", "Nigeria", "tropical_savanna", 50, True, False, False, "poor", "unstable", False),
    ("rio_de_janeiro", "Rio de Janeiro", "Brazil", "tropical_savanna", 45, True, False, False, "moderate", "variable", False),
    ("accra", "Accra", "Ghana", "tropical_savanna", 45, True, False, False, "moderate", "variable", False),
    ("bengaluru", "Bengaluru", "India", "tropical_savanna", 40, False, False, False, "moderate", "variable", True),

    
    ("dubai", "Dubai", "United Arab Emirates", "hot_arid", 80, True, False, False, "moderate", "stable", False),
    ("riyadh", "Riyadh", "Saudi Arabia", "hot_arid", 65, False, False, False, "poor", "stable", False),
    ("phoenix", "Phoenix", "United States", "hot_arid", 75, False, False, False, "moderate", "stable", False),
    ("las_vegas", "Las Vegas", "United States", "hot_arid", 78, False, False, False, "moderate", "stable", False),
    ("doha", "Doha", "Qatar", "hot_arid", 75, True, False, False, "moderate", "stable", False),
    ("kuwait_city", "Kuwait City", "Kuwait", "hot_arid", 70, True, False, False, "poor", "stable", False),
    ("cairo", "Cairo", "Egypt", "hot_arid", 35, False, False, False, "poor", "variable", False),


    ("jaipur", "Jaipur", "India", "hot_semi_arid", 30, False, False, True, "poor", "variable", False),
    ("marrakech", "Marrakech", "Morocco", "hot_semi_arid", 40, False, False, False, "moderate", "stable", False),
    ("karachi", "Karachi", "Pakistan", "hot_semi_arid", 32, True, True, False, "poor", "unstable", False),
    ("ahmedabad", "Ahmedabad", "India", "hot_semi_arid", 32, False, False, True, "poor", "variable", False),


    ("denver", "Denver", "United States", "cold_semi_arid", 88, False, False, False, "good", "stable", True),
    ("ankara", "Ankara", "Turkey", "cold_semi_arid", 45, False, False, True, "moderate", "stable", False),
    ("madrid", "Madrid", "Spain", "cold_semi_arid", 70, False, False, False, "good", "stable", False),
    ("salt_lake_city", "Salt Lake City", "United States", "cold_semi_arid", 82, False, False, False, "good", "stable", True),

    
    ("los_angeles", "Los Angeles", "United States", "mediterranean", 100, True, False, True, "poor", "stable", False),
    ("rome", "Rome", "Italy", "mediterranean", 78, False, False, False, "moderate", "stable", False),
    ("athens", "Athens", "Greece", "mediterranean", 65, True, False, True, "moderate", "stable", False),
    ("barcelona", "Barcelona", "Spain", "mediterranean", 75, True, False, False, "good", "stable", False),
    ("lisbon", "Lisbon", "Portugal", "mediterranean", 65, True, False, True, "good", "stable", False),
    ("san_francisco", "San Francisco", "United States", "mediterranean", 120, True, False, True, "good", "stable", False),
    ("perth", "Perth", "Australia", "mediterranean", 80, True, False, False, "good", "stable", False),

    
    ("tokyo", "Tokyo", "Japan", "humid_subtropical", 95, True, True, True, "moderate", "stable", False),
    ("shanghai", "Shanghai", "China", "humid_subtropical", 75, True, True, True, "poor", "stable", False),
    ("sydney", "Sydney", "Australia", "humid_subtropical", 95, True, False, False, "good", "stable", False),
    ("atlanta", "Atlanta", "United States", "humid_subtropical", 80, False, False, False, "moderate", "stable", False),
    ("istanbul", "Istanbul", "Turkey", "humid_subtropical", 55, True, False, True, "moderate", "stable", False),
    ("houston", "Houston", "United States", "humid_subtropical", 78, True, True, False, "poor", "stable", False),
    ("buenos_aires", "Buenos Aires", "Argentina", "humid_subtropical", 50, True, False, False, "moderate", "variable", False),
    ("new_orleans", "New Orleans", "United States", "humid_subtropical", 70, True, True, False, "moderate", "stable", False),
    ("new_delhi", "New Delhi", "India", "humid_subtropical", 42, False, False, True, "poor", "variable", False),

    
    ("london", "London", "United Kingdom", "temperate_oceanic", 100, False, False, False, "moderate", "stable", False),
    ("paris", "Paris", "France", "temperate_oceanic", 95, False, False, False, "moderate", "stable", False),
    ("amsterdam", "Amsterdam", "Netherlands", "temperate_oceanic", 95, True, False, False, "good", "stable", False),
    ("vancouver", "Vancouver", "Canada", "temperate_oceanic", 100, True, False, True, "good", "stable", False),
    ("auckland", "Auckland", "New Zealand", "temperate_oceanic", 95, True, False, False, "good", "stable", False),
    ("dublin", "Dublin", "Ireland", "temperate_oceanic", 90, True, False, False, "good", "stable", False),
    ("seattle", "Seattle", "United States", "temperate_oceanic", 105, True, False, True, "good", "stable", False),

    
    ("chicago", "Chicago", "United States", "continental", 90, False, False, False, "moderate", "stable", False),
    ("moscow", "Moscow", "Russia", "continental", 60, False, False, False, "poor", "stable", False),
    ("toronto", "Toronto", "Canada", "continental", 90, False, False, False, "good", "stable", False),
    ("berlin", "Berlin", "Germany", "continental", 80, False, False, False, "good", "stable", False),
    ("beijing", "Beijing", "China", "continental", 65, False, False, False, "poor", "stable", False),
    ("new_york", "New York", "United States", "continental", 130, True, True, False, "moderate", "stable", False),
    ("seoul", "Seoul", "South Korea", "continental", 85, False, False, False, "poor", "stable", False),

    
    ("anchorage", "Anchorage", "United States", "subarctic", 95, True, False, True, "good", "stable", False),
    ("oulu", "Oulu", "Finland", "subarctic", 85, True, False, False, "good", "stable", False),
    ("yellowknife", "Yellowknife", "Canada", "subarctic", 90, False, False, False, "good", "stable", False),
    ("fairbanks", "Fairbanks", "United States", "subarctic", 90, False, False, False, "good", "stable", False),
    ("murmansk", "Murmansk", "Russia", "subarctic", 55, True, False, False, "moderate", "variable", False),

    
    ("mexico_city", "Mexico City", "Mexico", "highland", 55, False, False, True, "poor", "variable", True),
    ("bogota", "Bogota", "Colombia", "highland", 45, False, False, True, "moderate", "variable", True),
    ("la_paz", "La Paz", "Bolivia", "highland", 35, False, False, True, "moderate", "variable", True),
    ("addis_ababa", "Addis Ababa", "Ethiopia", "highland", 35, False, False, False, "moderate", "unstable", True),
    ("nairobi", "Nairobi", "Kenya", "highland", 45, False, False, False, "moderate", "variable", True),
    ("quito", "Quito", "Ecuador", "highland", 42, False, False, True, "moderate", "variable", True),
]

_FIELDS = (
    "key", "name", "country", "climate_key", "cost_of_living_index",
    "coastal", "storm_risk", "seismic_risk", "air_quality", "grid_reliability",
    "highland",
)

LOCATIONS: Dict[str, Location] = {
    row[0]: Location(**dict(zip(_FIELDS, row))) for row in _RAW
}


def get_location(key: str) -> Location:
    try:
        return LOCATIONS[key]
    except KeyError as exc:
        raise KeyError(f"Unknown location key: {key!r}") from exc


def locations_by_country() -> Dict[str, List[Location]]:
    """Group all known locations by country, sorted for display purposes."""
    grouped: Dict[str, List[Location]] = {}
    for location in LOCATIONS.values():
        grouped.setdefault(location.country, []).append(location)
    for cities in grouped.values():
        cities.sort(key=lambda loc: loc.name)
    return dict(sorted(grouped.items()))
