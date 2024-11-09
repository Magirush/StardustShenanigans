import numpy as np
import random
import tensorflow as tf
from tensorflow.keras import layers

# Import Sudoku methods from the previous script
from sudoku_utils import generate_sudoku, print_board, remove_numbers, is_valid

class SudokuEnv:
    """Environment for the Sudoku game."""
    def __init__(self, board):
        self.original_board = board
        self.board = board
        self.done = False
        self.steps = 0

    def reset(self):
        self.board = [row[:] for row in self.original_board]
        self.done = False
        self.steps = 0
        return self.board

    def step(self, action):
        row, col, num = action
        if is_valid(self.board, row, col, num):
            self.board[row][col] = num
            reward = 1  # Reward for a valid move
        else:
            reward = -1  # Penalty for an invalid move
        
        self.steps += 1
        if self.steps >= 81 or all(num != 0 for row in self.board for num in row):
            self.done = True
        
        return self.board, reward, self.done

    def available_actions(self):
        """Get all possible actions (row, col, num) for the current board state."""
        actions = []
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # If the cell is empty
                    for num in range(1, 10):
                        if is_valid(self.board, row, col, num):
                            actions.append((row, col, num))
        return actions

class SudokuAgent:
    """Agent for solving Sudoku using a neural network."""
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Input(shape=(9, 9, 1)),  # Input shape for the board
            layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(9 * 9 * 9, activation='linear')  # Output for all possible actions
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train(self, states, actions, rewards):
        """Train the model on the collected states, actions, and rewards."""
        targets = self.model.predict(states)
        for i in range(len(actions)):
            # Ensure that actions[i] is a tuple (row, col, num)
            action = actions[i]
            row, col, num = action
            # Indexing correctly to assign reward to the target for the action taken
            target_index = row * 9 + col  # Convert (row, col) to a single index in the flat target array
            targets[i][target_index * 9 + (num - 1)] = rewards[i]  # Adjust for zero-indexing
        self.model.fit(states, targets, epochs=1, verbose=0)

def main():
    # Generate a completed Sudoku board
    completed_board = generate_sudoku()
    print("Original Completed Sudoku Board:")
    print_board(completed_board)

    # Remove numbers to create a Sudoku puzzle
    revealed_count = 15
    sudoku_puzzle = remove_numbers(completed_board, revealed_count)
    print("\nSudoku Puzzle:")
    print_board(sudoku_puzzle)

    # Initialize environment and agent
    env = SudokuEnv(sudoku_puzzle)
    agent = SudokuAgent()

    # Training loop (simplified)
    for episode in range(100):  # Number of episodes
        state = env.reset()
        done = False
        while not done:
            actions = env.available_actions()
            if actions:
                action = random.choice(actions)  # Random action for exploration
                next_state, reward, done = env.step(action)
                # Train agent with state, action, and reward
                agent.train(np.array([state]), [action], [reward])
                state = next_state
    agent.model.save_weights("sudoku_agent_weights.h5")

if __name__ == "__main__":
    main()
