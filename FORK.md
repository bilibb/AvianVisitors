# Fork-Pflege (bilibb/AvianVisitors)

## Branches

- `avian-visitors`: unveränderter Spiegel von `upstream/avian-visitors`. Nie selbst darauf committen.
- `german-dashboard-sets`: eigener Stand = Upstream-Tag + Fork-Commits.

Fork-Änderungen bleiben möglichst in eigenen Dateien (`avian/patch_homepage_de.py`,
`avian/scripts/use_illustration_set.py`, `tests/test_*_de.py`, dieses Dokument).
Upstream-Dateien werden nur angefasst in `newinstaller.sh` (Repo, Branch, Ort) und
in generierten Dateien (Bilder, `dims.json`, `masks.json`, Cache-Versionen in `apt.js`).

## Neue Upstream-Version übernehmen

```sh
git fetch upstream --tags
git switch german-dashboard-sets
git merge v1.3.0                      # neuer Tag
# Konflikte in dims.json / masks.json / apt.js-Versionen: Upstream-Seite nehmen,
# danach regeneriert das Skript sie für das eigene Bildset:
git checkout --theirs avian/frontend/dims.json avian/frontend/masks.json avian/frontend/apt.js
python3 avian/scripts/use_illustration_set.py
python3 tests/test_patch_homepage_de.py        # veraltete Übersetzungs-Keys finden
python3 tests/test_use_illustration_set.py
git add -A && git commit
git push origin german-dashboard-sets
```

`git config rerere.enabled true` ist gesetzt: einmal gelöste Konflikte löst Git beim
nächsten Mal selbst.

## Illustrationen

Rohbilder je Modell liegen als normale Git-Dateien (~0,5–1 GB pro Set) unter
`avian/assets/illustrations/<set>/<slug>.png` bzw. `<slug>-2.png` (Flug).
Aktiv ist, was in `avian/assets/illustrations/*.png` committed ist.

```sh
python3 avian/scripts/use_illustration_set.py               # Standard: qwen-image-2.1
python3 avian/scripts/use_illustration_set.py flux.2-dev    # anderes Set
ILLUSTRATION_SET=flux.2-dev python3 avian/scripts/use_illustration_set.py
```

Neues Set: Ordner mit gleichen Dateinamen daneben legen, Skript mit dem Ordnernamen
aufrufen, Ordner und Ergebnis committen. Jedes ersetzte Rohbild bleibt dauerhaft in
der History, also nur fertige Sets committen. Bilder mit Alpha-Kanal werden nur zugeschnitten,
Bilder auf flachem Hintergrund per rembg freigestellt (langsam, Ergebnis wird in
`<set>/.cut/` gecacht).
Der Pi-Installer klont partiell und sparse (`--filter=blob:none`, ohne `illustrations/<set>/`),
lädt die Rohbilder also nicht.
