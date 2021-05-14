import sys
import numpy
import heapq

ROWS = 4
COLS = 5


def leftRotate(lists, row):
    output_list = lists.copy()
    for i in range(0, COLS):
        if (i - 1 >= 0):
            output_list[row][i - 1] = lists[row][i]
        else:
            output_list[row][COLS + i - 1] = lists[row][i]

    return output_list


def rightRotate(lists, row):
    output_list = lists.copy()
    for i in range(0, COLS):
        if (i + 1 < COLS):
            output_list[row][i + 1] = lists[row][i]
        else:
            output_list[row][i + 1 - COLS] = lists[row][i]

    return output_list


def upRotate(lists, col):
    output_list = lists.copy()
    for i in range(0, ROWS):
        if (i - 1 >= 0):
            output_list[i - 1][col] = lists[i][col]
        else:
            output_list[ROWS + i - 1][col] = lists[i][col]

    return output_list


def downRotate(lists, col):
    output_list = lists.copy()
    for i in range(0, ROWS):
        if (i + 1 < ROWS):
            output_list[i + 1][col] = lists[i][col]
        else:
            output_list[i + 1 - ROWS][col] = lists[i][col]

    return output_list


def printable_board(board):
    return [('%3d ') * COLS % board[j:(j + COLS)] for j in range(0, ROWS * COLS, COLS)]


def heuristic(next_state):
    mismatched = 0
    for i in range(0, len(next_state)):
        if i + 1 != next_state[i]:
            mismatched = mismatched + 1
    return mismatched


# return a list of possible successor states 
def successors(state_tuple):
    successors = []
    state = numpy.reshape((state_tuple[0]), (ROWS, COLS))

    for r in range(0, ROWS):
        if r % 2 == 0:
            next_state = tuple(leftRotate(state, r).flatten())
            curr_path = state_tuple[1].copy()
            curr_path.append('L' + str(r + 1))
            successors.append(
                (next_state, curr_path, state_tuple[2] + 1, heuristic(next_state)))
        else:
            next_state = tuple(rightRotate(state, r).flatten())
            curr_path = state_tuple[1].copy()
            curr_path.append('R' + str(r + 1))
            successors.append(
                (next_state, curr_path, state_tuple[2] + 1, heuristic(next_state)))

    for c in range(0, COLS):
        if c % 2 == 0:
            next_state = tuple(upRotate(state, c).flatten())
            curr_path = state_tuple[1].copy()
            curr_path.append('U' + str(c + 1))
            successors.append(
                (next_state, curr_path, state_tuple[2] + 1, heuristic(next_state)))
        else:
            next_state = tuple(downRotate(state, c).flatten())
            curr_path = state_tuple[1].copy()
            curr_path.append('D' + str(c + 1))
            successors.append(
                (next_state, curr_path, state_tuple[2] + 1, heuristic(next_state)))
    return successors


# check if we've reached the goal
def is_goal(state):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    if state == goal_state:
        return True
    return False


def solve(initial_board):
    if is_goal(initial_board): return []
    curr_path = []
    curr_cost = 0
    curr_huristic = 0
    fringe = []
    heapq.heappush(fringe, (curr_cost + curr_huristic, (initial_board, curr_path, curr_cost, curr_huristic)))
    while fringe:
        state = heapq.heappop(fringe)[1]
        for succ in successors(state):
            if is_goal(succ[0]):
                return succ[1]
            else:
                Astar = succ[3] + succ[2]
                heapq.heappush(fringe, (Astar, succ))
    return -1

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))