from InfusionBoard import InfusionBoard as Ib
import heapq


def a_star_search(start_node):
    # Priority queue with (combined_score, node)
    open_set = []
    init_node = start_node.copy()
    heapq.heappush(open_set, (0 - board_value(start_node), start_node))

    # Track the best path to each node and cost to reach it
    came_from = {}
    path_costs = {start_node: 0}
    best_node = start_node
    best_combined_score = 0 - board_value(start_node)
    counter = 0

    while open_set:
        current_score, current = heapq.heappop(open_set)

        # If this is the best score we've seen, update the best node
        if current_score < best_combined_score:
            best_node = current
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

    print(f"Start Node:\n{init_node}\nCounter: {counter}")
    return best_node, -best_combined_score


#heuristic values for easy mod
actNovNeb = 5
noStarNova = 0#-3
noNovaNeb = 0#-5
plasma = 1
deleteNova = 0#-5
# Example functions for testing:
def board_value(node):
    board,metrics = node.copy().forge_item()
    starAddCount = 400 if metrics["num_stars"] == 10 else metrics["num_stars"] * 20
    starAddCount = -10000 if metrics['num_stars'] > 10 else starAddCount
    return (starAddCount + metrics["activated_nova_nebulas"] * actNovNeb + metrics["nova_no_star_change"] * noStarNova + metrics["nebula_no_nova_created"] * noNovaNeb + metrics["new_plasma"] * plasma + metrics["nova_destroyed_by_blackhole"] *deleteNova) #/ metrics["stardust_spent"]

def get_moves(node):
    arr = []
    node_cost = node.get_board_cost()
    if node_cost > 256:
        return arr
    for y in range(node.ySize): #
        for x in range(node.xSize):
            for type in [0,1,2,3,4,5,7]: #
                if(node.board[0,y,x] == 9 or node.board[0,y,x] == type or (type == 0 and node.board[0,y,x] != 2) or (type == 7 and ((x,y) == (0,0) or (x,y) == (0,node.ySize-1) or (x,y) == (node.xSize-1,0) or (x,y) == (node.xSize-1,node.ySize-1)))): #nebula and nova cannot be beneficial in corner
                    continue
                new_node = node.copy()
                new_node.change_type(x,y,type,True)
                new_node_cost = new_node.get_board_cost()
                arr.append((new_node, new_node_cost - node_cost))
    for y in range(node.ySize):
        for x in range(node.xSize):
            if(not node.hasTurn[node.board[0,y,x]]):
                continue
            for i in range(-(node.board[1,y,x] - 1), (node.get_max_turn() - node.board[1,y,x])):
                if i != 0:
                    new_node = node.copy()
                    new_node.change_time(x,y,i)
                    new_node_cost = new_node.get_board_cost()
                    arr.append((new_node, new_node_cost - node_cost))
    # Define your own logic here to get the next nodes from the current node
    return arr

def node_stats(node):
    value = board_value(node)
    result = node.forge_item()
    print(f"Value: {value} \nResult:\n{result}")