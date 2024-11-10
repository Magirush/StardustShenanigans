from InfusionBoard import InfusionBoard
import BoardHeuristics
def main():
    board = InfusionBoard(40,2,2)
    BoardHeuristics.node_stats(board)
    
    board1, cost = BoardHeuristics.a_star_search(board)
    # print("the best board found")
    # print(board1)
    # print(cost)
    # print("\n")
    # print(board1.forge_item())
    # boards = BoardHeuristics.get_moves(board)
    # for i in boards:
    #     print(i)
    #     print(BoardHeuristics.board_value(i))
    # print(len(boards))
    # print(BoardHeuristics.board_value(board))

    BoardHeuristics.node_stats(board1)
    

if __name__ == "__main__":
    main()