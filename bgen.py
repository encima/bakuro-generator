import random
import argparse
import csv
import ast
import png
import numpy as np
from tabulate import tabulate

class Bakuro_Gen():

	def __init__(self):
		pass

	def solve_grid(self, grid):
		#Columns
		col_totals = []
		for row_ind, row in enumerate(zip(*grid)):
			col_total = 0
			for col_ind, val in enumerate(row):
				if val is None:
					grid[col_ind][row_ind] = {'col_total':col_total}
					col_total = 0
				elif col_ind == len(row) - 1:
					col_total += val['dec']
					col_totals.append({'col_total':col_total})
					break
				else:
					col_total += val['dec']
		#Rows
		for index, row in enumerate(grid):
			row_total = 0
			for ind, val in enumerate(row):
				if 'col_total' in val:
					row[ind]['row_total'] = row_total
					row_total = 0
				elif ind == len(row) -1:
					row_total += val['dec']
					row.append({'row_total': row_total})
					break
				else:
					row_total += val['dec']
		grid.append(col_totals)
		return grid

	def generate_grid(self, grid_size=5, bits=4, max_num=None):
		self.grid_size = grid_size
		self.bits = bits
		#calculate the max number that can be represented by the bits
		if max_num is None:
			self.max_num = (2**self.bits)-1
		else:
			self.max_num = max_num
		grid = [[random.randrange(0, self.max_num) for _ in range(self.grid_size - 1)] for _ in range(self.grid_size - 1)]
		for row in grid:
			for index,val in enumerate(row):
				if(val == 0):
					row[index] = None
				else:
					row[index] = {'dec':val, 'bin':bin(val)}
		return self.solve_grid(grid)

	def read_grid(self, filepath):
		grid = []
		with open(filepath, "r") as infile:
			for line in csv.reader(infile):
				row = []
				for item in line:
					#convert string item to dict
					row.append(ast.literal_eval(item))
				grid.append(row)

		return grid

	def print_grid(self, grid, binary = False, solved = True):
		for row_index, row in enumerate(grid):
			unsolved = ''
			for col_index, value in enumerate(row):
				val = grid[row_index][col_index]
				if 'bin' in val and solved:
					if binary:
						unsolved += str(val['bin']) + (25*' ')
					else:
						unsolved += str(val['dec']) + (25*' ')
				elif 'bin' in val:
					unsolved += '[ ]' + (25*' ')
				elif ('row_total' in val or 'col_total' in val):
					unsolved += str(val)
				else:
					unsolved += ('[  ] . ')
		x = np.array(grid)
		print(tabulate(x, tablefmt="grid"))

	def save_grid(self, grid, filepath):
		x = np.array(grid)
		t = tabulate(x, tablefmt="latex")
		with open('{}.tex'.format(filepath), 'w') as outputfile:
			outputfile.write(t)


parser = argparse.ArgumentParser(description='Generate a bakuro grid')
parser.add_argument('--grid_size', default=5, help='size of grid to generate', type=int)
parser.add_argument('--bits', default=4, help='size of numbers to generate', type=int)
parser.add_argument('--sol', default=True, help='Print the solved grid', type=bool)
parser.add_argument('--max_num', default=None, help='Maximum number to generate up to, calculated from bits if none', type=int)
parser.add_argument('--outfile', default=None, help='file path to save grid to', type=str)
parser.add_argument('--infile', default=None, help='file path to read grid from', type=str)
args = parser.parse_args()
b = Bakuro_Gen()
if args.infile:
	grid = b.read_grid(args.infile)
	b.print_grid(grid, binary = False, solved = False)
else:
	grid = b.generate_grid(args.grid_size, args.bits, args.max_num)
	b.print_grid(grid, binary = False, solved = False)
	print('---------')
	#b.print_grid(grid, binary = False, solved = True)
if args.outfile:
	b.save_grid(grid, args.outfile)
