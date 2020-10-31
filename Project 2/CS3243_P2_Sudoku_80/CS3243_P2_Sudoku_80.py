import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

# returns a new puzzle which is identical to the puzzle passed into this method
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists
        self.matrix = [[Cell(0) for row in range(9)] for col in range(9)]
        for row in range(9):
            for col in range(9):
                self.matrix[row][col].value = self.puzzle[row][col]
        
        self.row_constraints = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)]
        self.col_constraints = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)]
        self.box_constraints = [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(3)] for j in range(3)]
        for row in range(9):
            for col in range(9):
                val = self.matrix[row][col].value
                if val != 0:
                    self.row_constraints[row].remove(val)
                    self.col_constraints[col].remove(val)
                    self.box_constraints[row // 3][col // 3].remove(val)

        self.initialize_domains()
        self.initialize_neighbors()

    def solve(self):
        # TODO: Write your code here
        self.backtrack_search()
        return self.matrix

    
    def backtrack_search(self):
        if self.is_complete():
            return True
        if not self.is_valid():
            return False
        (row, col) = self.least_domain()
        for val in self.matrix[row][col].domain:
            domain_changes = dict()
            self.matrix[row][col].value = val
            self.update(row, col, val, domain_changes)
            result = self.backtrack_search()
            if result is True:
                return True
            else:
                self.matrix[row][col].value = 0
                self.unupdate(row, col, domain_changes)

    def initialize_domains(self):
        for row in range(9):
            for col in range(9):
                domain = set()
                for i in self.row_constraints[row]:
                    if i in self.col_constraints[col] and i in self.box_constraints[row // 3][col // 3]:
                        domain.add(i)
                self.matrix[row][col].domain = domain

    def initialize_neighbors(self):
        for row in range(9):
            for col in range(9):
                self.matrix[row][col].neighbors = self.find_neighbors(row, col)

    def find_neighbors(self, var_row, var_col):
        neighbors = set()
        for i in range(9):
            if i != var_row and self.matrix[i][var_col].value == 0:
                neighbors.add((i, var_col))
        for j in range(9):
            if j != var_col and self.matrix[var_row][j].value == 0:
                neighbors.add((var_row, j))
        box_top_row = (var_row // 3) * 3
        box_left_col = (var_col // 3) * 3
        for i in range(box_top_row, box_top_row + 3):
            for j in range(box_left_col, box_left_col + 3):
                if i != var_row and j != var_col and self.matrix[i][j].value == 0:
                    neighbors.add((i, j))
        return neighbors

    def least_domain(self):
        least_domain = 100
        row = 10
        col = 10
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j].value == 0:
                    curr_domain = len(self.matrix[i][j].domain)
                    if curr_domain < least_domain:
                        least_domain = curr_domain
                        row = i
                        col = j
                    if curr_domain == least_domain:
                        # if curr_var has more neighbors than the least_var, then accept curr_var
                        if len(self.matrix[i][j].neighbors) > len(self.matrix[row][col].neighbors):
                            least_domain = curr_domain
                            row = i
                            col = j

        return (row, col)

    def update(self, row, col, val, domain_changes):
        for i, j in self.matrix[row][col].neighbors:
            self.matrix[i][j].neighbors.remove((row, col))
            if val in self.matrix[i][j].domain and self.matrix[i][j].value == 0:
                self.matrix[i][j].domain.remove(val)
                if domain_changes.has_key((i, j)):
                    domain_changes[(i, j)].add(val)
                else:
                    domain_changes[(i, j)] = set([val])

    def unupdate(self, row, col, domain_changes):
        for i, j in self.matrix[row][col].neighbors:
            self.matrix[i][j].neighbors.add((row, col))
        for (row, col), changes in domain_changes.items():
            while changes:
                self.matrix[row][col].domain.add(changes.pop())

    def is_valid(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j].value == 0 and len(self.matrix[i][j].domain) == 0:
                    return False
        return True
    
    def is_complete(self):
        for row in range(9):
            for col in range(9):
                if self.matrix[row][col].value == 0:
                    return False
        return True

class Cell:
    def __init__(self, value):
        self.value = value
        self.domain = set()
        self.neighbors = set()

    def __str__(self):
        return str(self.value)


    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
