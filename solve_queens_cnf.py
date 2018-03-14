import pycosat
import itertools
import argparse


def generate_cnf(n):
	clauses = []
	#only one true on the rows
	for row in range(n):
		clauses.append(range(1 + n * row, 1 + n * (row + 1)))
		clauses.extend(itertools.combinations(range(-1 - n * row, -1 - (row + 1) * n, -1), 2))
	#only one true om the columns
	for column in range(n):
		clauses.append(range(1 + column, 1 + column + n * n, n))
		clauses.extend(itertools.combinations(range(-1 - column, -1 - column - n * n, -n), 2))
	#maximum one true on looking left diagonals
	for i in range(n):
		diag = []
		x, y = i, n - 1
		while x >= 0 and y >= 0:
			diag.append(-1 -(y * n + x))
			x -= 1
			y -= 1
		clauses.extend(itertools.combinations(diag, 2))
		diag.clear()
		x, y = n - 1, i
		while x >= 0 and y >= 0:
			diag.append(-1 -(y * n + x))
			x -= 1
			y -= 1
		clauses.extend(itertools.combinations(diag, 2))
	#maximum one true on looking right diagonals
	for i in range(n):
		diag = []
		x, y = 0, i
		while 0 <= x < n and 0 <= y < n:
			diag.append(-1 -(y * n + x))
			x += 1
			y -= 1
		clauses.extend(itertools.combinations(diag, 2))
		diag.clear()
		x, y = i, n - 1
		while 0 <= x < n and 0 <= y < n:
			diag.append(-1 -(y * n + x))
			x += 1
			y -= 1
		clauses.extend(itertools.combinations(diag, 2))
	return clauses


def main():
	parser = argparse.ArgumentParser(description='N-Queens CNF solver')
	parser.add_argument('--count', help='determine the number of the solutions', action='store_true')
	parser.add_argument('n', type=int, help='board size')
	args = parser.parse_args()
	cnf = generate_cnf(args.n)
	print("Number of clauses in the CNF formula:", len(cnf))
	result = pycosat.solve(cnf)
	if result == 'UNSAT':
		print("No solution")
	else:
		for row in range(args.n):
			print(*('.' if x < 0 else 'Q' for x in result[row * args.n : row * args.n + args.n]), sep='')
		if args.count:
			print('Total solutions:', len(list(pycosat.itersolve(cnf))))


if __name__ == '__main__':
	main()
