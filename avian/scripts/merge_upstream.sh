#!/bin/sh
# AvianVisitors fork - merge an upstream tag/branch and re-apply the fork.
#
#   avian/scripts/merge_upstream.sh            # upstream/avian-visitors
#   avian/scripts/merge_upstream.sh v1.3.0     # a release tag
#
# Conflicting illustrations/*.png keep the fork side (our own renders).
# dims.json, masks.json and the apt.js cache versions take the upstream
# side and are then regenerated from the merged illustrations. Any other
# conflict is left for you: fix it, `git add`, then re-run this script.
set -e
cd "$(git rev-parse --show-toplevel)"
ref=${1:-upstream/avian-visitors}

if ! git rev-parse -q --verify MERGE_HEAD >/dev/null; then
  git fetch upstream --tags
  git merge --no-edit "$ref" || git rev-parse -q --verify MERGE_HEAD >/dev/null \
    || { echo "Merge nicht gestartet (siehe oben)." >&2; exit 1; }
fi
git diff --name-only --diff-filter=U | grep -E '^avian/assets/illustrations/[^/]+\.png$' | xargs -r git checkout --ours --
git diff --name-only --diff-filter=U | grep -E '^avian/frontend/((dims|masks)\.json|apt\.js)$' | xargs -r git checkout --theirs --

python3 avian/scripts/build_masks.py
digest=$(cat avian/assets/illustrations/*.png | sha1sum | cut -c1-8)
sed -i -E "s/(var (SKETCH|IMG|TABLE)_VERSION = '[^'-]+)(-[0-9a-f]{8})?'/\1-$digest'/" avian/frontend/apt.js
git add -A avian/frontend/dims.json avian/frontend/masks.json avian/frontend/apt.js avian/assets/illustrations

left=$(git diff --name-only --diff-filter=U)
if [ -n "$left" ]; then
  echo "Konflikte von Hand lösen, dann 'git add' und das Skript erneut starten:" >&2
  echo "$left" >&2
  exit 1
fi

python3 tests/test_patch_homepage_de.py || echo "WARNUNG: deutsche Übersetzungen veraltet (siehe oben)" >&2

if git rev-parse -q --verify MERGE_HEAD >/dev/null; then
  git commit --no-edit
elif ! git diff --cached --quiet; then
  git commit -m "Regenerate masks and cache versions after merging $ref"
fi
echo "Fertig. Prüfen, dann: git push origin $(git branch --show-current)"
