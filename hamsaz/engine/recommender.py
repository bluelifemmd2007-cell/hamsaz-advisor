"""Orchestrates the five category engines into one FullReport."""
from __future__ import annotations

from . import clothing, computers, devices, housing, vehicles
from .models import FullReport, UserProfile


def build_report(profile: UserProfile) -> FullReport:
    """Run every category engine against one user profile."""
    return FullReport(
        profile=profile,
        clothing=clothing.recommend(profile),
        vehicle=vehicles.recommend(profile),
        housing=housing.recommend(profile),
        devices=devices.recommend(profile),
        computer=computers.recommend(profile),
    )
