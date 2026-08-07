from __future__ import annotations

import json

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client


def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hamsaz" in resp.data
    assert b"location-select" in resp.data


def test_results_happy_path(client):
    resp = client.post(
        "/results",
        data={
            "location": "tehran",
            "budget_tier": "balanced",
            "use_case": "programming",
            "household_size": "3",
        },
    )
    assert resp.status_code == 200
    assert "Tehran".encode() in resp.data
    assert "seismic".lower().encode() in resp.data.lower()


def test_results_custom_location(client):
    resp = client.post(
        "/results",
        data={
            "location": "custom",
            "custom_name": "My Village",
            "custom_climate": "subarctic",
            "custom_col": "60",
            "budget_tier": "budget",
            "use_case": "general",
            "custom_grid_reliability": "unstable",
        },
    )
    assert resp.status_code == 200
    assert b"My Village" in resp.data


def test_results_missing_location_shows_error(client):
    resp = client.post(
        "/results",
        data={"budget_tier": "balanced", "use_case": "general"},
    )
    assert resp.status_code == 400
    assert b"choose a location" in resp.data.lower()


def test_results_invalid_budget_tier_shows_error(client):
    resp = client.post(
        "/results",
        data={"location": "tehran", "budget_tier": "nope", "use_case": "general"},
    )
    assert resp.status_code == 400


def test_results_custom_missing_climate_shows_error(client):
    resp = client.post(
        "/results",
        data={
            "location": "custom",
            "budget_tier": "balanced",
            "use_case": "general",
        },
    )
    assert resp.status_code == 400
    assert b"climate zone" in resp.data.lower()


def test_api_locations(client):
    resp = client.get("/api/locations")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "tehran" in data
    assert data["tehran"]["country"] == "Iran"


def test_api_recommend_with_known_location(client):
    resp = client.post(
        "/api/recommend",
        data=json.dumps({"location": "tokyo", "budget_tier": "premium", "use_case": "gaming"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["profile"]["location_name"] == "Tokyo, Japan"
    assert data["computer"]["category"] == "computer"


def test_api_recommend_with_custom_location(client):
    resp = client.post(
        "/api/recommend",
        data=json.dumps(
            {
                "budget_tier": "budget",
                "use_case": "office",
                "climate_key": "hot_arid",
                "location_name": "Somewhere Hot",
                "grid_reliability": "unstable",
            }
        ),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["profile"]["climate_key"] == "hot_arid"


def test_api_recommend_invalid_budget_tier(client):
    resp = client.post(
        "/api/recommend",
        data=json.dumps({"location": "tokyo", "budget_tier": "invalid"}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_api_recommend_unknown_location(client):
    resp = client.post(
        "/api/recommend",
        data=json.dumps({"location": "atlantis", "budget_tier": "balanced"}),
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_404_page(client):
    resp = client.get("/this-does-not-exist")
    assert resp.status_code == 404
    assert b"doesn't exist" in resp.data.lower() or b"404" in resp.data
