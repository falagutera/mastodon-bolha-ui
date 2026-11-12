# Changelog

All notable changes to Bolha UI. Versions follow [SemVer](https://semver.org/); releases are Git tags (`vX.Y.Z`).

## 1.2.0 — 2026-11-12

- Versions follow the bolha standard: `X.Y.Z-BUILD`, where `BUILD` is the GitLab pipeline number
  of the release. Each `vX.Y.Z` tag publishes a release tarball with that version built in; a copy
  from git or a tag archive shows `X.Y.Z-dev`.
- The theme carries its version: anything with the class `bolha-ui-version` shows
  "Bolha UI X.Y.Z-BUILD" (the bolha.us fork shows it in the sidebar footer). `install.sh` prints it.

## 1.1.0 — 2026-11-12

- Tinted surfaces: the accent (yellow, or red in GCN) is mixed into a few backgrounds so the
  controls stand out. Stronger tint on the search box and the notification filter bar (the selected
  filter is a plain card-coloured tab), softer tint on the compose footer and the
  "Filtered notifications" banner, now a rounded card. The compose toolbar icons and the
  visibility/language chips take the accent too. Light, dark and high contrast.

## 1.0.2 — 2026-11-09

- Markdown headings and quotes in posts: the line under headings and the bar beside quotes are a
  stronger yellow (red in GCN), easier to see in light and dark.

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
