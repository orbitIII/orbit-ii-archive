#!/usr/bin/env python3
"""Extract @svenmarquardt following list via instaloader (requires logged-in session)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "marquardt_following_raw.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Instagram following list for aesthetic mapping.")
    parser.add_argument("--username", required=True, help="Instagram login used for instaloader session file")
    parser.add_argument("--target", default="svenmarquardt", help="Profile whose following list to export")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        import instaloader
    except ImportError:
        print("Install instaloader: pip install instaloader", file=sys.stderr)
        print("Then login once: instaloader --login YOUR_USERNAME", file=sys.stderr)
        return 1

    loader = instaloader.Instaloader(quiet=True)
    try:
        loader.load_session_from_file(args.username)
    except FileNotFoundError:
        print(f"No session file for {args.username}. Run: instaloader --login {args.username}", file=sys.stderr)
        return 1

    profile = instaloader.Profile.from_username(loader.context, args.target)
    handles = []
    for followee in profile.get_followees():
        handles.append(
            {
                "handle": followee.username,
                "name": followee.full_name or "",
                "is_verified": followee.is_verified,
                "is_private": followee.is_private,
                "bio": (followee.biography or "")[:500],
            }
        )

    payload = {
        "anchor": args.target,
        "source": "instaloader_following",
        "extracted": date.today().isoformat(),
        "expected_following": profile.followees,
        "count": len(handles),
        "handles": handles,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(handles)} handles to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
