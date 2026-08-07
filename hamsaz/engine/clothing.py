"""Clothing recommendations driven by climate, budget, and air quality."""
from __future__ import annotations

from .models import Recommendation, UserProfile

# Per-climate wardrobe strategy. Each entry focuses on what actually differs
# between zones: fabric choice, layering strategy, footwear, and the single
# biggest mistake people make dressing for that climate.
_BASE = {
    "tropical_humid": {
        "summary": (
            "Heat and humidity never really let up, so the wardrobe job is "
            "moisture management, not warmth. Fewer, faster-drying pieces "
            "beat a big closet."
        ),
        "picks": [
            "Loose-fit linen, cotton-linen blends, or moisture-wicking synthetics",
            "Light colors that reflect heat and hide sweat marks less",
            "Breathable, quick-dry underwear and socks (avoid heavy cotton socks)",
            "Open, ventilated footwear (sandals, canvas sneakers) plus one pair of closed shoes for offices",
            "A packable rain shell for sudden downpours",
        ],
        "avoid": [
            "Heavy denim, wool, or anything double-layered for daily wear",
            "Dark, heat-absorbing colors for midday outdoor wear",
            "Leather-heavy shoes that don't tolerate constant humidity",
        ],
    },
    "tropical_savanna": {
        "summary": (
            "Plan two wardrobes in one: a breathable dry-season rotation and "
            "a quick-dry, mud-tolerant wet-season rotation."
        ),
        "picks": [
            "Lightweight cotton and linen for the long dry season",
            "Quick-dry synthetic layers and a real rain jacket for wet-season months",
            "Closed, grippy-sole shoes for wet-season mud and sudden rain",
            "A wide-brim hat and sunglasses for intense dry-season sun",
        ],
        "avoid": [
            "Suede or unsealed leather shoes during the wet season",
            "All-white outfits during red-dust dry season stretches",
        ],
    },
    "hot_arid": {
        "summary": (
            "Days are brutal and dry; nights and winters can be surprisingly "
            "cold. Dress for sun protection first, warmth second."
        ),
        "picks": [
            "Loose, long, lightweight cotton or linen (covers skin without trapping heat)",
            "A genuine wide-brim hat and UV-rated sunglasses",
            "A light jacket or shawl for cold desert nights and air-conditioned interiors",
            "Closed shoes with breathable mesh to protect from hot sand/pavement",
        ],
        "avoid": [
            "Tight synthetic fabrics against skin in direct midday sun",
            "Going without sun protection because 'it's a dry heat'",
        ],
    },
    "hot_semi_arid": {
        "summary": (
            "Similar sun exposure to true desert, but with occasional real "
            "rain and slightly milder nights - build in one rain layer."
        ),
        "picks": [
            "Breathable cotton/linen daywear with sun-protective layering",
            "A packable rain layer for the short wet spells",
            "A light sweater or jacket for cool evenings",
            "Sturdy, breathable walking shoes for dusty, uneven ground",
        ],
        "avoid": [
            "Fully sun-exposed outfits without a hat or sunglasses",
            "Non-breathable footwear in the hot months",
        ],
    },
    "cold_semi_arid": {
        "summary": (
            "The defining challenge is the swing: hot dry summers, genuinely "
            "cold winters, and dry air year-round that chaps skin fast. "
            "Layering is not optional here."
        ),
        "picks": [
            "A proper insulated winter coat rated for below-freezing wind chill",
            "Breathable summer layers plus a warm mid-layer for cool evenings",
            "Moisturizer, lip balm, and a humidifier mindset for indoor dry air",
            "Waterproof winter boots with good tread for occasional snow/ice",
            "Sunglasses and sunscreen even in winter - UV stays strong at altitude",
        ],
        "avoid": [
            "A single 'one weather' wardrobe - this climate genuinely needs two",
            "Cotton as a base layer in winter (it holds moisture and chills you)",
        ],
    },
    "mediterranean": {
        "summary": (
            "One of the gentlest climates to dress for: warm dry summers and "
            "mild rainy winters with no real extremes."
        ),
        "picks": [
            "Breathable cotton/linen for summer, a light wool or fleece layer for winter",
            "A reliable compact umbrella or light rain jacket for winter showers",
            "Comfortable everyday walking shoes - little need for heavy boots",
        ],
        "avoid": [
            "Overinvesting in heavy winter gear you'll rarely use",
            "Skipping sun protection - Mediterranean summer UV is intense",
        ],
    },
    "humid_subtropical": {
        "summary": (
            "Hot, muggy summers and mild winters, often with real storm "
            "season exposure near the coast - moisture control plus one "
            "genuine rain kit."
        ),
        "picks": [
            "Lightweight, moisture-wicking summer clothing",
            "A proper waterproof (not just water-resistant) jacket and sturdy umbrella",
            "A light-to-medium coat for cool, damp winter days",
            "Water-resistant footwear for storm season",
        ],
        "avoid": [
            "Down jackets as a daily driver (humidity kills their insulation value)",
            "Suede shoes without weatherproofing spray",
        ],
    },
    "temperate_oceanic": {
        "summary": (
            "Mild but grey and damp almost year-round. Dress in adaptable "
            "layers and assume it can rain on any given day."
        ),
        "picks": [
            "A genuinely waterproof (not just showerproof) outer layer",
            "Layerable mid-weight sweaters/fleeces for year-round mild cold",
            "Waterproof shoes or boots with good grip for wet pavement",
            "A compact umbrella that lives in your bag permanently",
        ],
        "avoid": [
            "Relying on sunny-day forecasts - conditions change within hours",
            "Non-waterproof suede or canvas shoes as daily footwear",
        ],
    },
    "continental": {
        "summary": (
            "Four real seasons. You need a genuine winter kit and a genuine "
            "summer kit, with transitional layers for spring/autumn."
        ),
        "picks": [
            "An insulated, wind-resistant winter coat plus hat, gloves, and scarf",
            "Insulated waterproof winter boots with real tread for snow and ice",
            "Breathable summer clothing for a genuinely hot summer stretch",
            "Layering pieces (thermal base layers) for shoulder-season swings",
        ],
        "avoid": [
            "Assuming one 'medium-weight' coat can cover the whole winter",
            "Smooth-sole shoes/boots on icy sidewalks",
        ],
    },
    "subarctic": {
        "summary": (
            "Long, dark, severely cold winters dominate the wardrobe budget. "
            "Treat cold-weather gear as safety equipment, not fashion."
        ),
        "picks": [
            "An arctic-rated parka (down or high-loft synthetic insulation)",
            "Insulated, windproof snow boots rated well below your local winter low",
            "Thermal base layers, insulated gloves/mittens, and a face-covering option",
            "Wool or synthetic thermal socks - never cotton socks in deep cold",
            "Sunglasses for snow glare in the bright, low-angle winter sun",
        ],
        "avoid": [
            "Fashion-first winter coats without a real insulation/wind rating",
            "Cotton base layers, which get dangerously cold when damp with sweat",
        ],
    },
    "highland": {
        "summary": (
            "Mild, spring-like temperatures hide two real risks: intense "
            "high-altitude sun and cold nights even when the day was warm."
        ),
        "picks": [
            "Light layers for daytime plus a warm layer for cool evenings",
            "Strong sunscreen and UV-rated sunglasses (thin air means stronger UV)",
            "A light rain shell for frequent afternoon showers",
            "Comfortable, broken-in walking shoes for hilly terrain",
        ],
        "avoid": [
            "Judging the whole day by a warm morning - evenings drop fast",
            "Skipping sun protection because the air feels cool",
        ],
    },
}

_BUDGET_NOTE = {
    "budget": (
        "Buy fewer, more versatile pieces and lean on secondhand or outlet "
        "stores for the expensive items (winter coats, real rain shells, "
        "sturdy boots) - those are the ones worth getting right even on a tight budget."
    ),
    "balanced": (
        "Spend on the two or three items you'll wear constantly for this "
        "climate (the main coat, the daily shoes) and keep everything else "
        "mainstream and replaceable."
    ),
    "comfortable": (
        "You can afford climate-specific technical fabrics (merino wool, "
        "quality Gore-Tex-type shells) that noticeably outperform basics "
        "in this climate."
    ),
    "premium": (
        "Invest in tailored, climate-appropriate outerwear and quality "
        "natural fibers throughout - they'll outlast and outperform fast "
        "fashion in this specific climate by a wide margin."
    ),
}


def recommend(profile: UserProfile) -> Recommendation:
    base = _BASE[profile.climate_key]
    picks = list(base["picks"])
    avoid = list(base["avoid"])
    tips = [_BUDGET_NOTE[profile.budget_tier]]

    if profile.air_quality == "poor":
        tips.append(
            "Air quality here is frequently poor: keep a well-fitted N95/KN95 "
            "mask on hand for high-pollution or dust-storm days, and choose "
            "outerwear with a hood you can cinch against blowing dust."
        )

    if profile.household_size > 1 and profile.has_children:
        tips.append(
            "For kids, prioritize durable, easy-to-layer basics over "
            "climate-optimized technical wear - they outgrow gear faster "
            "than they wear it out."
        )

    return Recommendation(
        category="clothing",
        headline="What to wear here",
        summary=base["summary"],
        picks=picks,
        avoid=avoid,
        tips=tips,
    )
