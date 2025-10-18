import csv

# Achtung! Damit das Programm funktioniert, muss es in jenem Ordner ausgeführt werden,
# indem die Datei 'fehler.csv' liegt. Ansonster wird die Datei nicht gefunden.

with open("fehler.csv") as csvfile:
    # CSV-Format erraten
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    # Datei mit erratenem Format einlesen
    csv_reader = csv.DictReader(csvfile, dialect=dialect)
    # Array mit allen Zeilen erstellen
    tabelle = [row for row in csv_reader]

header = csv_reader.fieldnames

print(f"Header: {header}")
print("\nTabelle als Liste von dictionaries:")
print(tabelle)

print("\nKonvertierung der Zahlen")
for zeile in tabelle:
    for spalte in header:
        zeile[spalte] = int(zeile[spalte])  # Aus Zeichenketten Zahlen machen

print(tabelle)


# Fehler finden und korrigieren


# CSV-Datei korrigiert schreiben
with open("korrigiert.csv", "w") as csvfile:
    # Writer vorbereiten
    writer = csv.DictWriter(csvfile, fieldnames=header, dialect=dialect)
    # Header (erste Zeile) schreiben
    writer.writeheader()
    # Alle Zeilen schreiben
    writer.writerows(tabelle)
