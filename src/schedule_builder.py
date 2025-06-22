"""
Utility that converts (n_posts, interval) → ['Monday', 'Tuesday', …] or ['Week 1', …].

Keeps date logic in one place so the LLM prompt stays dead-simple.
"""
from __future__ import annotations
from datetime import date, timedelta
from typing import List

__all__ = ["build_schedule"]


def build_schedule(
    n_posts: int,
    interval: str = "day",
    *,
    start_date: date | None = None,
) -> List[str]:
    """
    • interval == "day"  → consecutive weekday names
    • interval == "week" → 'Week 1', 'Week 2', …
    """
    if n_posts < 1:
        raise ValueError("n_posts must be ≥ 1")

    if interval not in {"day", "week"}:
        raise ValueError("interval must be 'day' or 'week'")

    if start_date is None:
        start_date = date.today()

    labels = []
    for i in range(n_posts):
        if interval == "day":
            labels.append((start_date + timedelta(days=i)).strftime("%A"))
        else:  # week
            labels.append(f"Week {i + 1}")
    return labels
