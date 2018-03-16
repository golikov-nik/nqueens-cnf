import pycosat
import itertools
import argparse
import numpy as np


def encode(n, x, y):
	return 1 + n * y + x


def generate_diagonals(n, x, y, dx, dy):
	while 0 <= x < n and 0 <= y < n:
		yield -encode(n, x, y)
		x += dx
		y += dy


def all_pairs(iterable):
	return itertools.combinations(iterable, 2)


def only_one_queen(cells):
	#at least one
	yield cells

	#no more than one
	yield from all_pairs((-x for x in cells))


def generate_cnf(n):
	for row in range(n):
		yield from only_one_queen(range(encode(n, 0, row), encode(n, 0, row + 1)))
	for column in range(n):
		yield from only_one_queen(range(encode(n, column, 0), encode(n, column + n * n, 0), n))
	for i in range(n):
		#looking left
		yield from all_pairs(generate_diagonals(n, i, n - 1, -1, -1))
		yield from all_pairs(generate_diagonals(n, n - 1, i, -1, -1))
		
		#looking right
		yield from all_pairs(generate_diagonals(n, 0, i, 1, -1))
		yield from all_pairs(generate_diagonals(n, i, n - 1, 1, -1))



def main():
	parser = argparse.ArgumentParser(description='N-Queens CNF solver')
	parser.add_argument('--count', help='determine the number of the solutions', action='store_true')
	parser.add_argument('n', type=int, help='board size')
	args = parser.parse_args()
	cnf = list(generate_cnf(args.n))
	print("Number of clauses in the CNF formula:", len(cnf))
	result = pycosat.solve(cnf)
	if result == 'UNSAT':
		print("No solution")
	else:
		for row in np.array_split(result, args.n):
			print(*('_' if x < 0 else 'Q' for x in row), sep='')
		if args.count:
			print('Total solutions:', len(list(pycosat.itersolve(cnf))))


if __name__ == '__main__':
	main()
