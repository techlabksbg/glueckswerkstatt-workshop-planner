from plan import Plan

# WICHTIG: Damit die Dateien gefunden werden können, muss diese Programm im 
# Verzeichnis 'planung' ausgeführt werden. ('cd planung' in der Kommandozeile unten)

# Daten einlesen
plan = Plan("../data/2024.csv", "../data/2024m_w.csv")

# Einfach alle Teilnehmer mit Präferenzen nach Ihrer Wahl einplanen:
for s in range(plan.S):  # Für jede Teilnehmernummer
    if not plan.laueri[s]:   # falls Präferenzen angegeben wurden
        for t in range(plan.T):    # Für jedes Zeitfenster
            plan.schedule(s, t, plan.o[s][t])      # Teilnehmer s zur Zeit t in den t-ter Wahl einteilen

plan.report()

print("\n----------------------------\n\nMit eingeplanten Laueris:\n\n")

plan.laueris_einplanen()

plan.report()

plan.plan2csv("zuteilung.csv")
