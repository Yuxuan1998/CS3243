# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here
        domains = dict()
        self.assign = copy.deepcopy(self.puzzle)
        self.initializeDomain(domains)
        print(domains)
        for i in range(9):
            for j in range(9):
                domains[(i, j)] = self.computeDomain(i, j, self.assign, domains)
        print(domains)
        self.ans = self.backTrack(self.assign, domains)
        
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.
    def backTrack(self, assign, domains):
        print (assign)
        if self.isComplete(assign):
            return assign
        var_row, var_col = self.leastDomain(domains)
        var = (var_row, var_col)
        for val in domains[(var_row, var_col)]:
            assign[var_row][var_col] = val
            print"assign" + str(var_row) + "," + str(var_col) + "=" + str(val)
            isValid = self.isValid(var, assign)
            if isValid:
                print "is valid"
                inference = self.infer(var, domains, assign)
                if inference != "failure":
                    self.backTrack(assign, domains)
#                    result = self.backTrack(assign, domains)
#                    if self.isComplete(result):
#                        return result
            assign[var_row][var_col] = 0
            print "is invalid"
            print "assign (" + str(var_row) + ", " + str(var_col) + ") = 0"
    
    def infer(self, var, domains, assign):
        domainChange = list()
        neighbors = self.findNeighbors(var)
        var_val = assign[var[0]][var[1]]
        for nb in neighbors:
            if var_val in domains.get((nb[0], nb[1])):
                domainChange.append(nb)
                domains[(nb[0], nb[1])].remove(var_val)
                if self.isEmpty(domains[(nb[0], nb[1])]):
                    for x in domainChange:
                        domains[(x[0], x[1])].append(var_val)
                    return "failure"
        return domains

    def isComplete(self, assign):
        flag = True
        for i in range(9):
            for j in range(9):
                if assign[i][j] == 0:
                    flag = False
                    return flag
        return flag

    def isValid(self, var, assign):
        var_row = var[0]
        var_col = var[1]
        var_val = assign[var_row][var_col]
        for i in range(9):
            if i != var_row and assign[i][var_col] == var_val:
                return False
        for j in range(9):
            if j != var_col and assign[var_row][j] == var_val:
                return False
        box_top_row = (var_row / 3) * 3
        box_left_col = (var_col / 3) * 3
        for i in range(box_top_row, box_top_row + 3):
            for j in range(box_left_col, box_left_col + 3):
                if i != var_row and j != var_col and assign[i][j] == var_val:
                    return False
        
        return True

    
    def computeDomain(self, var_row, var_col, assign, domains):
        if assign[var_row][var_col] != 0:
            return domains[(var_row, var_col)]

        for i in range(9):
            val = assign[i][var_col]
            if val != 0 and i != var_row:
                if val in domains[(var_row, var_col)]:
                    print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                    print domains[(var_row, var_col)]
                    domains[(var_row, var_col)].remove(val)
                    print"(" + str(var_row) + "," + str(var_col) + ")" + "remove " + str(val)
                    print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                    print domains[(var_row, var_col)]
                    if self.isEmpty(domains[(var_row, var_col)]):
                        return domains[(var_row, var_col)]
        
        for j in range(9):
            val = assign[var_row][j]
            if val != 0 and j != var_col:
                if val in domains[(var_row, var_col)]:
                    print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                    print domains[(var_row, var_col)]
                    domains[(var_row, var_col)].remove(val)
                    print"(" + str(var_row) + "," + str(var_col) + ")" + "remove " + str(val)
                    print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                    print domains[(var_row, var_col)]
                    if self.isEmpty(domains[(var_row, var_col)]):
                        return domains[(var_row, var_col)]

        box_top_row = (var_row / 3) * 3
        box_left_col = (var_col / 3) * 3

        for i in range(box_top_row, box_top_row + 3):
            for j in range(box_left_col, box_left_col + 3):
                val = assign[i][j]
                if val != 0 and i != var_row and j != var_col:
                    if val in domains[(var_row, var_col)]:
                        print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                        print domains[(var_row, var_col)]
                        domains[(var_row, var_col)].remove(val)
                        print"(" + str(var_row) + "," + str(var_col) + ")" + "remove " + str(val)
                        print "(" + str(var_row) + "," + str(var_col) + ") now has: " 
                        print domains[(var_row, var_col)]
                        if self.isEmpty(domains[(var_row, var_col)]):
                            return domains[(var_row, var_col)]

        return domains[(var_row, var_col)]

    def findNeighbors(self, var):
        neighbors = []
        var_row = var[0]
        var_col = var[1]
        for i in range(9):
            if i != var_row:
                neighbors.append((i, var_col))
        for j in range(9):
            if j != var_col:
                neighbors.append((var_row, j))
        
        box_top_row = (var_row / 3) * 3
        box_left_col = (var_col / 3) * 3

        for i in range(box_top_row, box_top_row + 3):
            for j in range(box_left_col, box_left_col + 3):
                if i != var_row and j != var_col:
                    neighbors.append((i, j))
        
        return neighbors


    def isEmpty(self, domain):
        if domain == None:
            return True
        return len(domain) == 0

    def leastDomain(self, domains):
        least_length = 9
        least_var = (9, 9)

        for i in range(9):
            for j in range(9):
                if self.assign[i][j] == 0:
                    curr_length = len(domains[(i, j)])
                    curr_var = (i, j)
                    if curr_length < least_length:
                        least_length = curr_length
                        least_var = curr_var
        return least_var
    
    def initializeDomain(self, domains):
        for i in range(9):
            for j in range(9):
                if self.assign[i][j] != 0:
                    domains[(i, j)] = [self.assign[i][j]]
                else:
                    domains[(i, j)] = list((1,2,3,4,5,6,7,8,9))

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
