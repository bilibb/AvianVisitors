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
git switch german-dashboard-sets
avian/scripts/merge_upstream.sh             # aktueller Stand von upstream/avian-visitors
avian/scripts/merge_upstream.sh v1.3.0      # oder ein Release-Tag
git push origin german-dashboard-sets
```

Das Skript holt `upstream`, merged und nimmt bei generierten Dateien (`dims.json`,
`masks.json`, Cache-Versionen in `apt.js`, `illustrations/*.png`) die Upstream-Seite.
Danach wendet `use_illustration_set.py` das eigene Bildset wieder an. Bleiben echte
Konflikte (z. B. in `newinstaller.sh`), bricht es mit einer Liste ab: lösen,
`git add`, Skript erneut starten. Veraltete deutsche Übersetzungen meldet
`test_patch_homepage_de.py` als Warnung.

`git config rerere.enabled true` merkt sich von Hand gelöste Konflikte für das nächste Mal.

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
