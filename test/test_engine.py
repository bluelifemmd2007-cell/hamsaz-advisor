"""Unit tests for the pure-Python recommendation engine."""
from __future__ import annotations

import pytest

from hamsaz.data.climate import CLIMATE_ZONES
from hamsaz.data.locations import LOCATIONS, get_location, locations_by_country
from hamsaz.engine.models import BUDGET_TIERS, USE_CASES, Recommendation, UserProfile
from hamsaz.engine.recommender import build_report


def make_profile(location_key: str, **overrides) -> UserProfile:
    loc = get_location(location_key)
    defaults = dict(
        location_key=loc.key,
        location_name=loc.name,
        climate_key=loc.climate_key,
        budget_tier="balanced",
        use_case="general",
        coastal=loc.coastal,
        storm_risk=loc.storm_risk,
        seismic_risk=loc.seismic_risk,
        air_quality=loc.air_quality,
        grid_reliability=loc.grid_reliability,
        cost_of_living_index=loc.cost_of_living_index,
        highland=loc.highland,
    )
    defaults.update(overrides)
    return UserProfile(**defaults)


def test_all_climate_zones_have_engine_coverage():
    """Every climate zone key must be handled by every category engine."""
    from hamsaz.engine import clothing, vehicles, housing, devices

    for module in (clothing, vehicles, housing, devices):
        for zone_key in CLIMATE_ZONES:
            assert zone_key in module._BASE, f"{module.__name__} missing {zone_key}"


def test_all_locations_produce_a_valid_report():
    for key in LOCATIONS:
        profile = make_profile(key)
        report = build_report(profile)
        for rec in (report.clothing, report.vehicle, report.housing, report.devices, report.computer):
            assert isinstance(rec, Recommendation)
            assert rec.summary
            assert rec.picks, f"{rec.category} produced no picks for {key}"


@pytest.mark.parametrize("budget_tier", BUDGET_TIERS)
def test_all_budget_tiers_work(budget_tier):
    profile = make_profile("tehran", budget_tier=budget_tier)
    report = build_report(profile)
    assert report.vehicle.tips


@pytest.mark.parametrize("use_case", USE_CASES)
def test_all_use_cases_produce_computer_advice(use_case):
    profile = make_profile("berlin", use_case=use_case)
    report = build_report(profile)
    assert report.computer.picks
    assert "CPU" in report.computer.picks[0]


def test_seismic_risk_adds_structural_guidance():
    profile = make_profile("tehran")
    assert profile.seismic_risk is True
    report = build_report(profile)
    joined = " ".join(report.housing.tips + report.housing.picks).lower()
    assert "seismic" in joined or "earthquake" in joined


def test_storm_risk_adds_storm_guidance():
    profile = make_profile("miami")
    assert profile.storm_risk is True
    report = build_report(profile)
    joined = " ".join(report.housing.tips + report.housing.picks + report.vehicle.tips).lower()
    assert "storm" in joined or "flood" in joined or "hurricane" in joined


def test_unstable_grid_pushes_laptop_and_ups_guidance():
    profile = make_profile("addis_ababa")
    assert profile.grid_reliability == "unstable"
    report = build_report(profile)
    joined = " ".join(report.computer.tips).lower()
    assert "laptop" in joined or "ups" in joined


def test_poor_air_quality_adds_purifier_and_mask_guidance():
    profile = make_profile("tehran")
    assert profile.air_quality == "poor"
    report = build_report(profile)
    devices_text = " ".join(report.devices.picks + report.devices.tips).lower()
    clothing_text = " ".join(report.clothing.tips).lower()
    assert "purifier" in devices_text
    assert "mask" in clothing_text


def test_coastal_flag_adds_corrosion_guidance():
    profile = make_profile("miami")
    assert profile.coastal is True
    report = build_report(profile)
    joined = " ".join(report.vehicle.picks + report.vehicle.tips).lower()
    assert "rust" in joined or "corros" in joined or "salt" in joined


def test_invalid_budget_tier_raises():
    with pytest.raises(ValueError):
        make_profile("tehran", budget_tier="not_a_real_tier")


def test_invalid_use_case_raises():
    with pytest.raises(ValueError):
        make_profile("tehran", use_case="not_a_real_use_case")


def test_locations_by_country_groups_and_sorts():
    grouped = locations_by_country()
    assert "Iran" in grouped
    iran_cities = [loc.name for loc in grouped["Iran"]]
    assert iran_cities == sorted(iran_cities)
    assert "Tehran" in iran_cities


def test_full_report_as_dict_is_json_serializable():
    import json

    profile = make_profile("tokyo", use_case="gaming", budget_tier="premium")
    report = build_report(profile)
    payload = json.dumps(report.as_dict())
    assert '"category": "computer"' in payload
