from lib.matrix import Matrix


def contains_smudge(line_a, line_b):
    differences = 0
    for i in range(len(line_a)):
        if line_a[i] != line_b[i]:
            differences += 1
    return differences == 1


def split_after_row(matrix, i):
    top = list(reversed(matrix.rows[:i+1]))
    bottom = matrix.rows[i+1:]
    k = min(len(top), len(bottom))
    return top[:k], bottom[:k]


def split_after_column(matrix, j):
    left = list(reversed(matrix.columns[:j+1]))
    right = matrix.columns[j+1:]
    k = min(len(left), len(right))
    return left[:k], right[:k]


def find_reflection(matrix, smudges=0):
    for i in range(matrix.height - 1):
        top, bottom = split_after_row(matrix, i)
        smudge_candidates = 0
        for k in range(len(top)):
            if top[k] == bottom[k]:
                continue
            elif contains_smudge(top[k], bottom[k]):
                smudge_candidates += 1
                continue
            else:
                smudge_candidates = None
                break
        if smudge_candidates == smudges:
            return 100 * (i + 1)

    for j in range(matrix.width - 1):
        left, right = split_after_column(matrix, j)
        smudge_candidates = 0
        for k in range(len(left)):
            if left[k] == right[k]:
                continue
            elif contains_smudge(left[k], right[k]):
                smudge_candidates += 1
                continue
            else:
                smudge_candidates = None
                break
        if smudge_candidates == smudges:
            return j + 1

    return 0


def read_input():
    matrices = []
    with open('input/day13.txt') as file:
        lines = []
        for line in file.readlines():
            if line.strip():
                lines.append(line)
            else:
                matrix = Matrix.parse('\n'.join(lines))
                matrices.append(matrix)
                lines = []
        matrix = Matrix.parse('\n'.join(lines))
        matrices.append(matrix)
    return matrices


def solution_1():
    n = 0
    for matrix in read_input():
        n += find_reflection(matrix)
    return n


def solution_2():
    n = 0
    for matrix in read_input():
        n += find_reflection(matrix, smudges=1)
    return n


if __name__ == '__main__':
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
