import sys
import numpy as np
import yaml
from cover.graph.figure import Point, Target
from cover.graph.figure import distance


ROOT_PATH = sys.path[1]

with open(ROOT_PATH + '/config.yaml', 'r') as pf:
    config = yaml.safe_load(pf)
    NUM_TARGET = config['NUM_TARGET']
    W = config['DOMAIN']['W']
    H = config['DOMAIN']['H']
    Rs = config['RADIUS']['SENSE']

xs = [np.random.randint(W) for i in range(NUM_TARGET)]
ys = [np.random.randint(H) for j in range(NUM_TARGET)]

targets = []
for i in range(NUM_TARGET):
    targets.append(Target(Point(xs[i], ys[i]), i+1))

for i in range(NUM_TARGET):
    for j in range(i, NUM_TARGET):
        if(i != j):
            if distance(targets[i].p, targets[j].p) <= Rs:
                targets[i].set_close_targets.append(targets[j])
                targets[j].set_close_targets.append(targets[i])

close_target = {}

for target in targets:
    close_target[target.id] = target.num_close_targets()
close_target = sorted(close_target.items(), key=lambda kv: kv[1], reverse=True)

print(close_target)