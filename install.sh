#!/bin/sh
# Install (or remove) Bolha UI in a Mastodon source tree.
#
# Usage: ./install.sh [--dry-run] [--uninstall] <mastodon-dir>
#   <mastodon-dir>  the Mastodon checkout, e.g. /home/mastodon/live
#   --dry-run       only print what would change
#   --uninstall     remove the files and the themes.yml entries this script added
#
# It copies the theme into <mastodon-dir> (styles, fonts, theme names) and adds two lines to
# config/themes.yml. Nothing else in the tree is touched. Afterwards, rebuild the assets and
# restart Mastodon (the script prints how).
set -eu

here=$(cd "$(dirname "$0")" && pwd)
dry=0
uninstall=0
while [ $# -gt 0 ]; do
	case "$1" in
	--dry-run) dry=1; shift ;;
	--uninstall) uninstall=1; shift ;;
	-h | --help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
	-*) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
	*) break ;;
	esac
done
[ $# -eq 1 ] || { echo "usage: $0 [--dry-run] [--uninstall] <mastodon-dir>" >&2; exit 2; }
dest=$(cd "$1" && pwd)

if [ ! -f "$dest/config/themes.yml" ] || [ ! -f "$dest/app/javascript/styles/application.scss" ]; then
	echo "$dest does not look like a Mastodon source tree (no config/themes.yml or app/javascript/styles/application.scss)" >&2
	exit 1
fi

run() {
	if [ "$dry" -eq 1 ]; then echo "would: $*"; else "$@"; fi
}

# The files the theme owns, relative to the Mastodon tree.
files="app/javascript/styles/bolha-ui.scss
app/javascript/styles/bolha-ui-gcn.scss
app/javascript/styles/bolha-ui
app/javascript/fonts/bolha-ui
config/locales/bolha-ui.yml"
themes="bolha-ui: styles/bolha-ui.scss
bolha-ui-gcn: styles/bolha-ui-gcn.scss"

if [ "$uninstall" -eq 1 ]; then
	for f in $files; do
		[ -e "$dest/$f" ] && run rm -rf "$dest/$f"
	done
	if grep -q '^bolha-ui' "$dest/config/themes.yml"; then
		if [ "$dry" -eq 1 ]; then
			echo "would: remove the bolha-ui lines from config/themes.yml"
		else
			tmp=$(mktemp)
			grep -v '^bolha-ui' "$dest/config/themes.yml" > "$tmp"
			cat "$tmp" > "$dest/config/themes.yml"
			rm -f "$tmp"
		fi
	fi
	echo "Bolha UI removed from $dest. Users who had it fall back to the site's default theme."
else
	for f in $files; do
		if [ -d "$here/src/$f" ]; then
			# Copy the directory's contents, so a reinstall updates it instead of nesting it.
			run mkdir -p "$dest/$f"
			run cp -R "$here/src/$f/." "$dest/$f/"
		else
			run mkdir -p "$(dirname "$dest/$f")"
			run cp "$here/src/$f" "$dest/$f"
		fi
	done
	echo "$themes" | while IFS= read -r line; do
		name=${line%%:*}
		if grep -q "^$name:" "$dest/config/themes.yml"; then
			echo "themes.yml already has $name"
		elif [ "$dry" -eq 1 ]; then
			echo "would: add '$line' to config/themes.yml"
		else
			# Make sure the file ends with a newline before appending.
			[ -z "$(tail -c 1 "$dest/config/themes.yml")" ] || echo >> "$dest/config/themes.yml"
			echo "$line" >> "$dest/config/themes.yml"
		fi
	done
	echo "$(sed -n 's/.*"\(Bolha UI [^"]*\)".*/\1/p' "$here/src/app/javascript/styles/bolha-ui/_version.scss") installed in $dest."
fi

cat <<EOF

Next steps:
  1. Rebuild the assets (as the mastodon user, in $dest):
       RAILS_ENV=production bundle exec rails assets:precompile
     Docker: build your own image from this tree (see the README).
  2. Restart Mastodon:
       sudo systemctl restart mastodon-web mastodon-sidekiq mastodon-streaming
  3. Users pick "Bolha UI" in Preferences > Appearance; admins can make it the
     site default in Administration > Server settings > Appearance.
EOF
