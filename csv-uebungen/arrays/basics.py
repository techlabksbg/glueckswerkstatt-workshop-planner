
# Array mit 3 Einträgen
a = [23,42,123]
print(f"a ist {a} und hat {len(a)} Elemente")
print(f"a[0]={a[0]}, a[2]={a[2]}")

a[1] = 4321
print(f"a ist jetzt {a}")

a.append(77)
print(f"Nach append: {a} mit Länge {len(a)}")


print("\n\nLoops\n------")
for e in a:
    print(f"e ist {e}")

for i,e in enumerate(a):
    print(f"Element mit Index {i} ist {e}")

print("\n\nQuadratzahlen\n------------")
quadrate = []
for i in range(10):
    quadrate.append(i*i)
print(f"Quadratzahlen {quadrate}")

q = [n*n for n in range(10)]
print(f"Quadrate als Einzeiler: {q}")

print("\n\nEinmaleins\n-----------")
xy = []   # Leeres Array
for y in range(5):
    xy.append([])
    for x in range(5):
        xy[-1].append(x*y) # Letztem Element von xy (also das vor dem x-loop leere Array) ein Element hinzufügen
print(f"Einmaleins: {xy}")
print(f"xy[4][3] = {xy[4][3]}")

print("\n\nBuchstaben\n-----------")
l = [chr(ord('A')+i) for i in range(26)]
print(l)
print("+".join(l))