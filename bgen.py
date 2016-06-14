import random
import argparse


class Bakuro_Gen():

	def __init__(self, grid_size):
		self.grid_size = grid_size
		self.generate_grid()

	def generate_grid(self):
		self.grid = [[random.randrange(0, 15) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
		for row in self.grid:
			for index,val in enumerate(row):
				if(val == 0):
					row[index] = None

	def calc_answers(self):
		pass 

	def print_grid(self):
		for row in self.grid:
			print(row)


parser = argparse.ArgumentParser(description='Generate a bakuro grid')
parser.add_argument('--grid_size', default=5, help='size of grid to generate', type=int)
parser.add_argument('--sol', default=True, help='Print the solved grid', type=bool)
args = parser.parse_args()
b = Bakuro_Gen(args.grid_size)
b.print_grid()


#TODO generate complete grid
#TODO generate grid with binary representation
#TODO print grid with no square filled in
#TODO solve grids passed to program in txt file
#TODO prettify grid printing and add zero padding
