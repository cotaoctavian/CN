import numpy as np
import random


# 1
def first_ex():
    m_v = 0
    u = 10 ** (-m_v)

    while 1.0 + u != 1.0:
        m_v += 1
        u /= 10

    m_v -= 1
    u *= 10

    return m_v, u


# 2
def second_ex(m_val):
    x = 1.0
    y = 10 ** (-m_val)
    z = 10 ** (-m_val)

    if (x + y) + z != x + (y + z):
        print("Adunarea nu este asociativa!")
    else:
        print("Adunarea este asociativa!")

    cnt = 0
    x = random.uniform(0.7, 1)
    y = random.uniform(0, 0.5)
    z = random.uniform(0, 0.5)
    while (x * y) * z == x * (y * z):
        x = random.uniform(0.7, 1)
        y = random.uniform(0, 0.5)
        z = random.uniform(0, 0.5)
        cnt += 1

    print(f"Solutia pentru inmultirea neasociativa este: {x} {y} {z}. Iteratii: {cnt} \n")


# 3
def make_a_sub_matrix(matrix_a, m_value, p_value):
    counter = 0
    new_sub_mtrx = list()

    for i in range(p_value):
        new_list = list()
        for j in range((len(matrix_a))):
            new_row = list()
            for k in range(counter, counter + m_value):
                new_row.append(matrix_a[j][k])
            new_list.append(new_row)
        new_sub_mtrx.append(new_list)
        counter += m_value

    new_submatrix = np.array(new_sub_mtrx, dtype=bool)
    return new_submatrix


def make_b_sub_matrix(matrix, m_value, p_value):
    counter = 0
    new_sub_mtrx = list()

    for i in range(p_value):
        new_row = list()
        for k in range(counter, counter + m_value):
            new_row.append(matrix[k])
        counter += m_value
        new_sub_mtrx.append(new_row)

    new_submatrix = np.array(new_sub_mtrx, dtype=bool)
    return new_submatrix


def get_decimal(arr):
    result = 0
    for it in range(len(arr)):
        result += arr[it] * (2 ** it)
    return result


if __name__ == '__main__':
    # 1
    res_m, res_u = first_ex()
    print(res_m, res_u)
    second_ex(res_m)

    n = 6
    a = np.array([
        [1, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0]
    ], dtype=bool)

    b = np.array([
        [1, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0]
    ], dtype=bool)

    c = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ], dtype=bool)

    m = int(np.floor(np.log2(n)))
    p = int(np.ceil(n / m))

    # Add columns to A
    if len(a[0]) % m != 0:
        no_of_zeros = m - len(a[0]) % m
        new_a = list()
        for row in a:
            new_row = list(row)
            for k in range(no_of_zeros):
                new_row.append(0)
            new_a.append(new_row)

        a = np.array(new_a, dtype=bool)

    sm_a = make_a_sub_matrix(a, m, p)  # A sub matrix

    # Add lines to B
    if len(b) % m != 0:
        no_of_lines = m - len(b) % m
        for k in range(no_of_lines):
            b = np.vstack([b, np.zeros(n, dtype=bool)])

    sm_b = make_b_sub_matrix(b, m, p)  # B sub matrix

    sum_linii_B = list()
    for itt in range(2 ** m):
        sum_linii_B.append(np.zeros(n, dtype=bool))

    sum_linii_B = np.array(sum_linii_B, dtype=bool)

    for i in range(0, p):
        k = 0

        sum_linii_B[0] = np.zeros(n, dtype=bool)

        for j in range(1, (2 ** m)):
            while 2 ** k < j:
                k += 1
            if 2 ** k > j:
                k -= 1

            sum_linii_B[j] = np.logical_or(sum_linii_B[j - (2 ** k)], sm_b[i][k ])

        ci = list()
        for r in range(n):
            res = get_decimal(sm_a[i][r])
            ci.append(sum_linii_B[res])

        ci = np.array(ci, dtype=bool)
        c = np.logical_or(c, ci)

    print(1.0 * c)


