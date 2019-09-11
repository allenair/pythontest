'''
Created on 2019年9月2日

@author: syp560
'''
import time

def runTime(func):
    def wrapper(*args, **kwargs):
        start = time.process_time()
        result = func(*args, **kwargs)
        print('{} Run time is {:.4f} seconds'.format(func.__name__, (time.process_time() - start)))
        return result
    wrapper.__name__ = func.__name__
    return wrapper