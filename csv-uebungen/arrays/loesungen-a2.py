import random

# Reproduzierbare «zufällige» Würfelwürfe
random.seed(42)
a = [random.randrange(6)+1 for _ in range(600)]
print(a)

# Zählen Sie, wie viel mal die Zahl 6 im Array a gespeichert ist
# Geben Sie den Text "Es sind ... 6en gewürfelt worden" aus. (Lsg 107)

anzahl = 0
for w in a:
    if w==6:
        anzahl += 1

print(f"Es wurden {anzahl} 6en gewürfelt")

#Kurzform:

print(f"Mit count: {a.count(6)} 6en")


# Finden Sie die Länge und Startindex der längsten Untersequenz ohne 6en. (Lsg 384, 23)
# Überlegen Sie sich genau und detailliert, wie man das von Hand machen würde und 
# übersetzen Sie in Python

# Länge der längsten Untersequenz bis jetzt
laenge = 0
# Startposition der längsten Sequenz bis jetzt
start = 0

# Aktuelle Position und Länge
p = 0
l = 0
while p < len(a): 
    if a[p]!=6:  # Keine sechs? Aktuelle Länge erhöhen
        l+=1
    else: # Sechs gefunden. Ende einer Sequenz
        if l>laenge:  # Neue beste Sequenz, also merken
            laenge = l
            start = p - laenge
        l = 0   # 6er gefunden, also Sequenz der Länge 0
    p += 1   # Nächste Position prüfen

print(f"Längste Sequenz hat die Länge {laenge}, start an Position {start}")

        
