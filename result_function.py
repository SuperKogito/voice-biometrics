import numpy as np
from math import e, pi, log

# X - матрица коэффициентов MFCC
# means - вектор средних значений
# cov - матрица ковариации
# w - вектор весов

def likelihood(X, means, cov, w):
    N, D = X.shape
    P = []
    for vector_index in range(N):
        weighted_prob = []
        for i in range(0, len(w)):
            gaussian = (w[i])*np.exp(-0.5*np.dot(np.dot((X[vector_index]-means[i]), (np.linalg.inv(cov[i]))), 
                (np.transpose(X[vector_index]-means[i]))))/(((2*pi)**(D/2))*((np.linalg.det(cov[i]))**0.5))
            weighted_prob.append(gaussian)
        P.append(sum(weighted_prob))
    S = (1/N)*sum(log(j) for j in filter(lambda a: a!=0, P))
    return S
