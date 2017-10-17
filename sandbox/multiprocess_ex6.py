from concurrent.futures import ProcessPoolExecutor
from multiprocessing import current_process, cpu_count
from time import time


def primes(n):
    """
    Find n primes (i.e., not primes from 2 to n)
    """
    s = current_process().name
    prime = [2]
    i = 3
    print('Process: {} started working on primes({})'.format(s, n))

    while len(prime) <= n:
        testlist = []

        for number in prime:
            testlist.append(i % number)

        if 0 not in testlist:
            prime.append(i)

        if i % 10000 == 0:
            # print: proc name, search number, number of primes
            print(s, i, len(prime))

        i = i + 1

    print(s, 'process completed.')
    return prime


if __name__ == '__main__':
    numbers = [16000, 14000, 12000, 10000, 8000, 7000, 6000, 5000, 4000, 3000, 2000]

    numnums = len(numbers)
    print('Number of numbers: {}'.format(numnums))
    cpus = cpu_count()
    print('{} CPUs'.format(cpus))
    start = time()
    pool = ProcessPoolExecutor(max_workers=cpus)
    results = list(pool.map(primes, numbers))
    print(results)
    end = time()
    print('Took %.3f seconds' % (end - start))
