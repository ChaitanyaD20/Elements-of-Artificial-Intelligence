#a0:

USER NAME: CHAITANYA SHEKHAR DESHPANDE

USER ID: cdeshpa

Part 1: Navigation: route_pichu.py

To implement the route_pichu.py program, I will be defining the search abstraction in the following way:
1. Set of Valid States: A Valid State will be considered such that “p” will traverse only the node which is “.” and not “X”. 
2. Successor Function: A successor function will move the “p” in any one valid direction when a “.” exists either in “U”,”R”,”L” or “D” returning a tuple of row and column of next state. This will be similar to the traversal of a child node in a tree.
3. Cost Function: The cost function will be the number of steps taken by “p” during each traversal of “p”. As “p” can only move in 1 direction(Left, Right, Up or Down) with 1 step only where “.” is present, hence “p” will have a cost function of 1. 
4. Goal State: The Goal State is when “p” will reach “@” after satisfying all the constraints.
5. Initial State: The Initial State is the (N rows*M columns) matrix present in map.txt or map2.txt which will be passed on the command line. It consists of a “p” which will be the starting point of our search towards reaching “@”.

INITIAL EXECUTION OF THE PROBLEM:
When we execute the initial program, the “p” begins its navigation to all the possible positions where “.” is present. The solution could be good if “p” can navigate to only one position, but the problem begins when it has more than 1 choice to navigate and it gets stuck in an infinite loop. 

SOLUTION TO THE PROBLEM:
I have implemented the Depth First Search algorithm to track the path of pichu from initial to goal state. We keep traversing the children of a node and keep updating the fringe with current value and it will be used as stack. We need to keep a track of previously visited nodes and if any particular node will not be a part of the path to reach “@”, it should be discarded. This can be done using a stack data structure. So to search the path for “p” to reach the goal node “@”, we can consider the map as a Tree and we need to traverse all the “.” which will be considered as a child node. Since the previous state is also a child node(as it also contains “.”), to avoid re-traversal of this, we use the visited list. The fringe is the stack here and it gets appended with the current node if it is not in visited. All child nodes will be pushed/appended to the stack after popping the top, i.e. its parent.  So the top of stack contains the current child node and unvisited child nodes will be below the visited child node in the stack. The top of stack, i.e. current child node gets popped off while generating its child nodes. Thus when the goal state is reached, the Depth First Search Traversal is complete.

The problem with it is that the solution also includes the nodes which have been visited, but are later discarded. I have designed an algorithm to remove the nodes which were visited during the search, but are not included in the path.

1. So initially, along with the fringe, we have a list named visited, which will store all the states which are visited. visited is initialized with initial board. visited list helps us to not revisit any previous state.
2. I have also initialized 2 more lists: optimal_path and deletion_list. Optimal path will store the correct traversal of the states. deletion_list will be used later on. 
3. I will be using map.txt as sample explanation. So we begin traversal from (5,0), traverse to the next valid state, visited list will ensure that it doesn't revisit a previous state.
4. If a dead end is reached, it will backtrack to the previous node, however that particular node will not be re-appended to the fringe. We will directly traverse to the next child of previous node.
5. For every traversal, based on array indexing, we will be updating the path with "U","L","R" or "D" and this will be stored in move_string. Eventually a path string with all nodes will be generated.
6. However the path also contains nodes which got backtracked, hence it is not optimal.
7. To find the optimal path, we need to delete the nodes that were visited, but are not a part of the path. So for map.txt, the fringe after we reach "@" is: 
[(5, 0), (4, 0), (3, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (4, 4), (3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (1, 5), (1, 4), (4, 6), (5, 6)].
8. However we can see that after (2,3), the next value is shown as (3,2), because a dead-end was reached at (2,3) and it backtracked to (2,2) and explored (3,2).
9. It can be observed that whenever the sum of the difference between the current and previous row values, and current and previous column values is greater than 1, it means that backtracking has taken place.
10. So we can simply place the previous tuple in deletion list and later it can be deleted from optimal_path, thereby yielding the optimal path. We need to keep adding such cases in deletion_list until the sum is 1.
11. For example: (2,3) to (3,2), it is abs(3-2)+abs(2-3)=2>1, hence we delete (2,3).
12. Similarly from (1,4) to (4,6), it is abs(6-4)+abs(4-1)=5. So we deleted (1,4). Next we have (1,5) to (4,6), the sum is 4, similarly for (1,6) sum is 3, for (2,6) it is 2, and finally for (3,6) to (4,6) sum is 1.
13. So after adding to deletion list, (1,4),(1,5),(1,6) and (2,6) are deleted. Thus the optimal path is generated.
14. Based on the evaluation of the string using "U,D,R,L", we generate the path and length of that string is the distance of the path.
15. If no path exists, then we return -1.

PART 2: Hide and Seek: arrange_pichus.py
1. Set of Valid States: Valid State is a state which satisfies all the constraints, i.e. 2 “p’s” cannot be in the same row or column, if they are present in a same row or column, there must be an “X” between them. So the set of valid states is a set which satisfies all the constraints.
2. Successor Function: The successor function adds a new “p” to an empty node, i.e. “.”. Thus when successor function is called, there will the same number of states generated as many as the number of “.” are present in the current map of fringe.
3. Cost Function: The cost function will be the cost required to generate a new successor of the fringe, i.e. after it checks the next state, i.e. for “p” to traverse to “.”. As it can only take 1 step at a time, the cost function will be 1 here per traversal.
4. Goal State: Goal state is a state which contains the number of pichus “p” which have been passed in the command line during the program execution satisfying all the constraints. eg. python3 arrange_pichus.py map.txt 9, will generate 9 pichus on a new board, in which 2 “p’s” will not be in the same row or column unless there is an “X” between them.
5. Initial State: The Initial State is the (N rows*M columns) matrix present in map.txt or map2.txt which will be passed on the command line. It must contain a “p”, whereas it can contain “X”, “.” or “@”.
 
INITIAL EXECUTION OF THE PROBLEM:
When we execute the initial arrange_pichus.py program, it only generates the successor states, and fits the number of “p’s” asked on the command line, but it does not satisfy the constraints, i.e. there are multiple “p’s” in the same row or column without any “X” between them. So we need to program the constraints to the initial map and eventually return the correct map. 

SOLUTION TO THE PROBLEM:
Initially we have the map.txt file, i.e. the initial_board which is considered as the tree and initial state. So we will be traversing the tree by placing “p” on the “.” positions one by one without removing the previous “p” which was in a valid position, checking if that particular state is valid, i.e. if they are not on the same row or column or there could be an “X” in between then. If a valid state is found, we then generate the successors of the new states, i.e. containing one more “p” than its previous state. Once a valid state is found, the fringe gets updated with that value, and the successors function is called on it. Thus that node becomes root and it’s child nodes are generated. This process is repeated till we have a goal state with number of “p’s” as requested in command line with all the constraints satisfied. 
1. To implement the map such that the constraints are satisfied, I have defined a helper function named: check_validity(matrix) which takes the input as a matrix which is a part of the state space after successor function has been applied to the previous state. Over here I will be iterating over the entire matrix along the rows, and this same function will be called on the transpose of the matrix to check the columns' validity. So we iterate over the rows of the matrix(array), if we encounter "p", then we slice the row from the next element and check the further elements. 
2. If it encounters "X", then we set the flag to True and break, if there is a ".", we will continue and if there is a "p", then we set the flag as False and break as we don't need to scan the entire row in such case. However it is possible that there may be a scenario like "pXpp" so we need to ensure that it will not allow such a case. So the last else mentioned below has a continue operation such that we don't encounter repeated p's after producing an “X”.
3. If another "p" is encountered, the same logic used above will be reused. If anywhere we find that the flag is False, the entire row execution is stopped. After all the scanning is performed, the flag is returned.
4. Within the solve() function, first the fringe has been assigned with the initial board, i.e. the map. While the fringe is not empty, we will generate the successors of fringe, i.e. by adding a "p", one by one to every position with ".". We also call the transpose function to check the column validity of the map. So we check the flags of row matrix as well as the column matrix. If both are true, it means that the current state is valid, and will be appended to the fringe. We will now break it and then the successors function will run on the new fringe value, i.e. the recent valid state. Any invalid states that are generated will get rejected by the “if” statement.
5. If at any stage the goal state is encountered, it will be returned. Thus, a new board with requested number of “p’s” in correct and valid positions is generated. If not, then None is returned. 
