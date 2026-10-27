#!/usr/bin/env python3
"""Sammelt Kennzahlen des Kurs-Repos für das Dashboard und schreibt data/dashboard.json.
Aufruf: python3 dashboard_daten.py [Pfad zum Kurs-Repo]"""
import json, re, subprocess, sys, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/s.munzert/Documents/github/hertie-ai-certificate/modul-2-2026")
OUT = Path(__file__).parent / "data" / "dashboard.json"

SESSIONS = [  # n, Tag, Zeit (h), Titel, Ordner, Deck-Stamm, Materialordner
    (1, 1, "11–13", "Data Science – Ein Überblick", "d1s1-ueberblick", "d1s1-ueberblick", []),
    (2, 1, "14–16", "Wo kommen die Daten her?", "d1s2-datenherkunft", "d1s2-datenherkunft", ["d1s2-datenherkunft/materialien"]),
    (3, 1, "16–18", "Mit Daten umgehen und zur Verfügung stellen", "d1s3-datengewinnung", "d1s3-datengewinnung", ["d1s3-datengewinnung/materials"]),
    (4, 1, "18–19", "Praxis-Session I: Web Scraping und APIs", "d1s4-web-scraping", "d1s4-web-scraping", ["d1s4-web-scraping/case-study-scraping", "d1s4-web-scraping/case-study-api"]),
    (5, 2, "9–11", "Möglichkeiten und Probleme mit Big Data", "d2s5-big-data-probleme", "d2s5-big-data-probleme", []),
    (6, 2, "11–13", "Informierter Konsum von Daten und Statistiken", "d2s6-statistikverstehen", "d2s6-statistikverstehen", ["d2s6-statistikverstehen/materialien"]),
    (7, 2, "14–16", "Praxis-Session II: Daten weiterverarbeiten und strukturieren", "d2s7-datenverarbeitung", None, ["d2s7-datenverarbeitung/praxis-ocr-llm", "d2s7-datenverarbeitung/uebung-klassifikation"]),
    (8, 2, "16–18", "Kommunikation von und mit Daten", "d2s8-kommunikation", "d2s8-kommunikation", []),
    (9, 3, "9–11", "Wie gewinnt man Data Scientists nachhaltig für Behörden?", "d3s9-rekrutierung", "d3s9-rekrutierung", ["übungsmaterialien/ausschreibungen-service-bund-de"]),
    (10, 3, "11–13", "Gastvortrag: Open Data Governance", None, None, []),
    (11, 3, "14–16", "Wrap-up und Ausblick", "d3s11-wrapup", "d3s11-wrapup", []),
]
PRAXIS = {4, 7}

def deck_metrics(rmd: Path):
    s = rmd.read_text(encoding="utf-8")
    body = s.split("---", 2)[2]
    chunks = re.findall(r"```\{r[^}]*\}.*?```", body, flags=re.S)
    nochunk = re.sub(r"```.*?```", "", body, flags=re.S)
    text = re.sub(r"<[^>]+>", "", nochunk)
    text = re.sub(r"\(https?://[^\)]*\)", "", text)
    text = re.sub(r"^\s*(class:|name:|\.pull|\]|\.font|\.content|layout:).*$", "", text, flags=re.M)
    return {
        "abschnitte": len(re.findall(r"^class:.*inverse", body, flags=re.M)),
        "uebungen": len(re.findall(r"^class:.*exercise", body, flags=re.M)),
        "bilder": len(re.findall(r"<img |!\[", body)),
        "links": len(set(re.findall(r"https?://[^\s\)\]\"'>]+", body))),
        "videos": len(re.findall(r"\.mp4|<video|youtube\.com|youtu\.be", body)),
        "woerter": len(re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß'\-]+", text)),
    }

def pdf_pages(paths):
    r = subprocess.run(["/Library/Frameworks/R.framework/Resources/bin/Rscript", "-e",
        "for (p in commandArgs(TRUE)) cat(pdftools::pdf_info(p)$pages, '\\n')", *[str(p) for p in paths]],
        capture_output=True, text=True)
    return [int(x) for x in r.stdout.split()]

def material_metrics(folders):
    files, r_lines, data_files, docs = 0, 0, 0, 0
    for f in folders:
        for p in (REPO / f).rglob("*"):
            if not p.is_file() or ".DS_Store" in p.name or "/archiv/" in str(p) or "_files/" in str(p) or "_cache/" in str(p):
                continue
            files += 1
            if p.suffix == ".R":
                r_lines += sum(1 for line in p.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())
            if p.suffix.lower() in (".csv", ".json", ".xml", ".txt", ".png", ".jpg", ".pdf") and "daten" in str(p).lower() or p.suffix.lower() == ".csv":
                data_files += 1
            if p.suffix == ".Rmd":
                docs += 1
    return {"dateien": files, "r_zeilen": r_lines, "datendateien": data_files, "fallstudien": docs}

decks = [(s, REPO / s[4] / f"{s[5]}.Rmd", REPO / s[4] / f"{s[5]}.pdf") for s in SESSIONS if s[5]]
pages = dict(zip([d[0][0] for d in decks], pdf_pages([d[2] for d in decks])))

sessions = []
for s in SESSIONS:
    n, tag, zeit, titel, ordner, stem, mats = s
    h0, h1 = [int(x) for x in zeit.replace("–", "-").split("-")]
    e = {"n": n, "tag": tag, "zeit": zeit + " Uhr", "start": h0, "ende": h1, "dauer": h1 - h0, "titel": titel,
         "praxis": n in PRAXIS, "gast": n == 10, "folien": 0, "abschnitte": 0, "uebungen": 0, "bilder": 0,
         "links": 0, "videos": 0, "woerter": 0, "dateien": 0, "r_zeilen": 0, "datendateien": 0, "fallstudien": 0}
    if stem:
        e.update(deck_metrics(REPO / ordner / f"{stem}.Rmd")); e["folien"] = pages[n]
    e.update(material_metrics(mats))
    e["woerter_je_folie"] = round(e["woerter"] / e["folien"]) if e["folien"] else None
    e["folien_je_stunde"] = round(e["folien"] / e["dauer"]) if e["folien"] else None
    sessions.append(e)

# Literatur je Session aus build.py
import importlib.util
spec = importlib.util.spec_from_file_location("build", Path(__file__).parent / "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
for e in sessions:
    src = next(x for x in b.SESSIONS if x["n"] == e["n"])
    e["literatur"] = len(src["kern"]) + len(src["hoeren"]) + len(src["lesen"])
    e["kern"] = len(src["kern"]); e["hoeren"] = len(src["hoeren"]); e["lesen"] = len(src["lesen"])

# Repo-Kennzahlen
pics = [p for p in (REPO / "pics").iterdir() if p.is_file() and p.name != ".DS_Store"]
pics_mb = round(sum(p.stat().st_size for p in pics) / 1e6)
commits = int(subprocess.run(["git", "-C", str(REPO), "rev-list", "--count", "HEAD"], capture_output=True, text=True).stdout.strip() or 0)

# Teilnehmende: nur Zahl und Zahl der Behörden (keine Namen)
teiln, behoerden = 26, None
try:
    z = zipfile.ZipFile("/Users/s.munzert/Dropbox/uni/teaching/executive-education/2026-ai-zertifikat/teilnehmer-profile.xlsx")
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    ss = ["".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns)]
    inst = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).find("m:sheetData", ns).findall("m:row", ns):
        c = r.findall("m:c", ns)[0]; v = c.find("m:v", ns)
        inst.append(ss[int(v.text)] if c.get("t") == "s" else v.text)
    teiln, behoerden = len(inst), len(set(inst))
except Exception as ex:
    print("Teilnehmerliste nicht gelesen:", ex)

daten = {"stand": __import__("datetime").date.today().isoformat(), "sessions": sessions,
         "repo": {"pics": len(pics), "pics_mb": pics_mb, "commits": commits},
         "teilnehmende": teiln, "behoerden": behoerden}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
tot = {k: sum(e[k] for e in sessions) for k in ("folien", "woerter", "bilder", "links", "uebungen", "literatur", "r_zeilen", "dateien")}
print("geschrieben:", OUT); print(tot); print("Teilnehmende", teiln, "Behörden", behoerden)
