import csv

class Plan:

    def __init__(self, csv_students, csv_workshops, T=2):
        self.T = T
        self.read_students(csv_students)
        self.read_workshops(csv_workshops)
        self.process_data()
        self.show_data()

    def show_data(self):
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
        # Workshop data
        self.W = len(self.workshop_data)
        self.workshops = [zeile["Workshop"] for zeile in self.workshop_data]
        self.m = [zeile["max Teilnehmer"] for zeile in self.workshop_data]

        self.students = []
        self.p = []
        self.k = []
        self.klassen = {}
        self.x = []
        self.o = []  # o[s] ist ein Array mit der Reihenfolge der Präferenzen
        for zeile in self.student_data:
            if zeile["1. Wahl"]!="":
                self.students.append(zeile["Name"])
                self.p.append([0 for i in range(self.W)])
                self.o.append([])
                for pref in range(1,5):
                    workshop = zeile[f"{pref}. Wahl"]
                    w = self.workshops.index(workshop)
                    self.p[-1][w] = 2**(4-pref)
                    self.o.append(w)
                klasse = zeile["Klasse"]
                if not klasse in self.klassen:
                    self.klassen[klasse] = len(self.klassen)
                self.k.append(self.klassen[klasse])
                self.x.appen([-1 for i in range(self.T)])
        self.S = len(self.students)

        # Beschränkungen
        # Anzahl Teilnehmer in Workshop w zur zeit t
        self.b = [[0 for t in range(self.T)] for w in range(self.W)]
        # Zielfunktion Q
        self.Q = 0


    # TODO: update self.Q
    def schedule(self, s,t,w):
        if w in self.x[s]:
            raise RuntimeError(f"Student {s} ist bereits im Workshop {w} verplant!")
        # Im Falle einer Umplanung, die Anzahl Teilnehmer am alten Workshop anpassen
        oldw = self.x[s][t]
        if oldw!=-1:
            self.b[oldw][t]-=1
            self.Q -= self.p[s][w]
        self.Q += self.p[s][w]
        self.x[s][t] = w
        # Anzahl Teilnehmer am Workshop w zur Zeit t anpassen
        self.b[w][t] += 1


    def unschedule(self, s,t):
        oldw = self.x[s][t]
        # Falls vorher geplant, Anzahl Teilnehmer anpassen
        if (oldw!=-1):
            self.b[oldw][t] -= 1
        self.x[s][t] = -1

    # Anzahl besuchte Workshops für Teilnehmer s
    def besuchte_Workshops(self, s):
        return self.x[s].count(lambda x:x!=-1)
    



    def read_students(self, csv_students):
        with open(csv_students) as csvfile:
            # CSV-Format erraten
            self.dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            # Datei mit erratenem Format einlesen
            csv_reader = csv.DictReader(csvfile, dialect=self.dialect)
            # Array mit allen Zeilen erstellen
            self.student_data = [row for row in csv_reader]
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




plan = Plan("../data/2024.csv", "../data/2024m_w.csv")
