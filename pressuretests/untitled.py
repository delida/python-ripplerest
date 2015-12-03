a = []
for i in range(1000):
    a.append(i)

fo = open("tmpresult.txt", "r")
lines = fo.readlines()
for l in lines:
    n, _, _ = l.split(":::")
    a.pop(a.index(int(n)))
fo.close()
print a, len(a)
