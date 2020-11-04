from cover.graph.figure import Point

x = set()

p1 = Point(1, 1)
p2 = Point(1, 2)
p3 = Point(1, 1)


x.add(p1)
x.add(p2)
x.add(p3)

print(p1)
print(x)

d = []
d.remove(1)
print(d)