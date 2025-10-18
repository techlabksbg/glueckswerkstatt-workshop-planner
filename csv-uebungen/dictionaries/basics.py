

d = {"Alter":34, "Einkommen":6540, 
     "Vorname": "Hans", "Name": "Wurst"}

print(d)

print(f"Name ist {d["Name"]}, Alter {d["Alter"]}")

print("\nLoop über Schlüssel in d:")
for schluessel in d:
    print(f"  {schluessel}")

print("\nLoop über Schlüssel/Wert-Paare")
for schluessel,wert in d.items():
    print(f"{schluessel} -> {wert}")

print("\nLohnerhöhung")
d["Einkommen"] += 500 # Lohnerhöhung!
print(d)

print("\nSpesen")
d["Spesen"] = [40,60,20,42]
print(d)
print(f"Zweiter Speseneintrag: d[\"Spesen\"][1] ist {d["Spesen"][1]}")

print("\nSchlüssel vorhanden?")
if "Alter" in d: 
    print(f"Alter ist gespeichert, nämlich {d["Alter"]}")

if not "Zivilstand" in d:
    print("Kein Schlüssel Zivilstand in d")
