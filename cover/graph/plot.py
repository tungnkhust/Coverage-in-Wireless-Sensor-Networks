import math
import matplotlib.pyplot as plt
from matplotlib import patches
from cover.graph.figure import Point, Target, get_intersections_from_2_circle
import numpy as np
import yaml
import sys


ROOT_PATH = sys.path[1]

with open(ROOT_PATH + '/config.yaml', 'r') as pf:
    config = yaml.safe_load(pf)
    NUM_TARGET = config['NUM_TARGET']
    W = config['DOMAIN']['W']
    H = config['DOMAIN']['H']
    Rs = float(config['RADIUS']['SENSE'])

B = (np.random.randint(W), np.random.randint(H))
xs = [np.random.randint(W) for i in range(NUM_TARGET)]
ys = [np.random.randint(H) for j in range(NUM_TARGET)]

figure, axes = plt.figure(), plt.gca()
for i in range(NUM_TARGET):
    axes.add_patch(plt.Circle((xs[i], ys[i]), radius=Rs, color='g', fill=False))
plt.scatter(xs, ys, c='b', marker='*', s=30)
targets = []
for i in range(NUM_TARGET):
    targets.append(Target(Point(xs[i], ys[i]), id=i))
plt.scatter([B[0]], [B[1]], c='y', marker='+', s=10)
for i in range(NUM_TARGET):
    for j in range(i+1, NUM_TARGET):
        res = get_intersections_from_2_circle(targets[i].p, Rs, targets[j].p, Rs)
        if res == None:
            continue

        if isinstance(res, Point):
            plt.scatter([res.x], [res.y], c='r', marker='x', s=10)
        else:
            ip1 = res[0]
            ip2 = res[1]
            plt.scatter([ip1.x], [ip1.y], c='r', marker='x', s=10)
            plt.scatter([ip2.x], [ip2.y], c='r', marker='x', s=10)

plt.axis('scaled')
plt.show()

