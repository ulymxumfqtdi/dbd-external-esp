# Security Policy

## Scope

`dbd-external-esp` is an **educational external cheat** for Dead by Daylight.
It reads process memory from outside the game and renders an overlay. It does
**not** modify game memory, inject DLLs, or interact with the anti-cheat
(EAC) in any active way.

## Reporting

If you find a bug that could:
- crash the game process
- leak user data from memory dumps
- cause the overlay to be detected by EAC in an unintended way

…please open a private security advisory on GitHub. Do **not** open a public
issue for anti-cheat bypass or detection concerns.

## Out of scope

- Requests for working offsets (see CONTRIBUTING)
- Requests for EAC / BattlEye bypass code
- HWID spoofer integration

## Disclaimer

Use strictly on your own private lobbies / offline mode. The maintainers
accept **no** responsibility for bans, account loss, or ToS violations.