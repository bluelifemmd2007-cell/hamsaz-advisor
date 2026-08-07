"""Digital device & home appliance recommendations by climate and budget."""
from __future__ import annotations

from .models import Recommendation, UserProfile

_BASE = {
    "tropical_humid": {
        "summary": (
            "Heat and constant humidity are hard on batteries, screens, and "
            "internal corrosion. Moisture control matters as much as raw specs."
        ),
        "picks": [
            "A dehumidifier for equipment storage spaces (closets, cabinets)",
            "Devices with IP-rated (dust/water resistant) housings where available",
            "Silica gel packs stored with cameras, lenses, and rarely-used electronics",
        ],
        "avoid": [
            "Leaving devices in direct sun or a hot parked car - heat degrades batteries fast",
            "Storing electronics in sealed non-ventilated cabinets, which trap humidity",
        ],
    },
    "tropical_savanna": {
        "summary": (
            "Dust in the dry season and humidity/flooding risk in the wet "
            "season both threaten electronics."
        ),
        "picks": [
            "Dust-resistant keyboards and sealed port covers for the dry season",
            "Surge protection for wet-season electrical storms",
        ],
        "avoid": [
            "Open-air equipment racks or vents that let in dry-season dust",
        ],
    },
    "hot_arid": {
        "summary": (
            "Fine dust and extreme heat are the two real threats. "
            "Cooling and dust management matter more than any spec sheet."
        ),
        "picks": [
            "Devices and appliances rated for high ambient operating temperatures",
            "Dust filters on any equipment with fans (routers, consoles, computers)",
            "A surge protector, since AC-heavy grids see more voltage fluctuation under peak summer load",
        ],
        "avoid": [
            "Leaving phones/laptops in a hot car or in direct window sun",
            "Skipping regular dust cleaning on fan intakes",
        ],
    },
    "hot_semi_arid": {
        "summary": (
            "Similar dust and heat concerns to true desert, with a bit more "
            "seasonal humidity to plan storage around."
        ),
        "picks": [
            "Sealed or dust-resistant device housings",
            "Basic surge protection for seasonal storm activity",
        ],
        "avoid": [
            "Unfiltered equipment left running in dusty rooms long-term",
        ],
    },
    "cold_semi_arid": {
        "summary": (
            "Very dry air causes static discharge issues, and cold nights "
            "can affect battery-powered devices left outdoors or in unheated spaces."
        ),
        "picks": [
            "A small humidifier near sensitive electronics to reduce static buildup",
            "Devices with good cold-tolerance if regularly used outdoors in winter",
        ],
        "avoid": [
            "Leaving battery-powered devices in an unheated car overnight in winter",
        ],
    },
    "mediterranean": {
        "summary": (
            "A mild, low-stress climate for electronics - focus on general "
            "quality and value rather than climate-specific ruggedization."
        ),
        "picks": [
            "Standard consumer-grade devices are fine here without special adaptation",
        ],
        "avoid": [
            "Overpaying for ruggedization features this climate doesn't require",
        ],
    },
    "humid_subtropical": {
        "summary": (
            "Persistent humidity plus, near the coast, real storm risk make "
            "moisture protection and backup power worth planning for."
        ),
        "picks": [
            "A dehumidifier for closets/cabinets storing sensitive electronics",
            "A UPS (battery backup) for essential devices if storms cause outages",
            "Surge protection rated for lightning-heavy storm seasons",
        ],
        "avoid": [
            "Storing cameras, consoles, or other gear in damp, unventilated spaces",
        ],
    },
    "temperate_oceanic": {
        "summary": (
            "Persistent damp weather is the main factor - beyond that, this "
            "is a low-stress climate for electronics."
        ),
        "picks": [
            "A small dehumidifier if storing equipment in an older or damp building",
        ],
        "avoid": [
            "Long-term storage of electronics in unheated, damp outbuildings",
        ],
    },
    "continental": {
        "summary": (
            "Cold, dry winters bring static-discharge risk and condensation "
            "when devices move between cold outdoors and warm indoors."
        ),
        "picks": [
            "A humidifier for dry winter indoor air, both for comfort and to reduce static",
            "Cold-rated batteries for anything used outdoors in winter",
        ],
        "avoid": [
            "Powering on a device immediately after bringing it in from the cold - let it reach room temperature first to avoid internal condensation",
        ],
    },
    "subarctic": {
        "summary": (
            "Extreme cold is genuinely hard on batteries and screens; "
            "condensation when moving indoors is a real, device-killing risk."
        ),
        "picks": [
            "Devices with published cold-weather operating ratings for outdoor use",
            "Insulated cases or pouches for phones/cameras carried outdoors",
            "A UPS or backup power source given a higher chance of storm-related outages",
        ],
        "avoid": [
            "Powering on a cold device immediately after bringing it inside - always let it acclimate first to avoid condensation damage",
            "Relying on battery percentage readings in deep cold - cold batteries drain and report unpredictably",
        ],
    },
    "highland": {
        "summary": (
            "Thinner air reduces the cooling efficiency of fan-based "
            "electronics, and strong UV degrades exposed screens/casings faster."
        ),
        "picks": [
            "Devices with efficient, well-reviewed cooling (thinner air cools less effectively)",
            "Screen protectors and cases with UV-resistant materials",
        ],
        "avoid": [
            "Leaving devices in direct high-altitude sun for extended periods",
        ],
    },
}

_TIER_DEVICES = {
    "budget": [
        "A reliable mid-range phone with good battery life over a flagship with marginal gains",
        "A basic surge protector power strip for every major appliance cluster",
    ],
    "balanced": [
        "A mainstream flagship-adjacent phone and a well-reviewed mid-range laptop",
        "A proper UPS for router/modem so the internet survives short outages",
    ],
    "comfortable": [
        "A current flagship phone and a premium ultrabook or 2-in-1",
        "A whole-home surge protector at the electrical panel level",
    ],
    "premium": [
        "Top-tier devices across phone, tablet, and laptop with priority given to reliability and support quality",
        "A whole-home battery backup / UPS system for essential circuits",
    ],
}


def recommend(profile: UserProfile) -> Recommendation:
    base = _BASE[profile.climate_key]
    picks = list(base["picks"]) + list(_TIER_DEVICES[profile.budget_tier])
    avoid = list(base["avoid"])
    tips = []

    if profile.grid_reliability in ("variable", "unstable"):
        picks.append(
            "A voltage stabilizer or automatic voltage regulator (AVR) ahead "
            "of expensive appliances and electronics"
        )
        tips.append(
            "With a less reliable grid, a UPS for your router, computer, and "
            "any medical or safety-critical devices pays for itself the "
            "first time the power drops mid-task."
        )

    if profile.air_quality == "poor":
        picks.append("A HEPA air purifier sized for your main living space and bedroom")
        tips.append(
            "Check an air purifier's CADR (Clean Air Delivery Rate) rating "
            "against your actual room size - undersized purifiers underperform badly."
        )

    if profile.coastal:
        tips.append(
            "Salt air corrodes exposed ports and connectors faster - favor "
            "sealed-port devices and wipe down equipment near open windows regularly."
        )

    if profile.climate_key in ("hot_arid", "hot_semi_arid", "tropical_humid", "tropical_savanna", "humid_subtropical"):
        tips.append(
            "Consider a dehumidifier or air conditioner with a dedicated "
            "'dry' mode to protect books, electronics, and instruments from humidity damage."
        )

    if profile.climate_key in ("cold_semi_arid", "continental", "subarctic"):
        tips.append(
            "A basic home humidifier improves both comfort and electronics "
            "longevity during long, dry heating seasons."
        )

    return Recommendation(
        category="devices",
        headline="Digital devices & home electronics",
        summary=base["summary"],
        picks=picks,
        avoid=avoid,
        tips=tips,
    )
