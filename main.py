from InfusionBoardUtils import InfusionBoard
import tkinter as tk
from tkinter import ttk
import numpy as np

class StardustInfusionReplicator:
    '''
    Class that defines the GUI for our replication of the Stardust Infusion minigame.
    '''
    
    def __init__(self, root):
        '''Setup GUI Main Window, initialize several variables.'''

        self.root = root
        self.root.title("Stardust Infusion Entry START")
        self.root.state('zoomed')
        self.root.wm_attributes("-topmost", 1)

        # Schedule a function to disable topmost priority.
        self.root.after(50, self.disable_topmost)

        # Start Page Structure
        self.notebook = ttk.Notebook(root)
        self.notebook.pack()

        self.start_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.start_frame, text="Stardust Infusion Entry Start")

        start_button = tk.Button(self.start_frame, text="START", command=self.entry_frame)
        start_button.pack(pady=20)
        
        self.dropdown_options = {
            "Gas":{"filename":"./gui/gas.png", "number":0, "lock_times":True},
            "Plasma":{"filename":"./gui/plasma.png", "number":1, "lock_times":True},
            "Black Hole":{"filename":"./gui/black_hole.png", "number":2, "lock_times":False},
            "Nova":{"filename":"./gui/nova.png", "number":3, "lock_times":False},
            "Supernova":{"filename":"./gui/supernova.png", "number":4, "lock_times":False},
            "Quasar":{"filename":"./gui/quasar.png", "number":5, "lock_times":False},
            "Pulsar":{"filename":"./gui/pulsar.png", "number":6, "lock_times":False},
            "Nebula":{"filename":"./gui/nebula.png", "number":7, "lock_times":False},
            "Star":{"filename":"./gui/star.png", "number":8, "lock_times":False},
            "Planet":{"filename":"./gui/planet.png", "number":9, "lock_times":True}
        }

        print(list(self.dropdown_options.keys()))

        # Dummy initial vars...
        self.root.mainloop()

    def disable_topmost(self):
        '''Disables topmost window priority.'''
        self.root.wm_attributes("-topmost", False)

    def entry_frame(self):
        '''The frame where we enter the initial state of the board.'''

        # Initialize Entry Frame
        self.entries_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entries_frame, text="Stardust Infusion Entry")

        self.all_dropdowns = []
        self.all_entries = []

        for row in range(6):
            for col in range(7):

                # Combobox
                dropdown = ttk.Combobox(self.entries_frame, values=list(self.dropdown_options.keys()), width=10)
                dropdown.grid(row=row, column=col*2, padx=5,pady=5,sticky="w")
                dropdown.current(0)

                # Entry Field
                # Default to 0.
                text = tk.StringVar()
                text.set("0")

                entry = tk.Entry(self.entries_frame, width=5, textvariable=text)
                entry.grid(row=row, column=col*2+1, padx=5, pady=5, sticky="e")

                self.all_dropdowns.append(dropdown)
                self.all_entries.append(entry)

        print(self.all_dropdowns)
        print(self.all_entries)

        button = tk.Button(self.entries_frame, width = 20, text="Process Input", command=self.process_inputs)
        button.grid(row=8, column=15, padx=0, pady=20)
        self.notebook.select(self.entries_frame)

    def process_inputs(self):

        # Gather all the inputs for the dropdowns
        state_string = "".join([str(self.dropdown_options[combobox.get()]["number"]) for combobox in self.all_dropdowns])
        turn_string = "".join([entry.get() for entry in self.all_entries])

        print(state_string)
        print(turn_string)
        state_arr = np.array(list(state_string),dtype=int).reshape((6,7))
        turn_arr = np.array(list(turn_string),dtype=int).reshape((6,7))

        board = InfusionBoard(0,0,0,True, state_arr, turn_arr)

        print(board)
        print("\n\n\n\n\n\n\n\n\n")
        print(board.forge_item())











def input_matrix():
    """Takes matrix input from the command line."""

    rows = int(input("Enter the number of rows (yDim): "))
    #cols = int(input("Enter the number of columns (xDim): "))

    matrix = []
    for i in range(rows):
        row = input(f"Enter the elements of row {i+1} (space-separated): ").split()
        row = [int(x) for x in row]
        matrix.append(row)

    return np.array(matrix)

def main():
    
    state = np.array([[0, 0, 0, 4, 0, 0, 0],
                      [0, 0, 0, 9, 0, 0, 0],
                      [0, 0, 0, 5, 8, 0, 9],
                      [0, 0, 0, 9, 0, 2, 0],
                      [0, 0, 0, 0, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]])
    
    turns = np.array([[0, 0, 0, 4, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 2, 3, 0, 0],
                      [0, 0, 0, 0, 0, 5, 0],
                      [0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]])


    b = InfusionBoard(0, 0, 0, True, state, turns)
    b.change_type(5, 3, 0)
    # This is tyler and magi's job
    #
    #
    #

    score_final=b.forge_item()
    print(score_final)

    app = tk.Tk()
    entry_app = StardustInfusionReplicator(app)
    app.mainloop()



if __name__ == "__main__":
    main()