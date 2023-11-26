import numpy as np

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
