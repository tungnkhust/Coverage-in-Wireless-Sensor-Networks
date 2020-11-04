from cover.graph.plot import *
from data.genarate_data import get_data
from cover.find_candidate import find_arc_of_target, find_pareto_of_targets


def visualize(targets: List[Target], B: Point, tarc: List[Target]=None, figure=None, axes=None, c='b', marker='*', s=10, show=True, image_name='cover.png'):
    if figure is None and axes is None:
        figure, axes = plt.figure(), plt.gca()

    plt.scatter([B.x], [B.y], c='black', marker='*', s=10)
    plt.text(x=B.x + 0.5, y=B.y + 0.5, s='B', fontsize=12)

    plot_target(targets, c=c, marker=marker, s=s, axes=axes, figure=figure)
    if tarc is not None:
        plot_arc(tarc)
    plt.axis('scaled')
    if show:
        plt.savefig(ROOT_PATH + '/figures/' + image_name)
        plt.show()


def main():
    B, targets = get_data()
    targets = find_arc_of_target(targets)
    paretos = find_pareto_of_targets(targets, B)
    # figure, axes = plt.figure(), plt.gca()
    for i in range(len(paretos)):
        set_arc = []
        for t in paretos[i]:
            set_arc.extend(t.set_arc)
        visualize(targets, B, tarc=paretos[i], c='C{}'.format(i), image_name='pareto_{}.png'.format(i))


if __name__ == '__main__':
    main()
