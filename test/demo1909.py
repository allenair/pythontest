# -*- coding: utf-8 -*-
'''
Created on 2019年9月2日

@author: syp560
'''
import numpy as np

import re


def And(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(w*x)+b
    if tmp<=0:
        return 0
    else:
        return 1

def findUrl():
    pattern = re.compile('.*<a href="//www.zgelevator.com/news.*')
    with open('d:/spider.txt', 'r', encoding='utf-8') as fin:
        with open('d:/tmp.txt', 'w', encoding='utf-8') as fout:
            for line in fin.readlines():
                if pattern.match(line):
                    print(line)
                    fout.write(line)


def findPage():
    pass


def sent2vec():
    vect_list = []
    vect_list.append([1.1, 2.2, 3.3])
    vect_list.append([4.4, 5.5, 6.6])

    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    print(vect / np.sqrt((vect ** 2).sum()))


if __name__ == '__main__':
    for xs in [(x1, x2) for x1 in range(2) for x2 in range(2)]:
        print(xs, "->", And(xs[0], xs[1]))
    
