# --- Day 11: Cosmic Expansion ---
#
# You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to
# be a researcher studying cosmic expansion using the giant telescope here.
#
# He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he
# confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once
# he's done with today's observation analysis.
#
# Maybe you can help him with the analysis to speed things up?
#
# The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The
# image includes empty space (.) and galaxies (#). For example:
# ...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....
#
# The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies.
# However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the
# observatory.
#
# Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or
# columns that contain no galaxies should all actually be twice as big.
#
# In the above example, three columns and two rows contain no galaxies:
#    v  v  v
#  ...#......
#  .......#..
#  #.........
# >..........<
#  ......#...
#  .#........
#  .........#
# >..........<
#  .......#..
#  #...#.....
#    ^  ^  ^
#
# These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:
# ....#........
# .........#...
# #............
# .............
# .............
# ........#....
# .#...........
# ............#
# .............
# .............
# .........#...
# #....#.......
#
# Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to
# assign every galaxy a unique number:
# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# ............6
# .............
# .............
# .........7...
# 8....9.......
#
# In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each
# pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly
# one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)
#
# For example, here is one of the shortest paths between galaxies 5 and 9:
# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .##.........6
# ..##.........
# ...##........
# ....##...7...
# 8....9.......
#
# This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations
# marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:
# Between galaxy 1 and galaxy 7: 15
# Between galaxy 3 and galaxy 6: 17
# Between galaxy 8 and galaxy 9: 5
#
# In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.
#
# Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of
# these lengths?
#
# --- Part Two ---
#
# The galaxies are much older (and thus much farther apart) than the researcher initially estimated.
#
# Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each
# empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty
# columns.
#
# (In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between
# every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the
# shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond
# these values.)
#
# Starting with the same initial image, expand the universe according to these new rules, then find the length of the
# shortest path between every pair of galaxies. What is the sum of these lengths?

import itertools
from lib.matrix import Matrix
from lib.metrics import Point, manhattan_distance


def is_empty(row):
    return all(element == '.' for element in row)


def sum_distances(insert_count):
    matrix = Matrix.from_file('input/day11.txt')
    points = [Point(i, j) for i, j in matrix.coordinates if matrix[i][j] == '#']
    already_calculated = set()

    # rows as a list of True/False value reflecting whether the row is empty or not
    rows = [is_empty(matrix.row(i)) for i in range(matrix.height)]

    # columns as a list of True/False value reflecting whether the column is empty or not
    columns = [is_empty(matrix.column(j)) for j in range(matrix.width)]

    d = 0
    for p1, p2 in itertools.product(points, points):
        if p1 != p2:
            if (p2, p1) in already_calculated:
                continue

            min_i = min(p1.x, p2.x)
            max_i = max(p1.x, p2.x)
            row_range = rows[min_i:max_i]
            empty_rows = sum(1 if row else 0 for row in row_range)

            min_j = min(p1.y, p2.y)
            max_j = max(p1.y, p2.y)
            column_range = columns[min_j:max_j]
            empty_columns = sum(1 if column else 0 for column in column_range)

            distance = manhattan_distance(p1, p2)
            distance += empty_rows * insert_count
            distance += empty_columns * insert_count
            d += distance

            already_calculated.add((p1, p2))
    return d


def solution_1():
    return sum_distances(insert_count=1)


def solution_2():
    return sum_distances(insert_count=1_000_000 - 1)


if __name__ == '__main__':
    print('--- Day 11: Cosmic Expansion ---')
    print('What is the sum of these lengths?')
    print(solution_1())
    print('--- Part Two ---')
    print('What is the sum of these lengths?')
    print(solution_2())
