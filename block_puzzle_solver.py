import numpy as np

# Define the puzzle size and the blocks
puzzle_size = 6

blocks = {
    'long_z': np.array([
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ]),
    'l': np.array([
        [1, 0],
        [1, 0],
        [1, 1]
    ]),
    'l2': np.array([
        [1, 0],
        [1, 0],
        [1, 1]
    ]),
    'l3': np.array([
        [1, 0],
        [1, 0],
        [1, 1]
    ]),
    'invert_l': np.array([
        [0, 1],
        [0, 1],
        [1, 1]
    ]),
    'invert_l2': np.array([
        [0, 1],
        [0, 1],
        [1, 1]
    ]),
    'invert_z': np.array([
        [0, 1, 1],
        [1, 1, 0]
    ]),
    'invert_z2': np.array([
        [0, 1, 1],
        [1, 1, 0]
    ]),
    'short_l': np.array([
        [1, 0],
        [1, 1]
    ])
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

def solve_puzzle(puzzle, blocks, idx=0):
    if idx == len(blocks):
        return True, puzzle

    block_key = list(blocks.keys())[idx]
    block_variants = [blocks[block_key]] + [rotate(blocks[block_key], i) for i in range(1, 4)]
    block_id = block_ids[block_key]

    for block in block_variants:
        for i in range(puzzle_size - block.shape[0] + 1):
            for j in range(puzzle_size - block.shape[1] + 1):
                if fits(puzzle, block, (i, j)):
                    puzzle = place_block(puzzle, block, (i, j), block_id)
                    success, result = solve_puzzle(puzzle, blocks, idx + 1)
                    if success:
                        return True, result
                    puzzle = remove_block(puzzle, block, (i, j))

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