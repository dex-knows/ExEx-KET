import time

def timeturn(func):
    """Times an agents reaction time when taking its turn (asking for a card from someone).
       """

    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        duration = (t2-t1)*1
        return res, duration

    return wrapper

def timereaction(func):
    """Times an agents reaction time for any call that does not result in a return value.
       """

    def wrapper(*arg):
        t1 = time.time()
        func(*arg)
        t2 = time.time()
        duration = (t2-t1)*1
        return duration

    return wrapper
