from collections import defaultdict
from scipy import sparse
import numpy as np

eps = 10 ** (-9)


# Generate library random sparse matrix
def generate_random_sparse_matrix(size_n, size_p):
    sparse_matrix = sparse.random(size_n, size_p, density=.3)
    sparse_matrix_u = sparse.triu(sparse_matrix)
    result = sparse_matrix_u + sparse_matrix_u.T - sparse.diags(sparse_matrix_u.diagonal())
    return result


# Check if library sparse matrix is symmetric.
def is_symmetric_library(matrix):
    return (matrix - matrix.T).nnz == 0


# Convert to special sparse matrix from homework 3
def convert_to_sparse_matrix(matrix, size):
    final_matrix = defaultdict(set)
    converted_matrix = sparse_m.toarray()
    for i in range(size):
        j = 0
        for item in converted_matrix[i]:
            if item > 0:
                final_matrix[i].add((item, j))
            j += 1

    return final_matrix


# Convert so special sparse matrix from homework 3 reading from a file.
def convert_to_sparse_matrix_from_file(filename):
    file = open(filename, "r")
    lines = file.readlines()

    size = int(lines[0].rstrip())
    sparse_matrix = defaultdict(set)

    for line in lines[1:]:
        value, lin, col = line.rstrip().split(", ")
        sparse_matrix[int(lin)].add((float(value), int(col)))

    return size, sparse_matrix


# Convert sparse matrix to transpose.
def convert_to_transpose(matrix, size):
    transpose_matrix = defaultdict(set)

    # line 0 -> 0 .. n cols => col 0, lines 0 ... n
    for i in range(size):
        for item in matrix[i]:
            transpose_matrix[item[1]].add((item[0], i))

    return transpose_matrix


# Check if the sparse matrix is symmetric
def check_symmetric(matrix, transpose_matrix, size):
    for i in range(size):
        for item in matrix[i]:

            found = False
            for item_t in transpose_matrix[i]:
                if item[1] == item_t[1]:
                    if abs(item[0] - item_t[0]) == 0:
                        found = True

            if found is False:
                return False
    return True


# Product between sparse matrix and array.
def product_sparse_with_array(matrix, a):
    b = []
    for j in range(len(a)):
        s = 0
        for f in matrix[j]:
            s += f[0] * a[f[1]]
        b.append(s)
    return b


# Method of power
def method_of_power(matrix, size):
    if check_symmetric(matrix, convert_to_transpose(matrix, size), size) is True:
        arr = np.random.randint(0, 100, n)
        arr_norm = np.linalg.norm(arr)

        # v = (1 / ||x||) * x
        v = (1 / arr_norm) * arr  # vectorul asociat

        # w = A * v
        w = product_sparse_with_array(matrix, v)

        complex_number = np.dot(w, v)  # lambda, valoarea proprie de modul maxim
        k = 0
        k_max = 1000000
        while np.linalg.norm(np.subtract(w, complex_number * v)) > n * eps and k < k_max:
            v = (1 / np.linalg.norm(w)) * np.array(w)
            w = product_sparse_with_array(matrix, v)
            complex_number = np.dot(w, v)
            k += 1

        if k > k_max:
            print("Nu s-a putut calcula valoarea proprie de modul maxim si vectorul asociat.")
        else:
            print(f"Valoarea proprie de modul maxim: {complex_number}")
            print(f"Vector asociat: \n{v}")


if __name__ == '__main__':
    # Reading the input file and saving the matrix.
    n, generated_sparse_matrix_file = convert_to_sparse_matrix_from_file("input/a_300.txt")
    transpose_matrix_file = convert_to_transpose(generated_sparse_matrix_file, n)

    sparse_m = generate_random_sparse_matrix(n, n)
    generated_sparse_matrix = convert_to_sparse_matrix(sparse_m, n)

    # Check symmetric value for generated matrix
    print(check_symmetric(generated_sparse_matrix, convert_to_transpose(generated_sparse_matrix, n), n))

    # Check symmetric value for input matrix
    print(check_symmetric(generated_sparse_matrix_file, convert_to_transpose(generated_sparse_matrix_file, n), n))

    # Method of power used on input matrix
    method_of_power(generated_sparse_matrix_file, n)

    # Method of power used on random generated matrix
    method_of_power(generated_sparse_matrix, n)

    print("\n-----------------------------------------------------------\n")

    # SVD using library
    n_prim, p_prim = 6, 9
    svg_matrix = np.random.rand(p_prim, n_prim)

    # U, S, V from SVD
    u, s, v = np.linalg.svd(svg_matrix, full_matrices=True)

    print(f"U using SVD from numpy library: \n{u}\n")
    print(f"S using SVD from numpy library: \n{s}\n")
    print(f"V using SVD from numpy library: \n{v}\n")

    # Matrix rannk
    rank = np.linalg.matrix_rank(svg_matrix)

    print(f"Rank of matrix using numpy library: {rank}\n")

    # Lambda
    condition_number = np.linalg.cond(svg_matrix)

    print(f"Condition number using numpy library: {condition_number}\n")

    # MP for A
    mp_normal_matrix = np.linalg.pinv(svg_matrix)

    print(f"Moore Penrose for A using numpy library: \n{mp_normal_matrix}\n")

    # MP for u.T * s * v
    mat = np.zeros((p_prim, n_prim), dtype=complex)
    mat[:n_prim, :n_prim] = np.diag(s)

    a_I = np.dot(u, np.dot(mat, v))
    mp_transpose_u = np.linalg.pinv(a_I)

    print(f"Moore Penrose for A^I = VSU^T using numpy library: \n{mp_transpose_u}\n")

    # b array
    b_arr = np.random.randint(0, 100, p_prim)
    x_I = a_I.T * b_arr

    # X^I
    print(f"X^I: \n{x_I}\n")

    # x from Ax = b
    x = np.linalg.solve(svg_matrix.T.dot(svg_matrix), svg_matrix.T.dot(b_arr))
    print(f"Solution of the equation Ax=b is: \n{x}\n")

    # ||b - Ax||
    first_norm = np.linalg.norm(np.subtract(b_arr, np.dot(svg_matrix, x)))
    print(f"||b - Ax|| is equal to: {first_norm}\n")

    # A^j = (A^T * A)^-1 * A^T
    a_J = np.dot(np.linalg.inv((np.dot(svg_matrix.T, svg_matrix))), svg_matrix.T)
    print(f"A^J = (A^T * A)^-1 * A^T:\n{a_J}\n")

    # ||A^I - A^J||
    second_norm = np.linalg.norm(np.subtract(a_I.T, a_J))
    print(f"||A^I - A^J|| is equal to: {second_norm}\n")
