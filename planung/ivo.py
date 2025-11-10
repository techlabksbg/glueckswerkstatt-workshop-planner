from plan import Plan
import random

# WICHTIG: Damit die Dateien gefunden werden können, muss diese Programm im 
# Verzeichnis 'planung' ausgeführt werden. ('cd planung' in der Kommandozeile unten)


def bester_workshop_planen(plan:Plan, s:int):
    randT = list(range(plan.T))
    
    randW = list(range(plan.W))
    random.shuffle(randW)  # Zufällige Liste mit allen Workshopnummern

    for w in plan.o[s]+randW:  # Workshops nach Priorität, dann zufällig
        if not w in plan.x[s]:  # s besucht w noch nicht
            random.shuffle(randT) # Liste mit Zeitslots verwürfeln
            for t in randT:
                if plan.x[s][t]==-1:    # s zur Zeit t noch unverplant
                    if plan.b[w][t]<plan.m[w]:  # w hat noch Platz zur Zeit t
                        plan.schedule(s,t,w)
                        return plan.p[s][w]  # Resultat ist score vom Workshop
                    




# Daten einlesen
plan = Plan("../data/2025.csv", "../data/2025m_w.csv")

def greedy(plan):
    randS = list(range(plan.S))
    random.shuffle(randS)  # Zufällige Reihenfolge der Teilnehmer
    for i in range(plan.T):  # 2x wiederholen
        for s in randS:
            if not plan.laueri[s]:
                bester_workshop_planen(plan,s)
        randS.reverse()

bestQ = 0
bestx = []
for i in range(1000):
    plan.reset()
    greedy(plan)
    if plan.Q > bestQ:
        bestQ = plan.Q
        bestx = plan.save()
        print(f"Neue beste Lösung {bestQ}")

plan.restore(bestx)

plan.laueris_einplanen()

plan.report()

plan.plan2csv("zuteilung.csv")
