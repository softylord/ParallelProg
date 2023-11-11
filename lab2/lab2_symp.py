import numpy as np
import random
from mpi4py import MPI
import math
import time


def simp_conjugate_gradient(A, b, x0):
    eps=0.00001
    x = x0
    r = b - np.dot(A, x)
    z = r
    rs_old = np.dot(np.transpose(r), r)

    while True:
        Az = np.dot(A, z)
        alpha = rs_old / np.dot(np.transpose(z), Az)
        x = x + alpha * z
        r = r - alpha * Az
        rs_new = np.dot(np.transpose(r), r)

        if np.sqrt(rs_new) < eps:
            break

        z = r + (rs_new / rs_old) * z
        rs_old = rs_new

    return x

start=time.time()
n=10000
A=np.zeros((n, n))
b=np.zeros((n))
u=np.zeros((n))
for i in range(n):
    #u[i]=random.uniform(0,20)
    #u[i]=math.sin(2*3.14*i/n)
    b[i]=random.uniform(0,20)
    for j in range(n):
        if i==j:
            A[i][j]=2.0
        else:
            A[i][j]=1

#print(u)
#b=np.dot(A, u)
#print('Вектор u:')
#print(u)

x=np.zeros((n))
x=simp_conjugate_gradient(A, b, x)
end=time.time()
#print('Вектор x:')
#print(x)
print('time is', (end-start))

