def read_sudoku(file):
    """ Прочитать судоку из файла"""

    def group(values, n):
        mass = []
        for i in range(n):
            mass.append(values[i * n:(i + 1) * n])
        return mass

    digits = [el for el in open(file).read() if el in "123456789."]
    sudoku = group(digits, 9)
    return sudoku


def print_sudoku(s):
    ''' Вывод судоку на экран'''
    print("- " * 13)
    for i in range(len(s)):
        print("|", end=" ")
        for j in range(len(s[i])):
            print(s[i][j], end=" ")
            if j in [2, 5, 8]:
                print("|", end=" ")
        print()
        if i in [2, 5, 8]:
            print("- " * 13)


def get_row(s, pos):
    row, _ = pos
    return s[row]


def get_column(s, pos):
    _, column = pos
    col = []
    for i in range(len(s)):
        col.append(s[i][column])
    return col


def get_block(s, pos):
    def find_c_and_d(column):
        if column < 3:  # 1 квадрат
            c = 0
            d = 3
        elif column < 6:  # 2 квадрат
            c = 3
            d = 6
        else:  # 3 квадрат
            c = 6
            d = 9
        return c, d

    row, column = pos
    block = []
    a, b, c, d = 0, 0, 0, 0
    if row < 3:  # первые 3 квадрата
        a = 0
        b = 3
        c, d = find_c_and_d(column)
    elif row < 6:
        a = 3
        b = 6
        c, d = find_c_and_d(column)
    else:
        a = 6
        b = 9
        c, d = find_c_and_d(column)
    for i in range(a, b):
        for j in range(c, d):
            block.append(s[i][j])
    return block


def search_possible_values(*mass):
    digits = []
    numbers = "123456789"
    for list in mass:
        for el in list:
            if el in numbers and el not in digits:
                digits.append(el)
    values = [x for x in numbers if x not in digits]
    return values


def search_all_empty(s):
    count = 0
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == ".":
                count += 1
    return count


def search_empty_pos(s):
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == ".":
                return i, j


def write_value(s, pos, value):
    row, column = pos
    s[row][column] = value


def conclusion(s):
    p = search_empty_pos(s)
    if not p:
        return True
    vals = search_possible_values(get_row(s, p), get_column(s, p), get_block(s, p))
    for val in vals:
        write_value(s, p, val)
        if conclusion(s):
            return True
        write_value(s, p, '.')
    return False


def check_conclusion(s):
    flag = True
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(s)):
        row = get_row(s, (i, 0))
        row_sorted = sorted(row)
        if digits != row_sorted:
            flag = False
    for i in range(len(s)):
        column = get_column(s, (0, i))
        column_sorted = sorted(column)
        if digits != column_sorted:
            flag = False
    posix = [(0, 0), (0, 3), (0, 6),
             (3, 0), (3, 3), (3, 6),
             (6, 0), (6, 3), (6, 6)]
    for pos in posix:
        block = get_block(s, pos)
        block_sorted = sorted(block)
        if digits != block_sorted:
            flag = False
    return flag


sudoku = read_sudoku("puzzle2.txt")
print("Нерешенный судоку:")
print_sudoku(sudoku)
print()
conclusion(sudoku)
print("Решенный судоку:")
print_sudoku(sudoku)
print("Проверка правильности решения судоку:", end=" ")
if check_conclusion(sudoku):
    print("Успешно!")
else:
    print("Неудачно")
