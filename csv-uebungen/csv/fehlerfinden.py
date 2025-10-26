import csv

# Achtung! Damit das Programm funktioniert, muss es in jenem Ordner ausgeführt werden,
# indem die Datei 'fehler.csv' liegt. Ansonsten wird die Datei nicht gefunden.
# Navigieren Sie dazu in der VS-Code Kommandozeile ins Verzeichnis 'csv-uebungen/csv'

with open("fehler.csv") as csvfile:
    # CSV-Format erraten
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    # Datei mit erratenem Format einlesen
    csv_reader = csv.DictReader(csvfile, dialect=dialect)
    # Array mit allen Zeilen erstellen
    tabelle = [row for row in csv_reader]

header : list[str] = csv_reader.fieldnames  # type: ignore

print(f"Header: {header}")
print("\nTabelle als Liste von dictionaries:")
print(tabelle)

print("\nKonvertierung der Zahlen")
for zeile in tabelle:
    for spalte in header:
        zeile[spalte] = int(zeile[spalte])  # Aus Zeichenketten Zahlen machen

print(tabelle)

print(f"\nZeile 3 (Index 2): tabelle[2]={tabelle[2]}")
print(f"tabelle[2]['x'] = {tabelle[2]['x']},  tabelle[2]['x^3'] = {tabelle[2]['x^3']}")

# TODO
# Fehler finden, ausgeben und in der tablle korrigieren




# CSV-Datei korrigiert schreiben
with open("korrigiert.csv", "w") as csvfile:
    # Writer vorbereiten
    writer = csv.DictWriter(csvfile, fieldnames=header, dialect=dialect)
    # Header (erste Zeile) schreiben
    writer.writeheader()
    # Alle Zeilen schreiben
    writer.writerows(tabelle)
