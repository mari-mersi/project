def read_sudoku(file):
    """Прочитать судоку из файла"""
    with open(file) as f:
        digits = [char for char in f.read() if char in "123456789."]
    return [digits[i:i + 9] for i in range(0, len(digits), 9)]


def print_sudoku(board):
    """Вывод судоку на экран"""
    separator = "- " * 13
    for i, row in enumerate(board):
        if i % 3 == 0:
            print(separator)
        print("|", end=" ")
        for j, value in enumerate(row):
            print(value, end=" ")
            if (j + 1) % 3 == 0:
                print("|", end=" ")
        print()
    print(separator)


def get_row(board, pos):
    row, _ = pos
    return board[row]


def get_column(board, pos):
    _, col = pos
    return [board[i][col] for i in range(9)]


def get_block(board, pos):
    row, col = pos
    block_row, block_col = row // 3 * 3, col // 3 * 3
    return [board[r][c] for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3)]


def search_possible_values(row, col, block):
    all_digits = "123456789"
    used_digits = set(row + col + block)
    return [digit for digit in all_digits if digit not in used_digits]


def search_empty_pos(board):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == ".":
                return i, j
    return None


def write_value(board, pos, value):
    row, col = pos
    board[row][col] = value


def conclusion(board):
    pos = search_empty_pos(board)
    if not pos:
        return True

    possible_values = search_possible_values(get_row(board, pos), get_column(board, pos), get_block(board, pos))
    for value in possible_values:
        write_value(board, pos, value)
        if conclusion(board):
            return True
        write_value(board, pos, ".")

    return False


def check_conclusion(board):
    digits = sorted("123456789")

    def check_group(group):
        return sorted(group) == digits

    for i in range(9):
        if not (check_group(get_row(board, (i, 0))) and check_group(get_column(board, (0, i)))):
            return False

    for pos in [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]:
        if not check_group(get_block(board, pos)):
            return False

    return True


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
