"""
Small command-line interface so non-Python teammates can run:

    python -m src.cli --url https://www.rtx.com --posts 7 --interval day
"""
from __future__ import annotations
import argparse
import asyncio
import json
from pathlib import Path

from .social_agent import generate_social_calendar


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a social-media content calendar")
    p.add_argument("--url", required=True, help="Target website URL")
    p.add_argument("--platform", default="instagram", help="instagram / facebook / etc.")
    p.add_argument("--posts", type=int, default=7, help="Number of posts to create")
    p.add_argument(
        "--interval",
        choices=["day", "week"],
        default="day",
        help="'day' = consecutive days, 'week' = once a week",
    )
    p.add_argument("--extra", default="", help="Extra info / campaign focus")
    p.add_argument(
        "--out",
        default="calendar.json",
        help="Path to write JSON output (also printed to stdout)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    calendar = asyncio.run(
        generate_social_calendar(
            n_posts=args.posts,
            interval=args.interval,
            url=args.url,
            platform=args.platform,
            extra_info=args.extra,
        )
    )

    # Write + pretty-print
    Path(args.out).write_text(json.dumps(calendar, indent=2))
    print(json.dumps(calendar, indent=2))
    print(f"\n✅ Saved to {args.out}")


if __name__ == "__main__":
    main()
