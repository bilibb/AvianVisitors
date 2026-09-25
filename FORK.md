# Fork-Pflege (bilibb/AvianVisitors)

## Branches

- `avian-visitors`: unveränderter Spiegel von `upstream/avian-visitors`. Nie selbst darauf committen.
- `german-dashboard-v2`: eigener Stand = Upstream-Tag + ein Fork-Commit (deutsche Oberfläche + eigene Bilder).

Fork-Änderungen bleiben möglichst in eigenen Dateien (`avian/patch_homepage_de.py`,
`avian/scripts/merge_upstream.sh`, `tests/test_patch_homepage_de.py`, dieses Dokument).
Upstream-Dateien werden nur angefasst in `newinstaller.sh` (Repo, Branch, Ort) und
in generierten Dateien (Bilder, `dims.json`, `masks.json`, Cache-Versionen in `apt.js`).
Die deutsche Oberfläche wird erst bei der Installation per `patch_homepage_de.py` erzeugt,
das Repo selbst bleibt englisch und damit konfliktarm.

## Neue Upstream-Version übernehmen

```sh
git switch german-dashboard-v2
avian/scripts/merge_upstream.sh             # aktueller Stand von upstream/avian-visitors
avian/scripts/merge_upstream.sh v1.3.0      # oder ein Release-Tag
git push origin german-dashboard-v2
```

Das Skript holt `upstream` und merged. Bei Konflikten in `illustrations/*.png` bleiben die
eigenen Bilder, bei `dims.json`, `masks.json` und `apt.js` wird die Upstream-Seite genommen
und danach per `build_masks.py` bzw. neuem Cache-Suffix in `apt.js` neu erzeugt. Bleiben echte
Konflikte (z. B. in `newinstaller.sh`), bricht es mit einer Liste ab: lösen, `git add`,
Skript erneut starten. Veraltete deutsche Übersetzungen meldet `test_patch_homepage_de.py`
als Warnung.

`git config rerere.enabled true` merkt sich von Hand gelöste Konflikte für das nächste Mal.

## Illustrationen

Eigene, bereits freigestellte Bilder liegen direkt in `avian/assets/illustrations/<slug>.png`
bzw. `<slug>-2.png` (Flug) und ersetzen gleichnamige Upstream-Bilder. Neue oder geänderte
Bilder dort ablegen, dann:

```sh
python3 avian/scripts/build_masks.py
digest=$(cat avian/assets/illustrations/*.png | sha1sum | cut -c1-8)
sed -i -E "s/(var (SKETCH|IMG|TABLE)_VERSION = '[^'-]+)(-[0-9a-f]{8})?'/\1-$digest'/" avian/frontend/apt.js
```

und alles committen.
