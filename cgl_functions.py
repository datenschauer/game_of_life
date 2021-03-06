import copy
import os
import time
import random


def cgl_initialize(size: int = 5, weight_t: int = 1, weight_f: int = 1):
    """
    create a matrix of size x and populate with True und False
    with weight y for True
    """
    population = [True, False]
    return [random.choices(population, weights=[weight_t, weight_f], k=size) for _ in range(size)]


def cgl_clear(sec):
    if os.name == "posix":
        time.sleep(sec)
        os.system('clear')
    else:
        time.sleep(sec)
        os.system('cls')


def cgl_get_alives(i: int, j: int, matrix: list) -> (bool, list):
    """
    Check the eight surrounding Cells of a cell (i,j),
    and store how many cells around them are alive.
    :return: (status of cell, list of statuses of surrounding cells)
    """
    status = matrix[i][j]

    alives = []

    # check the surrounding cells but beware of borders
    if i - 1 >= 0 and j - 1 >= 0:
        alives.append(matrix[i - 1][j - 1])

    if j - 1 >= 0:
        alives.append(matrix[i][j - 1])

    if i - 1 >= 0:
        alives.append(matrix[i - 1][j])

    if i - 1 >= 0 and j + 1 <= len(matrix[0]) - 1:
        alives.append(matrix[i - 1][j + 1])

    if j + 1 <= len(matrix[0]) - 1:
        alives.append(matrix[i][j + 1])

    if i + 1 <= len(matrix) - 1 and j - 1 >= 0:
        alives.append(matrix[i + 1][j - 1])

    if i + 1 <= len(matrix) - 1:
        alives.append(matrix[i + 1][j])

    if i + 1 <= len(matrix) - 1 and j + 1 <= len(matrix[0]) - 1:
        alives.append(matrix[i + 1][j + 1])

    return status, alives


def cgl_set_alive(i, j, matrix) -> bool:
    """the alives around a cell determine if a cell is alive or dead"""

    status, surrounding = cgl_get_alives(i, j, matrix)

    alives = surrounding.count(1)

    if status and alives in (2, 3):
        return True

    elif not status and alives == 3:
        return True

    else:
        return False


def cgl_update(matrix: list):
    matrix_copy = copy.deepcopy(matrix)

    for i in range(len(matrix)):

        for j in range(len(matrix[0])):
            matrix_copy[i][j] = cgl_set_alive(i, j, matrix)

    return matrix_copy


def cgl_print_matrix(matrix, cycle):
    print(
        """
    | Conway's Game of Life |
        """
    )
    alive = " # "
    dead = " . "
    for line in matrix:
        print("".join([alive if b else dead for b in line]))
    print(f"\nGeneration: {cycle}")


def cgl_play(matrix, cycles, sec=1):
    cycle = 1
    cgl_print_matrix(matrix, cycle)
    cgl_clear(sec)

    while cycle <= cycles:
        matrix = cgl_update(matrix)

        if cgl_is_exit_status(matrix):
            break

        cgl_print_matrix(matrix, cycle)
        cgl_clear(sec)
        cycle += 1

    cgl_print_matrix(matrix, cycle)


def cgl_is_exit_status(matrix: list) -> bool:
    """check conditions when program should exit"""

    # first condition: all cells are dead
    if all([not any(el) for el in matrix]):
        return True
    # second condition: only stable forms established
    # to be done!
    else:
        return False

