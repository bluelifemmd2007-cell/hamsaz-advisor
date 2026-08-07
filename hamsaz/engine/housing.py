"""Housing recommendations driven by climate, structural risk, and budget."""
from __future__ import annotations

from .models import Recommendation, UserProfile

_BASE = {
    "tropical_humid": {
        "summary": (
            "The house's main job is shedding heat and humidity while "
            "resisting mold. Ventilation and moisture control matter more "
            "than insulation."
        ),
        "picks": [
            "Raised foundations or good site drainage to keep moisture away from the structure",
            "High ceilings, cross-ventilation, and covered verandas/overhangs",
            "Mold-resistant materials (avoid moisture-trapping carpet in humid rooms)",
            "A dehumidifier and well-sized air conditioning for bedrooms at minimum",
        ],
        "avoid": [
            "Sealed, poorly ventilated designs that trap humidity indoors",
            "Untreated wood in direct ground contact",
        ],
    },
    "tropical_savanna": {
        "summary": (
            "Design for a long dry season (dust, heat) and a short intense "
            "wet season (drainage, sudden downpours) in the same building."
        ),
        "picks": [
            "Good roof drainage and gutters sized for intense, sudden rain",
            "Elevated door thresholds to keep flash-flood water out",
            "Shaded windows/overhangs to reduce dry-season heat gain",
        ],
        "avoid": [
            "Flat roofs without proper waterproofing and drainage slope",
            "Basements or below-grade rooms without real flood protection",
        ],
    },
    "hot_arid": {
        "summary": (
            "Thick walls, small shaded windows, and light-colored exteriors "
            "keep desert heat out during the day and retain warmth at "
            "night when temperatures fall fast."
        ),
        "picks": [
            "Thick, high-thermal-mass walls (adobe, block, or well-insulated framing)",
            "Light-colored roofing and exterior walls to reflect solar heat",
            "Small, shaded, or double-glazed windows on sun-facing walls",
            "Evaporative ('swamp') cooling where humidity is low, or efficient AC otherwise",
        ],
        "avoid": [
            "Large unshaded glass facades facing the afternoon sun",
            "Dark roofing materials that absorb and hold heat",
        ],
    },
    "hot_semi_arid": {
        "summary": (
            "Similar to true desert design, with a bit more attention to "
            "occasional heavy rain and dust infiltration."
        ),
        "picks": [
            "Thermal mass construction with shaded windows",
            "Good roof drainage for the occasional intense downpour",
            "Sealed window/door frames to reduce dust infiltration",
        ],
        "avoid": [
            "Poorly sealed windows that let in dust during dry, windy periods",
        ],
    },
    "cold_semi_arid": {
        "summary": (
            "The building needs to handle a hot, sun-intense summer and a "
            "genuinely cold, dry winter - insulation and heating matter as "
            "much as summer cooling."
        ),
        "picks": [
            "Strong wall and roof insulation rated for sub-freezing winters",
            "Double or triple-glazed windows to cut winter heat loss and summer glare",
            "A capable heating system (gas, heat pump rated for cold) plus efficient summer cooling",
            "A humidifier for the dry indoor winter air",
        ],
        "avoid": [
            "Single-pane windows - they lose enormous amounts of heat in this climate",
            "Underestimating heating costs because summers feel like a desert",
        ],
    },
    "mediterranean": {
        "summary": (
            "A genuinely forgiving climate for building: focus on shading "
            "for the dry summer and basic weatherproofing for the wet, "
            "mild winter."
        ),
        "picks": [
            "Shaded outdoor living space (pergolas, awnings) for summer",
            "Light-to-moderate insulation - extremes are rare here",
            "Good roof waterproofing for the rainy winter season",
        ],
        "avoid": [
            "Over-investing in heavy-duty heating/cooling systems this climate rarely needs",
        ],
    },
    "humid_subtropical": {
        "summary": (
            "Humidity plus, in coastal areas, real storm exposure make "
            "moisture control and structural wind resistance the priorities."
        ),
        "picks": [
            "Good ventilation and dehumidification, especially in bathrooms/basements",
            "Mold-resistant building materials in high-humidity rooms",
            "Storm-rated roofing and impact-resistant windows if in a storm-risk area",
            "A well-sized, well-maintained HVAC system for muggy summers",
        ],
        "avoid": [
            "Unsealed basements in high water-table, storm-prone areas",
            "Skipping storm shutters/impact glass in hurricane or typhoon-exposed areas",
        ],
    },
    "temperate_oceanic": {
        "summary": (
            "Mild but relentlessly damp weather rewards good waterproofing "
            "and moisture management over heating or cooling capacity."
        ),
        "picks": [
            "Well-sealed roofing and gutters sized for frequent rain",
            "Good vapor barriers and ventilation to prevent damp/mold buildup",
            "Double-glazed windows for modest heat retention on cool, damp days",
        ],
        "avoid": [
            "Skipping damp-proofing in older buildings - persistent humidity finds every gap",
        ],
    },
    "continental": {
        "summary": (
            "Four real seasons mean the building must handle serious "
            "winter cold and a genuinely hot summer stretch equally well."
        ),
        "picks": [
            "Strong insulation and double/triple-glazed windows for cold winters",
            "A steeper roof pitch to shed heavy snow load",
            "A reliable heating system (furnace, heat pump) plus adequate summer AC",
            "Weatherstripped doors/windows to control winter heating costs",
        ],
        "avoid": [
            "Flat or low-pitch roofs in heavy snowfall areas without a proper load rating",
            "Under-insulating to save upfront cost - it shows up in every winter heating bill",
        ],
    },
    "subarctic": {
        "summary": (
            "Extreme cold and long, dark winters make insulation, heating "
            "reliability, and structural cold-tolerance the entire design brief."
        ),
        "picks": [
            "Very high insulation ratings and airtight construction",
            "Foundations designed for frozen ground / permafrost where relevant",
            "A steep roof pitch for heavy, prolonged snow load",
            "A redundant or backup heating source in case of outages",
        ],
        "avoid": [
            "Standard 'temperate climate' insulation ratings - they are inadequate here",
            "Relying on a single, unbacked-up heating system through winter",
        ],
    },
    "highland": {
        "summary": (
            "Mild daytime temperatures hide cold nights and intense sun; "
            "design for both thermal swing and strong UV exposure."
        ),
        "picks": [
            "Moderate insulation to buffer the day/night temperature swing",
            "UV-resistant roofing and exterior materials (high-altitude sun degrades materials faster)",
            "Good drainage for frequent afternoon showers",
        ],
        "avoid": [
            "Assuming mild daytime temperatures mean no heating is ever needed",
        ],
    },
}

_BUDGET_NOTE = {
    "budget": (
        "Renting an apartment or condo, or buying an older home that needs "
        "retrofitting, is usually the most realistic path - prioritize "
        "structural safety retrofits (roof, wiring, seismic bracing where "
        "relevant) over cosmetic upgrades."
    ),
    "balanced": (
        "A townhouse or modest single-family home in a well-established "
        "neighborhood typically gives the best balance of space, safety, "
        "and resale value at this budget level."
    ),
    "comfortable": (
        "A single-family home with some climate-specific upgrades already "
        "installed (good insulation, updated HVAC, storm protection where "
        "relevant) is a reasonable, comfortable target."
    ),
    "premium": (
        "Custom-building or extensively renovating lets you specify "
        "climate-optimized materials and systems from the start - this is "
        "where premium spending has the most long-term payoff."
    ),
}


def recommend(profile: UserProfile) -> Recommendation:
    base = _BASE[profile.climate_key]
    picks = list(base["picks"])
    avoid = list(base["avoid"])
    tips = [_BUDGET_NOTE[profile.budget_tier]]

    if profile.seismic_risk:
        picks.append(
            "Reinforced concrete frame or certified seismic-resistant "
            "construction, with a lightweight (not heavy tile) roof"
        )
        tips.append(
            "In an earthquake-prone area, prioritize structural safety over "
            "everything else: get any home inspected for seismic retrofitting "
            "(bracing, foundation bolting, secured water heater) before "
            "focusing on finishes or aesthetics."
        )
        avoid.append("Unreinforced masonry construction, or homes with visible structural cracking")

    if profile.storm_risk:
        picks.append("Storm shutters or impact-rated windows, and a wind-rated roof")
        tips.append(
            "Confirm the home's flood zone designation and whether flood "
            "insurance is required or advisable - standard policies often "
            "exclude flood damage."
        )

    if profile.air_quality == "poor":
        tips.append(
            "With frequently poor outdoor air quality, prioritize a home "
            "with mechanical ventilation and HEPA filtration rather than "
            "relying on open windows for fresh air."
        )

    if profile.coastal:
        tips.append(
            "Salt air accelerates corrosion of metal fixtures, railings, "
            "and HVAC units - choose marine-grade or coated hardware where possible."
        )

    if profile.household_size >= 4:
        tips.append(
            "With a larger household, weigh extra bedrooms and shared "
            "living space at least as heavily as neighborhood prestige - "
            "usable space tends to matter more day-to-day."
        )

    return Recommendation(
        category="housing",
        headline="Which house fits this location",
        summary=base["summary"],
        picks=picks,
        avoid=avoid,
        tips=tips,
    )
