"""Vehicle recommendations driven by climate, terrain risk, and budget."""
from __future__ import annotations

from .models import Recommendation, UserProfile

# Per-climate vehicle guidance: drivetrain, body style, and the main
# mechanical concern that climate creates for that zone.
_BASE = {
    "tropical_humid": {
        "summary": (
            "Heat, humidity, and heavy rain are the enemy of rubber seals, "
            "electronics, and rust-prone metal. Reliability and corrosion "
            "resistance matter more than off-road capability here."
        ),
        "picks": [
            "A sedan, hatchback, or compact SUV with strong factory rust-proofing",
            "Powerful, well-rated air conditioning - test it thoroughly before buying",
            "Good wet-weather tires with real tread depth for sudden downpours",
            "Manufacturers with a strong local service network (parts availability beats badge prestige)",
        ],
        "avoid": [
            "Cars with known AC-system weak points in hot climates",
            "Unsealed or poorly maintained undercarriage components",
        ],
        "notes": [
            "Park under cover when possible - constant sun and heat degrade "
            "interior plastics, rubber, and battery life faster than driving does.",
        ],
    },
    "tropical_savanna": {
        "summary": (
            "You need a car that handles a dusty dry season and a muddy, "
            "flood-prone wet season equally well."
        ),
        "picks": [
            "A vehicle with slightly raised ground clearance (crossover/SUV)",
            "Good quality all-terrain tires for mud and loose dirt",
            "A robust air filtration system for dry-season dust",
        ],
        "avoid": [
            "Low-clearance sports sedans that bottom out on unpaved or flooded roads",
        ],
        "notes": [
            "Avoid driving through standing water after storms - engine flood "
            "damage is one of the most common costly repairs in this climate.",
        ],
    },
    "hot_arid": {
        "summary": (
            "Extreme heat stresses the cooling system, tires, and battery "
            "hardest. Prioritize a vehicle known for handling sustained high "
            "temperatures well."
        ),
        "picks": [
            "A model with a strong reputation for cooling-system reliability in heat",
            "Heat-rated tires and a battery rated for high ambient temperatures",
            "Light-colored paint and, ideally, tinted or heat-rejecting glass",
            "Strong AC system - this is a comfort and safety requirement, not a luxury",
        ],
        "avoid": [
            "Dark interiors/exteriors without heat-rejecting glass if you can choose",
            "Skipping regular coolant and battery checks - heat shortens both lifespans",
        ],
        "notes": [
            "Shaded or covered parking meaningfully extends tire, paint, and "
            "battery life in this climate.",
        ],
    },
    "hot_semi_arid": {
        "summary": (
            "Similar heat concerns to true desert, with more airborne dust "
            "and the occasional real rain to plan for."
        ),
        "picks": [
            "A durable engine air filtration setup for dusty conditions",
            "Solid AC performance and heat-tolerant tires",
            "Moderate ground clearance for unpaved roads and occasional flooding",
        ],
        "avoid": [
            "Overly low-slung vehicles on roads that turn to washboard gravel",
        ],
        "notes": [
            "Replace cabin and engine air filters more often than the 'temperate "
            "climate' service interval suggests.",
        ],
    },
    "cold_semi_arid": {
        "summary": (
            "Hot dry summers and genuinely cold winters mean the car needs "
            "to handle both extremes, including occasional snow and ice."
        ),
        "picks": [
            "All-wheel drive or a good winter-tire setup for icy/snowy stretches",
            "A cold-rated battery and block-heater compatibility for hard winters",
            "Strong AC for the hot summer half of the year",
        ],
        "avoid": [
            "All-season tires alone if winters here regularly drop below freezing - dedicated winter tires are worth it",
            "Ignoring battery health checks before winter - cold snaps kill weak batteries",
        ],
        "notes": [
            "This climate is genuinely two climates in one car - budget "
            "for both winter and summer maintenance needs.",
        ],
    },
    "mediterranean": {
        "summary": (
            "A genuinely easy climate on vehicles: mild temperatures, no "
            "real snow, and manageable rain. Focus on other factors first."
        ),
        "picks": [
            "Almost any well-reviewed sedan, hatchback, or EV suits this climate",
            "Standard all-season tires are sufficient year-round",
        ],
        "avoid": [
            "Overpaying for climate-specific ruggedization you won't need here",
        ],
        "notes": [
            "This is one of the best climates for EV ownership if charging "
            "infrastructure is available locally - mild weather is easy on batteries.",
        ],
    },
    "humid_subtropical": {
        "summary": (
            "Humidity accelerates rust, and coastal versions of this climate "
            "carry real hurricane/typhoon exposure. Corrosion resistance and "
            "storm awareness both matter."
        ),
        "picks": [
            "A model with strong factory rust-proofing and drainage design",
            "Good wet-weather tires for frequent heavy rain",
            "Comprehensive insurance that explicitly covers flood and storm damage",
        ],
        "avoid": [
            "Leaving a vehicle in low-lying, flood-prone parking during storm season",
            "Skipping annual undercarriage rust inspections",
        ],
        "notes": [
            "If you're in a storm-risk area, know your evacuation route and "
            "keep the fuel tank/charge above half during storm season.",
        ],
    },
    "temperate_oceanic": {
        "summary": (
            "Mild temperatures but near-constant damp and rain call for "
            "good wet-weather grip more than heat or cold engineering."
        ),
        "picks": [
            "Quality all-season or dedicated wet-weather tires with strong tread",
            "A vehicle with good visibility and fog/rain-rated lighting",
        ],
        "avoid": [
            "Worn tires - wet-road stopping distance is the main real risk here",
        ],
        "notes": [
            "This is another climate that suits EVs well: mild temperatures "
            "are gentle on batteries, and rain has no meaningful effect on range.",
        ],
    },
    "continental": {
        "summary": (
            "Real winters with snow and ice make cold-weather capability a "
            "genuine requirement, not a nice-to-have."
        ),
        "picks": [
            "All-wheel drive or dedicated winter tires for snow and ice season",
            "A cold-cranking-rated battery and functioning block heater where relevant",
            "Good AC for a genuinely hot summer stretch",
        ],
        "avoid": [
            "Summer-only tires left on through winter",
            "Deferring winter maintenance (wipers, washer fluid rated for freezing, battery testing)",
        ],
        "notes": [
            "Electric vehicles work fine here but expect noticeably reduced "
            "winter range - plan charging stops accordingly if you go electric.",
        ],
    },
    "subarctic": {
        "summary": (
            "Severe, long winters make cold-weather engineering the single "
            "most important factor in the vehicle decision."
        ),
        "picks": [
            "A vehicle with proven reliability at very low temperatures",
            "A block heater (often mandatory in practice) and an arctic-rated battery",
            "Dedicated studded or heavy winter tires",
            "All-wheel or four-wheel drive for snow-covered and icy roads",
        ],
        "avoid": [
            "Standard batteries and fluids not rated for deep cold",
            "Relying on an electric vehicle as your only vehicle unless cold-weather range and charging access are confirmed locally",
        ],
        "notes": [
            "Keep an emergency kit (blankets, food, a way to signal for help) "
            "in the car through winter - cold-climate breakdowns are genuinely dangerous.",
        ],
    },
    "highland": {
        "summary": (
            "Thin air at altitude reduces naturally aspirated engine power "
            "and stresses brakes on long mountain descents."
        ),
        "picks": [
            "A turbocharged or forced-induction engine, which loses less power at altitude",
            "A vehicle with strong, well-maintained brakes and engine-braking (manual/low gear) capability",
            "Good ground clearance for steep or unpaved mountain roads",
        ],
        "avoid": [
            "Relying on brakes alone on long descents - use lower gears to reduce brake fade",
            "Ignoring altitude-related power loss when comparing 'sea level' spec sheets",
        ],
        "notes": [
            "Strong, unfiltered high-altitude sun degrades tires, paint, and "
            "interior plastics faster - covered parking helps a lot here too.",
        ],
    },
}

_BUDGET_NOTE = {
    "budget": (
        "Favor a well-maintained used vehicle from a model line known for "
        "long-term reliability over a lower-mileage vehicle with a spotty "
        "reliability record - repair costs will decide your total cost of ownership."
    ),
    "balanced": (
        "A certified pre-owned vehicle (1-3 years old) usually gives you the "
        "best balance of remaining warranty, modern safety features, and price."
    ),
    "comfortable": (
        "A new or near-new vehicle with the full manufacturer warranty and "
        "climate-specific factory options (heated/cooled seats, all-wheel "
        "drive trims, etc.) is a reasonable, comfortable choice."
    ),
    "premium": (
        "You can choose based purely on fit and preference - focus on "
        "long-term service network quality and climate-specific factory "
        "packages rather than price."
    ),
}


def recommend(profile: UserProfile) -> Recommendation:
    base = _BASE[profile.climate_key]
    picks = list(base["picks"])
    avoid = list(base["avoid"])
    tips = list(base["notes"])
    tips.append(_BUDGET_NOTE[profile.budget_tier])

    if profile.coastal:
        picks.append("Extra underbody rust-proofing / undercoating (salt air accelerates corrosion)")
        tips.append(
            "In coastal, salty air, rinse the undercarriage regularly and "
            "choose stainless or coated hardware where the option exists."
        )

    if profile.storm_risk:
        tips.append(
            "Confirm your insurance policy explicitly covers flood and "
            "storm damage - many basic policies exclude flooding by default."
        )

    if profile.grid_reliability != "stable":
        tips.append(
            "With a less reliable power grid, a plug-in hybrid or "
            "conventional vehicle is currently a more dependable daily "
            "driver than a fully electric one, unless you have reliable "
            "home charging or a generator backup."
        )

    if profile.household_size >= 4:
        picks.append("Prioritize a 3-row SUV or minivan body style for household space and safety")

    return Recommendation(
        category="vehicle",
        headline="Which car fits this location",
        summary=base["summary"],
        picks=picks,
        avoid=avoid,
        tips=tips,
    )
