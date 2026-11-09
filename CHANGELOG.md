# Changelog

All notable changes to Bolha UI. Versions follow [SemVer](https://semver.org/); releases are Git tags (`vX.Y.Z`).

## 1.0.1 — 2026-11-09

- The compose drawer scrolls again when the text box grows (for example when editing a post with
  attachments): the drawer card no longer cuts off its own scrollbar.

## 1.0.0 — 2026-11-09

First release, running on bolha.us and jornalismo.social.

- Two themes: **Bolha UI** (yellow) and **Bolha UI GCN** (red), for Mastodon 4.7.
- Light, dark and high contrast, following each person's appearance settings.
- Ubuntu and Ubuntu Mono bundled (latin and latin-ext); the "use system font" preference still wins.
- Advanced web interface: columns as cards, mono column headers, pill buttons and tabs, the instance
  mascot centred at the bottom of the compose drawer without the zig-zag.
- `install.sh` to install, update or remove it in a Mastodon source tree (`--dry-run`, `--uninstall`).
- Plain-CSS builds in `dist/` for custom CSS or Stylus.
