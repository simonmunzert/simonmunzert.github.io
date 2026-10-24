#!/usr/bin/env python3
"""Generator für die Kurswebseite „Der Daten-Lifecycle“ (Modul 2, KI-Zertifikat, Hertie School).

Erzeugt statische HTML-Seiten aus den Daten unten:
  index.html, sessions.html, sessions/s01.html … s11.html, leistungen.html, ressourcen.html

Aufruf:  python3 build.py
Slides und Code-Materialien bleiben im Kurs-Repo und werden über raw.githack.com verlinkt.
"""
from pathlib import Path
import html

ROOT = Path(__file__).parent
REPO = "hertie-ai-certificate/modul-2-2026"
GH = f"https://github.com/{REPO}"
GH_TREE = f"{GH}/tree/main"
GH_BLOB = f"{GH}/blob/main"
GITHACK = f"https://raw.githack.com/{REPO}/main"
SITE_TITLE = "Der Daten-Lifecycle"
SITE_SUB = "Modul 2 · Zertifikatsprogramm „KI und Data Science für die öffentliche Verwaltung“"

# ---------------------------------------------------------------------------
# Daten
# ---------------------------------------------------------------------------

DAYS = {
    1: {"label": "Tag 1", "date": "Montag, 26. Oktober 2026", "theme": "Der Daten-Lifecycle und: Woher kommen Daten?"},
    2: {"label": "Tag 2", "date": "Dienstag, 27. Oktober 2026", "theme": "Big Data, Good Data? Die kritische Nutzung von Daten"},
    3: {"label": "Tag 3", "date": "Mittwoch, 28. Oktober 2026", "theme": "Auf dem Weg zur datenbewussten Organisation"},
}

def deck(folder, stem, pdf=True):
    d = {"html": f"{GITHACK}/{folder}/{stem}.html", "rmd": f"{GITHACK}/{folder}/{stem}.Rmd",
         "rmd_gh": f"{GH_BLOB}/{folder}/{stem}.Rmd", "folder": f"{GH_TREE}/{folder}"}
    if pdf:
        d["pdf"] = f"{GITHACK}/{folder}/{stem}.pdf"
    return d

def lit(text, url=None, note=None):
    return {"text": text, "url": url, "note": note}

SESSIONS = [
    {
        "n": 1, "day": 1, "time": "11–13 Uhr",
        "title": "Data Science – Ein Überblick",
        "short": "Was Data Science ist, was sie für die Verwaltung leisten kann und welche Rolle Daten dabei spielen.",
        "content": "In der ersten Session starten wir mit einem Überblick über Data Science und der Kernrolle von Daten für die Data-Science-Pipeline. Wir diskutieren, welche Beiträge die (Daten-)Wissenschaft zur öffentlichen Politik leisten kann und warum es wichtig ist, Rohdaten und verarbeitete Daten kritisch zu hinterfragen. An konkreten Anwendungsfeldern von Data Science in der Verwaltung machen wir uns außerdem ein Bild davon, was Data Science leisten kann – und was nicht. Abschließend definieren wir die allgemeinen Lernziele für dieses Modul.",
        "deck": deck("d1s1-ueberblick", "d1s1-ueberblick"),
        "materials": [],
        "kern": [lit("Keim, Daniel & Kai-Uwe Sattler (2020): Von Daten zu KI. Intelligentes Datenmanagement als Basis für Data Science und den Einsatz Lernender Systeme. White Paper aus der Plattform Lernende Systeme, München.")],
        "hoeren": [lit("Harvard Data Science Review Podcast, Episode 32: „What is Data Science?“", "https://hdsr.mitpress.mit.edu/podcast")],
        "lesen": [
            lit("Gesellschaft für Informatik (GI-Arbeitskreis Data Science/Data Literacy) unter Mitwirkung der Plattform Lernende Systeme: Data Science: Lern- und Ausbildungsinhalte.", "https://www.acatech.de/publikation/data-science-lern-und-ausbildungsinhalte/"),
            lit("Höchtl, J., Parycek, P., & Schöllhammer, R. (2016). Big data in the policy cycle: Policy decision making in the digital era. Journal of Organizational Computing and Electronic Commerce, 26(1–2), 147–169."),
        ],
    },
    {
        "n": 2, "day": 1, "time": "14–16 Uhr",
        "title": "Wo kommen die Daten her?",
        "short": "Datentypen, prozessproduzierte und aktiv erhobene Daten, Diskussion der Daten-Poster.",
        "content": "In dieser Session verschaffen wir uns zunächst einen Überblick über die wichtigsten Datentypen: strukturierte Daten – abgelegt in konventionellen Tabellen und Datenbanken – ebenso wie unstrukturierte Datentypen wie Text-, Bild- und Geodaten. Anschließend fragen wir, woher diese Daten eigentlich kommen, und unterscheiden dabei prozessproduzierte Daten einerseits und aktiv erhobene Daten andererseits. Zum Abschluss wenden wir uns Euren eigenen Daten zu: Anhand der vorbereiteten Daten-Poster diskutieren wir gemeinsam, welche Datenbestände in Euren Behörden entstehen und wie sie sich einordnen lassen.",
        "deck": deck("d1s2-datenherkunft", "d1s2-datenherkunft", pdf=False),
        "materials": [
            {"title": "Wikipedia-Aufrufe „ELSTER“", "desc": "R-Skript, das die Seitenaufrufe des Wikipedia-Artikels über die Wikimedia-API lädt und als Zeitreihe plottet (ggplot2), samt Daten als CSV.",
             "links": [("R-Skript", f"{GH_BLOB}/d1s2-datenherkunft/materialien/wiki-elster.R"), ("Daten (CSV)", f"{GH_BLOB}/d1s2-datenherkunft/materialien/wiki-elster-pageviews.csv"), ("Ordner", f"{GH_TREE}/d1s2-datenherkunft/materialien")]},
        ],
        "kern": [lit("Open Data Informationsstelle Berlin (2023). Open Data in der Berliner Verwaltung.")],
        "hoeren": [lit("ARD, Der KI-Podcast: „Erstickt die KI an ihren eigenen Daten?“", "https://www.ardaudiothek.de/episode/der-ki-podcast/erstickt-die-ki-an-ihren-eigenen-daten/ard/13653569/")],
        "lesen": [
            lit("Jean, N. et al. (2016). Combining satellite imagery and machine learning to predict poverty. Science, 353(6301), 790–794."),
            lit("Kitchin, R. (2014). The Data Revolution: Big Data, Open Data, Data Infrastructures and Their Consequences. Sage.", note="Kapitel 1–2 als Überblick über Datentypen und Dateninfrastrukturen."),
            lit("Gebru, T. et al. (2021). Datasheets for Datasets. Communications of the ACM, 64(12), 86–92.", note="Vorschlag für „Beipackzettel“ zu Datensätzen – gut anschlussfähig an die Daten-Poster."),
        ],
    },
    {
        "n": 3, "day": 1, "time": "16–18 Uhr",
        "title": "Mit Daten umgehen und zur Verfügung stellen",
        "short": "Gute und schlechte Tabellen, XML und JSON, relationale Datenbanken, XÖV-Standards wie XFall.",
        "content": "In dieser Session geht es um die konkrete Gestalt von Daten und darum, wie sie gewonnen, ausgetauscht und bereitgestellt werden. Wir beginnen bei der wohl verbreitetsten Form der Datenhaltung in der Verwaltung, dem Spreadsheet, und besprechen, was gute von schlechten Tabellen unterscheidet. Anschließend lernen wir mit XML und JSON die gängigen Austauschformate für strukturierte Daten kennen, werfen einen Blick auf relationale Datenbanken und auf die XÖV-Standards der öffentlichen Verwaltung (etwa XFall). Abschließend diskutieren wir, was es heißt, Daten so zur Verfügung zu stellen, dass andere sie tatsächlich nachnutzen können.",
        "deck": deck("d1s3-datengewinnung", "d1s3-datengewinnung", pdf=False),
        "materials": [
            {"title": "Übung: Eine XFall-Nachricht auseinandernehmen", "desc": "Zwei kommentierte, schema-valide XFall-Beispielnachrichten (Gewerbeanmeldung und Container) sowie die offiziellen Spezifikationen und XML-Schemata aus dem XRepository.",
             "links": [("Ordner mit README", f"{GH_TREE}/d1s3-datengewinnung/materials"), ("Beispiel Gewerbeanmeldung (XML)", f"{GH_BLOB}/d1s3-datengewinnung/materials/beispiel-gewerbeanmeldung_xfall-daten-4.0.0.xml"), ("Beispiel Container (XML)", f"{GH_BLOB}/d1s3-datengewinnung/materials/beispiel-container_xfall-container-3.0.0.xml")]},
        ],
        "kern": [lit("Broman, K. W., & Woo, K. H. (2018). Data organization in spreadsheets. The American Statistician, 72(1), 2–10.")],
        "hoeren": [
            lit("re|Staat digital – Der ÖFIT-Podcast, Folge 33: „Datenbezogene Standards“ (mit Gabriele Goldacker und Mike Weber)", "https://www.oeffentliche-it.de/oefit-podcast/datenbezogene-standards/"),
            lit("eGovernment Podcast, Torsten Frenzel", "https://egovernment-podcast.com/", note="Deutschsprachiger Langläufer zu Verwaltungsdigitalisierung, Datenstandards, Open Data und Smart City."),
        ],
        "lesen": [
            lit("Koordinierungsstelle für IT-Standards (KoSIT): XÖV-Standards der öffentlichen Verwaltung (u.a. XFall).", "https://www.xoev.de/"),
            lit("Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. Scientific Data, 3, 160018.", note="FAIR-Prinzipien: findable, accessible, interoperable, reusable."),
            lit("Ziemann, M., Eren, Y., & El-Osta, A. (2016). Gene name errors are widespread in the scientific literature. Genome Biology, 17, 177.", note="Kurzes, sehr plakatives Lehrbeispiel für Spreadsheet-Fallstricke."),
        ],
    },
    {
        "n": 4, "day": 1, "time": "18–19 Uhr",
        "title": "Praxis-Session I: Web Scraping und APIs",
        "short": "Daten automatisiert aus Webseiten extrahieren und über Schnittstellen abrufen, mit zwei Fallstudien aus der Verwaltung.",
        "content": "In dieser Praxis-Session lernen wir, mit externen Tools und Datenquellen zu interagieren. Erst beschäftigen wir uns mit der automatisierten Datensammlung aus dem Web: Wir sehen uns an, wie HTML-Strukturen genutzt werden können, um gezielt Daten von Webseiten zu extrahieren. Anschließend lernen wir, wie APIs als Schnittstellen für den Zugriff auf strukturierte Datenquellen und externe Tools dienen, und schauen uns an, wo APIs in der deutschen öffentlichen Verwaltung bereits im Einsatz sind. Zwei Fallstudien zeigen den Datenabruf an realen Szenarien: eine Karte der Bundesbehörden aus einer Wikipedia-Liste und der Zugriff auf Verwaltungs-APIs wie Pegelonline, XRepository und GovData.",
        "deck": deck("d1s4-web-scraping", "d1s4-web-scraping"),
        "materials": [
            {"title": "Fallstudie Web Scraping: Wo sitzen die Bundesbehörden?", "desc": "Schritt für Schritt von der Wikipedia-Liste über den Browser-Inspector und rvest bis zur geocodierten Karte der Bundesbehörden.",
             "links": [("Fallstudie (HTML)", f"{GITHACK}/d1s4-web-scraping/case-study-scraping/fallstudie-scraping.html"), ("R-Skript", f"{GH_BLOB}/d1s4-web-scraping/case-study-scraping/behoerden-karte.R"), ("Rmd-Quelle", f"{GH_BLOB}/d1s4-web-scraping/case-study-scraping/fallstudie-scraping.Rmd"), ("Ordner", f"{GH_TREE}/d1s4-web-scraping/case-study-scraping")]},
            {"title": "Fallstudie APIs: Verwaltungsdaten über Schnittstellen", "desc": "Pegelstände von Pegelonline, Codelisten aus dem XRepository und Datensätze aus GovData – mit httr2 und jsonlite abgerufen und ausgewertet.",
             "links": [("Fallstudie (HTML)", f"{GITHACK}/d1s4-web-scraping/case-study-api/fallstudie-api.html"), ("R-Skript", f"{GH_BLOB}/d1s4-web-scraping/case-study-api/behoerden-apis.R"), ("Rmd-Quelle", f"{GH_BLOB}/d1s4-web-scraping/case-study-api/fallstudie-api.Rmd"), ("Ordner", f"{GH_TREE}/d1s4-web-scraping/case-study-api")]},
        ],
        "kern": [lit("Kühnemann, H. (2021). Anwendungen des Web Scraping in der amtlichen Statistik. AStA Wirtschafts- und Sozialstatistisches Archiv, 15(1), 5–25.")],
        "hoeren": [lit("Coding Buddies, Episode „Was sind eigentlich APIs?“")],
        "lesen": [lit("Munzert, S., Rubba, C., Meißner, P., & Nyhuis, D. (2014). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.")],
    },
    {
        "n": 5, "day": 2, "time": "9–11 Uhr",
        "title": "Möglichkeiten und Probleme mit Big Data",
        "short": "KI-Technologien und ihre Datengrundlage, das Big-Data-Paradoxon, Repräsentativität und Messung.",
        "content": "Wir starten in den zweiten Tag mit einem Überblick über KI-Technologien und ihre Grundlage – große Datenmengen. Im Fokus steht das sogenannte „Big-Data-Paradoxon“ – die Idee, dass mehr Daten nicht zwangsläufig zu besseren Erkenntnissen führen. Dazu vertiefen wir zwei Konzepte, die maßgeblich über die Qualität von Daten entscheiden: Repräsentativität und Messung. Wir beleuchten, wie Verzerrungen, Datenqualität und Umfang die Zuverlässigkeit von Big Data beeinflussen und damit politisches und administratives Handeln beeinträchtigen können.",
        "deck": deck("d2s5-big-data-probleme", "d2s5-big-data-probleme"),
        "materials": [],
        "kern": [
            lit("Salganik, M. J. (2019). Bit by Bit: Social Research in the Digital Age. Princeton University Press.", "https://www.bitbybitbook.com/", note="Kapitel 2: Observing Behavior."),
            lit("Bergstrom, C. T., & West, J. D. (2021). Calling Bullshit: The Art of Skepticism in a Data-Driven World. Random House.", "https://callingbullshit.org/", note="Kapitel 6: Selection Bias."),
        ],
        "hoeren": [lit("Choiceology: „Survey Says“, mit W. Joseph Campbell und Emily Oster (Mai 2023)")],
        "lesen": [
            lit("Narayanan, A., & Kapoor, S. (2024). AI Snake Oil: What Artificial Intelligence Can Do, What It Can’t, and How to Tell the Difference. Princeton University Press."),
            lit("Meng, X.-L. (2018). Statistical paradises and paradoxes in big data (I): Law of large populations, big data paradox, and the 2016 US presidential election. Annals of Applied Statistics, 12(2), 685–726.", note="Die Originalquelle zum Big-Data-Paradoxon."),
            lit("Bradley, V. C. et al. (2021). Unrepresentative big surveys significantly overestimated US vaccine uptake. Nature, 600(7890), 695–700.", note="Sehr zugängliches Anwendungsbeispiel: Millionen Befragte, dennoch 14–17 Prozentpunkte daneben."),
            lit("Lazer, D., Kennedy, R., King, G., & Vespignani, A. (2014). The parable of Google Flu: traps in big data analysis. Science, 343(6176), 1203–1205."),
        ],
    },
    {
        "n": 6, "day": 2, "time": "11–13 Uhr",
        "title": "Informierter Konsum von Daten und Statistiken",
        "short": "Deskriptive Statistiken lesen, mit Wahrscheinlichkeiten und Unsicherheit umgehen, Effekte und Signifikanz beurteilen.",
        "content": "In dieser Session verlassen wir kurz das Feld von KI und wenden uns dem klassischen Geschäft mit Daten und Statistik zu. Viele Fallstricke im Umgang mit Data-Science- und KI-Anwendungen sind nicht neu, sondern wurzeln im kritischen Umgang mit Daten und Statistik. Wir vertiefen unser Verständnis dafür, wie man (a) deskriptive Statistiken interpretiert, (b) mit Wahrscheinlichkeiten und Unsicherheitsmaßen umgeht und (c) statistische Effekte und Signifikanz beurteilt.",
        "deck": deck("d2s6-statistikverstehen", "d2s6-statistikverstehen"),
        "materials": [
            {"title": "KI-Benchmarks: GPQA Diamond", "desc": "R-Skript und Daten (Epoch AI, CC BY 4.0) für die Grafik zur Entwicklung der Modellleistung auf dem GPQA-Diamond-Benchmark.",
             "links": [("R-Skript", f"{GH_BLOB}/d2s6-statistikverstehen/materialien/benchmark-gpqa.R"), ("Ordner", f"{GH_TREE}/d2s6-statistikverstehen/materialien")]},
        ],
        "kern": [lit("Gade, C. (2023). When is it justified to claim that a practice or policy is evidence-based? Reflections on evidence and preferences. Evidence & Policy, 1–10.")],
        "hoeren": [lit("More or Less: Behind the Stats, Tim Harford, BBC Radio 4", "https://www.bbc.co.uk/programmes/b006qshd")],
        "lesen": [
            lit("Spiegelhalter, D. (2020). The Art of Statistics: Learning from Data. Penguin.", note="Auch auf Deutsch erhältlich: Die Kunst der Statistik. Was uns Daten wirklich sagen und wie wir dies im Alltag nutzen können. Redline."),
            lit("Gigerenzer, G., Gaissmaier, W., Kurz-Milcke, E., Schwartz, L. M., & Woloshin, S. (2007). Helping doctors and patients make sense of health statistics. Psychological Science in the Public Interest, 8(2), 53–96."),
            lit("Rosling, H., Rosling, O., & Rosling Rönnlund, A. (2018). Factfulness: Wie wir lernen, die Welt so zu sehen, wie sie wirklich ist. Ullstein."),
        ],
    },
    {
        "n": 7, "day": 2, "time": "14–16 Uhr",
        "title": "Praxis-Session II: Daten weiterverarbeiten und strukturieren",
        "short": "Von Scans zu Tabellen: OCR, Sprachmodelle für Bereinigung und Klassifikation, saubere Ablage in CSVs.",
        "content": "In der zweiten Praxis-Session bauen wir eine kleine Verarbeitungspipeline für einen typischen Verwaltungsfall: Eingescannte Dokumente (Briefe, Formulare, Notizen) sollen in auswertbare Tabellen überführt werden. Wir lesen die Scans mit OCR ein, lassen ein Sprachmodell den fehlerhaften Text bereinigen und die zentralen Felder extrahieren, klassifizieren die Dokumente nach Kategorie und Dringlichkeit und legen alles sauber in CSV-Dateien ab. Die Pipeline läuft wahlweise mit einem lokalen Open-Source-Modell (Ollama) oder einem Cloud-Anbieter. Am Ende prüfen wir die Ergebnisse gegen einen Goldstandard und diskutieren, wo solche Pipelines verlässlich sind und wo nicht.",
        "deck": deck("d2s7-datenverarbeitung", "d2s7-datenverarbeitung"),
        "materials": [
            {"title": "Praxis-Pipeline: OCR und Sprachmodelle", "desc": "Dokumentation mit Erläuterungen, das vollständige R-Skript, acht Beispielscans mit Goldstandard sowie die Zwischen- und Endergebnisse jedes Schritts. Das README erklärt Installation (tesseract, ellmer, Ollama) und Alternativen mit API-Schlüssel.",
             "links": [("Dokumentation (HTML)", f"{GITHACK}/d2s7-datenverarbeitung/praxis-ocr-llm/praxis-2-ocr-llm.html"), ("R-Skript", f"{GH_BLOB}/d2s7-datenverarbeitung/praxis-ocr-llm/praxis-2-ocr-llm.R"), ("README", f"{GH_BLOB}/d2s7-datenverarbeitung/praxis-ocr-llm/README.md"), ("Ordner mit Daten", f"{GH_TREE}/d2s7-datenverarbeitung/praxis-ocr-llm")]},
        ],
        "kern": [],
        "hoeren": [],
        "lesen": [
            lit("Dokumentation des R-Pakets ellmer (Schnittstelle zu Sprachmodellen aus R heraus).", "https://ellmer.tidyverse.org/"),
            lit("Dokumentation des R-Pakets tesseract (OCR).", "https://docs.ropensci.org/tesseract/"),
        ],
    },
    {
        "n": 8, "day": 2, "time": "16–18 Uhr",
        "title": "Kommunikation von und mit Daten",
        "short": "Statistische und visuelle Kommunikation, gute Grafiken, Dashboards in der Verwaltung.",
        "content": "Wie kommuniziert man Daten und datenbasierte Entscheidungen? Wir widmen uns Kernstrategien statistischer und visueller Kommunikation. Ziel ist es, komplexe Datenerkenntnisse klar und präzise vermitteln zu können, sodass sie für unterschiedliche Zielgruppen verständlich und handlungsrelevant werden. Ein eigener Abschnitt widmet sich Dashboards in der Verwaltung: Beispiele aus der Praxis, Fragen der Governance und der Umsetzung sowie die Werkzeuge, mit denen sich Dashboards heute bauen lassen.",
        "deck": deck("d2s8-kommunikation", "d2s8-kommunikation"),
        "materials": [],
        "kern": [lit("Matheus, R., Janssen, M., & Maheshwari, D. (2020). Data science empowering the public: Data-driven dashboards for transparent and accountable decision-making in smart cities. Government Information Quarterly, 37(3), 101284.")],
        "hoeren": [
            lit("Data Stories Podcast, Enrico Bertini und Moritz Stefaner", "https://datastori.es/"),
            lit("The PolicyViz Podcast, Jon Schwabish", "https://policyviz.com/podcast/", note="Langlaufender Podcast zu Datenkommunikation und -visualisierung, häufig mit Public-Policy-Bezug (englisch)."),
        ],
        "lesen": [
            lit("Knaflic, C. N. (2017). Storytelling mit Daten: Die Grundlagen der effektiven Kommunikation und Visualisierung mit Daten. Vahlen."),
            lit("Cairo, A. (2019). How Charts Lie: Getting Smarter about Visual Information. W. W. Norton."),
            lit("Schwabish, J. (2021). Better Data Visualizations: A Guide for Scholars, Researchers, and Wonks. Columbia University Press."),
        ],
    },
    {
        "n": 9, "day": 3, "time": "9–11 Uhr",
        "title": "Wie gewinnt man Data Scientists nachhaltig für Behörden?",
        "short": "Data-Science-Workflows in der Behörde verankern, Datenstrategien, Rekrutierung und Arbeitsbedingungen.",
        "content": "Am letzten Tag widmen wir uns der Frage, wie Data Science dauerhaft in Behörden verankert werden kann. Zunächst geht es um die Umsetzung von Data-Science-Workflows und um die Planung effektiver Strategien zur Datennutzung und -verwaltung: Wir thematisieren den Wert von Datenmanagementplänen, den Aufbau geeigneter Datenbankinfrastrukturen sowie die Entwicklung einer nutzerorientierten Bereitstellungsinfrastruktur für Daten. Anschließend nehmen wir die Menschen hinter den Daten in den Blick und diskutieren Erfolgsfaktoren wie attraktive Arbeitsbedingungen, Weiterentwicklungsmöglichkeiten, sinnstiftende Projekte und Organisationskulturen. Gemeinsam blicken wir auf Ausschreibungsbeispiele und sammeln Ideen und Best Practices, wie öffentliche Institutionen im Wettbewerb um Data Scientists bestehen können.",
        "deck": deck("d3s9-rekrutierung", "d3s9-rekrutierung"),
        "materials": [
            {"title": "Stellenausschreibungen für Data Scientists in Behörden", "desc": "Sammlung von Ausschreibungen von service.bund.de als Diskussionsgrundlage.",
             "links": [("Ordner", f"{GH_TREE}/%C3%BCbungsmaterialien/ausschreibungen-service-bund-de")]},
        ],
        "kern": [lit("Bundesregierung (2023). Fortschritt durch Datennutzung – Datenstrategie der Bundesregierung. Berlin.")],
        "hoeren": [
            lit("The Data Governance 360 Podcast, Episoden 41 („Data, Records Management and Analytics in the Federal Government“) und 42 („The Growing Importance of Data Governance in an AI-Driven World“)"),
            lit("re|Staat digital – Der ÖFIT-Podcast, Folge 26: „Datenstrategien“ (mit Nicole Opiela und Mike Weber)", "https://www.oeffentliche-it.de/oefit-podcast/datenstrategien/"),
            lit("re|Staat digital – Der ÖFIT-Podcast, Folge 21: „Ein Open-Source-Ökosystem für die öffentliche Verwaltung“ (mit Christian Weidner)", "https://www.oeffentliche-it.de/oefit-podcast/ein-open-source-oekosystem-fuer-die-oeffentliche-verwaltung/"),
        ],
        "lesen": [
            lit("Veale, M., & Brass, I. (2019). Administration by Algorithm? Public Management Meets Public Sector Machine Learning. In: Yeung, K. & Lodge, M. (Hrsg.), Algorithmic Regulation. Oxford University Press."),
            lit("OECD (2019). The Path to Becoming a Data-Driven Public Sector. OECD Digital Government Studies, OECD Publishing, Paris.", "https://doi.org/10.1787/059814a7-en"),
            lit("Mergel, I., Edelmann, N., & Haug, N. (2019). Defining digital transformation: Results from expert interviews. Government Information Quarterly, 36(4), 101385."),
        ],
    },
    {
        "n": 10, "day": 3, "time": "11–13 Uhr",
        "title": "Gastvortrag: Open Data Governance",
        "speaker": "Betül Özdemir, Landesbeauftragte für Open Data des Landes Berlin",
        "short": "Wie eine Landesverwaltung Daten für die Veröffentlichung aufbereitet und was es braucht, damit daraus Nutzen entsteht.",
        "content": "In dieser Session ist Betül Özdemir, Landesbeauftragte für Open Data des Landes Berlin, zu Gast. Sie gibt Einblicke in die Governance offener Verwaltungsdaten: Wie werden Daten in einer Landesverwaltung für die Veröffentlichung aufbereitet, welche rechtlichen und organisatorischen Rahmenbedingungen sind dabei zu beachten, und was braucht es, damit aus veröffentlichten Daten tatsächlich Nutzen entsteht? Im Anschluss ist Raum für Fragen und Diskussion – auch mit Blick auf Open-Data-Vorhaben in Euren eigenen Häusern.",
        "deck": None,
        "materials": [],
        "kern": [
            lit("Data-Governance-Wegweiser", "https://data-governance-wegweiser.super.site/"),
            lit("Berlin Open Data Portal", "https://daten.berlin.de/"),
            lit("GovData – Das Datenportal für Deutschland", "https://www.govdata.de/"),
        ],
        "hoeren": [
            lit("#digdeep: „Schafft Open Government eine offenere Gesellschaft? Mit Oliver Rack“", "https://digdeep.de/"),
            lit("re|Staat digital – Der ÖFIT-Podcast, Folge 6: „Open Data“ (mit Jens Klessmann)", "https://www.oeffentliche-it.de/oefit-podcast/open-data/"),
            lit("„Open Data Café“, Podcast des EU-Datenportals data.europa.eu (englisch)", "https://data.europa.eu/de/podcasts"),
        ],
        "lesen": [
            lit("Gelman, A. (2021). Open data and quality: two orthogonal factors of a study. Blogpost in Statistical Modeling, Causal Inference, and Social Science.", "https://statmodeling.stat.columbia.edu/2021/04/25/open-data-and-quality-two-orthogonal-factors-of-a-study/"),
            lit("Janssen, M., Charalabidis, Y., & Zuiderwijk, A. (2012). Benefits, adoption barriers and myths of open data and open government. Information Systems Management, 29(4), 258–268."),
            lit("Ruijer, E., Grimmelikhuijsen, S., & Meijer, A. (2017). Open data for democracy: Developing a theoretical framework for open data use. Government Information Quarterly, 34(1), 45–52."),
        ],
    },
    {
        "n": 11, "day": 3, "time": "14–16 Uhr",
        "title": "Wrap-up und Ausblick",
        "short": "Der Daten-Lifecycle im Rückblick, Take-aways für die eigene Behörde, Details zur Abschlussaufgabe.",
        "content": "Wir nehmen abschließend noch einmal den kompletten Daten-Lifecycle in den Blick und sammeln praktische Take-aways für den Umgang mit Daten im Verwaltungskontext. Dazu werfen wir einen Blick nach vorn auf die nachfolgenden Module. Außerdem besprechen wir die Abschlussaufgabe (Daten-Podcast oder Daten-Literacy-Training) im Detail: inhaltliche Bausteine, technische Hinweise und Regeln zum KI-Einsatz.",
        "deck": deck("d3s11-wrapup", "d3s11-wrapup"),
        "materials": [],
        "kern": [],
        "hoeren": [],
        "lesen": [],
    },
]

BOOKS = [
    ("Bauer, T. K., Gigerenzer, G., & Krämer, W. (2014). Warum dick nicht doof macht und Genmais nicht tötet: Über Risiken und Nebenwirkungen der Unstatistik. Campus.", None,
     "Das erste Buch zur „Unstatistik des Monats“: kurze, pointierte Fallbeispiele dazu, wie Zahlen in Medien und Politik fehlinterpretiert werden. Gut in kleinen Dosen zu lesen und eine Fundgrube für Diskussionsanlässe."),
    ("Bauer, T. K., Gigerenzer, G., Krämer, W., & Schüller, K. (2022). Grüne fahren SUV und Joggen macht unsterblich: Über Risiken und Nebenwirkungen der Unstatistik. Campus.", None,
     "Der Nachfolgeband mit neueren Beispielen, unter anderem aus der Corona-Berichterstattung: Kausalität vs. Korrelation, Risikokommunikation und der Umgang mit Prognosen – thematisch sehr nah an Session 6."),
    ("Bergstrom, C. T., & West, J. D. (2021). Calling Bullshit: The Art of Skepticism in a Data-Driven World. Random House.", "https://callingbullshit.org/",
     "Äußerst unterhaltsames Buch dazu, wie Fehlinformationen, statistische Irreführungen und pseudowissenschaftliche Behauptungen unseren Alltag durchdringen. Buch und Webseite bieten praktische Werkzeuge, um kritisch mit Daten und Informationen umzugehen."),
    ("Fung, K. (2013). Numbersense: How to Use Big Data to Your Advantage. McGraw Hill.", None,
     "Strukturiert um Fallbeispiele zu Daten aus unterschiedlichen Domänen, z.B. Marketing, Wirtschaft oder Sport. Kurzweilig zu lesen und gut, um kritisch über bestimmte Datenversprechen nachzudenken."),
    ("Harford, T. (2022). The Data Detective: Ten Easy Rules to Make Sense of Statistics. Penguin.", None,
     "Zehn einfache, praxisnahe Regeln, um Daten und Statistiken zu verstehen und zu interpretieren. Geschrieben von einem der kompetentesten Daten- und Statistikjournalisten."),
    ("Narayanan, A., & Kapoor, S. (2024). AI Snake Oil: What Artificial Intelligence Can Do, What It Can’t, and How to Tell the Difference. Princeton University Press.", None,
     "Die Princeton-Forscher entlarven gängige Mythen über künstliche Intelligenz und geben einen klaren Überblick darüber, was KI tatsächlich leisten kann und was nicht."),
    ("Salganik, M. J. (2019). Bit by Bit: Social Research in the Digital Age. Princeton University Press.", "https://www.bitbybitbook.com/",
     "Eigentlich ein Lehrbuch für Computational Social Science, aber ein sehr unterhaltsamer Überblick darüber, wie digitale Daten und kreative Forschungsdesigns die empirische Forschung bereichert haben. Viele Beispiele, ethische Diskussionen und Übungsaufgaben."),
    ("Schüller, K. (2015). Statistik und Intuition: Alltagsbeispiele kritisch hinterfragt. Springer Spektrum.", None,
     "Systematischer aufgebaut als die Unstatistik-Bände: typische Denkfehler und Manipulationen im alltäglichen Umgang mit Statistik, jeweils an konkreten Beispielen durchgearbeitet."),
    ("Watts, D. J. (2011). Everything Is Obvious: Once You Know the Answer. Crown.", None,
     "Ein Buch zum „hindsight bias“, also dazu, wie leicht es ist, nachträglich plausible oder sogar zwangsläufig erscheinende Erklärungen für Ereignisse und Trends zu finden. Provokant und anregend, manchmal etwas langatmig."),
]

PODCASTS = [
    ("More or Less: Behind the Stats", "Tim Harford, BBC Radio 4", "https://www.bbc.co.uk/programmes/b006qshd",
     "Beleuchtet statistische Fragen und überprüft weit verbreitete Zahlen aus Medien und Alltag. Angenehm kurze, informative und unterhaltsame Happen (meist unter 12 Minuten pro Folge; englisch)."),
    ("Data Skeptic", "Kyle Polich", "https://dataskeptic.com/",
     "Lange laufender, professioneller Podcast, der sich einem Thema pro Staffel widmet (z.B. Animal Intelligence, Machine Intelligence, Surveys). Teilweise stark statistisch (30–40 Minuten; englisch)."),
    ("Stats + Stories", "Rosemary Pennington et al., Miami University und ASA", "https://statsandstories.net/",
     "„A Podcast About The Statistics Behind the Stories and the Stories Behind the Statistics.“ Inhaltlich seriös aufbereitet (20–30 Minuten; englisch)."),
    ("Harvard Data Science Review Podcast", "Xiao-Li Meng, Liberty Vittert", "https://hdsr.mitpress.mit.edu/podcast",
     "Betrachtet Nachrichten, Politik und Wirtschaft durch die Brille der Datenwissenschaft. Jede Folge eine „Fallstudie“ darüber, wie Daten genutzt werden, um zu informieren oder in die Irre zu führen (30–40 Minuten; englisch)."),
    ("Der KI-Podcast", "Gregor Schmalzried, Marie Kilg und Fritz Espenlaub; ARD", "https://www.ardaudiothek.de/sendung/der-ki-podcast/94632864/",
     "Wissenschafts-, Technik- und Gesellschaftsjournalismus rund um KI (30–40 Minuten; deutsch)."),
    ("KI verstehen", "Deutschlandfunk", "https://www.deutschlandfunk.de/ki-verstehen-102.html",
     "Wissenschaftsjournalismus rund um KI, mit einem Schwerpunktthema pro Folge (25–35 Minuten; deutsch)."),
    ("Logbuch: Netzpolitik", "Tim Pritlove, Linus Neumann", "https://logbuch-netzpolitik.de/",
     "Langjähriger Podcast aus dem CCC-Umfeld zu Netzpolitik, digitaler Gesellschaft und Datenschutz; zunehmend auch KI-Themen. Unterhaltsam bis ausufernd (1–2,5 Stunden; deutsch)."),
    ("#digdeep – Neues aus der digitalen Welt", "Frauke Kreuter, Christof Horn", "https://digdeep.de/",
     "Podcast zu digitaler Transformation und wie sie unser Leben beeinflusst. Mix aus wissenschaftlicher und Praktikerperspektive, mittlerweile im Interviewformat (30–60 Minuten; deutsch)."),
    ("re|Staat digital – Der ÖFIT-Podcast", "Kompetenzzentrum Öffentliche IT (Fraunhofer FOKUS)", "https://www.oeffentliche-it.de/oefit-podcast/",
     "Pro Folge ein Fachthema rund um Daten, IT und Digitalisierung in der öffentlichen Verwaltung, im Gespräch mit Forschenden des ÖFIT – näher an der Verwaltungspraxis als die meisten anderen Podcasts dieser Liste (deutsch)."),
]

WEB = [
    ("Unstatistik des Monats", "Thomas K. Bauer, Gerd Gigerenzer, Walter Krämer und Katharina Schüller; Harding-Zentrum für Risikokompetenz", "https://www.hardingcenter.de/de/transfer-und-nutzen/unstatistik-des-monats",
     "Seit 2012 wird jeden Monat eine öffentlich verbreitete Zahl oder Statistik auseinandergenommen. Jeder Beitrag ist in wenigen Minuten gelesen und eignet sich hervorragend als wiederkehrendes Trainingsformat für den eigenen Umgang mit Zahlen."),
    ("Data-Literacy-Charta", "Katharina Schüller, Henning Koch & Florian Rampelt; Stifterverband, Berlin 2021", "https://www.stifterverband.org/sites/default/files/data-literacy-charta_v1_2.pdf",
     "Kompaktes Grundlagenpapier zu der Frage, welche Datenkompetenzen Menschen in einer digitalisierten Welt brauchen. Guter gemeinsamer Bezugsrahmen – auch für die Diskussion, welche Kompetenzen in der eigenen Behörde aufgebaut werden sollten."),
    ("Future Skills: Ein Framework für Data Literacy", "Schüller, K., Busch, P., & Hindinger, C. (2019). Arbeitspapier Nr. 47, Hochschulforum Digitalisierung, Berlin", "https://hochschulforumdigitalisierung.de/sites/default/files/dateien/HFD_AP_Nr_47_DALI_Kompetenzrahmen_WEB.pdf",
     "Das Kompetenzframework hinter der Charta, mit ausformulierten Lernzielen entlang des Daten-Lifecycles. Nützlich, wenn Ihr Weiterbildungsangebote zum Thema Daten im eigenen Haus konzipieren wollt."),
    ("Introduction to Data Science (Hertie School)", "Simon Munzert, Vorlesungsfolien", "https://github.com/intro-to-data-science-25/lectures",
     "Ergänzende, englischsprachige Folien aus dem Master-Kurs, falls Ihr tiefer in einzelne Werkzeuge einsteigen wollt."),
]

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def esc(s):
    return html.escape(s, quote=True)

def page(title, body, depth=0, active=None, description=None):
    rel = "../" * depth
    nav = [("index.html", "Überblick", "home"), ("sessions.html", "Sessions", "sessions"),
           ("leistungen.html", "Leistungen", "leistungen"), ("ressourcen.html", "Ressourcen", "ressourcen")]
    nav_html = "".join(
        f'<a href="{rel}{href}"{" class=\"active\"" if key == active else ""}>{label}</a>' for href, label, key in nav)
    full_title = f"{title} · {SITE_TITLE}" if title != SITE_TITLE else f"{SITE_TITLE} · Modul 2"
    desc = description or "Kurswebseite zu Modul 2 „Der Daten-Lifecycle“ des Zertifikatsprogramms „KI und Data Science für die öffentliche Verwaltung“ der Hertie School."
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Fira+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}style.css">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{rel}index.html">
      <span class="brand-title">{SITE_TITLE}</span>
      <span class="brand-sub">{SITE_SUB}</span>
    </a>
    <nav class="site-nav" aria-label="Hauptnavigation">{nav_html}</nav>
    <a class="logo" href="https://www.hertie-school.org/" aria-label="Hertie School"><img src="{rel}assets/hertieschool-neg.svg" alt="Hertie School"></a>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <strong>{SITE_TITLE}</strong> · Modul 2 des Zertifikatsprogramms „KI und Data Science für die öffentliche Verwaltung“<br>
      <a href="https://simonmunzert.com/">Simon Munzert</a>, <a href="https://www.hertie-school.org/">Hertie School</a>, Berlin · 26.–28. Oktober 2026
    </div>
    <div class="footer-links">
      <a href="{GH}">Materialien auf GitHub</a>
      <a href="mailto:munzert@hertie-school.org">Kontakt</a>
    </div>
  </div>
</footer>
</body>
</html>
"""

def session_href(s, depth):
    rel = "../" * depth
    return f"{rel}sessions/s{s['n']:02d}.html"

def deck_links(s, cls="btn-row"):
    d = s["deck"]
    if not d:
        return '<p class="muted">Zu dieser Session gibt es keine Folien; der Gastvortrag wird nicht veröffentlicht.</p>'
    parts = [f'<a class="btn btn-primary" href="{d["html"]}">Folien (HTML)</a>']
    if "pdf" in d:
        parts.append(f'<a class="btn" href="{d["pdf"]}">Folien (PDF)</a>')
    parts.append(f'<a class="btn" href="{d["rmd_gh"]}">Quelltext (Rmd)</a>')
    parts.append(f'<a class="btn btn-ghost" href="{d["folder"]}">Ordner auf GitHub</a>')
    return f'<div class="{cls}">{"".join(parts)}</div>'

def lit_list(items):
    if not items:
        return ""
    out = ["<ul class=\"lit\">"]
    for it in items:
        text = esc(it["text"])
        if it["url"]:
            text = f'<a href="{it["url"]}">{text}</a>'
        note = f' <span class="note">{esc(it["note"])}</span>' if it["note"] else ""
        out.append(f"<li>{text}{note}</li>")
    out.append("</ul>")
    return "\n".join(out)

def session_page(s, i):
    day = DAYS[s["day"]]
    prev_s = SESSIONS[i - 1] if i > 0 else None
    next_s = SESSIONS[i + 1] if i + 1 < len(SESSIONS) else None
    speaker = f'<p class="speaker">{esc(s["speaker"])}</p>' if s.get("speaker") else ""

    mats = ""
    if s["materials"]:
        cards = []
        for m in s["materials"]:
            links = " ".join(f'<a class="btn btn-small" href="{u}">{esc(l)}</a>' for l, u in m["links"])
            cards.append(f'<div class="card"><h3>{esc(m["title"])}</h3><p>{esc(m["desc"])}</p><div class="btn-row">{links}</div></div>')
        mats = f'<h2 id="materialien">Code und Materialien</h2><div class="cards">{"".join(cards)}</div>'

    lit_blocks = []
    for key, heading in (("kern", "Kernliteratur"), ("hoeren", "Zum Weiterhören"), ("lesen", "Zum Weiterlesen")):
        if s[key]:
            lit_blocks.append(f"<h3>{heading}</h3>{lit_list(s[key])}")
    lit_html = f'<h2 id="literatur">Literatur und Medien</h2><p class="muted">Die Kernliteratur ist zur Vorbereitung gedacht, alles Weitere ist ein ergänzendes Angebot.</p>{"".join(lit_blocks)}' if lit_blocks else ""

    pn = '<nav class="prevnext" aria-label="Sessions">'
    pn += f'<a class="prev" href="s{prev_s["n"]:02d}.html"><span>Vorherige Session</span>{prev_s["n"]}: {esc(prev_s["title"])}</a>' if prev_s else "<span></span>"
    pn += f'<a class="next" href="s{next_s["n"]:02d}.html"><span>Nächste Session</span>{next_s["n"]}: {esc(next_s["title"])}</a>' if next_s else "<span></span>"
    pn += "</nav>"

    body = f"""
<p class="breadcrumb"><a href="../index.html">Überblick</a> › <a href="../sessions.html">Sessions</a> › Session {s['n']}</p>
<article class="session">
  <p class="kicker">{day['label']} · {esc(day['date'])} · {s['time']}</p>
  <h1><span class="num">Session {s['n']}</span>{esc(s['title'])}</h1>
  {speaker}
  <p class="theme">Tagesthema: {esc(day['theme'])}</p>
  {deck_links(s)}
  <h2 id="inhalte">Inhalte</h2>
  <p class="lead">{esc(s['content'])}</p>
  {mats}
  {lit_html}
</article>
{pn}
"""
    return page(f"Session {s['n']}: {s['title']}", body, depth=1, active="sessions", description=s["short"])

def schedule_table():
    slots = ["9–11 Uhr", "11–13 Uhr", "13–14 Uhr", "14–16 Uhr", "16–18 Uhr", "18–19 Uhr", "ab 19 Uhr"]
    by = {(s["day"], s["time"]): s for s in SESSIONS}
    rows = []
    for slot in slots:
        cells = []
        for d in (1, 2, 3):
            s = by.get((d, slot))
            if s:
                sp = f'<span class="cell-speaker">{esc(s["speaker"])}</span>' if s.get("speaker") else ""
                cells.append(f'<td><a href="sessions/s{s["n"]:02d}.html"><span class="cell-num">Session {s["n"]}</span>{esc(s["title"])}</a>{sp}</td>')
            elif slot == "13–14 Uhr":
                cells.append('<td class="pause">Mittagspause</td>')
            elif slot == "ab 19 Uhr" and d == 2:
                cells.append('<td class="pause">Gemeinsames Abendessen (Restaurant tbd)</td>')
            else:
                cells.append("<td></td>")
        rows.append(f'<tr><th scope="row">{slot}</th>{"".join(cells)}</tr>')
    heads = "".join(f'<th scope="col"><span class="day-label">{DAYS[d]["label"]} · {esc(DAYS[d]["date"].split(", ")[1])}</span><span class="day-theme">{esc(DAYS[d]["theme"])}</span></th>' for d in (1, 2, 3))
    # Kompakte Liste für schmale Bildschirme (per CSS umgeschaltet)
    lst = []
    for d in (1, 2, 3):
        items = "".join(
            f'<li><a href="sessions/s{s["n"]:02d}.html"><span class="li-time">{s["time"]}</span><span class="cell-num">Session {s["n"]}</span>{esc(s["title"])}</a></li>'
            for s in SESSIONS if s["day"] == d)
        lst.append(f'<li class="day"><span class="day-label">{DAYS[d]["label"]} · {esc(DAYS[d]["date"])}</span><span class="day-theme">{esc(DAYS[d]["theme"])}</span><ul>{items}</ul></li>')
    schedule_list = f'<ul class="schedule-list">{"".join(lst)}</ul>'
    return schedule_list + f'<div class="table-wrap"><table class="schedule"><thead><tr><th scope="col" class="corner"></th>{heads}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

def index_page():
    body = f"""
<section class="hero">
  <p class="kicker">Zertifikatsprogramm „KI und Data Science für die öffentliche Verwaltung“ · Modul 2 (KI-1002-F-2026)</p>
  <h1>Der Daten-Lifecycle</h1>
  <p class="subtitle">Vom Rohstoff zur KI-Anwendung</p>
  <p class="lead">Keine moderne KI-Anwendung funktioniert ohne Daten. Aber was zeichnet unterschiedliche Datentypen aus und weshalb ist ihre Qualität so entscheidend für Data-Science- und KI-Anwendungen? In diesem Modul beleuchten wir den Lifecycle von Daten Schritt für Schritt – von ihrer Generierung und Sammlung über die Verarbeitung und Analyse bis hin zur Speicherung und Veröffentlichung. Anhand von Anwendungsfällen und typischen Dos and Don’ts mit Daten erarbeiten wir eine Kompetenz zur kritischen Beurteilung von KI-Produkten anhand des Daten-Inputs und zum Aufbau einer datenbewussten Organisation.</p>
  <div class="facts">
    <div><span class="fact-label">Termine</span><span class="fact-value">26.–28. Oktober 2026</span></div>
    <div><span class="fact-label">Ort</span><span class="fact-value">Hertie School, Berlin</span></div>
    <div><span class="fact-label">Dozent</span><span class="fact-value"><a href="https://simonmunzert.com/">Simon Munzert</a><br><a href="mailto:munzert@hertie-school.org">munzert@hertie-school.org</a></span></div>
    <div><span class="fact-label">Assistenz</span><span class="fact-value">Alex Karras<br><a href="mailto:karras@hertie-school.org">karras@hertie-school.org</a></span></div>
  </div>
</section>

<section>
  <h2 id="programm">Programm</h2>
  <p>Drei Tage, elf Sessions. Jede Session hat eine eigene Seite mit Folien, Materialien und Literatur. Die Folien liegen im <a href="{GH}">GitHub-Repository des Moduls</a> und werden von dort direkt verlinkt.</p>
  {schedule_table()}
</section>

<section class="two-col">
  <div>
    <h2 id="leistungen">Leistungen</h2>
    <ul class="plain">
      <li><strong>Aufgabe 1: Daten-Poster</strong> (20 %) – Überblick zur Datennutzung in der eigenen Behörde, Abgabe bis 19. Oktober 2026.</li>
      <li><strong>Aufgabe 2: Daten-Podcast oder Daten-Literacy-Training</strong> (50 %) – im Team zu zweit oder zu dritt, Abgabe bis 23. November 2026.</li>
      <li><strong>Teilnahme</strong> (30 %) – aktive Beteiligung an Austausch und Diskussion.</li>
    </ul>
    <p><a class="btn" href="leistungen.html">Details zu den Aufgaben</a></p>
  </div>
  <div>
    <h2 id="materialien">Materialien</h2>
    <ul class="plain">
      <li><a href="{GH}">Repository mit allen Folien und Code-Materialien</a> (HTML, PDF, Rmd, R-Skripte, Beispieldaten)</li>
      <li><a href="sessions/s04.html#materialien">Fallstudien zu Web Scraping und APIs</a> (Session 4)</li>
      <li><a href="sessions/s07.html#materialien">Praxis-Pipeline zu OCR und Sprachmodellen</a> (Session 7)</li>
      <li><a href="ressourcen.html">Bücher, Podcasts und Webseiten</a> zur Vertiefung</li>
    </ul>
  </div>
</section>

<section class="dozent">
  <h2 id="dozent">Dozent</h2>
  <p><a href="https://simonmunzert.com/">Simon Munzert</a> ist Professor for Data Science and Public Policy an der Hertie School und leitet dort das Data Science Lab. In seiner Forschung beschäftigt er sich mit der Moderation von Online-Inhalten, mit Wahlprognosen und mit der Vermittlung datenbasierter Evidenz an die Öffentlichkeit sowie mit Meinungsbildung im digitalen Zeitalter und der Nutzung digitaler Verhaltensdaten in der Sozialforschung. Er ist Mitgründer von <a href="https://zweitstimme.org/">zweitstimme.org</a>, einem Projekt zur Prognose und Kommunikation von Wahlergebnissen. Neben seiner Lehre in den Studienprogrammen vermittelt er Daten- und KI-Kompetenz an Fach- und Führungskräfte. Seine Arbeiten sind unter anderem in Nature Human Behaviour, der American Political Science Review, PNAS und The Lancet erschienen.</p>
  <p>Als Gast ist am dritten Tag <strong>Betül Özdemir</strong>, Landesbeauftragte für Open Data des Landes Berlin, dabei (<a href="sessions/s10.html">Session 10</a>).</p>
</section>
"""
    return page(SITE_TITLE, body, depth=0, active="home")

def sessions_page():
    blocks = []
    for d in (1, 2, 3):
        day = DAYS[d]
        cards = []
        for s in [x for x in SESSIONS if x["day"] == d]:
            links = []
            if s["deck"]:
                links.append(f'<a href="{s["deck"]["html"]}">Folien</a>')
                if "pdf" in s["deck"]:
                    links.append(f'<a href="{s["deck"]["pdf"]}">PDF</a>')
            if s["materials"]:
                links.append(f'<a href="sessions/s{s["n"]:02d}.html#materialien">Materialien</a>')
            sp = f'<p class="cell-speaker">{esc(s["speaker"])}</p>' if s.get("speaker") else ""
            cards.append(f"""<div class="card session-card">
  <p class="kicker">Session {s['n']} · {s['time']}</p>
  <h3><a href="sessions/s{s['n']:02d}.html">{esc(s['title'])}</a></h3>
  {sp}
  <p>{esc(s['short'])}</p>
  <p class="card-links"><a href="sessions/s{s['n']:02d}.html">Zur Session</a>{"".join(" · " + l for l in links)}</p>
</div>""")
        blocks.append(f'<h2 id="tag{d}">{day["label"]}: {esc(day["theme"])}</h2><p class="muted">{esc(day["date"])}</p><div class="cards">{"".join(cards)}</div>')
    body = f"""
<h1>Sessions</h1>
<p class="lead">Elf Sessions an drei Tagen. Die Folien sind als HTML-Präsentation direkt im Browser abspielbar (Navigation mit den Pfeiltasten, <kbd>f</kbd> für Vollbild, <kbd>h</kbd> für Hilfe) und, wo vorhanden, als PDF verfügbar. Alle Quelltexte liegen im <a href="{GH}">GitHub-Repository</a>.</p>
{"".join(blocks)}
"""
    return page("Sessions", body, depth=0, active="sessions")

def leistungen_page():
    body = f"""
<h1>Leistungen</h1>
<p class="lead">Die Modulnote setzt sich aus drei Teilen zusammen. Alle Abgaben erfolgen über Moodle.</p>
<div class="table-wrap"><table class="grades">
<thead><tr><th>Leistung</th><th>Abgabe</th><th>Gewicht</th></tr></thead>
<tbody>
<tr><td><a href="#aufgabe1">Aufgabe 1: Daten-Poster</a><br><span class="muted">Vorbereitender Überblick zur Datennutzung in der eigenen Behörde</span></td><td>19. Oktober 2026</td><td>20 %</td></tr>
<tr><td><a href="#aufgabe2">Aufgabe 2: Daten-Podcast oder Daten-Literacy-Training</a><br><span class="muted">Im Team zu zweit oder zu dritt</span></td><td>23. November 2026</td><td>50 %</td></tr>
<tr><td><a href="#teilnahme">Teilnahme</a></td><td>–</td><td>30 %</td></tr>
</tbody></table></div>

<h2 id="aufgabe1">Aufgabe 1: Daten-Poster</h2>
<p>Die Vorab-Aufgabe schließt an Aufgabe 2 von Modul 1 an. Dort wurde ein Kernprozess aus der eigenen Behörde, der eine Datenquelle involviert, in einer Process Map beschrieben. In Vorbereitung auf Modul 2 erstellt Ihr ein Poster, das eine Datenquelle aus dieser Process Map genauer vorstellt. Das Poster informiert über folgende Punkte:</p>
<ul>
  <li><strong>Um welche Daten handelt es sich?</strong> Welcher Typ von Daten, und was zeichnet die Daten aus?</li>
  <li><strong>Wie sehen die Daten konkret aus?</strong> Wenn möglich mit einem oder mehreren Beispielen (gerne modifiziert, um keine echten Daten offenzulegen).</li>
  <li><strong>Wozu werden die Daten verwendet?</strong> Kurz auf den Punkt gebracht, auch wenn die Daten in mehreren Prozessen genutzt werden.</li>
  <li><strong>Wie sieht die Infrastruktur um die Daten aus?</strong> Wo sind sie abgelegt (Cloud, on premise, physische Akten) und wie werden sie verwaltet?</li>
  <li><strong>Wer ist involviert?</strong> Abteilungen und Akteure in Generierung, Verarbeitung, Nutzung und Verwahrung, gerne tabellarisch.</li>
</ul>
<div class="merke">
  <p><strong>Format.</strong> Das Poster kann zum Beispiel als PowerPoint-Folie oder Word-Seite entstehen, Hoch- oder Querformat. Einreichung als PDF; die Poster werden auf DIN A3 gedruckt und im Modul als Diskussionsgrundlage genutzt. Bitte sparsam mit Text umgehen und Schriftgrößen wählen, die aus einem Meter Entfernung lesbar sind.</p>
</div>

<h2 id="aufgabe2">Aufgabe 2: Daten-Podcast oder Daten-Literacy-Training</h2>
<p>Für die zweite Leistung könnt Ihr zwischen zwei Optionen wählen. Beide werden <strong>zu zweit oder zu dritt</strong> bearbeitet, ein Upload pro Team über Moodle bis zum <strong>23. November 2026</strong>. Die ausführlichen Hinweise aus dem Kurs stehen in den <a href="{GITHACK}/d3s11-wrapup/d3s11-wrapup.html">Folien zu Session 11</a>.</p>

<div class="two-col options">
<div class="card">
<h3>Option 1: Der Daten-Podcast</h3>
<p>Eine Podcast-Aufnahme, schwerpunktmäßig zu zwei Themen, die Kern des Kurses waren. Die Aufnahme enthält mindestens zwei der drei Bausteine:</p>
<ol>
  <li><strong>Einblick in einen Daten-Use-Case aus Eurer Behörde</strong>: ein Fall aus Eurer Arbeit, bei dem Daten eine zentrale Rolle spielen, als Best- oder Worst-Practice-Beispiel, mit Bezug zu Konzepten aus dem Kurs.</li>
  <li><strong>Daten-Fail der Woche</strong>: ein aktueller Artikel, Blogbeitrag oder Post mit problematischer oder missverständlicher Datennutzung. Was ist schiefgelaufen, was lernt man daraus?</li>
  <li><strong>Blick in die Zukunft</strong>: Eure Vision für den Umgang mit Daten in Eurer Behörde oder Einheit.</li>
</ol>
<p><strong>Länge:</strong> maximal 20 Minuten (zwei Personen) bzw. 30 Minuten (drei Personen).<br>
<strong>Einzureichen:</strong> Audiodatei (mp3 oder m4a), Transkript (automatisch erzeugt reicht) und Shownotes mit den besprochenen Quellen.<br>
<strong>Technik:</strong> Smartphone oder Laptop genügen; keine aufwändige Postproduktion nötig.<br>
<strong>KI-Einsatz:</strong> Selbst einsprechen ist Pflicht. KI-generierte Audio-Podcasts (NotebookLM, ElevenLabs o.Ä.) sind nicht erlaubt. KI-Unterstützung bei Skript oder Fragen ist in Ordnung.</p>
</div>
<div class="card">
<h3>Option 2: Daten-Literacy-Training</h3>
<p>Ein Trainingskonzept für die eigene Behörde zu <strong>einem Thema aus dem Kurs</strong>, das in Eurem Haus einen Unterschied machen würde: Datenqualität, Schnittstellen und Weiternutzung, Statistiken richtig lesen, Visualisierung oder KI-Werkzeuge im Arbeitsalltag.</p>
<p><strong>Einzureichen:</strong></p>
<ol>
  <li><strong>Ein One-Pager</strong>: Was Ihr anbietet (Thema, Lernziele, Format, Dauer), für wen (Zielgruppe und Vorwissen), von wem (samt Vorbereitung, Technik und Daten).</li>
  <li><strong>Ein Foliendeck</strong> für eine kurze Session mit etwa acht bis zwölf Folien.</li>
</ol>
<p><strong>Worauf ich achte:</strong> Der Einstieg macht klar, warum das Thema für die Zielgruppe relevant ist, am besten an einem Beispiel aus Eurem Haus. Mindestens ein aktivierendes Element (Übung, Diskussionsfrage, Beispieldatensatz, Quiz). Konzepte aus dem Kurs sind in die Sprache der Zielgruppe übersetzt.<br>
<strong>KI-Einsatz:</strong> erlaubt für Konzept, Text und Folien. Das Ergebnis muss aber aus einem Guss sein und auf Eure Zielgruppe passen. Bitte keine Beispiele unverändert aus dem Kurs übernehmen.</p>
<p class="muted">Bewertet wird nicht die Folienästhetik, sondern ob das Training bei Eurer Zielgruppe ankommen würde.</p>
</div>
</div>

<h2 id="teilnahme">Teilnahme</h2>
<p>Die Note für die Teilnahme geht davon aus, dass Ihr nicht rein passiv zuhört, sondern Euch aktiv am Austausch und der Diskussion der Kursinhalte beteiligt und eigene Erfahrungen, Einschätzungen und Ideen einbringt. Insbesondere solltet Ihr eine eigene Meinung zur vorzubereitenden Literatur entwickeln und diskutieren können. Eine gute Teilnahme zeichnet sich durch aktive Beteiligung, die Qualität der Beiträge und eine gute Interaktion mit den anderen Teilnehmenden aus.</p>

<h2 id="regeln">Regeln</h2>
<ul>
  <li><strong>Verspätete Einreichung:</strong> Bei verspäteter Abgabe ist der Kursleitung eine schriftliche Erklärung vorzulegen. Wird die Arbeit angenommen, wird die Verspätung mit einem Notenabzug belegt (Examination Rules §9).</li>
  <li><strong>Anwesenheit:</strong> Die Teilnahme am gesamten Modul ist verpflichtend. Bei Nicht-Erscheinen ist vorab eine schriftliche Begründung vorzulegen. Werden mehr als 20 % versäumt, entscheidet die Kursleitung über Nichtbestehen oder Zusatzanforderungen.</li>
  <li><strong>Academic Integrity:</strong> Plagiate, betrügerische Handlungen und Trittbrettfahren bei Gruppenarbeiten werden nicht toleriert (Examination Rules §15, Hertie Plagiarism Policy). Beim Arbeiten mit KI gelten die Hertie AI Guidelines.</li>
  <li><strong>Nachteilsausgleich und mildernde Umstände:</strong> Bei Behinderung, dauerhafter Erkrankung oder Pflege Angehöriger legt der Prüfungsausschuss auf Antrag Ausgleichsmaßnahmen fest (§13). Bei mildernden Umständen bitte rechtzeitig vor dem Abgabetermin an die Kursleitung wenden.</li>
</ul>
<p class="muted">Verbindlich ist der Syllabus auf Moodle sowie die <a href="https://moodle.hertie-school.org/mod/book/view.php?id=47912&chapterid=1159">Study, Examination and Admission Rules</a> der Hertie School.</p>
"""
    return page("Leistungen", body, depth=0, active="leistungen")

def ressourcen_page():
    def entry(title, by, url, blurb):
        t = f'<a href="{url}">{esc(title)}</a>' if url else esc(title)
        byl = f' <span class="by">{esc(by)}</span>' if by else ""
        return f'<li><p class="res-title">{t}{byl}</p><p class="res-blurb">{esc(blurb)}</p></li>'
    books = "".join(entry(t, None, u, b) for t, u, b in BOOKS)
    pods = "".join(entry(t, by, u, b) for t, by, u, b in PODCASTS)
    web = "".join(entry(t, by, u, b) for t, by, u, b in WEB)
    body = f"""
<h1>Ressourcen</h1>
<p class="lead">Die vorbereitenden Materialien zu den einzelnen Sessions findet Ihr auf den <a href="sessions.html">Session-Seiten</a>. Zusätzlich dienen die folgenden Bücher, Podcasts und Webseiten als allgemeine Einführung. Sie sind nicht verpflichtend, sondern ein ergänzendes Angebot.</p>
<h2 id="buecher">Bücher</h2>
<ul class="resources">{books}</ul>
<h2 id="podcasts">Podcasts</h2>
<ul class="resources">{pods}</ul>
<h2 id="web">Weitere Materialien im Netz</h2>
<ul class="resources">{web}</ul>
"""
    return page("Ressourcen", body, depth=0, active="ressourcen")

# ---------------------------------------------------------------------------

def main():
    (ROOT / "sessions").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    (ROOT / "sessions.html").write_text(sessions_page(), encoding="utf-8")
    (ROOT / "leistungen.html").write_text(leistungen_page(), encoding="utf-8")
    (ROOT / "ressourcen.html").write_text(ressourcen_page(), encoding="utf-8")
    for i, s in enumerate(SESSIONS):
        (ROOT / "sessions" / f"s{s['n']:02d}.html").write_text(session_page(s, i), encoding="utf-8")
    print(f"{4 + len(SESSIONS)} Seiten geschrieben nach {ROOT}")

if __name__ == "__main__":
    main()
