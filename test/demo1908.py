'''
Created on 2019年8月28日

@author: syp560
'''
import numpy as np
import math
from test.demo_decrorator import runTime

myName = 'Allen'


def demo0830():
    print(myName)


@runTime
def demo0828():
    demoList = [('0.67898', '11asdfgh'), ('0.7890567', '22sdfghj'),
                ('0.56789', '333tyui'), ('1.0000', '44sdfghj'),
                ('0.87653', '55sdfgh')]
    demoList.sort(key=lambda x: x[0], reverse=True)
    #     print(demoList)

    #     print(sent2vec())
    #     print(calSentenceVector())

    a_vect = np.array([1.11, 2.22, 3.33])
    b_vect = sent2vec()
    print(similarity(a_vect, b_vect))

    sv1 = [1.11, 2.22, 3.33]
    sv2 = calSentenceVector()
    print(calTwoSentenceSimilar(sv1, sv2))


def sent2vec():
    vect_list = []
    vect_list.append([1.1, 2.2, 3.3])
    vect_list.append([4.4, 5.5, 6.6])

    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    return vect / np.sqrt((vect**2).sum())


def calSentenceVector():
    vect_list = []
    vect_list.append([1.1, 2.2, 3.3])
    vect_list.append([4.4, 5.5, 6.6])

    res = []
    for vector in vect_list:
        if not res:
            res = [0.0] * len(vector)
        res = [res[i] + vector[i] for i in range(len(res))]

    total = sum(res[i]**2 for i in range(len(res)))
    total = math.sqrt(total)
    res = [res[i] / total for i in range(len(res))]

    return res


# def calSentenceVector(self, sentence):
#     '''
#                 计算句子的向量值并返回
#     '''
#     res = []
#
#     if sentence in self.sentenceDict:
#         return self.sentenceDict[sentence]
#
#     word_dict = self.getSentenceAllWordVector(sentence)
#     for _, vector in word_dict.items():
#         if not res:
#             res = [0.0] * len(vector)
#         res = [res[i] + vector[i] for i in range(len(res))]
#
#     total = sum(res[i] ** 2 for i in range(len(res)))
#     total = math.sqrt(total)
#     res = [res[i] / total for i in range(len(res))]
#
#     return res


def similarity(a_vect, b_vect):
    num = a_vect.dot(b_vect)
    denom = np.linalg.norm(a_vect) * np.linalg.norm(b_vect)

    if denom < 0.00001:
        return -1.0

    return num / denom


def calTwoSentenceSimilar(sv1, sv2):
    dotVal = sum(sv1[i] * sv2[i] for i in range(len(sv1)))
    rank1 = math.sqrt(sum(sv1[i]**2 for i in range(len(sv1))))
    rank2 = math.sqrt(sum(sv2[i]**2 for i in range(len(sv2))))

    return dotVal / (rank1 * rank2)


# def calTwoSentenceSimilar(self, sentence1, sentence2):
#         '''
#                     计算两个句子的余弦相似性，返回值为0-1浮点数
#         '''
#         sv1 = self.calSentenceVector(sentence1)
#         sv2 = self.calSentenceVector(sentence2)
#
#         if not sv1 or not sv2:
#             return -1.0
#
#         dotVal = sum(sv1[i] * sv2[i] for i in range(len(sv1)))
#         rank1 = math.sqrt(sum(sv1[i] ** 2 for i in range(len(sv1))))
#         rank2 = math.sqrt(sum(sv2[i] ** 2 for i in range(len(sv2))))
#
#         return dotVal / (rank1 * rank2)

if __name__ == '__main__':
    demo0830()
    print(myName)
