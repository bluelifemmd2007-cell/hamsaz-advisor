from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from hamsaz.data.budget import BUDGET_TIERS, USE_CASES
from hamsaz.data.climate import CLIMATE_ZONES
from hamsaz.data.locations import LOCATIONS, get_location, locations_by_country
from hamsaz.engine.models import UserProfile
from hamsaz.engine.recommender import build_report

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("HAMSAZ_SECRET_KEY", "dev-key-not-for-production")
app.config["JSON_SORT_KEYS"] = False


class ProfileFormError(ValueError):
    """Raised when the submitted form can't be turned into a UserProfile."""


def _bool_field(form, name: str) -> bool:
    """HTML checkboxes only appear in form data when checked."""
    return form.get(name) in ("on", "true", "1", "yes")


def profile_from_form(form) -> UserProfile:
    """Build a validated UserProfile from a submitted web form."""
    location_key = (form.get("location") or "").strip()
    budget_tier = (form.get("budget_tier") or "").strip()
    use_case = (form.get("use_case") or "general").strip()
    household_size_raw = (form.get("household_size") or "1").strip()

    if not location_key:
        raise ProfileFormError("Please choose a location, or select 'Custom location'.")
    if budget_tier not in BUDGET_TIERS:
        raise ProfileFormError("Please choose a valid budget level.")
    if use_case not in USE_CASES:
        raise ProfileFormError("Please choose a valid computer use case.")

    try:
        household_size = max(1, int(household_size_raw))
    except ValueError:
        household_size = 1

    if location_key == "custom":
        climate_key = (form.get("custom_climate") or "").strip()
        if climate_key not in CLIMATE_ZONES:
            raise ProfileFormError("Please choose a climate zone for your custom location.")
        location_name = (form.get("custom_name") or "Your location").strip() or "Your location"
        try:
            cost_of_living_index = float(form.get("custom_col") or 100)
        except ValueError:
            cost_of_living_index = 100.0

        return UserProfile(
            location_key="custom",
            location_name=location_name,
            climate_key=climate_key,
            budget_tier=budget_tier,
            use_case=use_case,
            household_size=household_size,
            has_children=_bool_field(form, "has_children"),
            coastal=_bool_field(form, "custom_coastal"),
            storm_risk=_bool_field(form, "custom_storm_risk"),
            seismic_risk=_bool_field(form, "custom_seismic_risk"),
            air_quality=(form.get("custom_air_quality") or "moderate"),
            grid_reliability=(form.get("custom_grid_reliability") or "stable"),
            cost_of_living_index=cost_of_living_index,
            highland=_bool_field(form, "custom_highland"),
        )

    try:
        loc = get_location(location_key)
    except KeyError as exc:
        raise ProfileFormError("Unknown location selected.") from exc

    return UserProfile(
        location_key=loc.key,
        location_name=f"{loc.name}, {loc.country}",
        climate_key=loc.climate_key,
        budget_tier=budget_tier,
        use_case=use_case,
        household_size=household_size,
        has_children=_bool_field(form, "has_children"),
        coastal=loc.coastal,
        storm_risk=loc.storm_risk,
        seismic_risk=loc.seismic_risk,
        air_quality=loc.air_quality,
        grid_reliability=loc.grid_reliability,
        cost_of_living_index=loc.cost_of_living_index,
        highland=loc.highland,
    )


def profile_from_json(payload: dict) -> UserProfile:
    """Build a validated UserProfile from a JSON API request body."""
    if not isinstance(payload, dict):
        raise ProfileFormError("Request body must be a JSON object.")

    location_key = str(payload.get("location", "")).strip()
    budget_tier = str(payload.get("budget_tier", "")).strip()
    use_case = str(payload.get("use_case", "general")).strip()

    if budget_tier not in BUDGET_TIERS:
        raise ProfileFormError("'budget_tier' must be one of: " + ", ".join(BUDGET_TIERS))
    if use_case not in USE_CASES:
        raise ProfileFormError("'use_case' must be one of: " + ", ".join(USE_CASES))

    if location_key and location_key != "custom":
        try:
            loc = get_location(location_key)
        except KeyError as exc:
            raise ProfileFormError(
                f"Unknown location key: {location_key!r}. See /api/locations."
            ) from exc
        return UserProfile(
            location_key=loc.key,
            location_name=f"{loc.name}, {loc.country}",
            climate_key=loc.climate_key,
            budget_tier=budget_tier,
            use_case=use_case,
            household_size=int(payload.get("household_size", 1) or 1),
            has_children=bool(payload.get("has_children", False)),
            coastal=loc.coastal,
            storm_risk=loc.storm_risk,
            seismic_risk=loc.seismic_risk,
            air_quality=loc.air_quality,
            grid_reliability=loc.grid_reliability,
            cost_of_living_index=loc.cost_of_living_index,
            highland=loc.highland,
        )

    climate_key = str(payload.get("climate_key", "")).strip()
    if climate_key not in CLIMATE_ZONES:
        raise ProfileFormError(
            "For a custom location, 'climate_key' must be one of: "
            + ", ".join(CLIMATE_ZONES)
        )

    return UserProfile(
        location_key="custom",
        location_name=str(payload.get("location_name", "Custom location")),
        climate_key=climate_key,
        budget_tier=budget_tier,
        use_case=use_case,
        household_size=int(payload.get("household_size", 1) or 1),
        has_children=bool(payload.get("has_children", False)),
        coastal=bool(payload.get("coastal", False)),
        storm_risk=bool(payload.get("storm_risk", False)),
        seismic_risk=bool(payload.get("seismic_risk", False)),
        air_quality=str(payload.get("air_quality", "moderate")),
        grid_reliability=str(payload.get("grid_reliability", "stable")),
        cost_of_living_index=float(payload.get("cost_of_living_index", 100.0) or 100.0),
        highland=bool(payload.get("highland", False)),
    )


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        countries=locations_by_country(),
        budget_tiers=BUDGET_TIERS,
        use_cases=USE_CASES,
        climate_zones=CLIMATE_ZONES,
        error=None,
        form=request.args,
    )


@app.route("/results", methods=["POST"])
def results():
    try:
        profile = profile_from_form(request.form)
    except (ProfileFormError, ValueError) as exc:
        return render_template(
            "index.html",
            countries=locations_by_country(),
            budget_tiers=BUDGET_TIERS,
            use_cases=USE_CASES,
            climate_zones=CLIMATE_ZONES,
            error=str(exc),
            form=request.form,
        ), 400

    report = build_report(profile)
    climate = CLIMATE_ZONES[profile.climate_key]
    return render_template(
        "results.html",
        report=report,
        climate=climate,
        budget_tiers=BUDGET_TIERS,
    )


@app.route("/api/locations", methods=["GET"])
def api_locations():
    return jsonify(
        {
            key: {
                "name": loc.name,
                "country": loc.country,
                "climate_key": loc.climate_key,
            }
            for key, loc in LOCATIONS.items()
        }
    )


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    payload = request.get_json(silent=True) or {}
    try:
        profile = profile_from_json(payload)
    except (ProfileFormError, ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400

    report = build_report(profile)
    return jsonify(report.as_dict())


@app.errorhandler(404)
def not_found(_exc):
    return render_template("404.html"), 404


if __name__ == "__main__":
    debug = os.environ.get("HAMSAZ_DEBUG", "1") == "1"
    app.run(debug=debug)
