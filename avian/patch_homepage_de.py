#!/usr/bin/env python3
"""Patch English UI strings in AvianVisitors frontend files to German.

Usage: patch_homepage_de.py <path-to-frontend-dir>

Add new translations by appending entries to the dicts below.
Replacements use str.replace() (literal match, no regex).
"""

import sys
from pathlib import Path

# ── index.html translations ──────────────────────────────────────────
# For short/generic words, include surrounding HTML (e.g. >menu<)
# to prevent false matches in attributes, class names, or JS.

HTML_TRANSLATIONS = {
    # Language attribute
    'lang="en"': 'lang="de"',
    # Title & Meta
    ">your birds<": ">Deine Vögel<",
    "A live bird collage from your window.": "Eine Live-Vogelcollage von deinem Fenster.",
    # Navigation (bottom slider)
    ">collage<": ">Collage<",
    ">stats<": ">Statistik<",
    ">atlas<": ">Atlas<",
    # Menu button
    ">menu<": ">Menü<",
    # Main header
    "Heard Recently": "Kürzlich gehört",
    # Stats section headings
    ">By Period<": ">Nach Zeitraum<",
    "detections, grouped by recency": "Erkennungen, nach Aktualität gruppiert",
    ">Top Species<": ">Häufigste Arten<",
    "most-heard, current window": "meistgehört, aktuelles Fenster",
    ">First Detections<": ">Ersterkennungen<",
    "newest additions to the life list": "neueste Einträge in der Gesamtliste",
    # Atlas sort tooltips & aria-labels
    "most heard": "meistgehört",
    "most recent": "neueste",
    # Detail modal labels
    ">all time<": ">gesamt<",
    ">window<": ">Fenster<",
    ">first heard<": ">erstmals gehört<",
    "Loading description...": "Beschreibung wird geladen...",
    ">genus<": ">Gattung<",
    ">rarity<": ">Seltenheit<",
    ">Recordings<": ">Aufnahmen<",
    "Loading recordings...": "Aufnahmen werden geladen...",
    # Pose toggle tooltips
    ">perched<": ">sitzend<",
    ">in flight<": ">im Flug<",
    # About modal
    "The birds outside your window": "Die Vögel vor deinem Fenster",
    "explore the birds": "entdecke die Vögel",
    "A tiny microphone identifies every passing bird with Cornell's": "Ein kleines Mikrofon erkennt jeden vorbeifliegenden Vogel mit Cornells",
    "Each species shows up as an illustration in the collage, sized by how often it's been heard.": "Jede Art erscheint als Illustration in der Collage, skaliert nach Häufigkeit der Erkennung.",
    # Lock screen
    "enter password to unlock tools.": "Passwort eingeben zum Entsperren.",
    'placeholder="password"': 'placeholder="Passwort"',
    # Return-to-atlas aria-label
    "back to collage": "zurück zur Collage",
    # Time window picker buttons
    ">7D<": ">7T<",
    ">ALL<": ">ALLE<",
}

# ── apt.js translations ──────────────────────────────────────────────
# Strings rendered by JavaScript at runtime.

JS_TRANSLATIONS = {
    # View titles (header text per tab)
    "'Heard Recently'": "'Kürzlich gehört'",
    "'Avian Visitors'": "'Vogelbesucher'",
    # Collage empty state
    "no birds heard in this window.": "keine Vögel in diesem Zeitfenster gehört.",
    # Stats empty state
    "no detections in this window": "keine Erkennungen in diesem Zeitfenster",
    "no detections in window": "keine Erkennungen im Fenster",
    "no detections yet": "noch keine Erkennungen",
    # Atlas empty states
    "No birds detected yet.": "Noch keine Vögel erkannt.",
    "The atlas fills up as BirdNET-Pi identifies new species.": "Der Atlas füllt sich, sobald BirdNET-Pi neue Arten erkennt.",
    "No detections in this window.": "Keine Erkennungen in diesem Zeitfenster.",
    "Try a longer time window.": "Versuche ein längeres Zeitfenster.",
    # Recordings modal
    "Loading recordings...": "Aufnahmen werden geladen...",
    "No recordings yet.": "Noch keine Aufnahmen.",
    "Failed to load recordings.": "Aufnahmen konnten nicht geladen werden.",
    # Stats "By Period" labels
    "'NOW'": "'JETZT'",
    "'TODAY'": "'HEUTE'",
    "'WEEK'": "'WOCHE'",
    "'ALL'": "'GESAMT'",
    "'last hour'": "'letzte Stunde'",
    "'today'": "'heute'",
    "'last 7 days'": "'letzte 7 Tage'",
    "'all time'": "'gesamt'",
    # windowLabel() return values (used in collage tooltips, stats captions, atlas)
    "'this hour'": "'diese Stunde'",
    "'past 12h'": "'letzte 12 Std.'",
    "'this week'": "'diese Woche'",
    # Collage tooltip & hover pill: "X call(s) <window>"
    "? 'call' : 'calls'": "? 'Ruf' : 'Rufe'",
    # Stats: most-heard caption (JS builds this at runtime)
    "'most-heard, '": "'meistgehört, '",
    "' most-heard of '": "' meistgehörte von '",
    # Atlas card play/stop button labels
    ">play</span>": ">abspielen</span>",
    ">stop</span>": ">stopp</span>",
    ">no audio</span>": ">kein Audio</span>",
    # Rarity labels (rarityLabel function)
    "return 'common'": "return 'häufig'",
    "return 'regular'": "return 'regelmäßig'",
    "return 'occasional'": "return 'gelegentlich'",
    "return 'rare'": "return 'selten'",
    # Fix the CSS-class comparison after translating 'rare' → 'selten'
    "rar === 'rare'": "rar === 'selten'",
    # Time-ago suffixes in fmtRecTime()
    "+ 's ago'": "+ ' Sek.'",
    "+ 'm ago'": "+ ' Min.'",
    "+ 'h ago'": "+ ' Std.'",
    "+ 'd ago'": "+ ' T.'",
    # Detail modal: "X captured"
    "+ ' captured'": "+ ' aufgenommen'",
    # Wikipedia: link and description in German.
    "https://en.wikipedia.org/wiki/": "https://de.wikipedia.org/wiki/",
    "No description available.": "Keine Beschreibung verfügbar.",
}

# ── wiki.php translations ────────────────────────────────────────────
# Targeted replacement: swap the English-only fetch block for a
# German-first loop with English fallback.

WIKI_PHP_TRANSLATIONS = {
    "$url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' . rawurlencode($sci);\n"
    "$raw = @file_get_contents($url, false, $ctx);\n"
    "if ($raw === false) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}\n"
    "$j = json_decode($raw, true);\n"
    "if (!is_array($j)) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}": "// German first, English fallback.\n"
    "$j = null;\n"
    "foreach (['de', 'en'] as $tryLang) {\n"
    "    $url = 'https://' . $tryLang . '.wikipedia.org/api/rest_v1/page/summary/' . rawurlencode($sci);\n"
    "    $raw = @file_get_contents($url, false, $ctx);\n"
    "    if ($raw === false) continue;\n"
    "    $candidate = json_decode($raw, true);\n"
    "    if (is_array($candidate) && !empty($candidate['extract'])) {\n"
    "        $j = $candidate;\n"
    "        break;\n"
    "    }\n"
    "}\n"
    "if (!is_array($j)) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}",
}


def patch_file(path: Path, translations: dict) -> int:
    """Apply translations to a single file. Returns number of replacements."""
    text = path.read_text(encoding="utf-8")
    count = 0
    for en, de in translations.items():
        if en in text:
            text = text.replace(en, de)
            count += 1
    path.write_text(text, encoding="utf-8")
    return count


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-frontend-dir>", file=sys.stderr)
        sys.exit(1)

    frontend = Path(sys.argv[1])
    if not frontend.is_dir():
        print(f"Error: {frontend} is not a directory", file=sys.stderr)
        sys.exit(1)

    total = 0

    index = frontend / "index.html"
    if index.is_file():
        n = patch_file(index, HTML_TRANSLATIONS)
        print(f"  index.html: {n} replacements")
        total += n

    aptjs = frontend / "apt.js"
    if aptjs.is_file():
        n = patch_file(aptjs, JS_TRANSLATIONS)
        print(f"  apt.js:     {n} replacements")
        total += n

    print(f"Patched frontend to German ({total} total replacements).")


if __name__ == "__main__":
    main()
