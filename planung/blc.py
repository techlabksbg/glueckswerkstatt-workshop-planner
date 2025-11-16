from plan import Plan
from xlsxeporter import exportXLSX
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

# Plan Teilnehmer s zur t in die best-mögliche Priorität ein, oder einen zufälligen, noch freien Workshop
def bester_workshop_planen(plan:Plan, s:int, t:int):
    wlist = list(range(plan.W))
    random.shuffle(wlist)
    for w in plan.o[s]+wlist:  # Workshops nach Priorität plus zufällige Reihenfolge aller Workshops
        if not w in plan.x[s]:  # s besucht w noch nicht
            if plan.b[w][t]<plan.m[w]:  # w hat noch Platz zur Zeit t
                plan.schedule(s,t,w)
                return plan.p[s][w]  # Resultat ist score vom Workshop

def goodMoves(plan:Plan, s:int, t:int, tabu:list[bool]):
    moves = []
    wnow = plan.x[s][t]  # Aktuelle Einteilung (evlt. -1 wenn nicht eingeteilt)
    for w in plan.o[s]:  # Prioritäten durchgehen
        if not w in plan.x[s]: # w noch nicht eingeplant
            dp = plan.p[s][w]  
            if wnow!=-1:
                dp -= plan.p[s][wnow]
            if plan.b[w][t]==plan.m[w]: # Workshop wird mit Umteilung überfüllt?
                plan.s_in_w[w][t].sort(key=lambda ss:plan.p[ss][w])  # Erst Teilnehmer entfernen, die eine kleine Präferenz für den Workshop w haben.
                for ss in plan.s_in_w[w][t]:                    
                    if not tabu[ss]:
                        moves.append( {"s":s, "w":w, "outs":ss, "t":t, "dp":dp-plan.p[ss][w]} )
            else: # «Gratis» einplanen!
                moves.append({"s":s, "w":w, "outs":-1, "t":t, "dp":dp})
    return moves



def tabuSearch(plan:Plan, tabuListLength=4):
    """ Suchraum: Kein Workshop ist überbelegt, Teilnehmer sind z.T. nicht eingeteilt.
        Move: x[s][t] wird zu neuem Workshop eingeteilt, Teilenehmer in überbelegten Workshops werden ungeplant.
        Qualität eines Moves: dp
        Tabu-Liste: Teilnehmer.
    """

    plan.unschedule_laueris()

    tabutime = [0 for s in range(plan.S)]
    # Liste aller Teilnehmer, ohne Laueris
    nl = [s for s in range(plan.S) if not plan.laueri[s]]

    bestx = plan.save()
    bestQ = plan.Q
    for iteration in range(1000):
        tabu = list(map(lambda tt:tt>iteration, tabutime))
        # Teilnehmerliste sortieren, aufsteigend nach Score
        nl.sort(key=lambda s:plan.q[s]-16*plan.x[s].count(-1))  # Choose unplanned preverably
        candidates = [s for s in nl if random.random()<0.5 and not tabu[s]][0:5]
        #print(candidates)
        moves = []
        for s in candidates:
            for t in range(plan.T):
                moves += goodMoves(plan, s, t, tabu)
        moves.sort(key=lambda m:-m["dp"]- (16 if m['outs']==-1 else 0))  # Sort moves, largest dp first, prefer moves where no kicking out is involved
        move = moves[random.randrange(min(10,len(moves)))]
        # print(move)
        plan.schedule(move['s'], move['t'], move['w'])
        tabutime[move['s']] = iteration+tabuListLength
        if move['outs']!=-1:
            plan.unschedule(move['outs'], move['t'])
            tabutime[move['outs']] = iteration+tabuListLength
            bester_workshop_planen(plan, move['outs'], move['t'])
            
        if plan.Q > bestQ:
            bestx = plan.save()
            bestQ = plan.Q
            #print(f"New best solution with Q={bestQ}")
#        if iteration%100==0:
#            print(f"{iteration:5d}: Q={plan.Q:4d} best={bestQ:4d}  unplanned: {plan.numNonLaueris*plan.T-plan.numNonLauerisPlanned}")
    plan.restore(bestx)
    plan.laueris_einplanen()


def greedy_then_tabu(plan:Plan):
    nobetter = 0
    bestx = []
    bestQ = 0
    stat = [[] for i in range(20)]
    while nobetter<150:
        greedyFromScratch(plan)
        tlen = 10+random.randrange(7)
        tabuSearch(plan, tlen)
        stat[tlen]+=[plan.Q]
        if plan.Q>bestQ:
            nobetter = 0
            bestQ = plan.Q
            bestx = plan.save()
            print(f"bestQ: {bestQ}")
        nobetter+=1
    plan.restore(bestx)
    with open("tabustat.csv", "w") as f:
        f.write("tlen\tQ\n")
        for t in range(len(stat)):
            for v in stat[t]:
                f.write(f"{t}\t{v}\n")
    
    



# Daten einlesen
#plan = Plan("../data/2025.csv", "../data/2025m_w.csv")
plan = Plan("../secretdata/2025.csv", "../data/2025m_w.csv")


greedy_then_tabu(plan)

plan.report()
plan.plan2csv("zuteilung.csv")
exportXLSX(plan)

# Plan B, ohne Workshop G21
plan.m[20] = 0

greedy_then_tabu(plan)
plan.report()
plan.plan2csv("zuteilung-planB.csv")
exportXLSX(plan, "zuteilung-planB.xlsx")

