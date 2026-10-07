# Fork-Pflege (bilibb/AvianVisitors)

## Branches

- `avian-visitors`: unveränderter Spiegel von `upstream/avian-visitors`. Nie selbst darauf committen.
- `german-dashboard-v3`: eigener Stand = Upstream-Tag + ein Fork-Commit (deutsche Oberfläche + eigene Bilder).

Fork-Änderungen bleiben möglichst in eigenen Dateien (`avian/patch_homepage_de.py`,
`avian/scripts/merge_upstream.sh`, `tests/test_patch_homepage_de.py`, dieses Dokument).
Upstream-Dateien werden nur angefasst in `newinstaller.sh` (Repo, Branch, Ort,
Stationsname `Gefiederte Besucher`, Confidence `0.9`), in generierten Dateien (Bilder, `dims.json`,
`masks.json`, Cache-Versionen in `apt.js`) und in einer Zeile in `apt.js`: Atlas
standardmäßig mit klassischen Karten (setzt `merge_upstream.sh` nach jedem Merge neu;
`tests/smoke_atlas_classic.mjs` erwartet deshalb absichtlich noch `stamps`).
Die deutsche Oberfläche wird erst bei der Installation per `patch_homepage_de.py` erzeugt,
das Repo selbst bleibt englisch und damit konfliktarm.

## Neue Upstream-Version übernehmen

```sh
git switch german-dashboard-v3
avian/scripts/merge_upstream.sh             # aktueller Stand von upstream/avian-visitors
avian/scripts/merge_upstream.sh v1.3.0      # oder ein Release-Tag
git push origin german-dashboard-v3
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

## Laufende Station von v2 auf v3 umstellen

Erkennungen (`~/BirdNET-Pi/scripts/birds.db`, `~/BirdNET-Pi/BirdDB.txt`), Aufnahmen
(`~/BirdSongs`) und Einstellungen (`/etc/birdnet/birdnet.conf`) sind nicht in Git und
bleiben beim Branch-Wechsel liegen. Trotzdem vorher sichern. `Tools → Pull latest` geht
im Fork nicht (der Updater verlangt das Original-Repo), deshalb von Hand per SSH:

```sh
# 1. Sicherung
sqlite3 ~/BirdNET-Pi/scripts/birds.db ".backup '$HOME/birds-$(date +%F).db'"
cp ~/BirdNET-Pi/BirdDB.txt /etc/birdnet/birdnet.conf ~/

# 2. Deutsche Patches von v2 beiseitelegen und v3 holen
cd ~/BirdNET-Pi
git -c user.name=station -c user.email=station@localhost stash push -m "v2 deutscher Patch"
git fetch --depth=1 origin german-dashboard-v3:refs/remotes/origin/german-dashboard-v3
git switch -c german-dashboard-v3 origin/german-dashboard-v3

# 3. Oberfläche wieder eindeutschen
python3 avian/patch_homepage_de.py avian/frontend
```

`git switch` bricht ab, statt eine nicht versionierte Datei zu überschreiben. Danach die Seite
neu laden. Stationsname `Gefiederte Besucher` und Confidence `0.9` setzt der Installer nur bei
Neuinstallation, auf der laufenden Station in **Settings** einstellen.

Grenze: So wird nur der Code getauscht. Die neuen Systemteile von v1.3 (`avian-bundle`,
Bundle-Helper unter `/usr/local/sbin`) kommen nur mit einer Neuinstallation über
`newinstaller.sh`. Bis dahin funktioniert **Settings → Bird bundle** nicht, Collage und Atlas
nutzen weiter die mitgelieferten Bilder.

Zurück auf v2: `git switch german-dashboard-v2 && git stash pop`.
