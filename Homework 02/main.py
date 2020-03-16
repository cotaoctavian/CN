import numpy as np
import math

if __name__ == '__main__':
    file = open("matrix.txt", "r")
    file = file.readlines()

    first_line = file[0].rstrip().split(' ')
    n = int(first_line[0])
    t = int(first_line[1])
    eps = 10 ** (-t)

    B = list(map(float, file[1].rstrip().split(' ')))

    a = list()
    for line in file[3:]:
        current_line = list(map(float, line.rstrip().split(' ')))
        a.append(current_line)

    A = np.array(a)
    A_init = np.array(a)
    for p in range(0, n):
        # U
        for i in range(p, n):
            res = 0
            for k in range(p):
                res += A[p, k] * A[k, i]
            A[p, i] = A_init[p, i] - res

        # L
        for i in range(p + 1, n):
            res = 0
            for k in range(p):
                res += A[i, k] * A[k, p]

            if math.fabs(A[p, p]) > eps:
                A[i, p] = (A_init[i, p] - res) / A[p, p]
            else:
                A[i, p] = (A_init[i, p] - res)

    print(f"Descompunerea LU este: \n{A}\n")
    det_U, det_L = 1, 1
    for i in range(0, n):
        det_U *= A[i, i]

    print(f"Determinantul matricei A este egal cu: {det_U * det_L}\n")

    X = np.zeros(n, dtype=float)
    Y = list()

    # Metoda substitutiei directe (L)
    for i in range(0, n):
        result = 0
        for j in range(0, i):
            if i == j:
                result += Y[j]
            else:
                result += A[i, j] * Y[j]

        Y.append((B[i] - result))

    # Metoda substitutiei inverse (U)
    for i in range(n - 1, -1, -1):
        result = 0
        for j in range(i, n):
            result += A[i, j] * X[j]

        if math.fabs(A[i, i]) > eps:
            X[i] = (Y[i] - result) / A[i, i]
        else:
            X[i] = (Y[i] - result)

    print(f"Solutia sistemului liniar Ax = B folosind metoda substitutiei directe si inverse pe LU este: {X}\n")

    # Norma euclidiana (||A*x - b||)^2
    y = list()
    for i in range(0, n):
        res = 0
        for j in range(0, n):
            res += A_init[i, j] * X[j]
        y.append(res)

    z = np.subtract(y, B)
    norm = 0
    for i in z:
        norm += i ** 2
    norm = math.sqrt(norm)

    print(f"Norma euclidiana este egala cu: {norm}\n")

    # Utilizare librarii
    x_lib = np.linalg.solve(A_init, B)
    print(f"Solutia sistemului liniar Ax = b este: {x_lib}\n")
    inverse = np.linalg.inv(A_init)
    print(f"Inversa matricei A initiale este: \n{inverse}\n")

    # Prima norma
    diff_one = np.subtract(X, x_lib)
    first_norm = 0
    for i in diff_one:
        norm += i ** 2
    first_norm = math.sqrt(first_norm)

    print(f"Norma euclidiana a ecuatiei ||xLU - x_lib||^2 este: {first_norm}\n")

    # A doua norma
    product_A_B = list()
    for i in range(0, n):
        res = 0
        for j in range(0, n):
            res += inverse[i, j] * B[j]
        product_A_B.append(res)

    diff_two = np.subtract(X, product_A_B)
    second_norm = 0
    for i in z:
        second_norm += i ** 2
    second_norm = math.sqrt(second_norm)

    print(f"Norma euclidiana a ecuatiei ||xLU - A^-1*b||^2 este: {second_norm}\n")

    # Inversa matricei A
    A_inv = np.zeros([n, n])
    for j in range(0, n):
        e = np.zeros(n)
        e[j] = 1

        Yj = list()
        Xj = np.zeros(n)

        for i in range(0, n):
            result = 0
            for k in range(i):
                result += (A[i, k] * Yj[k])
            Yj.append(e[i] - result)

        for i in range(n - 1, -1, -1):
            result = 0
            for k in range(i, n):
                result += A[i, k] * Xj[k]

            if math.fabs(A[i, i]) > eps:
                Xj[i] = (Yj[i] - result) / A[i, i]
            else:
                Xj[i] = (Yj[i] - result)

        for i in range(len(Xj)):
            A_inv[i][j] = Xj[i]

    print(f"Inversa matricei A este:\n{A_inv}\n")

    # Ultima norma
    last_norm = np.linalg.norm(np.subtract(inverse, A_inv), ord=1)
    print(f"Norma ||A_lu^-1 - A_lib^-1|| este egala cu: {last_norm}")
