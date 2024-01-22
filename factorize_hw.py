import time
import concurrent.futures
import multiprocessing
import logging



def factorize_synchronous(*numbers):
    result = []
    start_time = time.time()

    for number in numbers:
        factors = [i for i in range(1, number + 1) if number % i == 0]
        result.append(factors)

    end_time = time.time()
    delta_time = end_time - start_time
    logging.debug(f"Synchronous execution time: {delta_time:5f} [seconds]")

    return result

def factorize_parallel(*numbers):
    result = []
    start_time = time.time()
    cpu_count = get_cpu_count()
    print(f"Number of CPU cores: {cpu_count}")
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        result = list(executor.map(worker, numbers))
    end_time = time.time()
    delta_time = end_time - start_time
    logging.debug(f"Parallel execution time: {delta_time:5f} [seconds]")
    return result

def test_factorize_synchronous():
        start_time = time.time()
        a, b, c, d = factorize_synchronous(128, 255, 99999, 10651060)
        assert a == [1, 2, 4, 8, 16, 32, 64, 128]
        assert b == [1, 3, 5, 15, 17, 51, 85, 255]
        assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
        assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
             1521580, 2130212, 2662765, 5325530, 10651060]
        end_time=time.time()
        delta_time = end_time-start_time
        logging.debug(f"Execution time for factorize_synchronous: {delta_time:5f} [seconds]")

def factorize_single(number):
    return [i for i in range(1, number + 1) if number % i == 0]

def worker(number):
    return factorize_single(number)

def get_cpu_count():
    return multiprocessing.cpu_count()

def test_factorize_parallel():
        start_time = time.time()
        a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)
        assert a == [1, 2, 4, 8, 16, 32, 64, 128]
        assert b == [1, 3, 5, 15, 17, 51, 85, 255]
        assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
        assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
             1521580, 2130212, 2662765, 5325530, 10651060]
        end_time = time.time()
        delta_time = end_time - start_time
        logging.debug(f"Execution time for factorize_parallel: : {delta_time:5f} [seconds]")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    test_factorize_synchronous()
    test_factorize_parallel()


