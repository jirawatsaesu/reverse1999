import numpy as np

blocks = {
    'long_z': {
        'shape': np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]),
        'label': 'Z',
        'unique_rotations': 1
    },
    'long_t': {
        'shape': np.array([
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 1]
        ]),
        'label': 'T',
        'unique_rotations': 1
    },
    'u': {
        'shape': np.array([
            [1, 0, 1],
            [1, 1, 1]
        ]),
        'label': 'U',
        'unique_rotations': 1
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