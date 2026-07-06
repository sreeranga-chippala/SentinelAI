"""
SentinelAI - Allocation MCP Tools

Production-ready disaster resource allocation tools.
"""

from __future__ import annotations

from typing import Any


class AllocationToolException(Exception):
    """Raised when allocation fails."""


_PRIORITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def calculate_priority(
    disaster_type: str,
    severity: str,
    affected_people: int,
) -> dict[str, Any]:
    """
    Determine disaster priority.
    """

    severity = severity.lower()

    score = _PRIORITY_SCORE.get(severity, 1)

    if affected_people >= 50000:
        score += 2
    elif affected_people >= 10000:
        score += 1

    if disaster_type.lower() in {
        "earthquake",
        "tsunami",
        "cyclone",
    }:
        score += 1

    score = min(score, 4)

    reverse = {
        1: "Low",
        2: "Medium",
        3: "High",
        4: "Critical",
    }

    return {
        "priority": reverse[score],
        "score": score,
    }


def allocate_resources(
    priority: str,
    available_resources: dict[str, int],
) -> dict[str, Any]:
    """
    Allocate disaster resources based on priority.
    """

    priority = priority.lower()

    allocation_ratio = {
        "low": 0.25,
        "medium": 0.50,
        "high": 0.75,
        "critical": 1.00,
    }

    ratio = allocation_ratio.get(priority, 0.50)

    allocated = {}
    remaining = {}

    for resource, quantity in available_resources.items():

        assigned = int(quantity * ratio)

        allocated[resource] = assigned

        remaining[resource] = quantity - assigned

    return {
        "allocated": allocated,
        "remaining": remaining,
    }


def generate_recommendations(
    priority: str,
    remaining: dict[str, int],
) -> list[str]:
    """
    Generate operational recommendations.
    """

    recommendations = []

    if priority == "Critical":
        recommendations.append(
            "Deploy all available emergency resources immediately."
        )
        recommendations.append(
            "Request support from neighboring districts."
        )
        recommendations.append(
            "Establish temporary medical camps."
        )

    elif priority == "High":
        recommendations.append(
            "Deploy rapid response teams."
        )
        recommendations.append(
            "Prepare reserve resources."
        )

    else:
        recommendations.append(
            "Continue monitoring the situation."
        )

    exhausted = [
        name
        for name, value in remaining.items()
        if value == 0
    ]

    if exhausted:
        recommendations.append(
            "Resources exhausted: "
            + ", ".join(exhausted)
        )

    return recommendations


def perform_allocation(
    disaster_type: str,
    severity: str,
    affected_people: int,
    available_resources: dict[str, int],
) -> dict[str, Any]:
    """
    Complete allocation pipeline.
    """

    priority_result = calculate_priority(
        disaster_type,
        severity,
        affected_people,
    )

    allocation_result = allocate_resources(
        priority_result["priority"],
        available_resources,
    )

    recommendations = generate_recommendations(
        priority_result["priority"],
        allocation_result["remaining"],
    )

    return {
        "success": True,
        "disaster_type": disaster_type,
        "severity": severity,
        "affected_people": affected_people,
        "priority": priority_result["priority"],
        "allocation": allocation_result["allocated"],
        "remaining": allocation_result["remaining"],
        "recommendations": recommendations,
    }


def health_check() -> dict[str, Any]:
    """
    Allocation MCP health check.
    """

    return {
        "service": "Allocation MCP",
        "status": "healthy",
    }