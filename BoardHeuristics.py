from InfusionBoard import InfusionBoard as Ib
import heapq
import time


def a_star_search(start_node):
    # Priority queue with (combined_score, node)
    open_set = []
    init_node = start_node.copy()
    heapq.heappush(open_set, (0 - board_value(start_node), start_node))

    time_cutoff = 60
    start_time = time.time()

    total_neighbors = 0
    total_nodes_visited = 0

    # Track the best path to each node and cost to reach it
    came_from = {}
    path_costs = {start_node: 0}
    best_node = start_node
    best_combined_score = 0 - board_value(start_node)

    while open_set:
        current_score, current = heapq.heappop(open_set)

        # If this is the best score we've seen, update the best node
        if current_score < best_combined_score:
            best_node = current
            best_combined_score = current_score
            print(f"New Best Found: {current_score}")


        moves = get_moves(current)
        total_nodes_visited += 1
        current_neighbors = len(moves)
        total_neighbors += current_neighbors

        if total_nodes_visited % 1000 == 0:
            print(f"Explored {total_nodes_visited} nodes")

        # Explore neighbors
        for neighbor, cost in moves:
            tentative_g_score = path_costs[current] + cost
            combined_score = tentative_g_score - board_value(neighbor)

            # Add neighbor to open_set if this path is better
            if neighbor not in path_costs or tentative_g_score < path_costs[neighbor]:
                came_from[neighbor] = current
                path_costs[neighbor] = tentative_g_score
                heapq.heappush(open_set, (combined_score, neighbor))
        
        if time.time() - start_time > time_cutoff:
            break

    # Reconstruct the path by backtracking from the best node to the start node
    path = []
    current = best_node
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start_node)  # add the start node at the end
    path.reverse()  # reverse to get path from start to best node

    if total_nodes_visited > 1:
        branching_factor = total_neighbors / total_nodes_visited
    else:
        branching_factor = 0

    print(f"Counter: {total_nodes_visited} Branching Factor: {branching_factor} Start Node:\n\n")
    node_stats(init_node)

    print(f"Path:")
    for i, node in enumerate(path):
        print(f"Node: {i}")
        node_stats(node)


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
    if node_cost > 96:
        return arr
    for y in range(node.ySize): #
        for x in range(node.xSize):
            if (
                node.board[0,y,x] == 9 or    # Can't edit a planet
                node.has_tile_change_at(x,y) # Don't change a tile that is already edited
            ):
                continue

            for type in [0,1,2,3,4,5,7]: # Cannot place star, pulsar, or planet
                if(
                    node.board[0,y,x] == type or  # Don't change a tile to itself
                    (type == 0 and node.board[0,y,x] != 2) or  # Only use gas on black holes
                    (type == 7 and ((x,y) == (0,0) or          # Don't put nebulas on the edge
                                    (x,y) == (0,node.ySize-1) or 
                                    (x,y) == (node.xSize-1,0) or 
                                    (x,y) == (node.xSize-1,node.ySize-1)))
                ):
                    continue
                new_node = node.copy()
                new_node.change_type(x,y,type,True)
                new_node_cost = new_node.get_board_cost()
                arr.append((new_node, new_node_cost - node_cost))
    for y in range(node.ySize):
        for x in range(node.xSize):
            if(not node.hasTurn[node.board[0,y,x]] or node.has_turn_change_at(x,y)): # Don't edit a tile with no turn, or change a turn more than once
                continue
            for i in range(-(node.board[1,y,x] - 1), (node.get_max_turn() - node.board[1,y,x])):
                if i != 0:
                    new_node = node.copy()
                    new_node.change_time(x,y,i)
                    new_node_cost = new_node.get_board_cost()
                    arr.append((new_node, new_node_cost - node_cost))
    return arr

def node_stats(node):
    new_node = node.copy()
    value = board_value(new_node)
    result_board, metrics = new_node.forge_item()
    print(f"Board: {node}\n")
    print(f"Value: {value} \nResult Board:\n{result_board}\nMetrics:\n{metrics}")
    print(f"Latest Action: {node.latest_action}")
    print(f"Turn Ledger: {node.turnChangeLedger}")
    print(f"Stardust Cost: Forge-{node.forgeCost} + Tile-{node.get_tile_cost()} + Turn-{node.get_turn_cost()}")