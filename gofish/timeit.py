import time

def timeit(func):
    """
       """

    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        duration = (t2-t1)*1000.0
        return res, duration

    return wrapper
