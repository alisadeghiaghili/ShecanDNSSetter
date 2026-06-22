# 🌐 DNS Changer

> A Windows DNS manager for Iranian users — GUI + CLI, built with Python.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

---

[نسخه فارسی (Persian README)](README.md)

---

## About the Author

**Name:** Ali Sadeghi Aghili
**GitHub:** [github.com/alisadeghiaghili](https://github.com/alisadeghiaghili)
**Email:** [alisadeghiaghili@gmail.com](mailto:alisadeghiaghili@gmail.com)

---

## Overview

DNS Changer is a Windows desktop application that lets you switch between DNS providers with a single click or command. It supports 10 providers across four categories — anti-sanction, anti-filter, gaming, and general-purpose — and ships both a PyQt5 GUI and a Rich-powered interactive CLI.

---

## Features

- **10 pre-configured DNS providers** across four categories
- **GUI** — PyQt5 interface with categorised dropdown and per-provider descriptions
- **CLI** — interactive TUI menu *and* non-interactive one-shot commands
- Automatic **DNS snapshot** before any change — safe rollback to DHCP
- **UAC elevation** — auto-relaunches with admin privileges if needed
- WMI return-code checking — surfaces real errors instead of silent failures
- Layered architecture (core / ui / cli / utils) — each layer independently testable

---

## DNS Providers

| Provider    | Category      | Primary          | Secondary         |
|-------------|---------------|------------------|-------------------|
| Shecan      | Anti-Sanction | 178.22.122.100   | 185.51.200.2      |
| Begzar      | Anti-Sanction | 185.55.226.26    | 185.55.225.25     |
| Electro     | Anti-Sanction | 78.157.42.100    | 78.157.42.101     |
| HostIran    | Anti-Sanction | 172.29.0.100     | 172.29.2.100      |
| 403         | Anti-Filter   | 10.202.10.202    | 10.202.10.102     |
| Radar Game  | Gaming        | 10.202.10.10     | 10.202.10.11      |
| AsiaTech    | Gaming        | 185.98.113.113   | 185.98.114.114    |
| Cloudflare  | General       | 1.1.1.1          | 1.0.0.1           |
| Google      | General       | 8.8.8.8          | 8.8.4.4           |
| Quad9       | General       | 9.9.9.9          | 149.112.112.112   |

---

## Requirements

- Windows 10 / 11
- Python 3.11+
- Administrator privileges

```bash
pip install PyQt5 rich
```

---

## Usage

### GUI

```bash
python -m dns_changer.main
```

Or download the pre-built executable:
[Download DNS Changer (.exe)](https://github.com/alisadeghiaghili/ShecanDNSSetter/releases/download/pre-release/dnsSetter.exe)

> **Must be run as Administrator.**

### CLI

```bash
# Interactive TUI menu
python -m dns_changer.cli.dns_cli

# One-shot commands
python -m dns_changer.cli.dns_cli list             # list all providers
python -m dns_changer.cli.dns_cli status           # show current DNS
python -m dns_changer.cli.dns_cli set Shecan       # activate a provider
python -m dns_changer.cli.dns_cli reset            # revert to DHCP
```

---

## Project Structure

```
dns_changer/
├── main.py                  # GUI entry point
├── core/
│   ├── providers.py         # DNSProvider dataclass + registry
│   ├── adapter.py           # WMI calls (isolated here only)
│   └── dns_service.py       # business logic + state machine
├── ui/
│   └── main_window.py       # PyQt5 window
├── cli/
│   └── dns_cli.py           # Rich CLI (interactive + one-shot)
└── utils/
    └── privileges.py        # UAC elevation helpers
```

---

## How to Contribute

1. Fork the repository from [github.com/alisadeghiaghili/ShecanDNSSetter](https://github.com/alisadeghiaghili/ShecanDNSSetter)
2. Create a new branch for your changes
3. Commit with descriptive messages following [Conventional Commits](https://www.conventionalcommits.org/)
4. Push and open a pull request

To add a new DNS provider, edit **only** `core/providers.py` — no other file needs to change.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
