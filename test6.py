import random


def main():
    new_table = key_a_d_s_w()
    if new_table:
        print('congratulation! You won!')
    else:
        print('Game Over! :(')


def initial_table():
    width = 4
    length = 4
    matrix = [[0 for x in range(length)] for y in range(width)]
    r = generate_initial_random_indexes()
    for x in r:
        matrix[x[0]][x[1]] = 2

    return [matrix, r]


def generate_initial_random_indexes():
    width = 4
    length = 4
    s = 0
    random_elements_indexes = []
    # seeds = list(range(2))
    # seed_counter = 0
    a = 0
    while a < 2:
        # random.seed(seeds[seed_counter] + 1)
        # seed_counter += 1
        random_row_index = random.randint(0, width - 1)
        random_column_index = random.randint(0, length - 1)
        if [random_row_index, random_column_index] in random_elements_indexes:
            continue
        random_elements_indexes.append([random_row_index, random_column_index])
        a += 1

    return random_elements_indexes


def key_a_d_s_w():
    width = 4
    length = 4
    initials = initial_table()
    index, table = initials[1], initials[0]
    for row in table:
        print(row)
    print('\n')
    columns = [[table[i][j] for i in range(width)] for j in range(length)]

    while True:
        # columns = [[table[i][j] for i in range(width)] for j in range(length)]
        print('Game not over yet.')
        key = input('please inter a or d or s or w: ')
        print('\n')
        if key.lower() == 'd':
            for c, row in enumerate(table):
                for i in reversed(range(width)):
                    for j in reversed(range(width - 1)):
                        if row[i] != 0 or row[j] != 0:
                            if row[i] == row[j]:
                                # we are going to move the cell by (number of zeros + 1) between them
                                row[j] = 0
                                if row[j+1:i] == [0 for n in range(i-j-1)]:
                                    row[j + row[j+1:i].count(0) + 1] *= 2
                                else:
                                    row[j + row[j + 1:i].count(0)] *= 2
                                # row[i] *= 2
                            else:
                                # we are going to move the cell by (number of zeros) between them
                                row[j + row[j + 1:i].count(0)] = row[j]
                                if row[j:i].count(0) > 0:
                                    row[j] = 0
        elif key.lower() == 'a':
            for c, row in enumerate(table):
                for i in range(width):
                    for j in range(width - 1):
                        if i < j and (row[i] != 0 or row[j] != 0):
                            if row[i] == row[j]:
                                # we are gonna move the cell by (number of zeros + 1) between them
                                row[j] = 0

                                if row[i+1:j] == [0 for n in range(j-i-1)]:
                                    row[j - (row[i:j].count(0) + 1)] *= 2
                                else:
                                    row[j - row[i:j].count(0)] *= 2
                                # row[i] *= 2
                            else:
                                # we are gonna move the cell by (number of zeros) between them
                                row[j - row[i:j].count(0)] = row[j]
                                if row[i:j].count(0) > 0:
                                    row[j] = 0
        elif key.lower() == 'w':
            for c, column in enumerate(columns):
                for i in range(length):
                    for j in range(length - 1):
                        if i < j and (column[i] != 0 or column[j] != 0):
                            if column[i] == column[j]:
                                # we are gonna move the cell by (number of zeros + 1) between them

                                column[j] = 0
                                if column[i+1:j] == [0 for n in range(j - i - 1)]:
                                    column[j - (column[i:j].count(0) + 1)] *= 2
                                else:
                                    column[j - column[i:j].count(0)] *= 2
                                # row[i] *= 2
                            else:
                                # we are gonna move the cell by (number of zeros) between them
                                column[j - column[i:j].count(0)] = column[j]
                                if column[i:j].count(0) > 0:
                                    column[j] = 0
        elif key.lower() == 's':
            for c, column in enumerate(columns):
                for i in reversed(range(length)):
                    for j in reversed(range(length - 1)):
                        if i > j and (column[i] != 0 or column[j] != 0):
                            if column[i] == column[j]:
                                ...
                                # we are gonna move the cell by (number of zeros + 1) between them
                                column[j] = 0
                                if column[j + 1:i] == [0 for n in range(i - j - 1)]:
                                    column[j + column[j:i].count(0) + 1] *= 2
                                else:
                                    column[j + column[j:i].count(0)] *= 2                                # row[i] *= 2
                            else:
                                # we are gonna move the cell by (number of zeros) between them
                                column[j + column[j:i].count(0)] = column[j]
                                if column[j:i].count(0) > 0:
                                    column[j] = 0

        # creating empty cells list
        empty_cells = []
        for r, row in enumerate(table):
            for c, column in enumerate(columns):
                if row[c] == 0:
                    empty_cells.append([r, c])

        # adding a random '2' each step to the table in empty cells
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if [x, y] in empty_cells:
                table[x][y] = 2
                break

        # if empty_cell doesn't change, it means that you can't move forward anymore and game is over!

        for row in table:
            print(row)

        available = 0
        for row in table:
            for i in range(width - 1):
                if row[i] == row[i + 1]:
                    available += 1
        for c in columns:
            for i in range(length - 2):
                if c[i] == c[i + 1]:
                    available += 1
        if available == 0:
            return False

        # if 2048 you won
        for _ in table:
            for e in _:
                if e == 2048:
                    return True


if __name__ == "__main__":
    main()
