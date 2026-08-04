#!/usr/bin/env python3
"""Patch English UI strings in AvianVisitors frontend files to German.

Usage: patch_homepage_de.py <path-to-frontend-dir>

Add new translations by appending entries to the dicts below.
Replacements use str.replace() (literal match, no regex). Keys that no
longer match are reported on stderr - upstream renamed or rewrote the
string and the entry needs updating.
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
    # Return-to-collage pill (admin overlays only)
    "\n  collage\n</a>": "\n  Collage\n</a>",
    "back to collage": "zurück zur Collage",
    # Menu button
    ">menu<": ">Menü<",
    'aria-label="unlock"': 'aria-label="entsperren"',
    'aria-label="close"': 'aria-label="schließen"',
    # Main header
    "Heard Recently": "Kürzlich gehört",
    # View landmarks
    'aria-label="Bird collage"': 'aria-label="Vogelcollage"',
    'aria-label="Stats"': 'aria-label="Statistik"',
    'aria-label="View"': 'aria-label="Ansicht"',
    # Stats date pager + calendar
    'aria-label="Stats date"': 'aria-label="Statistik-Datum"',
    'aria-label="Previous day"': 'aria-label="Vorheriger Tag"',
    'aria-label="Next day"': 'aria-label="Nächster Tag"',
    'aria-label="Choose stats date"': 'aria-label="Statistik-Datum wählen"',
    'aria-label="Previous month"': 'aria-label="Vorheriger Monat"',
    'aria-label="Next month"': 'aria-label="Nächster Monat"',
    'aria-controls="statsCalendar">today<': 'aria-controls="statsCalendar">heute<',
    'id="statsLatestDate">latest heard<': 'id="statsLatestDate">zuletzt gehört<',
    'id="statsTodayDate">today<': 'id="statsTodayDate">heute<',
    # Weekday initials, Sunday-first (So Mo Di Mi Do Fr Sa)
    "<span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span>":
        "<span>S</span><span>M</span><span>D</span><span>M</span><span>D</span><span>F</span><span>S</span>",
    # Chart picker
    'aria-label="chart"': 'aria-label="Diagramm"',
    'aria-label="detection timeline"': 'aria-label="Erkennungs-Zeitleiste"',
    ">timeline</span>": ">Zeitleiste</span>",
    'aria-label="by hour"': 'aria-label="nach Stunde"',
    ">by hour</span>": ">nach Stunde</span>",
    # Stats section headings
    ">By Period<": ">Nach Zeitraum<",
    "detections, grouped by recency": "Erkennungen, nach Aktualität gruppiert",
    ">Top Species<": ">Häufigste Arten<",
    "most-heard, current window": "meistgehört, aktuelles Fenster",
    ">First Detections<": ">Ersterkennungen<",
    "newest additions to the life list": "neueste Einträge in der Gesamtliste",
    # Rhythm panel defaults (apt.js overwrites these per window)
    ">Today's Rhythm<": ">Rhythmus heute<",
    "detections through the day, over last week's average":
        "Erkennungen im Tagesverlauf, über dem Wochenmittel",
    # Atlas sort tooltips & aria-labels
    'aria-label="sort atlas"': 'aria-label="Atlas sortieren"',
    'aria-label="life list"': 'aria-label="Gesamtliste"',
    ">life list</span>": ">Gesamtliste</span>",
    'aria-label="by family"': 'aria-label="nach Familie"',
    ">by family</span>": ">nach Familie</span>",
    'aria-label="alphabetical"': 'aria-label="alphabetisch"',
    "most heard": "meistgehört",
    # Postcard modal
    'aria-label="Drag down or press to close postcard"':
        'aria-label="Nach unten ziehen oder drücken zum Schließen"',
    'aria-label="Bird illustration"': 'aria-label="Vogelillustration"',
    ">generate image<": ">Bild erzeugen<",
    'aria-label="External bird references"': 'aria-label="Externe Vogel-Quellen"',
    'aria-label="Bird history"': 'aria-label="Vogel-Verlauf"',
    "</b> heard</span>": "</b> gehört</span>",
    "</b> first heard</span>": "</b> erstmals gehört</span>",
    'aria-label="selected stamp"': 'aria-label="ausgewählte Marke"',
    "<span>About</span>": "<span>Über</span>",
    "Loading description...": "Beschreibung wird geladen...",
    '<span class="k">Family</span>': '<span class="k">Familie</span>',
    '<span class="k">Genus</span>': '<span class="k">Gattung</span>',
    '<span class="k">Species</span>': '<span class="k">Art</span>',
    '<span class="k">Rarity</span>': '<span class="k">Seltenheit</span>',
    ">Recordings<": ">Aufnahmen<",
    "<span>Last heard</span><span>Confidence</span><span>Date &amp; time</span>":
        "<span>Zuletzt gehört</span><span>Sicherheit</span><span>Datum &amp; Zeit</span>",
    "Loading recordings...": "Aufnahmen werden geladen...",
    # Pose toggle tooltips
    ">perched<": ">sitzend<",
    'aria-label="perched"': 'aria-label="sitzend"',
    ">in flight<": ">im Flug<",
    'aria-label="in flight"': 'aria-label="im Flug"',
    'aria-label="menu"': 'aria-label="Menü"',
    # About modal
    "The birds outside your window": "Die Vögel vor deinem Fenster",
    "explore the birds": "entdecke die Vögel",
    "A tiny microphone identifies every passing bird with Cornell's": "Ein kleines Mikrofon erkennt jeden vorbeifliegenden Vogel mit Cornells",
    "Each species shows up as an illustration in the collage, sized by how often it's been heard.": "Jede Art erscheint als Illustration in der Collage, skaliert nach Häufigkeit der Erkennung.",
    # Lock screen
    "enter password to unlock tools.": "Passwort eingeben zum Entsperren.",
    'placeholder="password"': 'placeholder="Passwort"',
    # Time window picker buttons
    ">7D<": ">7T<",
    ">ALL<": ">ALLE<",
}

# ── apt.js translations ──────────────────────────────────────────────
# Strings rendered by JavaScript at runtime.

JS_TRANSLATIONS = {
    # View titles (header text per tab)
    "'Heard Recently'": "'Kürzlich gehört'",
    "'Avian Atlas'": "'Vogel-Atlas'",
    # Collage / stats empty states
    "'no detections heard in this window'": "'keine Erkennungen in diesem Zeitfenster'",
    'alt="an empty nest"': 'alt="ein leeres Nest"',
    "no detections yet": "noch keine Erkennungen",
    # Atlas empty states
    "No birds detected yet.": "Noch keine Vögel erkannt.",
    "The atlas fills up as BirdNET-Pi identifies new species.": "Der Atlas füllt sich, sobald BirdNET-Pi neue Arten erkennt.",
    # Recordings modal
    "Loading recordings...": "Aufnahmen werden geladen...",
    "? ' recording' : ' recordings'": "? ' Aufnahme' : ' Aufnahmen'",
    "No recordings yet.": "Noch keine Aufnahmen.",
    "Failed to load recordings.": "Aufnahmen konnten nicht geladen werden.",
    "'Play recording'": "'Aufnahme abspielen'",
    "'Pause recording'": "'Aufnahme pausieren'",
    "'Repeat a selected section'": "'Ausschnitt wiederholen'",
    "'Stop repeating selected section'": "'Wiederholung beenden'",
    'aria-label="Repeat a selected section"': 'aria-label="Ausschnitt wiederholen"',
    'aria-label="Repeat section start"': 'aria-label="Ausschnitt-Anfang"',
    'aria-label="Repeat section end"': 'aria-label="Ausschnitt-Ende"',
    'aria-label="Play recording"': 'aria-label="Aufnahme abspielen"',
    'aria-label="Scrub recording spectrogram"': 'aria-label="Im Spektrogramm suchen"',
    "'Recording unavailable'": "'Aufnahme nicht verfügbar'",
    "'recording unavailable'": "'Aufnahme nicht verfügbar'",
    "loading spectrogram...": "Spektrogramm wird geladen...",
    "'rendering spectrogram...'": "'Spektrogramm wird erzeugt...'",
    "'spectrogram unavailable'": "'Spektrogramm nicht verfügbar'",
    # Stats "By Period" labels
    "'NOW'": "'JETZT'",
    "'TODAY'": "'HEUTE'",
    "'HOUR'": "'STUNDE'",
    "'DAY'": "'TAG'",
    "'ALL'": "'GESAMT'",
    "'last hour'": "'letzte Stunde'",
    "'final hour'": "'letzte Stunde des Tages'",
    "'today'": "'heute'",
    "'that day'": "'an dem Tag'",
    "'selected date'": "'gewähltes Datum'",
    "'last 7 days'": "'letzte 7 Tage'",
    "'through this date'": "'bis zu diesem Datum'",
    "'all time'": "'gesamt'",
    ">all time<": ">gesamt<",
    # Stats side-panel captions
    "'detections through '": "'Erkennungen bis '",
    "'detections, grouped by recency'": "'Erkennungen, nach Aktualität gruppiert'",
    "'life list as of '": "'Gesamtliste am '",
    "'newest additions to the life list'": "'neueste Einträge in der Gesamtliste'",
    "'most-heard, '": "'meistgehört, '",
    "' most-heard of '": "' meistgehörte von '",
    # windowLabel() / statsWindowLabel() return values
    "'this hour'": "'diese Stunde'",
    "'past 12h'": "'letzte 12 Std.'",
    "'this week'": "'diese Woche'",
    "'selected hour'": "'gewählte Stunde'",
    "'final 12h'": "'letzte 12 Std. des Tages'",
    "'selected day'": "'gewählter Tag'",
    "'selected 7 days'": "'gewählte 7 Tage'",
    "'through selected day'": "'bis zum gewählten Tag'",
    # Rhythm panel titles + captions
    '"Week\'s Rhythm"': "'Rhythmus der Woche'",
    '"Hour\'s Rhythm"': "'Rhythmus der Stunde'",
    '"Today\'s Rhythm"': "'Rhythmus heute'",
    '"Day\'s Rhythm"': "'Rhythmus des Tages'",
    "'average day in this 7-day window, over the previous 7 days'":
        "'Durchschnittstag dieser 7 Tage, über den vorherigen 7 Tagen'",
    "'detections through the selected hour, over the prior week\\'s average'":
        "'Erkennungen in der gewählten Stunde, über dem Wochenmittel'",
    "'detections on the selected date, over the prior week\\'s average'":
        "'Erkennungen am gewählten Datum, über dem Wochenmittel'",
    "'detections through the current 12-hour window, over last week\\'s average'":
        "'Erkennungen der letzten 12 Std., über dem Wochenmittel'",
    "'detections through the day, over last week\\'s average'":
        "'Erkennungen im Tagesverlauf, über dem Wochenmittel'",
    # Stats date pager
    "'Choose stats date, '": "'Statistik-Datum wählen, '",
    # Hourly ledger
    '<th class="heatmap-total">total</th>': '<th class="heatmap-total">Gesamt</th>',
    "'Show less'": "'Weniger'",
    "'Show more'": "'Mehr'",
    # Collage tooltip & hover pill: "X call(s) <window>"
    "? 'call' : 'calls'": "? 'Ruf' : 'Rufe'",
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
    # Time-ago suffixes in fmtRecTime() and the First Detections list
    "+ 's ago'": "+ ' Sek.'",
    "+ 'm ago'": "+ ' Min.'",
    "+ 'h ago'": "+ ' Std.'",
    "+ 'd ago'": "+ ' T.'",
    "(past ? 'd prior' : 'd ago')": "(past ? ' T. davor' : ' T.')",
    "'Loading description...'": "'Beschreibung wird geladen...'",
    "'No description available.'": "'Keine Beschreibung verfügbar.'",
    # Generated illustration placeholders / button states
    "'Nest with eggs, bird illustration temporarily unavailable for '":
        "'Nest mit Eiern, Vogelillustration vorübergehend nicht verfügbar für '",
    "'Nest with eggs, bird image not generated yet for '":
        "'Nest mit Eiern, Vogelbild noch nicht erzeugt für '",
    "'generate image'": "'Bild erzeugen'",
    "'generating...'": "'wird erzeugt...'",
    "'finishing...'": "'fertigstellen...'",
    "'starting...'": "'startet...'",
    "'generated'": "'erzeugt'",
    "'failed, try again'": "'fehlgeschlagen, nochmal'",
    # Wikipedia link: German article, but accept the en URL wiki.php falls
    # back to (must run before the en → de host swap below).
    "/^https:\\/\\/en\\.wikipedia\\.org\\/wiki\\//":
        "/^https:\\/\\/(?:de|en)\\.wikipedia\\.org\\/wiki\\//",
    "https://en.wikipedia.org/wiki/": "https://de.wikipedia.org/wiki/",
}

# ── wiki.php translations ────────────────────────────────────────────
# Fetch the German article first and fall back to English. $GLOBALS
# ['wikiLang'] carries the language that answered into the follow-up
# requests (expanded lead, Description section, source URL).

WIKI_PHP_TRANSLATIONS = {
    "$url = 'https://en.wikipedia.org/w/api.php?' . http_build_query([\n"
    "    'action'        => 'query',\n"
    "    'format'        => 'json',\n"
    "    'formatversion' => '2',\n"
    "    'redirects'     => '1',\n"
    "    'prop'          => 'extracts|pageimages',\n"
    "    'exintro'       => '1',\n"
    "    'explaintext'   => '1',\n"
    "    'piprop'        => 'thumbnail',\n"
    "    'pithumbsize'   => '640',\n"
    "    'titles'        => $sci,\n"
    "], '', '&', PHP_QUERY_RFC3986);\n"
    "$raw = @file_get_contents($url, false, $ctx);\n"
    "if ($raw === false) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}\n"
    "$j = json_decode($raw, true);\n"
    "if (!is_array($j)) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}\n"
    "\n"
    "$page = $j['query']['pages'][0] ?? null;\n"
    "if (!is_array($page)) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}":
    "// German Wikipedia first, English fallback when de has no article.\n"
    "$page = null;\n"
    "foreach (['de', 'en'] as $tryLang) {\n"
    "    $GLOBALS['wikiLang'] = $tryLang;\n"
    "    $url = 'https://' . $tryLang . '.wikipedia.org/w/api.php?' . http_build_query([\n"
    "        'action'        => 'query',\n"
    "        'format'        => 'json',\n"
    "        'formatversion' => '2',\n"
    "        'redirects'     => '1',\n"
    "        'prop'          => 'extracts|pageimages',\n"
    "        'exintro'       => '1',\n"
    "        'explaintext'   => '1',\n"
    "        'piprop'        => 'thumbnail',\n"
    "        'pithumbsize'   => '640',\n"
    "        'titles'        => $sci,\n"
    "    ], '', '&', PHP_QUERY_RFC3986);\n"
    "    $raw = @file_get_contents($url, false, $ctx);\n"
    "    if ($raw === false) continue;\n"
    "    $j = json_decode($raw, true);\n"
    "    $candidate = is_array($j) ? ($j['query']['pages'][0] ?? null) : null;\n"
    "    if (is_array($candidate) && !empty($candidate['extract'])) {\n"
    "        $page = $candidate;\n"
    "        break;\n"
    "    }\n"
    "}\n"
    "if (!is_array($page)) {\n"
    "    echo json_encode(['extract' => null, 'thumbnail' => null]);\n"
    "    exit;\n"
    "}",
    # Follow-up requests use whichever language answered.
    "'https://en.wikipedia.org/w/api.php?'":
        "'https://' . $GLOBALS['wikiLang'] . '.wikipedia.org/w/api.php?'",
    "'https://en.wikipedia.org/wiki/'":
        "'https://' . $GLOBALS['wikiLang'] . '.wikipedia.org/wiki/'",
    # German articles name the appearance section differently.
    "$wanted = ['description', 'identification', 'appearance'];":
        "$wanted = ['beschreibung', 'merkmale', 'aussehen', 'kennzeichen', "
        "'description', 'identification', 'appearance'];",
}


def patch_file(path: Path, translations: dict) -> int:
    """Apply translations to a single file. Returns number of replacements."""
    text = path.read_text(encoding="utf-8")
    count = 0
    for en, de in translations.items():
        if en in text:
            text = text.replace(en, de)
            count += 1
        else:
            # Upstream renamed or rewrote this string: the entry is dead and
            # the UI keeps showing English until it is updated.
            print(f"    ! no match in {path.name}: {en[:70]!r}", file=sys.stderr)
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

    # Patch wiki.php fetch block: German-first with English fallback.
    wiki_php = frontend.parent / "api" / "wiki.php"
    if wiki_php.is_file():
        n = patch_file(wiki_php, WIKI_PHP_TRANSLATIONS)
        print(f"  wiki.php:   {n} replacements")
        total += n

    print(f"Patched frontend to German ({total} total replacements).")


if __name__ == "__main__":
    main()
