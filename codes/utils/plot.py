import numpy as np
from numpy.typing import NDArray

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap





def plot_matrix(matrix : list[ list[int] ] | NDArray[np.int32]):
    matrix = np.asarray(matrix)

    # Kétszínű csempék: 0 = első játékos nyert (kék), 1 = második játékos nyert (naracssárga)
    cmap = ListedColormap(['#1a80bb', '#ea801c'])

    fig, ax = plt.subplots(figsize=(10, 10))

    # ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, interpolation='nearest', aspect='equal', origin='lower')
    ax.imshow(matrix, cmap='plasma', vmin=0, vmax=1, interpolation='nearest', aspect='equal', origin='lower')

    # Tengelyfeliratok
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels(np.arange(1, matrix.shape[1] + 1))
    ax.set_yticklabels(np.arange(1, matrix.shape[0] + 1))

    plt.tight_layout()
    plt.show()
