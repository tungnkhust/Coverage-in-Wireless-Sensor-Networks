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

    return targets


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
    max_dominant = max([si.dominant for si in s_])
    res = [[]]*(max_dominant+1)
    for t in s_:
        res[t.dominant].append(t)
    for i, pareto in enumerate(res):
        far_target = {}
        for target in pareto:
            far_target[target] = distance(target, B)
        far_target = sorted(far_target.items(), key=lambda kv: kv[1], reverse=True)
        pareto = [item[0] for item in far_target]
        res[i] = pareto
    return res


def find_pareto(s: List[Target], B: Point):
    if len(s) == 0:
        return []
    if len(s) == 1:
        s[0].dominant = 0
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
    while all(ci is True for ci in check) is False:
        d0 = []
        for i in range(len(d)):
            if check[i] is False:
                if len(d[i]) == 0:
                    s[i].dominant = c
                    check[i] = True
                    d0.append(i)
        for i in d0:
            for j in range(len(d)):
                if i in d[j]:
                    d[j].remove(i)
        c += 1
    return s


def find_arc_of_target(targets: List[Target]):
    targets = get_close_target(targets)
    for i in range(NUM_TARGET):
        targets[i].find_coverage_arc()

    return targets


def find_candidates(targets: List[Target], B):
    targets = find_arc_of_target(targets)

    paretos = find_pareto_of_targets(targets, B)

    candidates = []
    for i, pareto in enumerate(paretos):
        close_target = {}
        for target in pareto:
            close_target[target] = target.num_close_targets()
        close_target = sorted(close_target.items(), key=lambda kv: kv[1], reverse=True)
        pareto = [item[0] for item in close_target]
        cans = []
        for t in pareto:
            cans.extend(t.get_candidate(B))
            t.located = True
        candidates.append(cans)
    return candidates