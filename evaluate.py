from data.genarate_data import generate_data
from cover.find_candidate import find_candidates
from config.get_config import *
import time
import pandas as pd


def test_find_candidate(n_test, n_target, q_min, q_max):
    total_nq = 0
    total_nc = 0
    with open(ROOT_PATH + '/results/T{}_QMax{}.txt'.format(n_target, q_max), 'w') as pf:
        pf.write('')

    pf = open(ROOT_PATH + '/results/T{}_QMax{}.txt'.format(n_target, q_max), 'a')
    t_start = time.time()
    for i in range(n_test):
        print('-' * 30 + 'TEST {}'.format(i + 1) + '-' * 30)
        pf.write('-' * 30 + 'TEST {}'.format(i + 1) + '-' * 30 + '\n')
        B, targets = generate_data(n_target=n_target, q_min=q_min, q_max=q_max)
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
        print(n_q)
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
    print('*' * 30 + 'FINAL {}'.format(n_target) + '*' * 30)
    print('Mean Q         :{}'.format(total_nq/n_test))
    print('Mean candidates:{}'.format(total_nc/n_test))
    print("Ratio          :{:.2f}".format(total_nc / total_nq))
    print('Mean Time      :{}s'.format((t_end-t_start)/n_test))
    pf.write('*' * 30 + 'FINAL {}'.format(n_target) + '*' * 30 + '\n')
    pf.write('Mean Q         :{}\n'.format(total_nq/n_test))
    pf.write('Mean candidates:{}\n'.format(total_nc/n_test))
    pf.write('Ratio          :{:.2f}\n'.format(total_nc/total_nq))
    pf.write('Mean Time      :{}s\n'.format((t_end-t_start)/n_test))
    pf.close()
    return total_nq/n_test, total_nc/n_test, total_nc/total_nq, (t_end-t_start)/n_test


if __name__ == '__main__':
    n_targets = [500]
    final_list = []
    for n_t in n_targets:
        q_, c_, r_, t_ = test_find_candidate(n_test=30, n_target=n_t, q_min=1, q_max=30)
        final_list.append({
            'n_tartget': n_t,
            'q_max': 30,
            'mean_q': q_,
            'mean_c': c_,
            'ratio': r_,
            'mean_time': t_
        })

    df = pd.DataFrame(final_list)
    df.to_csv(ROOT_PATH + '/results/result2.csv', index=False)
