import numpy as np

# Define the puzzle size and the blocks
puzzle_size = 6
blocks = {
    'long_z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]),
        'quantity': 1,
        'id': 'Z'
    },
    'L': {
        'shape': np.array([
            [1, 0],
            [1, 0],
            [1, 1]
        ]),
        'quantity': 3,
        'id': 'L'
    },
    'invert_l': {
        'shape': np.array([
            [0, 1],
            [0, 1],
            [1, 1]
        ]),
        'quantity': 2,
        'id': '<'
    },
    'invert_z': {
        'shape': np.array([
            [0, 1, 1],
            [1, 1, 0]
        ]),
        'quantity': 2,
        'id': 'S'
    },
    'short_l': {
        'shape': np.array([
            [1, 0],
            [1, 1]
        ]),
        'quantity': 1,
        'id': 'sL'
    }
}

block_ids = {
    'long_z': 'Z',
    'l': 'L',
    'l2': 'L',
    'l3': 'L',
    'invert_l': '<',
    'invert_l2': '<',
    'invert_z': 's',
    'invert_z2': 's',
    'short_l': 'l'
}

def rotate(block, times=1):
    return np.rot90(block, times)

def fits(puzzle, block, pos):
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i][j] == 1:
                if (i + pos[0] >= puzzle_size or
                        j + pos[1] >= puzzle_size or
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

def solve_puzzle(puzzle, blocks, block_keys=None, idx=0):
    if block_keys is None:
        block_keys = list(blocks.keys())
    
    if idx == len(block_keys):
        return True, puzzle

    block_key = block_keys[idx]
    block_data = blocks[block_key]
    block_variants = [block_data['shape']] + [rotate(block_data['shape'], i) for i in range(1, 4)]
    block_id = block_data['id']

    for block in block_variants:
        if block_data['quantity'] == 0:
            break  # Skip if no more blocks of this type are left to place
        for i in range(puzzle_size - block.shape[0] + 1):
            for j in range(puzzle_size - block.shape[1] + 1):
                if fits(puzzle, block, (i, j)):
                    puzzle = place_block(puzzle, block, (i, j), block_id)
                    blocks[block_key]['quantity'] -= 1  # Decrement the block quantity
                    success, result = solve_puzzle(puzzle, blocks, block_keys, idx + (block_data['quantity'] == 0))
                    if success:
                        return True, result
                    puzzle = remove_block(puzzle, block, (i, j))
                    blocks[block_key]['quantity'] += 1  # Increment the block quantity back

    return False, puzzle


# Initialize the puzzle grid with spaces representing empty slots
puzzle_grid = np.full((puzzle_size, puzzle_size), ' ', dtype='<U1')

# Attempt to solve the puzzle
solution_exists, solved_puzzle = solve_puzzle(puzzle_grid, blocks)
if solution_exists:
    print("Solution found:")
    print(np.array2string(solved_puzzle, separator=' '))
else:
    print("No solution exists.")