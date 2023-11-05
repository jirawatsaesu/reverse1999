import numpy as np

# Define the puzzle size and the blocks
puzzle_size = 5
blocks = {
    'long_z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]),
        'quantity': 0,
        'id': 'Z'
    },
    'l': {
        'shape': np.array([
            [1, 0],
            [1, 0],
            [1, 1]
        ]),
        'quantity': 0,
        'id': 'L'
    },
    'j': {
        'shape': np.array([
            [0, 1],
            [0, 1],
            [1, 1]
        ]),
        'quantity': 0,
        'id': 'J'
    },
    's': {
        'shape': np.array([
            [0, 1, 1],
            [1, 1, 0]
        ]),
        'quantity': 0,
        'id': 's'
    },
    'z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 1]
        ]),
        'quantity': 0,
        'id': 'z'
    },
    'square': {
        'shape': np.array([
            [1, 1],
            [1, 1]
        ]),
        'quantity': 0,
        'id': 'o'
    },
    'short_t': {
        'shape': np.array([
            [0, 1, 0],
            [1, 1, 1]
        ]),
        'quantity': 0,
        'id': 't'
    },
    'i': {
        'shape': np.array([
            [1, 1, 1, 1]
        ]),
        'quantity': 0,
        'id': 'I',
    },
    'short_l': {
        'shape': np.array([
            [1, 0],
            [1, 1]
        ]),
        'quantity': 0,
        'id': 'l'
    },
    'short_i': {
        'shape': np.array([
            [1, 1]
        ]),
        'quantity': 0,
        'id': 'i'
    },
    'dot': {
        'shape': np.array([
            [1]
        ]),
        'quantity': 0,
        'id': 'd'
    }
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

    # If no blocks of this type should be placed, skip to the next block
    if block_data['quantity'] == 0:
        return solve_puzzle(puzzle, blocks, block_keys, idx + 1)

    block_variants = [block_data['shape']] + [rotate(block_data['shape'], i) for i in range(1, 4)]
    block_id = block_data['id']

    for block in block_variants:
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
