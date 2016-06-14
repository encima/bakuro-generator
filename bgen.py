import random
import argparse

class Bakuro_Gen():

	def __init__(self, grid_size, bits):
		self.grid_size = grid_size
		self.bits = bits
		#calculate the max number that can be represented by the bits
		self.max_num = (2**self.bits)-1
	
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

	def generate_grid(self):
		grid = [[random.randrange(0, self.max_num) for _ in range(self.grid_size - 1)] for _ in range(self.grid_size - 1)]
		for row in grid:
			for index,val in enumerate(row):
				if(val == 0):
					row[index] = None
				else:
					row[index] = {'dec':val, 'bin':bin(val)}
		return self.solve_grid(grid)

	def print_grid(self, grid, binary = False, solved = True):
		for row_index, row in enumerate(grid):
			unsolved = ''
			for col_index, value in enumerate(row):
				val = grid[row_index][col_index]
				if 'bin' in val:
					if binary:
						unsolved += str(val['bin']) + ' . '
					else:
						unsolved += str(val['dec']) + ' . '
				elif ('row_total' in val or 'col_total' in val) and solved:
					unsolved += str(val) + ' . '
				else:
					unsolved += ('[  ] . ')
			print(unsolved)


parser = argparse.ArgumentParser(description='Generate a bakuro grid')
parser.add_argument('--grid_size', default=5, help='size of grid to generate', type=int)
parser.add_argument('--bits', default=4, help='size of numbers to generate', type=int)
parser.add_argument('--sol', default=True, help='Print the solved grid', type=bool)
args = parser.parse_args()
b = Bakuro_Gen(args.grid_size, args.bits)
grid = b.generate_grid()
b.print_grid(grid, binary = False, solved = False)
print('---------')
b.print_grid(grid, binary = False, solved = True)
#TODO solve grids passed to program in txt file
#TODO prettify grid printing and add zero padding
