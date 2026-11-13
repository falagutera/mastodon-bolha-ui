# AGENTS.md

Notes for coding agents (and people) changing Bolha UI. The README says what it is and how to
install it; this file says how to change it without breaking what the README promises.

## What it is

A Mastodon theme: SCSS on top of Mastodon's own `application.scss`, plus the Ubuntu fonts. No
JavaScript. Everything under `src/` mirrors the Mastodon tree and is copied there by `install.sh`.

## Commands

```sh
scripts/build-dist.sh            # regenerate dist/ after any change to _theme.scss or _gcn.scss
scripts/build-dist.sh --check    # what CI runs
scripts/test-install.sh          # install.sh against a fake Mastodon tree
shellcheck install.sh scripts/*.sh
docker run --rm -v "$PWD":/w -w /w node:22-alpine npx --yes sass@1.93.2 --no-source-map \
  --load-path=ci/stub src/app/javascript/styles/bolha-ui.scss > /dev/null
```

To see a change on a real server without building: inject the plain CSS into a logged-in tab (a
constructable stylesheet: `document.adoptedStyleSheets`), it works over the default theme.

## Rules that must hold

1. **Tokens first.** Colours go through Mastodon's tokens (`--color-*`) or the `--b-*` variables, set
   per `:root[data-color-scheme='dark'|'light']` and `[data-contrast='high']`. A component rule only
   when no token reaches it; never a hex in a component rule.
2. **Both schemes and high contrast.** A new token is set for dark and light; check high contrast.
3. **Variants only swap the accent.** `_gcn.scss` sets `--b-accent-*` and nothing else.
4. **The user's preferences win.** Keep `.system-font` working (don't force `font-family` on `body`)
   and never hide what Mastodon shows.
5. **dist/ is generated.** Edit the SCSS, run `scripts/build-dist.sh`; CI fails if they differ.
6. **install.sh writes only the theme's files** and its two `themes.yml` lines, is idempotent and
   reversible (`scripts/test-install.sh`). POSIX sh, shellcheck clean.
7. **English** in code, comments, commits and the README; `README.pt-BR.md` follows the README.

## Releasing

Bump `VERSION` (fix or small visual change = patch, new rule or variant = minor, renamed theme keys
= major), add the `CHANGELOG.md` entry (CI fails without it), update the version in the install
commands of both READMEs, run `scripts/build-dist.sh` (it also regenerates `_version.scss` as
`X.Y.Z-dev`), commit, tag `vX.Y.Z` and push the tag. The tag's `release` job builds the tarball
with `X.Y.Z-BUILD` (BUILD = its pipeline number) and keeps it as an artifact; never move a tag
that already has a release.

## Website

`site/build.py` (Python stdlib) builds [ui.bolha.us](https://ui.bolha.us): pt-BR at `/`, English at
`/en/`. It reads `VERSION`, `CHANGELOG.md` and `screenshots/`, so a release updates it by itself; the
`pages` job publishes it on every push to `main`. Preview: `python3 site/build.py /tmp/ui && python3 -m
http.server -d /tmp/ui`. Keep both languages in step when you change the text.
