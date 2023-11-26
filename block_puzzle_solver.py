import tkinter as tk
from tkinter import messagebox
from config import blocks, block_colors
import numpy as np
from solve_puzzle import solve_puzzle

def get_block_representation(block, fill='[]', empty='  '):
    """Create a string representation of a block with given fill and empty symbols."""
    return '\n'.join([''.join([fill if cell else empty for cell in row]) for row in block])

def order_blocks(blocks):
    # Sort blocks by size (number of filled cells) and then by number of unique rotations (fewer first)
    sorted_blocks = sorted(blocks.items(), key=lambda x: (-np.sum(x[1]['shape']), 'unique_rotations' in x[1]))
    return [block[0] for block in sorted_blocks]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.total_value = 0
        self.create_widgets()
        self.solution_labels = []  # List to keep track of solution labels

    def create_widgets(self):
        default_puzzle_size = 5

        self.width_label = tk.Label(self, text="Width:")
        self.width_label.grid(row=0, column=0)
        self.width_entry = tk.Entry(self)
        self.width_entry.insert(0, str(default_puzzle_size))
        self.width_entry.grid(row=0, column=1)

        self.height_label = tk.Label(self, text="Height:")
        self.height_label.grid(row=1, column=0)
        self.height_entry = tk.Entry(self)
        self.height_entry.insert(0, str(default_puzzle_size))
        self.height_entry.grid(row=1, column=1)

        # Label for the block entries
        self.blocks_label = tk.Label(self, text="Blocks:")
        self.blocks_label.grid(row=2, column=0, columnspan=8)

        # Dictionary to hold the quantity entries for each block
        self.block_entries = {}
        i = 3  # Start at row 3 for the block entries
        j = 0  # Start at column 0 for the block entries
        for block_name, block_info in blocks.items():
            block_visual = get_block_representation(block_info['shape'])
            block_label = tk.Label(self, text=block_visual, font=("Courier", 12), justify=tk.LEFT)
            block_label.grid(row=i, column=j)

            label = tk.Label(self, text=f"{block_name} quantity:")
            label.grid(row=i, column=j+1)
            
            entry = tk.Entry(self)
            entry.insert(0, "0")  # Set default value to 0
            entry.grid(row=i+1, column=j+1)
            
            self.block_entries[block_name] = entry
            
            # Increase column count by 2 for the next entry pair (label and entry)
            j += 2
            
            # If we have added 4 input pairs, increase row count and reset column count
            if j >= 8:
                i += 2
                j = 0

        self.height_entry.bind('<KeyRelease>', self.update_total_value)
        self.width_entry.bind('<KeyRelease>', self.update_total_value)

        for block_name, entry in self.block_entries.items():
            entry.bind('<KeyRelease>', self.update_total_value)

        # Volume display
        self.total_volume = tk.Label(self, text="total")
        self.total_volume.grid(row=i+2, column=0, columnspan=8)
        self.total_volume["text"] = f"Total Block value: {self.total_value}"

        # Solve button
        self.solve_button = tk.Button(self, text="Solve", command=self.solve)
        self.solve_button.grid(row=i+3, column=0, columnspan=8)

        # Result display
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=i+4, column=0, columnspan=8)
    
    def update_total_value(self, event=None):
        # Reset the total value to 0 before calculating it again
        self.total_value = 0

        # Calculate the total value without solving the puzzle
        for block_name, entry in self.block_entries.items():
            try:
                quantity = int(entry.get())
                block_value = np.sum(blocks[block_name]['shape'])
                self.total_value += quantity * block_value
            except ValueError:
                # If the entry is not a number, we can either skip it or set it to 0
                continue

        # Calculate the area of the puzzle
        try:
            height = int(self.height_entry.get())
            width = int(self.width_entry.get())
            puzzle_area = height * width
        except ValueError:
            puzzle_area = 0  # Default to 0 if height/width are invalid

        # Enable or disable the "Solve" button
        if self.total_value > puzzle_area:
            self.solve_button["state"] = "disabled"
        else:
            self.solve_button["state"] = "normal"

        # Now update the volume label's text with the new total value
        self.total_volume["text"] = f"Total block value: {self.total_value}"

    def solve(self):
        try:
            # Clear any previous solution
            for label in self.solution_labels:
                label.destroy()
            self.solution_labels.clear()
            self.result_label["text"] = ""

            # Get puzzle dimensions
            height = int(self.height_entry.get())
            width = int(self.width_entry.get())
            
            # Update blocks with quantities from entries
            for block_name, entry in self.block_entries.items():
                blocks[block_name]['quantity'] = int(entry.get())
            
            # Initialize the puzzle grid with spaces representing empty slots
            puzzle_grid = np.full((height, width), ' ', dtype='<U1')

            ordered_block_keys = order_blocks(blocks)

            # Attempt to solve the puzzle
            solution_exists, solved_puzzle = solve_puzzle(puzzle_grid, blocks, ordered_block_keys)
            
            if solution_exists:
                # Show the solution in the result label
                self.display_solution(solved_puzzle)
            else:
                self.result_label["text"] = "No solution exists."
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for all fields.")

    def display_solution(self, solved_puzzle):
        start_row = 15  # Start after the buffer row and an additional space for clarity

        # Display the solution grid
        for i, row in enumerate(solved_puzzle):
            for j, cell in enumerate(row):
                block_label = cell
                color = block_colors.get(block_label, 'white')  # Fetch the color for the block

                # Create a label for each cell in the solution grid
                cell_label = tk.Label(self, text=f"{block_label}", bg=color, borderwidth=1, relief="solid")

                # Adjust the row index by adding start_row to place it under the input fields
                cell_label.grid(row=start_row + i, column=j, sticky="nsew", padx=1, pady=1)
                self.solution_labels.append(cell_label)  # Add the label to the list

        # Adjust row/column configurations for better display if needed
        for i in range(len(solved_puzzle)):
            self.grid_rowconfigure(start_row + i, weight=1)
        for j in range(len(solved_puzzle[0])):
            self.grid_columnconfigure(j, weight=1)


root = tk.Tk()
root.title("Block Puzzle Solver")
app = Application(master=root)
app.mainloop()
