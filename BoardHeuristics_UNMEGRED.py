from InfusionBoardUtils import InfusionBoard as Ib
import heapq
import numpy as np


def a_star_search(start_state):
    # Priority queue with (combined_score, state)
    open_set = []
    init_state = start_state.copy()
    heapq.heappush(open_set, (0 - board_value(start_state), start_state))

    # Track the best path to each state and cost to reach it
    came_from = {}
    path_costs = {start_state: 0}
    best_state = start_state
    best_combined_score = 0 - board_value(start_state)
    counter = 0

    while open_set:
        current_score, current = heapq.heappop(open_set)

        # If this is the best score we've seen, update the best state
        if current_score < best_combined_score:
            best_state = current
            best_combined_score = current_score

        # Explore neighbors
        for neighbor, cost in get_moves(current):
            counter += 1
            tentative_g_score = path_costs[current] + cost
            combined_score = tentative_g_score - board_value(neighbor)

            # Add neighbor to open_set if this path is better
            if neighbor not in path_costs or tentative_g_score < path_costs[neighbor]:
                came_from[neighbor] = current
                path_costs[neighbor] = tentative_g_score
                heapq.heappush(open_set, (combined_score, neighbor))

    print(f"Start state:\n{init_state}\nCounter: {counter}")
    return best_state, -best_combined_score


#heuristic values for easy mod
actNovNeb = 5
noStarNova = 0#-3
noNovaNeb = 0#-5
plasma = 1
deleteNova = 0#-5
# Example functions for testing:
def board_value(state):
    board,metrics = state.copy().forge_item()
    starAddCount = 400 if metrics["num_stars"] == 10 else metrics["num_stars"] * 20
    starAddCount = -10000 if metrics['num_stars'] > 10 else starAddCount
    return (starAddCount + metrics["activated_nova_nebulas"] * actNovNeb + metrics["nova_no_star_change"] * noStarNova + metrics["nebula_no_nova_created"] * noNovaNeb + metrics["new_plasma"] * plasma + metrics["nova_destroyed_by_blackhole"] *deleteNova) #/ metrics["stardust_spent"]

def get_moves(state):
    arr = []
    state_cost = state.get_board_cost()
    if state_cost > 256:
        return arr
    for y in range(state.ySize): #
        for x in range(state.xSize):
            for type in [0,1,2,3,4,5,7]: #
                if(state.board[0,y,x] == 9 or state.board[0,y,x] == type or (type == 0 and state.board[0,y,x] != 2) or (type == 7 and ((x,y) == (0,0) or (x,y) == (0,state.ySize-1) or (x,y) == (state.xSize-1,0) or (x,y) == (state.xSize-1,state.ySize-1)))): #nebula and nova cannot be beneficial in corner
                    continue
                new_state = state.copy()
                new_state.change_type(x,y,type,True)
                new_state_cost = new_state.get_board_cost()
                arr.append((new_state, new_state_cost - state_cost))
    for y in range(state.ySize):
        for x in range(state.xSize):
            if(not state.hasTurn[state.board[0,y,x]]):
                continue
            for i in range(-(state.board[1,y,x] - 1), (state.get_max_turn() - state.board[1,y,x])):
                if i != 0:
                    new_state = state.copy()
                    new_state.change_time(x,y,i)
                    new_state_cost = new_state.get_board_cost()
                    arr.append((new_state, new_state_cost - state_cost))
    # Define your own logic here to get the next states from the current state
    return arr

def is_goal(state):
    finalboard, metrics = state.forge_item()
    # Goal states are any which, if measured, have exactly 10 stars.
    if metrics["num_stars"] == 10: return True
    else: return False

def list_moves(state):
    '''A variant of get_moves that lists the function calls on state instead.'''
    arr = ["state.forge_item()"]
    state_cost = state.get_board_cost()
    if state_cost > 256:
        return arr
    for y in range(state.ySize): #
        for x in range(state.xSize):
            for type in [0,1,2,3,4,5,7]: #
                if(state.board[0,y,x] == 9 or state.board[0,y,x] == type or (type == 0 and state.board[0,y,x] != 2) or (type == 7 and ((x,y) == (0,0) or (x,y) == (0,state.ySize-1) or (x,y) == (state.xSize-1,0) or (x,y) == (state.xSize-1,state.ySize-1)))): #nebula and nova cannot be beneficial in corner
                    continue
                
                move = f"new_state.change_type({x},{y},{type},True)"
                print(move[:21])
                print(move[22])
                print(move[24])
                print(move[26])
                arr.append(move)

                #new_state = state.copy()
                #new_state.change_type(x,y,type,True)
                #new_state_cost = new_state.get_board_cost()
                #arr.append((new_state, new_state_cost - state_cost))
    for y in range(state.ySize):
        for x in range(state.xSize):
            if(not state.hasTurn[state.board[0,y,x]]):
                continue
            for i in range(-(state.board[1,y,x] - 1), (state.get_max_turn() - state.board[1,y,x])):
                if i != 0:
                    
                    move = f"new_state.change_time({x},{y},{i})"
                    print(move[26:27])
                    arr.append(move)

                    #new_state = state.copy()
                    #new_state.change_time(x,y,i)
                    #new_state_cost = new_state.get_board_cost()
                    #arr.append((new_state, new_state_cost - state_cost))
    return arr



def state_stats(state):
    new_state = state.copy()
    value = board_value(new_state)
    result = new_state.forge_item()
    print(f"Value: {value} \nResult:\n{result}")

if __name__ == "__main__":
    # Artificial Constraints
    state = 9*np.ones((6,7), dtype=int)
    state[5,6] = 0
    state[5,5] = 0
    state[4,6] = 0
    state[4,5] = 0
    turns = np.zeros((6,7),dtype=int)
    
    print(list_moves(Ib(40, 2, 2)))