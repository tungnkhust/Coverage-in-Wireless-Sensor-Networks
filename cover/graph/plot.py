import math
import matplotlib.pyplot as plt
from cover.graph.figure import *
from cover.find_candidate import find_pareto_of_targets, find_arc_of_target
from config.get_config import *
from data.genarate_data import get_data
from typing import List


def plot_target(targets: List[Target], c='b', marker='*', s=10, plot_circel=True, figure=None, axes=None):
    if figure is None and axes is None:
        figure, axes = plt.figure(), plt.gca()

    for t in targets:
        plt.scatter([t.x], [t.y], c=c, marker=marker, s=s)
        plt.text(x=t.x + 0.5, y=t.y + 0.5, s=str(t.q), fontsize=8)
        if plot_circel:
            axes.add_patch(plt.Circle((t.x, t.y), radius=Rs, color='g', fill=False))


def plot_point(targets: List[Point], c='b', marker='*', linewidths=10, figure=None, axes=None):
    if figure is None and axes is None:
        figure, axes = plt.figure(), plt.gca()

    for t in targets:
        plt.scatter([t.x], [t.y], c=c, marker=marker, linewidths=linewidths)


def plot_arc(targets: List[Target]):
    for j, t in enumerate(targets):
        for arc in t.set_arc:
            plt.plot([arc.p1.x, arc.p2.x], [arc.p1.y, arc.p2.y], 'C{}'.format(j % 10), '-')
            mid = midpoint(arc.p1, arc.p2)
            plt.text(x=mid.x, y=mid.y, s=str(arc.degree), fontsize=8, color='r')




