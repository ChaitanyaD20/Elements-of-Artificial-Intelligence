#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : CHAITANYA SHEKHAR DESHPANDE, cdeshpa
#
# Based on skeleton code provided in CSCI B551, Spring 2021.


import sys
import json

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

	# Return only moves that are within the board and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
#
"""
1. I have implemented the Depth First Search algorithm to track the path of pichu from initial to goal state. We keep traversing the children of a node and keep updating the fringe with current value and it will be used as a stack.
The problem with it is that the solution also includes the nodes which have been visited, but are later discarded. I have designed an algorithm to remove the nodes which were visited during the search, but are not included in the path. 
2. So initially, along with the fringe, we have a list named visited, which will store all the states which are visited. visited is initialized with initial board. visited list helps us to not revisit any previous state.
I have also initialized 2 more lists: optimal_path and deletion_list. Optimal path will store the correct traversal of the states. deletion_list will be used later on. 
3. I will be using map.txt as sample explanation. So we begin traversal from (5,0), traverse to the next valid state, visited list will ensure that it doesn't revisit a previous state.
4. If a dead end is reached, it will backtrack to the previous node, however that particular node will not be re-appended to the fringe. We will directly traverse to the next child of previous node.
5. For every traversal, based on array indexing, we will be updating the path with "U","L","R" or "D" and this will be stored in move_string. Eventually a path string with all nodes will be generated.
6. However the path also contains nodes which got backtracked, hence it is not optimal.
7. To find the optimal path, we need to delete the nodes that were visited, but are not a part of the path. So for map.txt, the fringe after we reach "@" is: 
[(5, 0), (4, 0), (3, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (4, 4), (3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (1, 5), (1, 4), (4, 6), (5, 6)].
8. However we can see that after (2,3), the next value is shown as (3,2), because a dead-end was reached at (2,3) and it backtracked to (2,2) and explored (3,2).
9. It can be observed that whenever the sum of the difference between the current and previous row values, and current and previous column values is greater than 1, it means that backtracking has taken place.
10. So we can simply place the previous tuple in deletion list and later it can be deleted from optimal_path, thereby yielding the optimal path. We need to keep adding such cases in deletion_list until the sum is 1.
11. For (2,3) to (3,2), it is abs(3-2)+abs(2-3)=2>1, hence we delete (2,3).
12. Similarly from (1,4) to (4,6), it is abs(6-4)+abs(4-1)=5. So we deleted (1,4). Next we have (1,5) to (4,6), the sum is 4, similarly for (1,6) sum is 3, for (2,6) it is 2, and finally for (3,6) to (4,6) sum is 1.
13. So after adding to deletion list, (1,4),(1,5),(1,6) and (2,6) are deleted. Thus the optimal path is generated.
14. Based on the evaluation of the string using "U,D,R,L", we generate the path and length of that string is the length of the path.  
"""

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0)]
        visited=[pichu_loc]
        move_string=""
        optimal_path=[]
        deletion_list=[]        
        while fringe:
                (curr_move, curr_dist)=fringe.pop()
                optimal_path.append(curr_move)
                for move in moves(house_map, *curr_move):
                        #print(move)
                        if house_map[move[0]][move[1]]=="@":
                                move_string=""
                                visited.append(move)                                 
                                optimal_path.append(move)
                                #print(optimal_path)                                                         
                                for i in range(1,len(optimal_path)-1):
                                        j=1
                                        if(abs(optimal_path[i][0]-optimal_path[i-1][0])+abs(optimal_path[i][1]-optimal_path[i-1][1])>1):
                                                while(abs(optimal_path[i][0]-optimal_path[i-j][0])+abs(optimal_path[i][1]-optimal_path[i-j][1])>1):
                                                        deletion_list.append(optimal_path[i-j])
                                                        j=j+1
                                        else:
                                                continue

                                for i in deletion_list:
                                        if i in optimal_path:
                                                optimal_path.remove(i)
                                
                                for i in range(1,len(optimal_path)):                
                
                                        if optimal_path[i][0]-optimal_path[i-1][0]==-1:
                                                move_string=move_string+"U"
                                        elif optimal_path[i][0]-optimal_path[i-1][0]==1:
                                                move_string=move_string+"D"
                                        elif optimal_path[i][1]-optimal_path[i-1][1]==1:
                                                move_string=move_string+"R"
                                        elif optimal_path[i][1]-optimal_path[i-1][1]==-1:
                                                move_string=move_string+"L"
                                
                                move_count=len(move_string)                               
                                return (move_count, move_string)  # return a dummy answer
                        else:   
                                
                                if move not in visited:
                                        visited.append(move)
                                        fringe.append((move, curr_dist + 1))
                                else:
                                        continue
        return -1, ""                    


# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Routing in this board:\n" + printable_board(house_map) + "\n")
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + str(solution[1]))

