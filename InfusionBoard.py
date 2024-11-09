import numpy as np
import random

class InfusionBoard:
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

    '''
    Class to represent the board and its state during the infusion minigame.
    '''
    def __init__(self, state: np.ndarray, turns: np.ndarray) -> np.ndarray:
        self.board = np.stack((state, turns))
    
    def __repr__(self):
        print(self.board)
    
    def __str__(self):
        return str(self.board)
    
    def change_time(self, idx_y:int, idx_x:int, change:int):
        '''Changes time on a tile and updates accordingly.'''
        assert change in [-1, 1]
        assert idx_x in range(7)
        assert idx_y in range(6)

        if self.board[1,idx_y, idx_x] == 0:
            '''Checks if the turn order is 0, if so, then nothing happens; for Gas, Plasma, or Planets, time cannot be adjusted.'''
            self.board = self.board
        else:
            # Get current order
            time_current = self.board[1, idx_y, idx_x]

            # Time we want to adjust to.
            time_new = time_current + change
            if time_new == 0:
                # This is the first element timewise and it cannot be changed; 
                # This case can only happen if we take the "first" object timewise and try to advance its time.
                self.board = self.board
            else:
                # Do a swap operation
                idx_y_swap, idx_x_swap = np.where(np.isin(self.board[1], time_current))
                self.board[1,idx_y_swap, idx_x_swap] = time_current
                self.board[1, idx_y, idx_x] = time_new

    def change_type(self, idx_x:int, idx_y:int, type:int):
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
        assert idx_x in range(7)
        assert idx_y in range(6)
        assert type in range(9)

        # Adjust type
        self.board[0, idx_y, idx_x] = type

        # Parsing needed time adjustments associated with conversion, if any.
        current_time = self.board[1, idx_y, idx_x]

        if current_time != 0:
            pass
        else:
            next_time = max(self.board[1]) + 1
            self.board[1, idx_y, idx_x] = next_time
    
        
    '''                
    def create_turn_ledger(self):
        #creates an empty list for a ledger that will dictate turn order
        current_ledger = []
        for idx_y in range(6):
            for idx_x in range(7):
                if self.board[1,idx_y,idx_x] != 0:
                    current_ledger.append()

        (timedomain, idx_y, idx_x) = np.where(self.board[1,idx_y,idx_x] != 0)

    
    def forge_item(self):
        
        i =  1
        
        while i in self.board[1]:
            # while current turn i exists in board
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
        #calls the check_results() function to calculate infusion result
        self.check_results()
        

                        
    def resolve_tile(self,currentType: int,currentX:int ,currentY:int):
        if currentType = 2:
            blackHoleFunct(currentX, currentY)
        elif currentType = 3:
            novaFunct(currentX, currentY)
        elif currentType = 4; 
            sNovaFunct(currentX, currentY)
        elif currentType = 5:
            quasarFunct(currentX, currentY)
        elif currentType = 6:
            pulsarFunct(currentX, currentY)
        elif currentType = 7:
            nebFunct(currentX, currentY)
        elif currentType = 8;
            starFunct(currentX, currentY)
    
    def blackHoleFunct(self,x: int, y: int):
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x , new_y = x + dx, y+dy
            if not(in_bounds(new_x,new_y):
                pass
            if self.board[0,new_y,new_x] == 6 or self.board[0,new_y,new_x] == 8:
                self.change_type(x,y,5)
                break
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if not(in_bounds(new_x,new_y):
                pass
            self.change_type(x,y,1)
            
    def novaFunct(self, x: int, y: int):
        count = 0
        for dx,dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if not(in_bounds(new_x,new_y):
                pass
            if self.board[0,y+dy,x+dx] == 1:
                count += 1
        if count >= 3:
            self.change_type(x,y,8)
        
    def sNovaFunct(self, x: int, y: int):
        for dx,dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if self.board[0,y+dy,x+dx] == 1:
                count += 1
        if count >= 3:
            self.change_type(x,y,8)        
            
    def check_results(self)
        score = 0
        for k in range(6):
            for j in range(7):
                if self.board[0, k, j] == 6 or self.board[0, k, j] == 8:
                    score += 1
        return score
                    
        
            

    
    '''
    

    def randomPlacementItem(self, costLimit: int):
            eligible = [i for i, value in enumerate(self.startingValues) if value < costLimit]
            return -1 if not eligible else random.choice(eligible)
                        
    def createNewBoard(self, startingValue: int, planetCount: int, starCount: int):
        eligible = []

        ySize, xSize = self.board[0].shape
        print(ySize)
        print(xSize)

        for x in range(xSize):
            for y in range(ySize):
                self.board[0, y, x] = 0
                self.board[1, y, x] = 0
                eligible.append((x,y))
        
        for i in range(planetCount):
            if len(eligible) == 0:
                x, y = eligible[random.randrange(len(eligible))]
                self.board[0, y, x] = 9
                eligible.remove((x,y))

        for i in range(starCount):
            if len(eligible) == 0:
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
        y, x = np.where(np.isin(state_TEST, [0,1,9], invert=True))
        coords = zip(x,y)
        for coord in coords:
            eligible.append(coord)

        print(eligible)
        
        itemTurn = 1
        while len(eligible) > 0:
            x, y = eligible[random.randrange(len(eligible))]
            self.board[1, y, x] = itemTurn
            itemTurn += 1
            eligible.remove((x,y))

    
def in_bounds(x:int,y:int):
    #checks if the x and y values are in bounds of the board and reuturns true if it is in bounds and false if not
    if x>=0 and x<6 and y>= 0 and y<7:
        return True
    else:
        return False



            

    

state_TEST = np.random.randint(0,9,(6,7))
print(state_TEST)
# Generic time assigner
turns_TEST = np.zeros((6,7))
time = 1

# Unpack to coordinates i,j values where state is NOT (by invert=True) 0, 1, 9; not GAS, PLASMA, or PLANET.
i, j = np.where(np.isin(state_TEST, [0,1,9], invert=True))
for idx_y, idx_x in zip(i, j): # To navigate as coordinates (y, x), use zip.
        turns_TEST[idx_y, idx_x] = time
        time+=1
        
print(turns_TEST)

testboard = InfusionBoard(state_TEST, turns_TEST)
testboard.createNewBoard(40,2,2) # 40 starting value, 2 planets, 2 stars
print(testboard)

