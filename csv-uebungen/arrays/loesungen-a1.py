# 5 Lösungvorschläge

a = []
for i in range(103,1000,17):
    a.append(i)
print(a)


b = []
for i in range(100,1000):
    if i%17 == 1:
        b.append(i)
print(b)


c=[]
n = (100//17+1)*17+1   # // ist die Ganzzahldivision (auf nächste ganze Zahl abgerundet)
while n<1000:
    c.append(n)
    n+=17
print(c)


d = [i for i in range(103,1000,17)]
print(d)


e = []
for i in range(6,1000//17+1):
    e.append(i*17+1)
print(e)