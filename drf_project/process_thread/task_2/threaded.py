import sys
from time import time
from threading import Thread
sys.set_int_max_str_digits(100000000)


def power(x):
    print(x ** 1000000)


start = time()

thread1 = Thread(target=power, args=(2,))
thread2 = Thread(target=power, args=(3,))
thread3 = Thread(target=power, args=(5,))
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()

print(time() - start)
