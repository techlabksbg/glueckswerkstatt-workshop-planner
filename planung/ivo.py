from plan import Plan
import random

# WICHTIG: Damit die Dateien gefunden werden können, muss diese Programm im 
# Verzeichnis 'planung' ausgeführt werden. ('cd planung' in der Kommandozeile unten)


def bester_workshop_planen(plan:Plan, s:int):
    randT = list(range(plan.T))
    for w in plan.o[s]:  # Workshops nach Priorität
        if not w in plan.x[s]:  # s besucht w noch nicht
            random.shuffle(randT) # Liste mit Zeitslots verwürfeln
            for t in randT:
                if plan.x[s][t]==-1:    # s zur Zeit t noch unverplant
                    if plan.b[w][t]<plan.m[w]:  # w hat noch Platz zur Zeit t
                        plan.schedule(s,t,w)
                        return plan.p[s][w]  # Resultat ist score vom Workshop
                    




# Daten einlesen
plan = Plan("../data/2024.csv", "../data/2024m_w.csv")

for i in range(plan.T):  # 2x wiederholen
    randS = list(range(plan.S))
    random.shuffle(randS)  # Zufällige Reihenfolge der Teilnehmer
    for s in randS:
        if not plan.laueri[s]:
            bester_workshop_planen(plan,s)


plan.laueris_einplanen()

plan.report()

plan.plan2csv("zuteilung.csv")
