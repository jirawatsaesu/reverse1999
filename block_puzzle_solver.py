import tkinter as tk
from tkinter import messagebox
import numpy as np

# Define the blocks
blocks = {
    'long_z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]),
        'label': 'Z'
    },
    'long_t': {
        'shape': np.array([
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 1]
        ]),
        'label': 'T'
    },
    'u': {
        'shape': np.array([
            [1, 0, 1],
            [1, 1, 1]
        ]),
        'label': 'U',
    },
    'plus': {
        'shape': np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]),
        'label': '+',
        'unique_rotations': 1
    },
    'l': {
        'shape': np.array([
            [1, 0],
            [1, 0],
            [1, 1]
        ]),
        'label': 'L'
    },
    'j': {
        'shape': np.array([
            [0, 1],
            [0, 1],
            [1, 1]
        ]),
        'label': 'J'
    },
    's': {
        'shape': np.array([
            [0, 1, 1],
            [1, 1, 0]
        ]),
        'label': 's'
    },
    'z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 1]
        ]),
        'label': 'z'
    },
    'square': {
        'shape': np.array([
            [1, 1],
            [1, 1]
        ]),
        'label': 'O',
        'unique_rotations': 1
    },
    't': {
        'shape': np.array([
            [0, 1, 0],
            [1, 1, 1]
        ]),
        'label': 't'
    },
    'i': {
        'shape': np.array([
            [1, 1, 1, 1]
        ]),
        'label': 'I',
        'unique_rotations': 2
    },
    'short_l': {
        'shape': np.array([
            [1, 1],
            [1, 0]
        ]),
        'label': 'l'
    },
    'short_i': {
        'shape': np.array([
            [1, 1]
        ]),
        'label': 'i',
        'unique_rotations': 2
    },
    'dot': {
        'shape': np.array([
            [1]
        ]),
        'label': 'o',
        'unique_rotations': 1
    }
}

block_colors = {
    'Z': 'red',
    'T': 'green',
    'U': 'brown',
    '+': 'violet',
    'L': 'blue',
    'J': 'orange',
    's': 'yellow',
    'z': 'purple',
    'O': 'cyan',
    't': 'magenta',
    'I': 'pink',
    'l': 'lime',
    'i': 'navy',
    'o': 'grey',
}


def fits(puzzle, block, pos):
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i][j] == 1:
                if (i + pos[0] >= puzzle.shape[0] or
                        j + pos[1] >= puzzle.shape[1] or
                        puzzle[i + pos[0]][j + pos[1]] != ' '):
                    return False
    return True

def place_block(puzzle, block, pos, block_id):
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i][j] == 1:
                puzzle[i + pos[0]][j + pos[1]] = block_id
    return puzzle

def remove_block(puzzle, block, pos):
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i][j] == 1:
                puzzle[i + pos[0]][j + pos[1]] = ' '
    return puzzle

def get_block_representation(block, fill='[]', empty='  '):
    """Create a string representation of a block with given fill and empty symbols."""
    return '\n'.join([''.join([fill if cell else empty for cell in row]) for row in block])

def solve_puzzle(puzzle, blocks, block_keys=None, idx=0):
    if block_keys is None:
        block_keys = list(blocks.keys())
    
    if idx == len(block_keys):
        return True, puzzle

    block_key = block_keys[idx]
    block_data = blocks[block_key]

    # If no blocks of this type should be placed, skip to the next block
    if block_data['quantity'] == 0:
        return solve_puzzle(puzzle, blocks, block_keys, idx + 1)

    # Generate the block variants based on the number of unique rotations
    if 'unique_rotations' in block_data:
        block_variants = [np.rot90(block_data['shape'], i) for i in range(block_data['unique_rotations'])]
    else:
        block_variants = [block_data['shape']] + [np.rot90(block_data['shape'], i) for i in range(1, 4)]

    block_id = block_data['label']

    for block in block_variants:
        for i in range(puzzle.shape[0] - block.shape[0] + 1):
            for j in range(puzzle.shape[1] - block.shape[1] + 1):
                if fits(puzzle, block, (i, j)):
                    puzzle = place_block(puzzle, block, (i, j), block_id)
                    blocks[block_key]['quantity'] -= 1  # Decrement the block quantity
                    success, result = solve_puzzle(puzzle, blocks, block_keys, idx + (block_data['quantity'] == 0))
                    if success:
                        return True, result
                    puzzle = remove_block(puzzle, block, (i, j))
                    blocks[block_key]['quantity'] += 1  # Increment the block quantity back

    return False, puzzle

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.total_value = 0
        self.create_widgets()

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
            self.result_label["text"] = ""

            # Get puzzle dimensions
            height = int(self.height_entry.get())
            width = int(self.width_entry.get())
            
            # Update blocks with quantities from entries
            for block_name, entry in self.block_entries.items():
                blocks[block_name]['quantity'] = int(entry.get())
            
            # Initialize the puzzle grid with spaces representing empty slots
            puzzle_grid = np.full((height, width), ' ', dtype='<U1')

            # Attempt to solve the puzzle
            solution_exists, solved_puzzle = solve_puzzle(puzzle_grid, blocks)
            
            if solution_exists:
                # Show the solution in the result label
                self.display_solution(solved_puzzle)
            else:
                self.result_label["text"] = "No solution exists."
        except ValueError as e:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for all fields.")

    def display_solution(self, solved_puzzle):
        start_row = 15  # Start after the buffer row and an additional space for clarity

        # Calculate block width for proper display (optional)
        block_width = max(len(str(item)) for row in solved_puzzle for item in row)

        # Display the solution grid
        for i, row in enumerate(solved_puzzle):
            for j, cell in enumerate(row):
                block_label = cell
                color = block_colors.get(block_label, 'white')  # Fetch the color for the block

                # Create a label for each cell in the solution grid
                cell_label = tk.Label(self, text=f"{block_label}" * block_width, bg=color, borderwidth=1, relief="solid")

                # Adjust the row index by adding start_row to place it under the input fields
                cell_label.grid(row=start_row + i, column=j, sticky="nsew", padx=1, pady=1)

        # Adjust row/column configurations for better display if needed
        for i in range(len(solved_puzzle)):
            self.grid_rowconfigure(start_row + i, weight=1)
        for j in range(len(solved_puzzle[0])):
            self.grid_columnconfigure(j, weight=1)


root = tk.Tk()
root.title("Block Puzzle Solver")
app = Application(master=root)
app.mainloop()
