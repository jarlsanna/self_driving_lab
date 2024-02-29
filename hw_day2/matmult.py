# Program to multiply two matrices using nested loops
import random
import numpy as np

@profile
def matmult():
    N = 250

    # NxN matrix
    X = np.random.randint(0, 100, size=(N, N))

    # Nx(N+1) matrix
    Y = np.random.randint(0, 100, size=(N, N + 1))

    # result is Nx(N+1)
    result = np.dot(X, Y)

    for r in result:
        print(r)

matmult()
# Total time: 0.206821 s, using line profiling