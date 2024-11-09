import numpy as np
import random

class InfusionBoard:
    '''
    Class to represent the board and its state during the infusion minigame.
    '''

    # Constants for board size
    xSize = 7
    ySize = 6
    Domains = 2

    # Constants for board cost
    forgeCost = 10
    turnCost = 1

    # Constants for stardust costs
    placementValues = [
        0, # Gas
        7, # Plasma
        5, # Black Hole
        5, # Nova
        24, # Supernova
        18, # Quasar
        64, # Pulsar
        3, # Nebula
        64, # Star
        1, # Planet
    ]

    # Probability-of-placement constants
    startingValues = [
        10000, # Gas
        1, # Plasma
        7, # Black Hole
        5, # Nova
        18, # Supernova
        12, # Quasar
        10000, # Pulsar
        3, # Nebula
        10000, # Star
        10000, # Planet
    ]

    # Truth list for whether or not a tile-type should be ticked.
    hasTurn = [
        False, # Gas
        False, # Plasma
        True, # Black Hole
        True, # Nova
        True, # Supernova
        True, # Quasar
        True, # Pulsar
        True, # Nebula
        True, # Star
        False, # Planet
    ] 
    


    # Representation functions
    def __repr__(self):
        print(self.board)
    
    def __str__(self):
        return str(self.board)
    
    def copy(self):
        copy_board = InfusionBoard(0,0,0)
        np.copyto(copy_board.board, self.board)
        np.copyto(copy_board.boardinitial, self.boardinitial)
        self.turnChangeLedger = self.turnChangeLedger
        self.tileChangeLedger = self.tileChangeLedger
        return copy_board

    # Utility for board-creator 
    def randomPlacementItem(self, costLimit: int):
            eligible = [i for i, value in enumerate(self.startingValues) if value < costLimit]
            return -1 if not eligible else random.choice(eligible)
 
    # Board creator function (random, in-game style)
    def __init__(self, startingValue: int, planetCount: int, starCount: int):
        eligible = []

        self.board = np.zeros((self.Domains, self.ySize, self.xSize),dtype=int)

        # Initialise empty ledgers for turn & tile change
        self.turnChangeLedger = []
        self.tileChangeLedger = []

        # Initialise counters
        self.activated_nova_nebulas = 0
        self.nova_no_star_change = 0
        self.nebula_no_nova_created = 0
        self.new_plasma = 0
        self.nova_destroyed_by_blackhole = 0

        for x in range(self.xSize):
            for y in range(self.ySize):
                eligible.append((x,y))
        
        for i in range(planetCount):
            if len(eligible) != 0:
                x, y = eligible[random.randrange(len(eligible))]
                self.board[0, y, x] = 9
                eligible.remove((x,y))

        for i in range(starCount):
            if len(eligible) != 0:
                x, y = eligible[random.randrange(len(eligible))]
                self.board[0, y, x] = 8 if random.random() < 0.66 else 6
                eligible.remove((x,y))
        
        placeItem = self.randomPlacementItem(startingValue)
        while(placeItem != -1 and len(eligible) > 0):
            x, y = eligible[random.randrange(len(eligible))]
            self.board[0, y, x] = placeItem
            eligible.remove((x,y))
            startingValue -= self.placementValues[placeItem]
            placeItem = self.randomPlacementItem(startingValue)
        
        eligible.clear()
        y, x = np.where(np.isin(self.board[0], [0,1,9], invert=True))
        coords = zip(x,y)
        for coord in coords:
            eligible.append(coord)
        
        itemTurn = 1
        while len(eligible) > 0:
            x, y = eligible[random.randrange(len(eligible))]
            self.board[1, y, x] = itemTurn
            itemTurn += 1
            eligible.remove((x,y))
        
        self.boardinitial=np.copy(self.board)

    def alternate_constructor(self, state: np.ndarray, turns: np.ndarray):
        if type(state) == None or type(turns) == None:
            self.board=self.__init__(0,0,0)
        else:
            self.board = np.stack((state, turns))
            self.boardinitial = np.copy(self.board)
    
    # Utils
    def in_bounds(self, x:int,y:int) -> bool:
        # Checks if the x and y values are in-bounds of the board 
        # Reuturns true if in bounds and false otherwise
        if 0<=x<self.xSize and 0<=y<self.ySize:
            return True
        else:
            return False
    
    
    def change_time(self, idx_x:int, idx_y:int, change:int):
        '''Changes time on a tile and updates all other tiles which would be affected accordingly.'''
        assert idx_x in range(self.xSize), f"X coord is negative, or larger than {self.xSize - 1}."
        assert idx_y in range(self.ySize), f"Y coord is negative, or larger than {self.ySize - 1}."

        # Pre-checks for whether or not a change can be made.
        if self.board[1,idx_y, idx_x] == 0:
            # Checks if the turn order is 0
            # If so, then nothing happens; for Gas, Plasma, or Planets, time cannot be adjusted.
            self.board = self.board
            change = 0
        elif (self.board[1, idx_y, idx_x] == np.max(self.board[1]) and change>=0) or (self.board[1, idx_y, idx_x] == 1 and change < 0):
            # Checks if this is the maximum/minimum turn order.
            # If so, then nothing happens; the last time cannot be delayed infinitely, nor can the first time be advanced further.
            self.board = self.board
            change = 0
        else:
            # Get current time for this tile.
            time_current = self.board[1, idx_y, idx_x]
            print(f"Current time on {(idx_x, idx_y)} is {time_current}.")

            # Time we want to adjust to.
            time_new = time_current + change
            print(f"We'd like to adjust this to {time_new}.")

            # Handling cases where time may be adjusted to go beyond max, or under one-- these cannot be allowed.
            if time_new < 1:
                time_new = 1
            elif time_new > np.max(self.board[1]):
                time_new = np.max(self.board[1])

            # Redefine change in case the real change was adjusted by the above correction. 
            # We need change for Stardust Cost eval.
            change = time_new - time_current
             
            # Do a swap operation of the times; adjust others accordingly.

            # Find a set of affected coords.
            print((np.arange(time_current+1, time_new+1)) if change>=0 else -1*np.arange(-time_current, -time_new))
            mutable_y, mutable_x = np.where(np.isin(self.board[1], (np.arange(time_current+1, time_new+1) if change>=0 else -1*np.arange(-time_current+1, -time_new+1))))
            
            # Adjust the coords we pass over by +/- 1 based on change.
            mutable_coords = zip(mutable_x, mutable_y)
            for coord in mutable_coords:
                print(f"Adjusting coord {coord}. It currently has time {self.board[1, coord[1], coord[0]]}.")
                if change >=0: self.board[1,coord[1], coord[0]] -= 1 
                else: self.board[1, coord[1], coord[0]] += 1
            
            # A simple equality operation handles the step at time_new.
            self.board[1, idx_y, idx_x] += change
        
            self.add_turn_ledger_entry(idx_x, idx_y, change)
    

    def change_time_manual(self, idx_x:int, idx_y:int, time:int): 
        '''Used for manual time adjustments, such as when a tile transforms into another tile.'''
        assert idx_x in range(self.xSize), f"X coord is negative, or larger than {self.xSize - 1}."
        assert idx_y in range(self.ySize), f"Y coord is negative, or larger than {self.ySize - 1}."

        # Perform a manual time adjust on a tile.
        self.board[1, idx_y, idx_x] = time

    def get_max_turn(self):
        return np.max(self.board[1])

    def change_type(self, idx_x:int, idx_y:int, type:int, userplaced:bool = False):
        '''
        Converts tile at (idx_x, idx_y) to a given type.
        0 - GAS
        1 - PLASMA
        2 - BLACK HOLE
        3 - NOVA
        4 - SUPERNOVA
        5 - QUASAR
        6 - PULSAR
        7 - NEBULA
        8 - STAR
        9 - PLANET <-- WARNING! NOT ACCESSIBLE.
        array uses (z, y, x), z = 0  for tile types, z = 1 for tile turn order
        '''
        # Assertions
        assert idx_x in range(self.xSize), f"X coord is negative, or larger than {self.xSize - 1}."
        assert idx_y in range(self.ySize), f"Y coord is negative, or larger than {self.ySize - 1}."
        assert type in range(9), "Type not defined, or inaccessible!"

        # Adjust type
        self.board[0, idx_y, idx_x] = type

        #User placement flag
        if userplaced:
            self.add_tile_ledger_entry(idx_x, idx_y, type)

        # Parsing needed time adjustments associated with conversion, if any.
        current_time = self.board[1, idx_y, idx_x]
        current_type = self.board[0, idx_y, idx_x]

        if current_time != 0:
            pass
        elif current_time == 0 and current_type in [0, 1]:
            # From State to State. Not an Arcana Achievement, but it should be!
            pass
        else:
            next_time = np.max(self.board[1]) + 1
            self.board[1, idx_y, idx_x] = next_time
    
    # State evaluator function.
    def forge_item(self):
        '''
        Function that runs a given board-state to completion, and returns the number of stars/pulsars on the board (i.e. the infusion rank).
        '''
        i =  1

        # Reset counters to 0
        self.activated_nova_nebulas = 0
        self.nova_no_star_change = 0
        self.nebula_no_nova_created = 0
        self.new_plasma = 0
        self.nova_destroyed_by_blackhole = 0

        while i in self.board[1]:
            # while current turn i exists in board
            found = False
            for k in range(6):
                for j in range(7):
                    # traverses to where i exists, scanning left to right, then top to bottom
                    # if encounters i, resolves that tile, then breaks to while loop
                    if self.board[1, k, j] == i:
                        currentX, currentY = j, k
                        currentType = self.board[0, k, j]
                        self.resolve_tile(currentType,currentX,currentY)
                        found = True
                        i += 1
                    if found:
                        break
                if found:
                    break
        # Calls check_results() to calculate infusion result
        score = self.check_results()
        # Calls stardust_cost() to calculate stardust cost
        cost = self.get_board_cost()

        # Assemble metrics for this board
        metrics = {"activated_nova_nebulas":self.activated_nova_nebulas, "nova_no_star_change":self.nova_no_star_change, 
                    "nebula_no_nova_created":self.nebula_no_nova_created, "new_plasma":self.new_plasma, 
                    "nova_destroyed_by_blackhole":self.nova_destroyed_by_blackhole, "num_stars":score, "stardust_spent":cost}
        return self.board, metrics

    # Logic handling for black hole tiles
    def black_hole_funct(self,x: int, y: int):
        flag = False
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] in [2,5,6,8]:
                # Flag that the Black Hole needs to turn into a quasar.
                flag = True
                break
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            # Nebulae are immune to black holes.
            elif self.board[0,new_y,new_x] != 7:
                # If activation of black hole destroys a Nova (3), nova_destroyed_by_blackhole counter is increased by 1
                if self.board[0,new_y,new_x] == 3:
                    self.nova_destroyed_by_blackhole += 1
                # Create new plasma and increase counter
                self.change_type(new_x,new_y,1)
                self.new_plasma += 1
            # Plasma time consistency.
            elif self.board[0, new_y, new_x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder for this plasma
                pass
        
        if flag:
            # Change own tile type, kick time to end, based on flag.
            # Change the black hole into a quasar
            self.change_type(x,y,5)
            next_time = np.max(self.board[1]) + 1
            print(next_time)
            self.change_time_manual(x, y, next_time)
    
    # Logic handling for nova tiles
    def nova_funct(self, x: int, y: int):
        count = 0
        flag = False
        # Searches for 3 plasma in the 4 adjacent tiles
        for dx,dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 1:
                count += 1
        if count >= 3:
            flag = True
        else:
            pass
        if flag:
            # Change own type, kick time to end, based on flag
            # Change the nova to a star
            self.change_type(x,y,8)
            next_time = np.max(self.board[1]) + 1
            self.change_time_manual(x, y, next_time)
            # Increases activated_nova_nebulas count by 1 due to full activation
            self.activated_nova_nebulas += 1
        else:
            # Change own type, kick time to end, based on flag
            # Change the nova into plasma
            self.change_type(x,y,1)
            next_time = np.max(self.board[1]) + 1
            self.change_time_manual(x, y, next_time)
            # Increases nova_no_star_change count by 1 and new_plasma count by 1 due to failed activation
            self.nova_no_star_change += 1
            self.new_plasma += 1

    # Logic handling for supernova tiles
    def supernova_funct(self, x: int, y: int):
        for dx,dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (-2,0), (2,0), (0,2), (0,-2)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 0:
                self.change_type(new_x,new_y,1)
                self.new_plasma += 1
            elif self.board[0, new_y, new_x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder.
                pass
        # Change own type, kick time to end.
        self.change_type(x,y,5)
        next_time = np.max(self.board[1]) + 1
        self.change_time_manual(x, y, next_time)    
    
    # Logic handling for quasar tiles
    def quasar_funct(self, x: int, y: int):   
        for dx,dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 0:
                # Create new plasma and increase counter
                self.change_type(new_x,new_y,1)
                self.new_plasma += 1
            elif self.board[0, new_y, new_x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder.
                pass
        # Create new plasma in the column in spaces with gas
        for y in range(self.ySize):
            if self.board[0,y,x] == 0:
                # Create new plasma and increase counter
                self.change_type(x,y,1)
                self.new_plasma += 1
            elif self.board[0,y,x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder.
                pass

    # Logic handling for pulsar tiles
    def pulsar_funct(self, x: int, y: int):
        for dx,dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 0:
                # Create new plasma and increase counter
                self.change_type(new_x,new_y,1)
                self.new_plasma += 1
            elif self.board[0, new_y, new_x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder.
                pass

    # Logic handling for nebula tiles
    def neb_funct(self, x: int, y: int): 
        count = 0
        flag = False
        for dx,dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 1:
                count += 1
        if count >= 4:
            # Did nebula activate successfully?
            flag = True
        else:
            pass

        if flag:    
            # Change own type, kick time to end, based on flag
            # Sets type to star
            self.change_type(x,y,3)
            next_time = np.max(self.board[1]) + 1
            self.change_time_manual(x, y, next_time)
            # Increases activated_nova_nebulas count by 1 as nebula transforms successfully
            self.activated_nova_nebulas += 1
        else:
            # In the case that the nebula does nothing, increase counter for no nova creation
            self.nebula_no_nova_created += 1

    # Logic handling for star tiles
    def star_funct(self, x: int, y: int):   
        for dx,dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_x , new_y = x + dx, y+dy
            if not(self.in_bounds(new_x,new_y)):
                pass
            elif self.board[0,new_y,new_x] == 0:
                # Create new plasma and increase counter
                self.change_type(new_x,new_y,1)
                self.new_plasma += 1
            elif self.board[0, new_y, new_x] == 1:
                # If this is already plasma, do nothing, do NOT add a new turnorder.
                pass

    # Checking results by counting the amount of pulsars and stars
    def check_results(self):
        #print(self.board)

        # Finding stars, pulsars
        i, j = np.where(np.isin(self.board[0], [6,8]))
        coords = zip(i,j)
        coordlist = [coord for coord in coords]

        # How many are there?
        score = len(coordlist)
        return score

    # Logic handler for tiles
    def resolve_tile(self,currentType: int,currentX:int ,currentY:int):
        # Redirects the function to the correct tile type to be processed
        if currentType == 2:
            self.black_hole_funct(currentX, currentY)
        elif currentType == 3:
            self.nova_funct(currentX, currentY)
        elif currentType == 4: 
            self.supernova_funct(currentX, currentY)
        elif currentType == 5:
            self.quasar_funct(currentX, currentY)
        elif currentType == 6:
            self.pulsar_funct(currentX, currentY)
        elif currentType == 7:
            self.neb_funct(currentX, currentY)
        elif currentType == 8:
            self.star_funct(currentX, currentY)

    # Add a tile change to the ledger
    def add_tile_ledger_entry(self, x: int, y: int, type: int):
        self.tileChangeLedger = [entry for entry in self.tileChangeLedger if not (entry[0] == x and entry[1] == y)]

        if self.boardinitial[0, y, x] != type:
            self.tileChangeLedger.append((x,y,type))
    
    # Add a turn change to the ledger
    def add_turn_ledger_entry(self, x: int, y: int, change: int):
        if change == 0:
            return
        remaining = np.abs(change)

        for i, entry in enumerate(self.turnChangeLedger):
            if entry[0] == x and entry[1] == y and np.sign(change) != np.sign(entry[2]):
                del self.turnChangeLedger[i]
                remaining -= 1
                if remaining == 0:
                    break
        
        if remaining > 0:
            for i in range(remaining):
                self.turnChangeLedger.append((x,y,np.sign(change)))

    # Get cost of changing turn order
    def get_tile_cost(self):
        return len(self.turnChangeLedger) * self.turnCost

    # Get cost of changing tile type
    def get_turn_cost(self):
        cost = 0
        for entry in self.tileChangeLedger:
            cost += self.placementValues[entry[2]]
        return cost
    
    # Get cost of layout
    def get_board_cost(self):
        return self.forgeCost + self.get_tile_cost() + self.get_turn_cost()


def main():
    '''A test case of this function running off a null board.'''
    testboard = InfusionBoard(0,0,0)
    testboard.change_type(0,0,2, True) # Create Black Hole
    testboard.change_type(2,4,0, True) # Turn (2,4) to gas
    testboard.change_type(4,4,5, True) # Create Quasar
    testboard.change_type(5,5,5, True) # Create Yet Another Quasar
    testboard.change_type(0,3,3, True) # Create Nova
    print(testboard)
    print('TWO TIME ADJUSTMENTS LATER...')
    testboard.change_time(0,0,2) # Try to delay the Black Hole two turns
    print(testboard)
    print("ANOTHER TIME ADJUSTMENT AFTER THAT...")
    testboard.change_time(0,3,-1) # Try to advance a Nova one turn
    print(testboard)
    print(testboard.forge_item())

if __name__ == "__main__":
    main()