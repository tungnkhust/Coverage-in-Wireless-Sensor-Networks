import math
import matplotlib.pyplot as plt
from cover.graph.figure import *
from cover.find_candidate import find_pareto_of_targets, find_arc_of_target
from config.get_config import *
from data.genarate_data import get_data
from typing import List

B, targets = get_data()

targets, close_target = find_arc_of_target(targets)



figure, axes = plt.figure(), plt.gca()

plt.text(x=B.x + 1, y=B.y + 1, s='B', fontsize=12)
plt.scatter([B.x], [B.y], c='black', marker='*', s=10)
for t in targets:
    axes.add_patch(plt.Circle((t.x, t.y), radius=Rs, color='g', fill=False))
    plt.scatter([t.x], [t.y], c='k', marker='+', s=10)
    plt.text(x=t.x + 1, y=t.y + 1, s=str(t.id), fontsize=8)
# plt.plot([B.x, B.x], [-20, 120])
# plt.plot([-20, 120], [B.y, B.y], )
color = ['b', 'r', 'y', 'c', 'm', 'k']

paretos = find_pareto_of_targets(targets, B)

for temp in paretos[0]:
    plt.scatter([temp.x], [temp.y], c=color[0], marker='*', s=10)
    for arc in temp.set_arc:
        plt.plot([arc[0].x, arc[1].x], [arc[0].y, arc[1].y], 'b', '-')
        mid = midpoint(arc[0], arc[1])
        plt.text(x=mid.x, y=mid.y, s=str(arc[2]), fontsize=8, color='r')


plt.axis('scaled')
plt.savefig('graph.png')
plt.show()

