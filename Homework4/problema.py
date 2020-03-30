import copy
import numpy as np


def formula_3(A, B, Xp, Xc, m):
    for p in range(0, m):
        aux = 0
        res = 0
        result = 0
        for j in A[str(p)]:
            if int(j[1]) < p:
                res += j[0] * Xc[int(j[1])]
            if p + 1 <= int(j[1]) < m:
                result += j[0] * Xp[int(j[1])]
            if p == int(j[1]):
                aux = j[0]
        Xc[p] = (B[p] - res - result) / aux
    return Xc


def metoda_relaxarii(A, B, Xgs, m):
    delta = 0
    for p in range(0, m):
        aux = 0
        res1 = 0
        for j in A[str(p)]:
            if int(j[1]) != p:
                res1 += j[0] * Xgs[int(j[1])]
            if p == int(j[1]):
                aux = j[0]
        temp = (B[p] - res1) / aux
        delta += (temp - Xgs[p]) ** 2
        Xgs[p] = temp
    d = delta ** 0.5
    return Xgs, d


if __name__ == '__main__':
    a = dict()
    b = list()
    eps = 10 ** (-9)
    # Saving b_2.txt data into a list
    b_file = open("input/b_5.txt", "r")

    lines_b = b_file.readlines()
    for line in lines_b[1:]:
        b.append(float(line.rstrip()))
    # Saving a_2.txt data into a dictionary where the key is i and the values are tuples by type (value, col)
    a_file = open("input/a_5.txt", "r")

    lines = a_file.readlines()
    n = int(lines[0])
    for line in lines[1:]:
        value, lin, col = line.rstrip().split(", ")
        if lin in a:
            is_duplicate = False
            for item in a[lin]:
                if item[1] == col:
                    item[0] += float(value)
                    is_duplicate = True

            if is_duplicate is False:
                a[lin].append([float(value), col])
        else:
            a[lin] = [[float(value), col]]

    # Checking if exist 0 elements on principal diagonal
    ok = True
    for i in a.keys():
        check = False
        for j in a[i]:
            if j[1] == i:
                check = True
        if check is False:
            ok = False
            break

    if ok is True:
        print("Toate elementele de pe diagonala principala sunt nenule!")
    else:
        print("Nu toate elementele de pe diagonala principala sunt nenule!")

    xc = [0 for i in range(n)]
    xp = [0 for i in range(n)]
    k_max = 10000
    xc = copy.deepcopy(formula_3(a, b, xp, xc, n))
    delta_x = np.linalg.norm(np.subtract(xc, xp))
    k = 1
    while 10 ** 8 >= delta_x >= eps and k <= k_max:
        xp = copy.deepcopy(xc)
        xc = copy.deepcopy(formula_3(a, b, xp, xc, n))
        delta_x = np.linalg.norm(np.subtract(xc, xp))
        k += 1

    if delta_x < eps:
        print(xc)
    else:
        print("divergenta")

    multiple_matrix = list()
    for k in range(n):
        res = 0
        for item in a[str(k)]:
            res += item[0] * xc[int(item[1])]
        multiple_matrix.append(res)

    diff1 = np.subtract(multiple_matrix, b)
    norm = np.linalg.norm(diff1, ord=np.inf)
    print(norm)

    print(
        "-------------------------------------------------------------Metoda relaxarii-----------------------------------------------------------------")

    xgs = [0 for i in range(n)]
    xgs, delta_xgs = metoda_relaxarii(a, b, xgs, n)
    k_xgs = 1
    while 10 ** 8 >= delta_xgs >= eps and k_xgs <= k_max:
        xgs, delta_xgs = metoda_relaxarii(a, b, xgs, n)
        k_xgs += 1

    if delta_xgs < eps:
        print(xgs)
    else:
        print("divergenta")
