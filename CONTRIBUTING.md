# Contributing to dbd-external-esp

Educational project — external ESP / overlay cheats for Dead by Daylight,
built for reverse-engineering research and cheat-detection studies.

## Ground rules

- **Never** ship working offsets for live game versions. Offsets in
  `src/offsets/` are placeholders. Contributions that include real,
  currently-valid offsets will be rejected — this is a research sandbox.
- Keep the pipeline architecture intact: `ingest -> process -> render`.
- Every new feature needs a test under `tests/`.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --dry-run
```

## Commit style

`feat(esp): add survivor distance ring` / `fix(reader): handle process exit`

## Code style

- ruff + black, line length 100
- Type hints required on public functions
- No `print()` — use `src/utils/logging_util.py`

## Disclaimer

Submitting a PR means you accept that this code is for **educational
purposes only** and that using it in live matches violates BHVR's ToS.