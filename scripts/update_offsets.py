"""Utility to regenerate placeholder offsets from a local dump (research only).

Reads `dumps/current.bin` if it exists and writes `offsets/local_offsets.json`.
This repo deliberately ships with placeholder offsets — the script is here so
researchers can wire in their own dump pipeline without touching core code.
"""
from __future__ import annotations

import json
from pathlib import Path

DUMP = Path("dumps/current.bin")
OUT = Path("offsets/local_offsets.json")


def main() -> int:
    if not DUMP.exists():
        print(f"[!] no dump at {DUMP} — nothing to do")
        return 1
    data = DUMP.read_bytes()
    payload = {
        "note": "placeholder — replace with real dump offsets during research",
        "size": len(data),
        "sha_prefix": data[:8].hex(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"[+] wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())