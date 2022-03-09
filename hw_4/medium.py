import math
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import logging
import os
from timeit import timeit

logging.basicConfig(format='%(asctime)s  %(message)s',
                    datefmt='%H:%M:%S %d-%m-%y',
                    filename='artifacts/medium_log.txt',
                    level=logging.INFO)
logger = logging.getLogger("ExperimentLogger")


def get_square(args):
    """
        function for a task
    """

    f, left_bound, step, type_task = args
    logger.info(f'start task ({type_task}) S({left_bound:.3f}, {left_bound + step:.3f})')
    return f(left_bound) * step


def integrate(f, a, b, n_iter=1000, parallel_type=None, n_jobs=None,):
    acc = 0
    step = (b - a) / n_iter

    if parallel_type is None:
        for i in range(n_iter):
            acc += f(a + i * step) * step

    elif parallel_type == 'threads':
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            squares = executor.map(get_square, [(f, a + i * step, step, 'threads') for i in range(n_iter)])
        acc += sum(squares)

    elif parallel_type == 'processes':
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            squares = list(executor.map(get_square, [(f, a + i * step, step, 'processes') for i in range(n_iter)]))
        acc += sum(squares)

    return acc


def experiments(n_jobs=8, a=0, b=math.pi / 2):
    logging.info(f'########## n_jobs = {n_jobs} ##########')

    # synchronously
    execution_time_1 = timeit(lambda: integrate(math.cos, a, b), number=1)

    # threads
    execution_time_2 = timeit(lambda: integrate(math.cos, a, b, parallel_type='threads', n_jobs=n_jobs), number=1)

    # processes
    execution_time_3 = timeit(lambda: integrate(math.cos, a, b, parallel_type='processes', n_jobs=n_jobs), number=1)

    with open('artifacts/medium.txt', 'a') as f:
        f.write(f'{n_jobs}\t\t\t{execution_time_1:.7f}\t\t\t\t{execution_time_2:.5f}\t\t\t\t{execution_time_3:.5f}\n')


if __name__ == '__main__':
    with open('artifacts/medium.txt', 'w') as f:
        f.write(f'n_jobs\t\tsynchronously(sec)\t\tthreads (sec)\t\tprocesses (sec)\n')
    for i in range(1, os.cpu_count() * 2 + 1):
        experiments(n_jobs=i)
