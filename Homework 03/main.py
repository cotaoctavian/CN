if __name__ == '__main__':

    a = dict()
    b = dict()
    eps = 10 ** (-9)

    # Saving a.txt data into a dictionary where the key is i and the values are tuples by type (value, col)
    a_file = open("input_files/a.txt", "r")
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

    for item in a.keys():
        if len(a[item]) > 10:
            print(f"Linia {int(item)} din matricea A are mai mult de 10 elemente!")

    # Saving b.txt data into a dictionary where the key is i and the values are tuples by type (value, col)
    b_file = open("input_files/b.txt", "r")
    lines = b_file.readlines()
    m = int(lines[0])

    for line in lines[1:]:
        value, lin, col = line.rstrip().split(", ")
        if lin in b:
            is_duplicate = False
            for item in b[lin]:
                if item[1] == col:
                    item[0] += float(value)
                    is_duplicate = True

            if is_duplicate is False:
                b[lin].append([float(value), col])
        else:
            b[lin] = [[float(value), col]]

    for item in b.keys():
        if len(b[item]) > 10:
            print(f"Linia {int(item)} din matricea B are mai mult de 10 elemente!")

    # ------------------------- A + B ----------------------------
    print("\n --------------------------- A + B ----------------------------------------\n")
    addition_matrix = dict()
    for i in range(n):
        addition_matrix[str(i)] = []

        # If A is in B => C = A + B, else C = A
        for a_item in a[str(i)]:
            found = False
            for b_item in b[str(i)]:
                if a_item[1] == b_item[1]:
                    addition_matrix[str(i)].append([a_item[0] + b_item[0], a_item[1]])
                    found = True
            if found is False:
                addition_matrix[str(i)].append(a_item)

        # Add the rest of the elements from B are in the addition matrix
        for b_item in b[str(i)]:
            found = False
            for item in addition_matrix[str(i)]:
                if item[1] == b_item[1]:
                    found = True
            if found is False:
                addition_matrix[str(i)].append(b_item)

    # --------------------- Result A + B ---------------------------
    """for item in addition_matrix.keys():
        print(f"{item} -> {addition_matrix[item]}")"""

    # -------------------- Check the result ------------------------
    # Read the file aplusb.txt
    addition = open("output_files/aplusb.txt", "r").readlines()
    a_plus_b = dict()

    for line in addition[1:]:
        value, lin, col = line.rstrip().split(", ")
        if lin in a_plus_b:
            a_plus_b[lin].append([float(value), col])
        else:
            a_plus_b[lin] = [[float(value), col]]

    good_result = True
    for i in range(n):
        for item in addition_matrix[str(i)]:
            for res_item in a_plus_b[str(i)]:
                if item[1] == res_item[1]:
                    if abs(item[0] - res_item[0]) > eps:
                        good_result = False
                        break

    if good_result is True:
        print("Rezultatul pentru A + B este corect.")
    else:
        print("Rezultatul pentru A + B este incorect.")

    # ------------------------- A * B ------------------------------
    multiply_matrix = dict()

    print("\n --------------------------- A * B ----------------------------------------\n")
    # No of columns
    for k in range(n):
        # No of rows
        for i in range(n):
            res = 0
            # For each item of A from line i, check it with every item from B that has line equal with the column
            # of the item from A.
            for item in a[str(i)]:
                # coloana lui A trebuie sa fie linia lui B.
                for b_item in b[item[1]]:
                    if b_item[1] == str(k):
                        res += b_item[0] * item[0]

            if res > 0:
                if str(i) not in multiply_matrix:
                    multiply_matrix[str(i)] = [[res, str(k)]]
                else:
                    multiply_matrix[str(i)].append([res, str(k)])

    # ------------------------------ Result A * B ----------------------------------
    """for item in multiply_matrix.keys():
        print(f"{item} -> {multiply_matrix[item]}")"""

    # Read the file aorib.txt
    multiply = open("output_files/aorib.txt", "r").readlines()
    a_ori_b = dict()

    for line in multiply[1:]:
        value, lin, col = line.rstrip().split(", ")
        if lin in a_ori_b:
            a_ori_b[lin].append([float(value), col])
        else:
            a_ori_b[lin] = [[float(value), col]]

    # ----------------------------- Check the result -------------------------------
    good_result = True
    for i in range(n):
        for item in multiply_matrix[str(i)]:
            for res_item in a_ori_b[str(i)]:
                if item[1] == res_item[1]:
                    if abs(item[0] - res_item[0]) > eps:
                        good_result = False
                        break

    if good_result is True:
        print("Rezultatul pentru A * B este corect.")
    else:
        print("Rezultatul pentru A * B este incorect.")
