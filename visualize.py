from cover.graph.plot import plot_arc, plot_target, plot_point
from cover.graph.figure import Point, Target
from data.genarate_data import get_data
from cover.find_candidate import find_arc_of_target, find_pareto_of_targets, find_candidates
from config.get_config import ROOT_PATH
from typing import List
import matplotlib.pyplot as plt


def plot_pareto(targets: List[Target], B: Point, tarc: List[Target] = None,
              figure=None, axes=None,
              c='b', marker='*', s=10,
              show=True,
              image_name='cover.png', title='pareto'):
    if figure is None and axes is None:
        figure, axes = plt.figure(), plt.gca()

    plt.scatter([B.x], [B.y], c='black', marker='*', s=10)
    plt.text(x=B.x + 0.5, y=B.y + 0.5, s='B', fontsize=12)

    plot_target(targets, c=c, marker=marker, s=s, axes=axes, figure=figure)
    if tarc is not None:
        plot_arc(tarc)
    plt.axis('scaled')
    plt.title(title)
    if show:
        plt.savefig(ROOT_PATH + '/figures/' + image_name)
        plt.show()
    else:
        plt.savefig(ROOT_PATH + '/figures/' + image_name)


def plot_candidate(targets: List[Target], B: Point):
    figure, axes = plt.figure(), plt.gca()
    plt.scatter([B.x], [B.y], c='black', marker='*', s=10)
    plt.text(x=B.x + 0.5, y=B.y + 0.5, s='B', fontsize=12)
    plot_target(targets, axes=axes, figure=figure)
    cans = find_candidates(targets, B)
    candidates = []
    for cans_pareto in cans:
        candidates.extend(cans_pareto)

    candidates = list(set(candidates))
    plot_point(candidates, c='r', marker='+', axes=axes, figure=figure,)
    n_candidates = len(candidates)
    qs = [t.q for t in targets]
    n_q = sum(qs)
    plt.title('N_Q:{}    N_CANDIDATE:{}    RATIO:{:.3f}'.format(n_q, n_candidates, n_candidates/n_q))
    plt.savefig(ROOT_PATH + '/figures/candidate.png')
    plt.axis('scaled')
    plt.show()


def main():
    B, targets = get_data()
    # targets = find_arc_of_target(targets)
    # paretos = find_pareto_of_targets(targets, B)

    # for i in range(len(paretos)):
    #     set_arc = []
    #     for t in paretos[i]:
    #         set_arc.extend(t.set_arc)
    #     plot_pareto(targets, B, tarc=paretos[i], c='C{}'.format(i),
    #                 image_name='pareto_{}.png'.format(i),
    #                 title='pareto_{}'.format(i))

    plot_candidate(targets, B)

if __name__ == '__main__':
    main()
