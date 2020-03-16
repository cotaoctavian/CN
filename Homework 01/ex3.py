import math
import numpy as np


def submatrix_def(matrix, lines, m_value):
    cnt = 0
    submatrix = list()
    new_matrix = list()

    for row in matrix:
        if cnt < m_value:
            new_matrix.append(row)
            cnt += 1
        else:
            cnt = 1
            submatrix.append(new_matrix)
            new_matrix = [row]

    if cnt > 0:
        while cnt < m_value:
            new_matrix.append([0 for f in range(lines)])
            cnt += 1
        submatrix.append(new_matrix)

    return submatrix


def reverse(matrix):
    new_matrix = list()
    for f in range(0, len(matrix)):
        new_line = list()
        for d in range(0, len(matrix)):
            new_line.append(matrix[d][f])
        new_matrix.append(new_line)

    return new_matrix


def transform(v, x, contor):
    result = 0
    for f in range(x):
        result += v[f][contor] * (2 ** f)

    return result


def or_function(v, x):
    lista = list()
    for f in range(0, len(v)):
        lista.append(v[f] | x[f])

    return lista


if __name__ == '__main__':
    a = [[1, 0, 0, 1, 1, 1],
         [1, 1, 1, 0, 0, 0],
         [0, 1, 1, 0, 1, 0],
         [0, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 1, 0],
         [1, 0, 0, 0, 1, 0]
         ]

    b = [[1, 0, 0, 1, 1, 1],
         [1, 1, 1, 0, 0, 0],
         [0, 1, 1, 0, 1, 0],
         [0, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 1, 0],
         [1, 0, 0, 0, 1, 0]
         ]

    n = 6
    m = math.floor(math.log2(n))
    p = math.ceil(n / m)
    submatrix_A = submatrix_def(reverse(a), n, m)
    submatrix_B = submatrix_def(b, n, m)

    C = [[0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

    sum_linii_B = list()
    for i in range(2 ** m):
        new_row = list()
        for j in range(n):
            new_row.append(0)
        sum_linii_B.append(new_row)

    for i in range(p):
        k = 0
        ci = list()

        new_r = list()
        for f in range(n):
            new_r.append(0)
        sum_linii_B[0] = new_r

        for j in range(1, 2 ** m):
            k = int(math.log2(j))
            sum_linii_B[j] = or_function(sum_linii_B[j - (2 ** k)], submatrix_B[i][k])

        for r in range(n):
            val = transform(submatrix_A[i], len(submatrix_A[i]), r)
            ci.append(sum_linii_B[val])

        print(ci)
        for z in range(len(ci)):
            for c in range(len(ci)):
                C[z][c] = (C[z][c] | ci[z][c])

    for i in C:
        print(i)

