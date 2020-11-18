import os
import numpy as np
from config.get_config import *
from cover.graph.figure import Target, Point


def get_data():
    if os.path.exists(ROOT_PATH + '/data/data.txt') is False or CHANGE_DATA:
        B = Point(np.random.randint(W), np.random.randint(H))
        xs = np.random.randint(W, size=NUM_TARGET)
        ys = np.random.randint(H, size=NUM_TARGET)
        qs = np.random.randint(low=Q_MIN, high=Q_MAX, size=NUM_TARGET)
        targets = [Target(xs[i], ys[i], i, qs[i]) for i in range(NUM_TARGET)]
        with open(ROOT_PATH + '/data/data.txt', 'w') as pf:
            pf.write('{} {}\n'.format(B.x, B.y))
            pf.write(' '.join([str(x) for x in xs]))
            pf.write('\n')
            pf.write(' '.join([str(y) for y in ys]))
            pf.write('\n')
            pf.write(' '.join([str(q) for q in qs]))
    else:
        with open(ROOT_PATH + '/data/data.txt', 'r') as pf:
            data = pf.readlines()
            B = data[0].replace('\n', '').split(' ')
            xs = data[1].replace('\n', '').split(' ')
            ys = data[2].replace('\n', '').split(' ')
            if CHANGE_Q:
                qs = np.random.randint(low=Q_MIN, high=Q_MAX, size=NUM_TARGET)
                with open(ROOT_PATH + '/data/data.txt', 'w') as pf:
                    pf.write('{} {}\n'.format(B[0], B[1]))
                    pf.write(' '.join([str(x) for x in xs]))
                    pf.write('\n')
                    pf.write(' '.join([str(y) for y in ys]))
                    pf.write('\n')
                    pf.write(' '.join([str(q) for q in qs]))
            else:
                qs = data[3].replace('\n', '').split(' ')
            B = Point(float(B[0]), float(B[1]))
            targets = [Target(float(xs[i]), float(ys[i]), i, int(qs[i])) for i in range(NUM_TARGET)]

    return B, targets


def generate_data(n_target=None, q_min=None, q_max=None):
    B = Point(np.random.randint(W), np.random.randint(H))
    xs = np.random.randint(W, size=n_target)
    ys = np.random.randint(H, size=n_target)
    qs = np.random.randint(low=q_min, high=q_max, size=n_target)
    targets = [Target(xs[i], ys[i], i, qs[i]) for i in range(n_target)]
    return B, targets