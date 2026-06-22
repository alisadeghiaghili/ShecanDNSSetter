# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-06-22

### Added
- **Rich CLI** (`cli/dns_cli.py`) with interactive TUI menu and non-interactive
  one-shot subcommands: `list`, `status`, `set <provider>`, `reset`
- **8 new DNS providers** — Begzar, Electro, HostIran, Radar Game, AsiaTech,
  Cloudflare, Google, Quad9
- `Category` enum (`ANTI_SANCTION`, `ANTI_FILTER`, `GAMING`, `GENERAL`) for
  grouping providers in both UI and CLI
- `description` field on `DNSProvider` dataclass — shown as subtitle in GUI
  and CLI tables
- `providers_by_category()` helper for grouped rendering
- `cli/` package with `__init__.py` exposing `main()`

### Changed
- GUI combo box now displays providers grouped by category with separators
  and per-item description label
- Combo box stores provider key in `userData` instead of raw display text —
  decouples display labels from internal keys

---

## [1.1.0] — 2026-06-22

### Changed (Architectural Refactor)
- Split monolith into layered architecture: `core/`, `ui/`, `utils/`
- `core/providers.py` — `DNSProvider` dataclass and `DNS_PROVIDERS` registry;
  adding a provider now requires a single line here and nothing else
- `core/adapter.py` — all WMI calls isolated here; only file that imports `wmi`
- `core/dns_service.py` — business logic and `IDLE`/`ACTIVE` state machine;
  zero UI dependency; independently testable
- `ui/main_window.py` — pure PyQt5 view; receives `DNSService` via constructor
  injection; no WMI or OS knowledge
- `utils/privileges.py` — UAC elevation helpers (`is_admin`, `ensure_admin`,
  `relaunch_as_admin`)
- `main.py` — thin entry point; wires `DNSService` into `MainWindow`

### Removed
- Monolithic `DNSChangerApp` class — replaced by the layered structure above

---

## [1.0.1] — 2026-06-22

### Fixed
- **DNS snapshot bug** — original DNS was captured *after* `SetDNSServerSearchOrder`
  instead of before, causing reset to restore the new DNS rather than the original
- **Silent WMI failure** — `SetDNSServerSearchOrder` return code was never checked;
  failures now surface a user-facing error dialog
- **Admin privilege check** — app would silently fail DNS changes when not running
  as Administrator; now auto-relaunches via UAC elevation at startup
- **DNS label comparison** — `update_current_dns_label` compared against a string
  literal that never matched the actual server list; replaced with empty-list check
  for DHCP detection
- **Unhandled exceptions** — WMI calls now wrapped in `try/except` with descriptive
  error messages shown to the user

---

## [1.0.0] — 2023-07-27

### Added
- Initial PyQt5 GUI application (`dnsSetter.py`)
- Support for Shecan (`178.22.122.100`, `185.51.200.2`) and
  403 (`10.202.10.202`, `10.202.10.102`) DNS providers
- Activate / Deactivate toggle button
- Provider combo box — button disabled until a provider is selected
- Current DNS display label updated on every toggle
- Automatic reset when switching providers while one is active
