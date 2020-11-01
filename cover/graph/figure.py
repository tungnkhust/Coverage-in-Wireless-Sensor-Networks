import yaml
import sys
import numpy as np
from typing import Union
import math

ROOT_PATH = sys.path[1]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = id
        self.overlap = []

    def num_overlap(self):
        return len(self.overlap)

    def print(self):
        print('({}, {})'.format(self.x, self.y))


class Target:
    def __init__(self, p: Union[Point, tuple], id):
        if isinstance(p, tuple):
            p = Point(p[0], p[1])
        self.p = p
        self.id = id
        self.set_covered = []
        self.set_close_targets = []

    def num_covered(self):
        return len(self.set_covered)

    def num_close_targets(self):
        return len(self.set_close_targets)


def distance(p1: Union[Point, tuple], p2: Union[Point, tuple]):
    if isinstance(p1, tuple):
        p1 = Point(p1[0], p1[1])
    if isinstance(p2, tuple):
        p2 = Point(p2[0], p2[1])
    x_dis = np.abs(p1.x - p2.x)
    y_dis = np.abs(p1.y - p2.y)
    return np.sqrt(x_dis**2 + y_dis**2)


def get_intersections_from_2_circle(p0: Point, r0, p1: Point, r1):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles

    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        d_temp = distance((x3, y3), (x4, y4))
        if d_temp <= 0.5:
            return Point((x3+x4)/2, (y3+y4)/2)

        return (Point(x3, y3), Point(x4, y4))


def get_intersection_from_circle_and_line(center: Point, r, p: Point):
    
