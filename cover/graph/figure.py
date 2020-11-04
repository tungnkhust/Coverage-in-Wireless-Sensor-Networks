import yaml
import sys
import numpy as np
from typing import Union, List
import math
from config.get_config import EPSILON, Rs


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.set_cover = []
        self.set_covered = []

    def degree(self):
        return len(self.set_cover)

    def __eq__(self, other):
        if (np.abs(self.x-other.x) <= EPSILON) and (np.abs(self.y-other.y) <= EPSILON):
            return True
        else:
            return False

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash('{}{}'.format(round(self.x, 2), round(self.y, 2)))


def midpoint(p1: Point, p2:Point):
    x = (p1.x + p2.x) / 2
    y = (p1.y + p2.y) / 2
    return Point(x, y)


def distance(p1: Union[Point, tuple], p2: Union[Point, tuple]):
    if isinstance(p1, tuple):
        p1 = Point(p1[0], p1[1])
    if isinstance(p2, tuple):
        p2 = Point(p2[0], p2[1])
    x_dis = np.abs(p1.x - p2.x)
    y_dis = np.abs(p1.y - p2.y)
    return np.sqrt(x_dis**2 + y_dis**2)


def cover(p1: Point, p2: Point, r=Rs):
    if distance(p1, p2) - r <= EPSILON:
        return True
    return False


def get_intersections_from_2_circle(p0: Point = None, r0=Rs, p1: Point = None, r1=Rs):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    if abs(d - (r0 + r1)) < EPSILON:
        x = (p0.x + p1.x)/2
        y = (p0.y + p1.y)/2
        return Point(x, y)
    # non intersecting
    if d - (r0 + r1) > EPSILON:
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

        return Point(x3, y3), Point(x4, y4)


def get_intersection_from_circle_and_point(c: Point = None, r=Rs, p: Point = None):
    d = distance(c, p)
    if d <= r:
        return None
    x = c.x + r/d*(p.x-c.x)
    y = c.y + r/d*(p.y-c.y)
    return Point(x, y)


def find_cover_of_point(p: Point = None, points: List[Point] = None):
    if len(points) == 0:
        return []
    set_cover = []
    for pi in points:
        if cover(p, pi, Rs):
            set_cover.append(pi)
    return set_cover


def cover_line(line: [Point, Point], p: Point):
    mid = midpoint(line[0], line[1])
    if cover(p, mid) and cover(p, line[0]) and cover(p, line[1]):
        return True
    else:
        return False


def find_cover_of_line(line: [Point, Point] = None, points: List[Point] = None):
    if len(points) == 0:
        return []
    set_cover = []
    for pi in points:
        if cover_line(line, pi):
            set_cover.append(pi)
    return set_cover


class Target(Point):
    def __init__(self, x, y, id, q):
        super(Target, self).__init__(x, y)
        self.x = x
        self.y = y
        self.id = id
        self.q = q
        self.d = -1
        self.candidate = False
        self.located = False
        self.set_arc = []
        self.set_close_targets = []
        self.set_intersection_points = []

    def num_covered(self):
        return len(self.set_covered)

    def num_close_targets(self):
        return len(self.set_close_targets)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return 'T{}({}, {}): {}'.format(self.id, self.x, self.y, self.d)

    def __str__(self):
        return 'T{}({}, {}): {}'.format(self.id, self.x, self.y, self.d)

    def find_close_target(self, targets):
        for t in targets:
            if self != t:
                if abs(distance(self, t) - 2 * Rs) < EPSILON:
                    self.set_close_targets.append(t)

    def find_intersection_point(self):
        for t in self.set_close_targets:
            res = get_intersections_from_2_circle(self, Rs, t, Rs)
            if res is None:
                continue

            if isinstance(res, Point):
                if res not in self.set_intersection_points:
                    self.set_intersection_points.append(res)
            else:
                ip1 = res[0]
                ip2 = res[1]
                if ip1 not in self.set_intersection_points:
                    self.set_intersection_points.append(ip1)
                if ip2 not in self.set_intersection_points:
                    self.set_intersection_points.append(ip2)

    def find_coverage_arc(self):
        if len(self.set_intersection_points) == 0:
            if len(self.set_close_targets) == 0:
                return
            self.find_intersection_point()
        set_close_targets = self.set_close_targets
        set_close_targets.append(self)
        for i, p in enumerate(self.set_intersection_points):
            self.set_intersection_points[i].set_cover = find_cover_of_point(p, set_close_targets)

        for i in range(len(self.set_intersection_points)):
            p1 = self.set_intersection_points[i]
            for j in range(i+1, len(self.set_intersection_points)):
                p2 = self.set_intersection_points[j]
                mid = midpoint(p1, p2)
                set_line_cover = find_cover_of_line([p1, p2], set_close_targets)
                line_degree = len(set_line_cover)
                if (line_degree == p1.degree()) or (line_degree == p2.degree()):
                    if p1.degree() != p2.degree() and (p1.degree() == 2 or p2.degree() == 2) and line_degree == 2:
                        if mid == midpoint(set_line_cover[0], set_line_cover[1]):
                            continue
                        else:
                            self.set_arc.append((p1, p2, line_degree))
                    else:
                        self.set_arc.append((p1, p2, line_degree))









