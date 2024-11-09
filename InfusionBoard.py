import numpy as np

class InfusionBoard:
    '''
    Class to represent the board and its state during the infusion minigame.
    '''
    def __init__(self, state: np.ndarray, turns: np.ndarray) -> np.ndarray:
        self.board = np.stack((state, turns))
    
    def __repr__(self):
        print(self.board)
    
    def __str__(self):
        return str(self.board)

    def change_to_gas(self, idx_x:int, idx_y:int):
        'Converts tile at (idx_x, idx_y)  to GAS (0)'
        self.board[0, idx_x, idx_y] = 0

state_PLASMA = np.ones((6,7))
turns_NULL = np.zeros((6,7))

testboard = InfusionBoard(state_PLASMA, turns_NULL)

print(testboard)
testboard.change_to_gas(0,0)
print(testboard)
