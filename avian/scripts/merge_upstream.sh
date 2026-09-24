#!/bin/sh
# AvianVisitors fork - merge an upstream tag/branch and re-apply the fork.
#
#   avian/scripts/merge_upstream.sh            # upstream/avian-visitors
#   avian/scripts/merge_upstream.sh v1.3.0     # a release tag
#
# Conflicts in generated files (dims.json, masks.json, the apt.js cache
# versions, the shipped illustrations/*.png) take the upstream side;
# use_illustration_set.py then regenerates the fork side. Any other
# conflict is left for you: fix it, `git add`, then re-run this script.
set -e
cd "$(git rev-parse --show-toplevel)"
ref=${1:-upstream/avian-visitors}
GENERATED='^avian/frontend/(dims|masks)\.json$|^avian/frontend/apt\.js$|^avian/assets/illustrations/[^/]+\.png$'

if ! git rev-parse -q --verify MERGE_HEAD >/dev/null; then
  git fetch upstream --tags
  git merge --no-edit "$ref" || git rev-parse -q --verify MERGE_HEAD >/dev/null \
    || { echo "Merge nicht gestartet (siehe oben)." >&2; exit 1; }
fi
git diff --name-only --diff-filter=U | grep -E "$GENERATED" | xargs -r git checkout --theirs --

python3 avian/scripts/use_illustration_set.py
git add -A avian/frontend/dims.json avian/frontend/masks.json avian/frontend/apt.js avian/assets/illustrations

left=$(git diff --name-only --diff-filter=U)
if [ -n "$left" ]; then
  echo "Konflikte von Hand lösen, dann 'git add' und das Skript erneut starten:" >&2
  echo "$left" >&2
  exit 1
fi

python3 tests/test_use_illustration_set.py
python3 tests/test_patch_homepage_de.py || echo "WARNUNG: deutsche Übersetzungen veraltet (siehe oben)" >&2

if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
  git commit --no-edit
elif ! git diff --cached --quiet; then
  git commit -m "Re-apply illustration set after merging $ref"
fi
echo "Fertig. Prüfen, dann: git push origin $(git branch --show-current)"
