from plan import Plan
import random


def greedyFromScratch(plan:Plan):
    plan.reset()
    randomS = list(range(plan.S))
    random.shuffle(randomS)
    randomT = list(range(plan.T))
    random.shuffle(randomT)
    randomW = list(range(plan.W))
    random.shuffle(randomW)

    # Erste Wahl wo möglich:
    for s in randomS:
        if not plan.laueri[s]:
            ersteW = plan.o[s][0]
            random.shuffle(randomT)
            ok = False
            for t in randomT:
                if plan.b[ersteW][t] < plan.m[ersteW]:
                    #print(f"Plane {s} in erste Wahl {ersteW} zum Zeitpunkt {t} ein. x[s]={plan.x[s]}")
                    plan.schedule(s,t,ersteW)
                    ok = True
                    break
            if not ok: # Erste Wahl ist voll, also sofort alles einplanen
                planned = 0
                for w in plan.o[s]:
                    random.shuffle(randomT)
                    for t in randomT:
                        if plan.x[s][t] == -1 and plan.b[w][t] < plan.m[w]:
                            #print(f"Erste Wahl nicht möglich: Plane {s} in {w} zum Zeitpunkt {t} ein. x[s]={plan.x[s]}")
                            plan.schedule(s,t,w)
                            planned += 1
                            break
                    if planned==plan.T:
                        break

    # In umgekehrter Reihenfolge die restlichen Slots füllen
    randomS.reverse()
    for s in randomS:
        if not plan.laueri[s]:
            # Anzahl geplante Workshops
            planned = plan.T - plan.x[s].count(-1)
            for w in plan.o[s]:
                if not w in plan.x[s]:
                    random.shuffle(randomT)
                    for t in randomT:
                        if (plan.x[s][t]==-1):
                            if plan.b[w][t] < plan.m[w]:
                                #print(f"Auffüllen: Plane {s} in {w} zum Zeitpunkt {t} ein. x[s]={plan.x[s]}")
                                plan.schedule(s,t,w)
                                planned += 1
                                break
                if planned==plan.T:
                    break
            if planned<plan.T:
                # print(f" :-( {s} kann gar nicht in eine Präferenz eingeteilt werden: prios={plan.o[s]} x={plan.x[s]}")
                random.shuffle(randomW)
                for w in randomW:
                    if not w in plan.x[s]:
                        for t in range(plan.T):
                            if plan.x[s][t]==-1:
                                if plan.b[w][t] < plan.m[w]:
                                    plan.schedule(s,t,w)
                                    #print(f"Nicht auf Prio-Liste: Plane {s} in {w} zum Zeitpunkt {t} ein. x[s]={plan.x[s]}")
                                    planned+=1
                                    break
                    if planned==plan.T:
                        break
    plan.laueris_einplanen()


def improve(plan:Plan) -> bool:
    for w in range(plan.W):
        for t in range(plan.T):
            u = plan.umteilungen(w,t)
            best_s = list(u.keys())[0]
            best_w = u[best_s][0]["w"]
            best_dp = u[best_s][0]["dp"]
            if best_dp>0:
                print(f"Umteilung von {best_s} nach {best_w} zum Zeitpunkt {t} verbessert um {best_dp}")
                plan.schedule(best_s, t, best_w)
                return True
    return False       

# Daten einlesen
plan = Plan("../data/2024.csv", "../data/2024m_w.csv")

bestx : list[list[int]] = [[]]
bestQ = 0
for i in range(10000):
    greedyFromScratch(plan)
    if plan.Q>bestQ:
        bestx = plan.save()
        bestQ = plan.Q
        print(f"[{i}] bestQ = {bestQ}")

plan.restore(bestx)
plan.report()


plan.plan2csv("zuteilung.csv")

