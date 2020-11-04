import sys
import numpy as np
import yaml
from cover.graph.figure import Point, Target
from cover.graph.figure import distance, get_intersection_from_circle_and_point, get_intersections_from_2_circle
from data.genarate_data import get_data
from config.get_config import *
from typing import List


def get_close_target(targets):
    for i in range(NUM_TARGET):
        for j in range(i, NUM_TARGET):
            if i != j:
                if distance(targets[i], targets[j]) <= 2 * Rs:
                    targets[i].set_close_targets.append(targets[j])
                    targets[j].set_close_targets.append(targets[i])
    close_target = {}
    for target in targets:
        close_target[target] = target.num_close_targets()
    close_target = sorted(close_target.items(), key=lambda kv: kv[1], reverse=True)
    return targets, close_target


def find_pareto_of_targets(targets: List[Target], B: Point):
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    for t in targets:
        if (t.x >= B.x) and (t.y >= B.y):
            s1.append(t)
        elif (t.x > B.x) and (t.y < B.y):
            s2.append(t)
        elif (t.x <= B.x) and (t.y <= B.y):
            s3.append(t)
        elif (t.x < B.x) and (t.y > B.y):
            s4.append(t)
    s = [s1, s2, s3, s4]
    s_ = []
    for si in s:
        s_.extend(find_pareto(si, B))

    res = [[]]
    for t in s_:
        if t.d < len(res):
            res[t.d].append(t)
        else:
            res.append([])
            res[t.d].append(t)

    return res


def find_pareto(s: List[Target], B: Point):
    if len(s) == 0:
        return []
    if len(s) == 1:
        s[0].d = 0
    temp = [(np.abs(t.x - B.x), np.abs(t.y - B.y)) for t in s]
    d = []
    for i in range(len(s)):
        di = []
        for j in range(len(s)):
            if i != j:
                if (temp[j][0] >= temp[i][0]) and (temp[j][1] >= temp[i][1]):
                    if temp[j][0] > temp[i][0] or temp[j][1] > temp[i][1]:
                        di.append(j)
        d.append(di)

    check = [False] * len(d)
    c = 0
    while all(c is True for c in check) is False:
        d0 = []
        for i in range(len(d)):
            if check[i] is False:
                if len(d[i]) == 0:
                    s[i].d = c
                    check[i] = True
                    d0.append(i)
        for i in d0:
            for j in range(len(d)):
                if i in d[j]:
                    d[j].remove(i)
        c += 1
    return s


def find_arc_of_target(targets: List[Target]):
    targets, close_target = get_close_target(targets)
    for i in range(NUM_TARGET):
        targets[i].find_coverage_arc()

    return targets, close_target

# B, targets = get_data()
#
# find_pareto_of_targets(targets, B)