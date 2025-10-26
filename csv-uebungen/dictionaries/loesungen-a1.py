import random

random.seed(42)
namen = [["Cloe", "Shreya", "Adrian", "Jaron", "Paulina", "Ashlyn", "Sheyla", "Halle", "Giselle", "Alvaro"][int(random.random()**1.5*10)] for _ in range(1000)]
print(namen)

# Zählen Sie, wie oft welcher Name vorkommt
# Erstellen Sie dazu ein dictionary mit den Namen als Schlüsseln und der Anzahl als Wert

# Leerer dictionary
anzahl = {}

for name in namen:
    # Gibt es den Schlüssel name schon?
    if name in anzahl:
        # Falls ja, Eintrag um 1 erhöhen
        anzahl[name] += 1
    else:
        # Ansonsten Eintrag mit dem Wert 1 erstellen
        anzahl[name] = 1

print(anzahl)




# Schlüsselliste nach anzahl absteigend sortieren 
nn = sorted(anzahl.keys(), key=lambda name:-anzahl[name])
# Ausgaben
for name in nn:
    print(f"{name}\t {anzahl[name]:3d}")
