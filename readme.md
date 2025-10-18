# Vorbereitende Aufgaben
Siehe [csv-uebungen/readme.md](csv-uebungen/readme.md)

# Workshop Planung

Um die Programmierung etwas zu vereinfachen, sind alle Indizies 0-basiert.

## Daten
  * Es gibt $T=2$ Zeitfenster $t=0, 1$.
  * Es gibt $W$ (gut 20) Workshops $w=0,1,2,\ldots, W-1$.
  * Jeder Workshop $w$ hat hat eine maximale Teilnehmeranzahl $m_w$.
  * Es gibt $S$ (ca. 320) Teilnehmer $s=0,1,2,\ldots, S-1$.
  * Jeder Teilnehmer $s$ hat eine Präferenz $p_{s,w}$ für jeden Workshop $w$.
    * Z.B. 8,4,2,1,0,0,0,... für erste, zweite, dritte, vierte Wahl etc.
  * Jeder Teilnehmer $s$ hat eine Klasse $k_s$ (etwa 0 bis 15).

## Entscheidungsvariablen
  * 0-1 Variablen $y_{s,t,w}$, die genau dann 1 sind, wenn der Teilnehmer $s$ im Zeitfenster $t$ dem Workshop $w$ zugeteilt wurde.

Daraus ergibt sich die Zuteilung vom Teilnehmer $s$ zur Zeit $t$ durch
$$x_{s,t} = \sum_{w} w \cdot y_{s,t,w}$$

## Beschränkungen

Jeder Teilnehmer besucht $T$ Workshops:
$$ \sum_{t,w} y_{s,t,w} = T \quad \forall s $$

Jeder Teilnehmer besucht jeden Workshop höchstens einmal:
$$ \sum_{t} y_{s,t,w} \leq 1 \quad \forall s,w $$

Keine Überbelegung von Workshops:
$$ b_{w,t} = \sum_{s} y_{s,t,w} < m_w \quad \forall w,t $$

$b_{w,t}$ zählt die Teilnehmer am Workshop $w$ im Zeitfenster $t$.

### Optionale Beschränkungen
Die Anzahl Teilnehmer in einem Workshop aus der gleichen Klasse soll beschränkt werden, entweder absolut (auf z.B. 10), oder der Unterschied
der Anzahl Teilnehmer einer Klasse in den verschiedenen Zeitfenstern ist «klein».



## Zielfunktion

$$ \max Q = \sum_s q_s $$

wobei $q_s$ ein Mass für die Erfüllung der Präferenzen von Teilnehmer $s$:
$$
q_s = \sum_{t,w} y_{s,t,w} \cdot p_{s,w}
$$

