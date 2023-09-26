import sys
from time import time
from multiprocessing import Process
sys.set_int_max_str_digits(100000000)


def power(x):
    print(x ** 1000000)


if __name__ == '__main__':
    start = time()

    process1 = Process(target=power, args=(2,))
    process2 = Process(target=power, args=(3,))
    process3 = Process(target=power, args=(5,))
    process1.start()
    process2.start()
    process3.start()
    process1.join()
    process2.join()
    process3.join()

    print(time() - start)
