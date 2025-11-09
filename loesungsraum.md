# Lösungsraum
322 Teilnehmer, 22 Workshops

Mögliche Zuteilungen pro Teilnehmer (inkl. keine Workshop-Zuteilung): ca. $23 \cdot 22 = 506$

Mögliche Pläne: ca. $506^{322} \approx 10^{870}$. (Anzahl Elementarteilchen im Universum: $10^{80}$).

Je nach Einschränkung ist der Lösungsraum kleiner, aber wohl immer noch $>10^{100}$.



# Greedy
Schrittweise Aufgabe einer Lösung, wobei in jedem Schritt die lokal beste Variante (gierig) gewählt wird.

Vorteile: Sehr schnell und einfach.

Nachteile: Lösungen je nach Problem von eher schlechter Qualität. Es gibt aber Problemklassen, wo diese Strategie immer die optimale Lösung liefert.

## Planungsreihenfolgen
Fragen:
  * Findet der Greedy-Algorithmus mit der korrekten Reihenfolge der Teilnehmer eine optimale Lösung?
  * Gibt es für jede optimale Lösung eine Reihenfolge, mit der der Greedy-Algorithmus diese Lösung erzeugt?

Immerhin gibt es, je nach Implementation, mehr mögliche Reihenfolgen als Lösungen $(644!)^2 > 10^{870}$.


# Visualisierung
Alle Lösungen als Punkte in der Ebene. 

Wert der Zielfunktion gibt Höhe an: Es entsteht eine Landschaft.

Suche einer optimalen Lösung ist gleichbedeutend mit Finden des höchsten Gipfels.


# Tabu-Search

Move: Kleine Änderung an einer Lösung im Lösungsraum.

Tabu-Liste: Ein Move darf während der nächsten Schritte (Länge der Tabu-Liste) nicht rückgängig gemacht werden. Mögliche Ausnahme: man erhält eine neue beste Lösung.

Auswahl eines Moves: Zufällig, aber «gute» Moves sollen bevorzugt werden. Z.B. aus den 10 besten Moves, die nicht tabu sind, wird zufällig einer ausgewählt.

