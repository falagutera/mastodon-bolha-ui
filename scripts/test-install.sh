#!/bin/sh
# Test install.sh against a throwaway fake Mastodon tree: install, reinstall (idempotent),
# dry-run (no changes) and uninstall (back to the original files).
set -eu
cd "$(dirname "$0")/.."
t=$(mktemp -d)
trap 'rm -rf "$t"' EXIT
mkdir -p "$t/config/locales" "$t/app/javascript/styles"
printf 'default: styles/application.scss\n' > "$t/config/themes.yml"
echo "// stub" > "$t/app/javascript/styles/application.scss"
orig=$(cd "$t" && find . -type f | sort; cat config/themes.yml)

fail() { echo "FAIL: $*" >&2; exit 1; }

./install.sh --dry-run "$t" > /dev/null
[ "$(cd "$t" && find . -type f | sort; cat config/themes.yml)" = "$orig" ] || fail "dry-run changed files"

./install.sh "$t" | grep -q "^Bolha UI $(cat VERSION)-" || fail "install.sh does not print the version"
./install.sh "$t" > /dev/null # twice: must not duplicate anything
[ "$(grep -c '^bolha-ui:' "$t/config/themes.yml")" = 1 ] || fail "bolha-ui not added exactly once"
[ "$(grep -c '^bolha-ui-gcn:' "$t/config/themes.yml")" = 1 ] || fail "bolha-ui-gcn not added exactly once"
for f in app/javascript/styles/bolha-ui.scss app/javascript/styles/bolha-ui-gcn.scss \
	app/javascript/styles/bolha-ui/_theme.scss app/javascript/styles/bolha-ui/_version.scss app/javascript/fonts/bolha-ui/ubuntu-latin-400-normal.woff2 \
	app/javascript/fonts/bolha-ui/LICENCE.txt config/locales/bolha-ui.yml; do
	[ -f "$t/$f" ] || fail "missing $f"
done
[ ! -e "$t/app/javascript/styles/bolha-ui/bolha-ui" ] || fail "reinstall nested the styles directory"

./install.sh --uninstall "$t" > /dev/null
[ "$(cd "$t" && find . -type f | sort; cat config/themes.yml)" = "$orig" ] || fail "uninstall left changes"
echo "install.sh: ok"
