from data.genarate_data import get_data
from cover.find_candidate import find_candidates
from config.get_config import *


def main():
    total_nq = 0
    total_nc = 0
    for i in range(N_TEST):
        print('-'*30 + 'TEST {}'.format(i+1) + '-'*30)
        B, targets = get_data()
        qs = [t.q for t in targets]
        n_q = sum(qs)
        cans = find_candidates(targets, B)
        candidates = []
        for cans_pareto in cans:
            candidates.extend(cans_pareto)

        candidates = list(set(candidates))
        n_candidates = len(candidates)

        total_nq += n_q
        total_nc += n_candidates
        print('Total Q         :', n_q)
        print('Total candidates:', n_candidates)
        print("Ratio           : {:.2f}".format(n_candidates/n_q))

    print('*' * 30 + 'FINAL {}' + '*' * 30)
    print('Total Q         :', total_nq)
    print('Total candidates:', total_nc)
    print("Ratio           : {:.2f}".format(total_nc / total_nq))

if __name__ == '__main__':
    main()