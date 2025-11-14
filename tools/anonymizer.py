
# Lesen von CSV-Dateien, siehe https://docs.python.org/3/library/csv.html
import csv

# Kommandozeilenargumente
import sys
# Überprüfen, ob Dateien existieren etc.
import os.path
# Zufallszahlen
import random


######################
# Start vom Programm #
######################


# Genug Kommandozeilenargumente?
if len(sys.argv)!=3:
    print("Bitte Input- und Output-Dateien angeben (im CSV-Format)")
    quit(-1)

# Input- und Outputdatei
csv_in = sys.argv[1]
csv_out = sys.argv[2]

# Input existiert?
if not os.path.isfile(csv_in):
    print(f"Input Datei {csv_in} existiert nicht.")
    quit(-1)

# Output existiert noch nicht?
if os.path.isfile(csv_out):
    print(f"Die Output-Datei {csv_out} existiert bereits.")
    quit(-1)

# CSV Datei als Array von Dictionaries in die Variable tabelle einlesen
with open(csv_in, newline='') as csvfile:
    # CSV-Format erraten
    dialect = csv.Sniffer().sniff(csvfile.read(2048))
    csvfile.seek(0)
    # csv_reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
    # Datei mit erratenem Format einlesen
    csv_reader = csv.DictReader(csvfile, dialect=dialect)
    # Array mit allen Zeilen erstellen
    tabelle = [row for row in csv_reader]

# Reihenfolge im Array verwürfeln        
random.shuffle(tabelle)

# Dictionary und Zähler für Klassen
klassen = {}
klasse = 0

for student in range(len(tabelle)):
    # Klassennamen dieses Eintrags
    kl = tabelle[student]["Klasse"]
    # Falls Klasse zum ersten mal gesehen
    if not kl in klassen:
        # Aktuelle Nummer dieser Klasse zuordnen
        klassen[kl] = klasse
        # Anzahl gesehener Klassen erhöhen
        klasse += 1
    # Nummer der aktuellen Klasse
    klassennummer = klassen[kl]
    # Eintrag anonymisieren
    tabelle[student]["Name"] = f"student{student:03d}"
    tabelle[student]["Klasse"] = f"class{klassennummer:02d}"
    tabelle[student]["E-Mail"] = "no.mail"

# Anonymisierte Tabelle nach Klasse, dann Namen sortieren
tabelle.sort(key=lambda x:x["Klasse"]+x["Name"])

fields = ["Name", "Klasse", "1. Wahl", "2. Wahl", "3. Wahl", "4. Wahl"]
needed = [{k:zeile[k] for k in fields} for zeile in tabelle]


# CSV-Datei schreiben
with open(csv_out, "w") as csvfile:
    # Writer vorbereiten
    writer = csv.DictWriter(csvfile, fieldnames=fields, dialect=dialect)
    # Header (erste Zeile) schreiben
    writer.writeheader()
    # Alle Zeilen schreiben
    writer.writerows(needed)