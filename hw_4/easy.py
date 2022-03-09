from time import time
from threading import Thread
from multiprocessing import Process


def fib_num(n):
    curr_num, next_num = 0, 1
    for _ in range(n):
        tmp = curr_num
        curr_num = next_num
        next_num = tmp + next_num
    return curr_num


def run(n=10_000, times=8, parallel_type=None):
    start = time()

    if parallel_type is None:
        for _ in range(times):
            fib_num(n)

    elif parallel_type == 'threads':
        threads = []
        for i in range(times):
            t = Thread(target=fib_num, args=(n,), name=f"Thread-{i + 1}")
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif parallel_type == 'processes':
        processes = []
        for i in range(times):
            p = Process(target=fib_num, args=(n,), name=f"Process-{i + 1}")
            processes.append(p)
        for p in processes:
            p.start()
        for p in processes:
            p.join()

    execution_time = time() - start
    return execution_time


def experiments(n=100_000, times=8,):
    # synchronously
    execution_time = run(n=n, times=times)
    with open('artifacts/easy.txt', 'w') as f:
        f.write(f'synchronously: {execution_time:.5f} seconds\n')

    # threads
    execution_time = run(n=n, times=times, parallel_type='threads')
    with open('artifacts/easy.txt', 'a') as f:
        f.write(f'threads:       {execution_time:.5f} seconds\n')

    # processes
    execution_time = run(n=n, times=times, parallel_type='processes')
    with open('artifacts/easy.txt', 'a') as f:
        f.write(f'processes:     {execution_time:.5f} seconds\n')


if __name__ == '__main__':
    experiments()
