import random
import argparse
import csv
import ast
import numpy as np
from tabulate import tabulate

class Bakuro_Gen():

    def __init__(self, bits):
        self.grid_size = bits + 1
        self.bits = bits

    def get_column(self, matrix, index):
        return [str(row[index]) for row in matrix if row[index] is not None]
    
    def get_row(self, matrix, index):
        return [str(x) for x in matrix[index] if x is not None]
 
    
    def generate_bin_grid(self):
        # random generation of binary numbers
        #bin_nums = [bin(x)[2:].rjust(bits, '0') for x in range(2**bits)]
        grid_size = self.bits
        grid = [[None for x in range(grid_size+1)] for x in range(grid_size+1)]
        #create grid with binary numbers
        for i in range(grid_size):
            for j in range(grid_size):
                grid[i][j] = random.randint(0,1)
        #solve by combining row and column elements for total
        for i in range(grid_size):
            row = self.get_row(grid, i)
            col = self.get_column(grid, i)
            col_binary = "".join(col) 
            row_binary = "".join(row)
            grid[i][grid_size] = int(row_binary, 2)
            grid[grid_size][i] = int(col_binary, 2)
        return grid

    def print_bin_grid(self, grid):
        print_grid = [] 
        for key, row in enumerate(grid):
            if key == len(grid) - 1:
                print_grid.append(row)
            else:
                print_grid.append([v if k == len(grid)-1 else None for k,v in enumerate(row)])
        return print_grid

    def get_table(self, grid, fmt):
        col_replace = "l" * self.grid_size
        col_replace_with = "|l|" * self.grid_size
        row_replace = "\\\\"
        row_replace_with = "\\\\ \\hline"
        return tabulate(grid, tablefmt=fmt).replace(row_replace, row_replace_with).replace(col_replace, col_replace_with)


    def save_grid(self, grid, filepath, fmt="latex"):
        solved = grid 
        unsolved = self.print_bin_grid(grid)
        t = tabulate(unsolved, tablefmt=fmt)
        with open('output/{}.tex'.format(filepath), 'w') as outputfile:
            outputfile.write("""\\documentclass[]{article}
            \\usepackage[margin=1in]{geometry}

            \\begin{document}
            \\section{Bakuro Exercise}""")
            outputfile.write(self.get_table(unsolved, fmt))
            outputfile.write("\\newpage \n \\section{Bakuro Solution} \n")
            outputfile.write(self.get_table(solved, fmt))
            outputfile.write("\n \\end{document}")

parser = argparse.ArgumentParser(description='Generate a bakuro grid')
parser.add_argument('--bits', default=4, help='size of numbers to generate', type=int)
parser.add_argument('--outfile', default=None, help='file path to save grid to', type=str)
args = parser.parse_args()
b = Bakuro_Gen(args.bits)
grid = b.generate_bin_grid()
print_grid = b.print_bin_grid(grid)
if args.outfile:
    b.save_grid(grid, args.outfile)
