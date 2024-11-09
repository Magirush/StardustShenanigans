import random

def print_board(board):
    """Helper function to print the Sudoku board with ASCII boundaries."""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-"*9 + "+" + "-"*10 + "+" + "-"*9)  # Print horizontal boundary for 3x3 sub-grids
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # Print vertical boundary for 3x3 sub-grids
            print(f"{num:2}", end=" ")  # Print the number with padding
        print()  # Newline at the end of each row

def is_valid(board, row, col, num):
    """Check if it's valid to place num in board[row][col]."""
    # Check the row
    if num in board[row]:
        return False
    
    # Check the column
    if num in (board[i][col] for i in range(9)):
        return False
    
    # Check the 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row_start + i][box_col_start + j] == num:
                return False
                
    return True

def solve_sudoku(board):
    """Backtracking function to solve the Sudoku board."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find an empty space
                random_nums = list(range(1, 10))
                random.shuffle(random_nums)  # Shuffle numbers for randomness
                
                for num in random_nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # Place the number
                        if solve_sudoku(board):  # Recur
                            return True
                        board[row][col] = 0  # Reset and backtrack
                return False  # Trigger backtracking
    return True  # Successfully filled the board

def generate_sudoku():
    """Generate a completed Sudoku board."""
    board = [[0] * 9 for _ in range(9)]  # Start with an empty board
    solve_sudoku(board)
    return board

def remove_numbers(board, revealed_count):
    """Remove numbers from the Sudoku board until only revealed_count spaces remain."""
    # Create a copy of the board to avoid modifying the original one
    board_copy = [row[:] for row in board]
    total_cells = 81  # 9x9 Sudoku board has 81 cells

    # List of positions to remove
    positions_to_remove = random.sample(range(total_cells), total_cells - revealed_count)
    
    for pos in positions_to_remove:
        row = pos // 9
        col = pos % 9
        board_copy[row][col] = 0  # Remove the number by setting it to 0

    return board_copy

# Generate and print the Sudoku board
sudoku_board = generate_sudoku()
print_board(sudoku_board)
print("\n\n\n")
print_board(remove_numbers(sudoku_board, 10))
