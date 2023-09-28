import sys
from time import time

sys.set_int_max_str_digits(100000000)


def power(x):
    return x ** 1000000


start = time()
print(power(2))
print(power(3))
print(power(5))
print(time() - start)
