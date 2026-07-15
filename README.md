# P166-Ausfüllhilfe

Eine kleine [Streamlit](https://streamlit.io)-App, die beim Ausfüllen des
Einstellungsformulars **P166** (Tutorate/Hilfskräfte) hilft: Sie liest ausgefüllte
PDF-Bewerbungsformulare ein und befüllt daraus automatisch einige Felder des P166.

## Installation

```
git clone https://github.com/pfaffelh/pdf_form
cd pdf_form
pip install -r requirements.txt
```

## Starten

```
streamlit run Pdf_form.py
```

## Ablauf

1. Ein oder mehrere ausgefüllte PDF-Bewerbungsformulare hochladen (Mehrfachauswahl möglich).
2. Die App liest die Formularfelder aus und zeigt die Daten in einer editierbaren Tabelle.
3. Für jede Zeile wird ein vorbefülltes P166 erzeugt; alle zusammen gibt es als
   `data.tgz` zum Download.

## Konfiguration

- Die verwendete P166-Vorlage steht am Anfang von `Pdf_form.py`
  (`p166pdf = 'static/P166_07_2026.pdf'`). Ältere Vorlagen liegen ebenfalls in `static/`.
- Das Feld-Mapping (Feldname im Bewerbungsformular → Feldname im P166) steht im
  Dictionary `felder` in `Pdf_form.py`. Wechselt die Vorlage, sollten die dort
  genutzten Feldnamen im neuen PDF vorhanden sein.

## Verzeichnisse

- `static/` – P166-Vorlagen
- `input/`, `output/`, `tmp/` – Arbeitsverzeichnisse zur Laufzeit (Inhalte werden nicht versioniert)
