#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : CHAITANYA SHEKHAR DESHPANDE, cdeshpa
#
# Based on skeleton code in CSCI B551, Spring 2021
#


import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' ]

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k

"""
To implement the map such that the constraints are satisfied, I have defined a helper function named: check_validity(matrix) which takes the input as a matrix which is a part of the the state space
after successor function has been applied to the previous state. Over here I will be iterating over the entire matrix along the rows, and this same function will be called on the transpose of the matrix
to check the columns' validity. So we iterate over the rows of the matrix(array), if we encounter "p", then we slice the row from the next element and check the further elements. 
If it encounters "X", then we set the flag to True and break, if there is a ".", we will continue and if there is a "p", then we set the flag as False and break as we don't need to scan the entire row in such case.
However it is possible that there may be a scenario like "pXpp" so we need to ensure that it will not allow such a case. So the last else mentioned below has a continue operation such that we don't encounter repated p's.
If another "p" is encountered, the same logic used above will be reused. If anywhere we find that the flag is False, the entire row execution is stopped. After all scanning is performed, the flag is returned.
"""
def check_validity(matrix):
	flag=True
	for i in range(len(matrix)):
		for k in range(len(matrix[i])):
			if matrix[i][k]=="p" and flag==True:
				for j in range(len(matrix[i][k+1:])):
					if matrix[i][k+1:][j]=="X":
						flag=True
						break
					elif matrix[i][k+1:][j]=="p":
						flag=False
						break
					else:
						continue
			elif(flag==False):
				break
			else:
				continue

	return flag


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#

"""
Within the solve() function, first the fringe has been assigned with the initial board, i.e. the map. While the fringe is not empty, we will generate the successors of fringe, i.e. by adding a "p",
one by one to every position with ".". We also call the transpose function to check the column validity of the map. So we check the flags of row matrix as well as the column matrix. If both are true,
it means that the current state is valid, and will be appended to the fringe. We will now break it and then a the successors function will run on the new fringe value, i.e. the recent valid state.
If at any stage the goal is encountered, it will be returned.
"""
def solve(initial_board, k):
    fringe = [initial_board]
    while(len(fringe)>0):
    	for s in successors( fringe.pop() ):
    		#The below line, "transpose_s=list(map(list, zip(*s)))" has been used as the shortcut to generate the transpose of a matrix and its source page is: https://stackoverflow.com/questions/6473679/transpose-list-of-lists
    		transpose_s=list(map(list, zip(*s)))
    		#The previous line has its source as https://stackoverflow.com/questions/6473679/transpose-list-of-lists
	    	if (check_validity(s) and check_validity(transpose_s)==True):
	    		fringe.append(s)
	    		if (is_goal(s, k)):
	    			return(s,True)
	    			break
	    		else:
	    			break
	    		
    return ([],False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")