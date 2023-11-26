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

def heuristic_score(puzzle, block, pos):
    # Example heuristic: Count the number of adjacent empty spaces
    score = 0
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            if block[i][j] == 1:
                # Check adjacent cells
                for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                    ni, nj = i + pos[0] + di, j + pos[1] + dj
                    if 0 <= ni < puzzle.shape[0] and 0 <= nj < puzzle.shape[1]:
                        if puzzle[ni][nj] == ' ':
                            score += 1
    return score

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
        possible_placements = []
        for i in range(puzzle.shape[0] - block.shape[0] + 1):
            for j in range(puzzle.shape[1] - block.shape[1] + 1):
                if fits(puzzle, block, (i, j)):
                    score = heuristic_score(puzzle, block, (i, j))
                    possible_placements.append(((i, j), score))
    
        # Sort placements based on heuristic score
        possible_placements.sort(key=lambda x: x[1], reverse=True)  # High score first

        for pos, _ in possible_placements:
            puzzle = place_block(puzzle, block, pos, block_id)
            blocks[block_key]['quantity'] -= 1  # Decrement the block quantity

            success, result = solve_puzzle(puzzle, blocks, block_keys, idx + (blocks[block_key]['quantity'] == 0))
            if success:
                return True, result  # Solution found

            puzzle = remove_block(puzzle, block, pos)  # Backtrack
            blocks[block_key]['quantity'] += 1  # Increment the block quantity back
    return False, puzzle
