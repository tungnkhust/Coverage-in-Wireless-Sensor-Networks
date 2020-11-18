from data.genarate_data import get_data
from cover.find_candidate import find_candidates
from config.get_config import *
import time
import pandas as pd


def run():
    total_nq = 0
    total_nc = 0
    with open(ROOT_PATH + '/results/T{}_QMax{}.txt'.format(NUM_TARGET, Q_MAX), 'w') as pf:
        pf.write('')

    pf = open(ROOT_PATH + '/results/T{}_QMax{}.txt'.format(NUM_TARGET, Q_MAX), 'a')
    t_start = time.time()
    for i in range(N_TEST):
        print('-' * 30 + 'TEST {}'.format(i + 1) + '-' * 30)
        print()
        pf.write('-' * 30 + 'TEST {}'.format(i + 1) + '-' * 30 + '\n')
        B, targets = get_data()
        xs = [t.x for t in targets]
        ys = [t.y for t in targets]
        qs = [t.q for t in targets]
        print(B)
        print(xs)
        print(ys)
        print(qs)
        pf.write(str(B) + '\n')
        pf.write(str(xs) + '\n')
        pf.write(str(ys) + '\n')
        pf.write(str(qs) + '\n')
        n_q = sum(qs)
        cans = find_candidates(targets, B)
        candidates = []
        for cans_pareto in cans:
            candidates.extend(cans_pareto)

        candidates = list(set(candidates))
        n_candidates = len(candidates)

        total_nq += n_q
        total_nc += n_candidates

        print('N_Q             :{}'.format(n_q))
        print('N candidates    :{}'.format(n_candidates))
        print("Ratio           :{:.2f}".format(n_q / n_candidates))
        pf.write('N_Q             :{}\n'.format(n_q))
        pf.write('N candidates    :{}\n'.format(n_candidates))
        pf.write("Ratio           :{:.2f}\n".format(total_nc / total_nq))

    t_end = time.time()
    print('*' * 30 + 'FINAL {}'.format(NUM_TARGET) + '*' * 30)
    print('Mean Q         :{}'.format(total_nq/N_TEST))
    print('Mean candidates:{}'.format(total_nc/N_TEST))
    print("Ratio          :{:.2f}".format(total_nc / total_nq))
    print('Mean Time      :{}s'.format((t_end-t_start)/N_TEST))
    pf.write('*' * 30 + 'FINAL {}'.format(NUM_TARGET) + '*' * 30 + '\n')
    pf.write('Mean Q         :{}\n'.format(total_nq/N_TEST))
    pf.write('Mean candidates:{}\n'.format(total_nc/N_TEST))
    pf.write('Ratio          :{:.2f}\n'.format(total_nc/total_nq))
    pf.write('Mean Time      :{}s\n'.format((t_end-t_start)/N_TEST))
    pf.close()


if __name__ == '__main__':
    run()
