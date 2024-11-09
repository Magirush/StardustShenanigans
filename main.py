from InfusionBoardUtils import InfusionBoard



def main():
    b = InfusionBoard(0, 0, 0)
    while True:
        # Prints array at start
        print(b[0])
        user_input = input("Enter X, y, type, and turn seperated by comma: \n") # Get user input of tile info
        x, y, tile_type, turn = [int(x.strip()) for x in user_input.split(",")] # Split input into x, y, tile, and turn
        if turn-1 not in b[1]:
            print("Error: Enter tiles in ascending turn order. \n") # User must enter tiles in ascending turn order
            turn = int(input("Enter turn: \n"))
        # assign tile to board and assign them turns
        b.change_type(x, y, tile_type)
        b.change_time_manual(x, y, turn)
        print(b[0]) # prints array after changes
        # If user is done adding starting tiles, break loop 
        stop_loop = input("Are you done adding tiles? (y/n)\n")
        if stop_loop == "y":
            break
    
    # This is tyler and magi's job
    #
    #
    #

    score_final=b.forge_item()
    print(score_final)
    print(b)



if __name__ == "__main__":
    main()