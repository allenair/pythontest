# -*- coding: utf-8 -*-
'''
Created on 2019年9月2日

@author: syp560
'''
import numpy as np
from test.demo_decrorator import runTime
import re


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


@runTime
def sent2vec():
    vect_list = []
    vect_list.append([1.1, 2.2, 3.3])
    vect_list.append([4.4, 5.5, 6.6])
    
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    print(vect / np.sqrt((vect ** 2).sum()))

@runTime
def aaa():
    aa = [x**3 for x in range(100)]


if __name__ == '__main__':
    findUrl()
