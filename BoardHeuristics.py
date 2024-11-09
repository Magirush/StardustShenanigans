from InfusionBoard import InfusionBoard as Ib
import heapq

def a_star_search(start_node):
    # Priority queue (max-heap) to store nodes as (priority, node) pairs
    open_set = [(-board_value(start_node), start_node)]  # Using negative because heapq is min-heap
    heapq.heapify(open_set)
    
    # Dictionary to keep track of the best value found for each node
    best_values = {start_node: board_value(start_node)}
    
    # Initialize best node with the start node
    best_node = start_node
    
    while open_set:
        # Get the node with the highest priority (i.e., highest board value)
        _, current = heapq.heappop(open_set)
        
        # Update the best node if the current node has a higher board value
        current_value = board_value(current)
        if current_value > board_value(best_node):
            best_node = current

        # Explore neighbors
        for neighbor in get_moves(current):
            neighbor_value = board_value(neighbor)
            
            # If this path leads to a higher value, update and add to open_set
            if neighbor not in best_values or neighbor_value > best_values[neighbor]:
                best_values[neighbor] = neighbor_value
                heapq.heappush(open_set, (-neighbor_value, neighbor))
    
    return best_node, board_value(best_node)  # Return the best node found and its value
#heuristic values for easy mod
actNovNeb = 5
noStarNova = -3
noNovaNeb = -5
plasma = 1
deleteNova = -5
# Example functions for testing:
def board_value(node):
    board,metrics = node.forge_item()
    
    return metrics["activated_nova_nebulas"] * actNovNeb + metrics["nova_no_star_change"] * noStarNova + metrics["nebula_no_nova_created"] * noNovaNeb + metrics["new_plasma"] * plasma + metrics["nova_destroyed_by_blackhole"] *deleteNova

def get_moves(node):
    arr = []
    if node.get_board_cost() > 75:
        return arr
    for y in range(node.ySize): #
        for x in range(node.xSize):
            for type in [0,1,2,3,4,5,7]: #
                if(node.board[0,y,x] == 9 
                or node.board[0,y,x] == type 
                or (type == 0 and node.board[0,y,x] != 2) 
                or (type == 7 and ((x,y) == (0,0) or (x,y) == (0,node.ySize-1) or (x,y) == (node.xSize-1,0) or (x,y) == (node.xSize-1,node.ySize-1))) #nebula and nova cannot be beneficial in corner
                ):
                    continue
                arr.append(node.copy().change_type(x,y,type,True))
    for y in range(node.ySize):
        for x in range(node.xSize):
            if(not node.hasTurn[node.board[0,y,x]]):
                continue
            for i in range(-(node.board[1,y,x] - 1), (node.get_max_turn() - node.board[1,y,x])):
                if i != 0:
                    arr.append(node.copy().change_time(x,y,i))
    # Define your own logic here to get the next nodes from the current node
    pass