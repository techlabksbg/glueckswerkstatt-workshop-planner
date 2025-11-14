import csv

class Plan:
    """ Alle Daten für einen Plan
    Attribute:
        T: Anzahl Zeitslots
        W: Anzahl Workshops
        S: Anzahl Teilnehmende
        workshops[w]: Name vom Workshop w
        students[s]: Name vom Teilnehmer s
        m[w]: Maximale Teilnehmerzahl am Workshop w
        p[s][w]: Präferenz von Teilnehmer s für Workshop w
        k[s]: Nummer der Klasse von Teilnehmer s
        laueri[s]: True, wenn der Teilnehmer keine Präferenzen abgegeben hat
        o[s][i]: Für Nicht-Laueris, Liste der Workshops in der Reihenfolge der Präferenzen von i=0 (1. Prio) bis 3 (4. Prio)
        x[s][t]: Workshopnummer für Teilnehmer s zur Zeit t (-1 heisst ungeplant)
        b[w][t]: Anzahl geplante Teilnehmer im Workhop w zur Zeit t
        Q: Aktueller Wert der Zielfunktion
        q[s]: Score für Teilnehmer s

        student_data: Input-Datei der Studenten/Präferenzen als Liste von Dictionaries (Zeilen der CSV-Datei)
        workdhop_data: Input-Datei der Workshop-Definitionen als Liste von Dictionaries (Zeilen der CSV-Datei)

    Methoden:
        schedule(s,t,w): Teilnehmer s zur Zeit t in Workshop w ein- oder umplanen
        unschedule(s,t): Teilnehmer s zur Zeit t als ungeplant markieren
        
        save(): Kopie der x-Variable zum Zwischenspeichern einer Planung
        reset(): Alles auf ungeplant zurücksetzen
        restore(x): Plan mit gegebener x-Variable wieder herstellen

        teilnehmer(w,t): Liste mit Teilnehmernummern im Workshop w zur Zeit t
        ueberbelegt(): Liste mit Dictionaries mit einträgen "w" und "t" (überbelegte Workshops)
        umteilungen(w,t): Mögliche Umteilungen (ohne Überfüllen) mit Bewertungen (Differenz in Scorepunkten)
        worstStudents(): Liste mit Teilnehmernummern mit schlechtestem Score

    """
    def __init__(self, csv_students:str, csv_workshops:str, T:int=2):
        """ Initialisierung eines Plans, Parameter sind

        csv_students: Dateipfad zur CSV-Datei mit Teilnehmern/Präferenzen

        csv_workshop: Dateipfad zur CSV-Datei mit Workshop-Definitionen
        """
        self.T = T
        """ Anzahl Zeitslots """
        self.k : list[int]= []
        """ k[s] ist die Nummer der Klasse des Teilnehmers s """
        self.W : int = 0
        """ Anzahl Workshops """
        self.workshops : list[str]= []
        """ Arrary mit einem Dictionary zu jedem Workshop """
        self.m : list[int]= []
        """ m[w]: Maximale Teilnehmerzahl in Workshop w """
        self.students : list[str] = []
        """ students[s]: Name des Teilnehmers s """
        self.p :list[list[int]]= []
        """ p[s][w] ist die Präferenz von Teilnehmer s für Workshop w """
        self.klassen : dict = {}
        """ Name der Klasse als Schlüssel liefert als Wert Nummer der Klasse """
        self.x : list[list[int]]= []
        """ x[s][t] liefert den geplanten Workshop (-1, falls ungeplant) """
        self.o : list[list[int]]= []
        """ o[s] ist ein Array mit der Reihenfolge der Workshopnummern nach Präferenzen """
        self.laueri :list[bool] = []
        """ laueri[s] ist True, wenn keine Präferenzen angegeben wurden. """
        self.q : list[int] = []
        """ q[s] ist das Score für Teilnehmer s """
        self.Q : int = 0
        """ Summe alle Teilnehmerscores"""
        self.b : list[list[int]]= []
        """ b[w][t] ist die Anzahl geplanter Teilnehmer in Workshop w zur zeit t """
        self.s_in_w : list[list[list[int]]] = []
        """ s_in_w[w][t] ist eine Liste mit allen Teilnehmern eines Workshops zur Zeit t """
        self.allNonLauerisPlanned : bool = False
        """ True, wenn alle nicht-Laueris in T (2) Workshops eingeteilt sind """
        self.numNonLauerisPlanned : int = 0
        """ Anzahl eingeplanter nicht-Laueris """
        self.numNonLaueris : int  = 0
        """ Anazahl nicht-laueris """

        self.read_students(csv_students)
        self.read_workshops(csv_workshops)
        self.process_data()
        #self.show_data()

    def show_data(self):
        """ Zeigt die eingelesenen Daten an """
        print(f"Zeitfenster T={self.T}")
        print(f"Anzahl Workshops W={self.W}")
        print(f"   {self.workshops}")
        print(f"   m_w = {self.m}")
        print(f"Anzahl Teilnhemer S={self.S}")
        print(f"Präferenzen für die ersten drei Teilehmer:")
        for pref in self.p[0:3]:
            print(f"   {pref}")
        print(f"Klassen für die Teilnehmer:")
        print(self.k)

    def process_data(self):
        """ Konvertiert die eingelesenen Daten in die nötigen Variablen """
        self.W = len(self.workshop_data)
        """ Anzahl Workshops """
        self.workshops = [zeile["Workshop"] for zeile in self.workshop_data]
        """ Arrary mit einem Dictionary zu jedem Workshop """
        self.m = [int(zeile["max Teilnehmer"]) for zeile in self.workshop_data]
        """ m[w]: Maximale Teilnehmerzahl in Workshop w """

        self.students = []
        """ students[s]: Name des Teilnehmers s """
        self.p = []
        """ p[s][w] ist die Präferenz von Teilnehmer s für Workshop w """
        self.klassen = {}
        """ Name der Klasse als Schlüssel liefert als Wert Nummer der Klasse """
        self.x = []
        """ x[s][t] liefert den geplanten Workshop (-1, falls ungeplant) """
        self.o = []  
        """ o[s] ist ein Array mit der Reihenfolge der Workshopnummern nach Präferenzen """
        self.laueri = []
        """ laueri[s] ist True, wenn keine Präferenzen angegeben wurden. """
        for zeile in self.student_data:
            self.students.append(zeile["Name"])
            self.p.append([0 for i in range(self.W)])
            self.o.append([])
            klasse = zeile["Klasse"]
            if not klasse in self.klassen:
                self.klassen[klasse] = len(self.klassen)
            self.k.append(self.klassen[klasse])
            self.x.append([-1 for i in range(self.T)])
            self.laueri.append(zeile["1. Wahl"]=="")
            if not self.laueri[-1]:     # Teilnehmer mit Präferenzen
                self.numNonLaueris+=1
                for pref in range(1,5):
                    workshop = zeile[f"{pref}. Wahl"]
                    w = self.workshops.index(workshop)
                    self.p[-1][w] = 2**(4-pref)
                    self.o[-1].append(w)
            else:  # Teilnehmer ohne Präferenzen
                self.o[-1] = [-1 for _ in range(self.W)]


        self.S = len(self.students)
        """ Anzahl Teilnehmende """
        self.q = [0 for s in range(self.S)]
        """ q[s]: Aktueller Score für Teilnehmer s """

        self.s_in_w = [[[] for t in range(self.T)] for w in range(self.W)]

        # Beschränkungen
        self.b = [[0 for t in range(self.T)] for w in range(self.W)]
        """ b[w][t] ist die Anzahl geplanter Teilnehmer in Workshop w zur zeit t """
        self.Q = 0
        """ aktueller Wert der Zielfunktion Q """


    def schedule(self, s:int,t:int,w:int) -> None:
        """ Den Teilnehmer s zur Zeit t in den Workshop w einplanen """
        if w in self.x[s]:
            raise RuntimeError(f"Student {s} ist bereits im Workshop {w} verplant!")
        # Im Falle einer Umplanung, die Anzahl Teilnehmer am alten Workshop anpassen
        oldw = self.x[s][t]
        if oldw!=-1:
            self.b[oldw][t]-=1
            self.Q -= self.p[s][oldw]
            self.q[s] -= self.p[s][oldw]
            self.s_in_w[oldw][t].remove(s)
            if not self.laueri[s]:
                self.numNonLauerisPlanned -= 1
        self.Q += self.p[s][w]
        self.q[s] += self.p[s][w]
        self.x[s][t] = w
        self.s_in_w[w][t].append(s)
        # Anzahl Teilnehmer am Workshop w zur Zeit t anpassen
        self.b[w][t] += 1
        if not self.laueri[s]:
            self.numNonLauerisPlanned += 1
            self.allNonLauerisPlanned = self.T*self.numNonLaueris == self.numNonLauerisPlanned


    def unschedule(self, s,t):
        """ Teilnehmer s im Zeitslot t wieder aus dem Plan entfernen (dann ungeplant)"""
        oldw = self.x[s][t]
        # Falls vorher geplant, Anzahl Teilnehmer anpassen
        if (oldw!=-1):
            self.b[oldw][t] -= 1
            self.Q -= self.p[s][oldw]
            self.q[s] -= self.p[s][oldw]
            self.s_in_w[oldw][t].remove(s)
            self.x[s][t] = -1
            if not self.laueri[s]:
                self.numNonLauerisPlanned -= 1
                self.allNonLauerisPlanned = False

    def unschedule_laueris(self):
        """ Entfernt alle Laueris aus dem Plan """
        for s in range(self.S):
            if self.laueri[s]:
                for t in range(self.T):
                    self.unschedule(s,t)


    def besuchte_Workshops(self, s:int) -> int:
        """ berechnet die Anzahl besuchter Workshops für Teilnehmer s """
        return self.T-self.x[s].count(-1)
    



    def read_students(self, csv_students):
        with open(csv_students) as csvfile:
            # CSV-Format erraten
            self.dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            # Datei mit erratenem Format einlesen
            csv_reader = csv.DictReader(csvfile, dialect=self.dialect)
            # Array mit allen Zeilen erstellen
            self.student_data : list[dict[str,str]]= [row for row in csv_reader]
            """ Teilnehmerdaten aus Nesa Export """
            self.student_header = csv_reader.fieldnames

    def read_workshops(self, csv_workshops):
        with open(csv_workshops) as csvfile:
            # CSV-Format erraten
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            # Datei mit erratenem Format einlesen
            csv_reader = csv.DictReader(csvfile, dialect=dialect)
            # Array mit allen Zeilen erstellen
            self.workshop_data = [row for row in csv_reader]

    def laueris_einplanen(self):
        """ Plant alle Laueris in den jeweils am wenigsten belegten Workshop ein."""
        for s in range(self.S):
            if self.laueri[s]:   # Laueri?
                for t in range(self.T):
                    if self.x[s][t]==-1: # noch unverplant?
                        minB = self.S   # Viel zu grosser Wert
                        bestW = -1      # Bester Workshop 
                        for w in range(self.W):
                            # Workshop mit kleinerer Belegung als der kleinste bis jetzt
                            # und Workshop noch nicht ausgebucht
                            # und Workshop noch nicht vom Teilnehmer s besucht
                            if self.b[w][t]<minB and self.b[w][t]<self.m[w] and not w in self.x[s]:
                                # Neuer bester Workshop merken
                                minB = self.b[w][t]
                                bestW = w
                        # Workshop einplanen
                        self.schedule(s,t,bestW)


    def report(self):
        """ Gibt einen Report auf die Konsole aus """
        print(f"Zielfunktion Q = {self.Q}\n")
        print("Workshops:")
        ok = True
        for w in range(self.W):
            res = f"{self.workshops[w]} (max {self.m[w]}) "
            overbooked = False
            for t in range(self.T):
                res += f" {self.b[w][t]}"
                if self.b[w][t]>self.m[w]:
                    overbooked = True
            if overbooked:
                print("❌ " + res)
                ok = False
        if ok:
            print("✅ Kein Workshop ist überbelegt.")
        
        print("\nTeilnehmer:")
        ok = True
        totalUnplanned = 0
        histogramm = [0 for i in range(max(self.q)+1)]
        for s in range(self.S):
            if not self.laueri[s]:
                histogramm[self.q[s]] += 1
            if self.x[s].count(-1)>0:
                if ok:
                    print(f"❌ Teilnehmer {self.students[s]} muss noch zu {self.x[s].count(-1)} workshops zugeteilt werden.")
                totalUnplanned += 1
                ok = False
            else: # check if all workshops are different
                if len(set(self.x[s]))!=self.T:
                    print(f"❌❌❌ Teilnehmer {s} besucht einen Workshop mehrfach: Geplant: {self.x[s]} ❌❌❌")
                    ok = False

        if ok:
            print("✅ Alle Teilnehmer sind eingeplant.")
        else:
            print(f" Total sind {totalUnplanned} Teilnehmer nicht vollständig oder mit Mehrfachbsuch eingeplant")

        legende = ["keine Wahl", "nur 4. Wahl", "nur 3. Wahl", "3. & 4. Wahl", "nur 2. Wahl", "2. & 4. Wahl", "2. & 3. Wahl", "",
                   "nur 1. Wahl", "1. & 4. Wahl", "1. & 3. Wahl", "", "1. & 2. Wahl"]
        
        print("\nScores:")        
        for i,w in enumerate(histogramm):
            if w>0:
                print(f"{i:2d} Punkte: {w:3d} Teilnehmer mit  {legende[i]:15s}  {w/self.numNonLaueris*100:2.1f}%   (mit Laueris {w/self.S*100:2.1f}%)")
        

    def plan2csv(self, datei:str):
        """ Schreibt den Gesamtplan in eine CSV-Datei"""
        data = []
        # Tabelle befüllen
        for s in range(self.S):
            for t in range(self.T):
                w = self.x[s][t]
                kursname = self.workshops[w]+f".{t+1}"
                h = {"Klasse": kursname, "Schüler/Schülerin" : self.student_data[s]["Name"]}
                data.append(h)
        # Tabelle als CSV rausschreiben
        with open(datei, "w") as csvfile:
            # Writer vorbereiten
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), dialect=self.dialect)
            # Header (erste Zeile) schreiben
            writer.writeheader()
            # Alle Zeilen schreiben
            writer.writerows(data)
                


    def teilnehmer(self, w:int,t:int) -> list[int] :
        """ Liefert eine (möglicherweise leere) Liste mit Teilnehmernummern, die zur Zeit t im Workshop w eingeteilt sind """
        return [s for s in range(self.S) if self.x[s][t]==w]  # Alle Teilnehmer am Workshop w zur Zeit t

    def ueberbelegt(self) -> list[dict[str,int]]:
        """ Liefert eine Liste von dictionaries mit keys "w" und "t" der überbelegten workshops. """
        res = []
        for w in range(self.W):
            for t in range(self.T):
                if self.b[w][t]>self.m[w]:
                    res.append({"w":w, "t":t})
        return res

    def umteilungen(self, w:int, t:int) -> dict[int, list[dict[str, int]]]:
        """ Berechnet alle möglichen Umteilungen (ohne Überfüllen von Workshops) der Teilnehmer von Workshop w zur Zeit t.
            Liefert einen nach Scoreänderung sortierten dictionary mit Teilnehmernummer als Schlüssel und Folgenden Werten:
            eine nach Scoreänderung sortierte Liste mit dictionaries mit Schlüsseln "w" (Workshopnummer) und "dp" (Scoreänderung).
            d = plan.umteilungen(w,t)
            best_s = d.keys()[0]
            best_w = d[best_s][0]["w"]
            best_dp = d[best_s][0]["dp"]
        """
        res = {}
        for s in self.teilnehmer(w,t):
            res[s] = []
            for otherw in range(self.W):
                if otherw != w and self.b[otherw][t] < self.m[otherw] and (not otherw in self.x[s]):
                    res[s].append({"w":otherw, "dp":self.p[s][otherw]-self.p[s][w]})
            res[s].sort(key=lambda e:-e["dp"])  # Absteigend nach Scoreänderung sortieren

        # Teilnehmer absteigend nach Scoreänderung sortieren.
        return {key:res[key] for key in sorted(res.keys(), key=lambda s:-res[s][0]["dp"])}
    
    def worstStudents(self) -> list[int]:
        """ Liefert eine Liste der nicht-Laueris mit den schlechtesten Scores """
        worstScore = 99999
        worstStuds = []
        for s in range(self.S):
            if not self.laueri[s]:
                if self.q[s]<worstScore:
                    worstScore = self.q[s]
                    worstStuds = [s]
                elif self.q[s]==worstScore:
                    worstStuds.append(s)
        return worstStuds

    def upperBound(self) -> int:
        frei = [self.m[w]*self.T for w in range(self.W)]  # Freie Plätze in Workshop w (Summe aller Zeitslots)
        eingeteilt = [0 for s in range(self.S)]  # Anzahl workshops in die Teilnehmer s eingeteilt ist.
        upperQ = 0
        for prio in range(4):
            for s in range(self.S):
                if not self.laueri[s] and eingeteilt[s]<self.T:
                    w = self.o[s][prio]
                    if frei[w]>0:
                        frei[w]-=1
                        upperQ += 2**(3-prio)
                        eingeteilt[s]+=1
        return upperQ




    def save(self) -> list[list[int]]:
        """ Gibt eine Kopie der x-Variable zurÜck, um einen Plan zu speichern."""
        return [xx.copy() for xx in self.x]
    
    def reset(self) -> None:
        """ Setzt den aktuellen Plan zurück (nichts eingeplant) """
        self.x = [[-1 for t in range(self.T)] for s in range(self.S)]
        self.q = [0 for s in range(self.S)]
        self.b = [[0 for t in range(self.T)] for w in range(self.W)]
        self.s_in_w = [[[] for t in range(self.T)] for w in range(self.W)]
        self.Q = 0
        self.numNonLauerisPlanned = 0
        self.allNonLauerisPlanned = False

    def restore(self, x:list[list[int]]) -> None:
        """ Lädt den Plan von der Variablen x """
        # x kopieren
        self.x = [[x[s][t] for t in range(self.T)] for s in range(self.S)]
        # q berechnen
        for s in range(self.S):
            self.q[s] = 0
            for w in self.x[s]:
                if (w!=-1):
                    self.q[s] += self.p[s][w]
        # Q
        self.Q = sum(self.q)
        # b
        self.b = [[0 for t in range(self.T)] for w in range(self.W)]
        self.numNonLauerisPlanned = 0
        for s in range(self.S):
            for t in range(self.T):
                w = self.x[s][t]
                if w!=-1:
                    self.b[w][t] += 1
                    if not self.laueri[s]:
                        self.numNonLauerisPlanned += 1
        # s_in_w
        self.s_in_w = [[[s for s in range(self.S) if self.x[s][t]==w] for t in range(self.T)] for w in range(self.W)]

