import random
import numpy as np

shapez = [
        np.array([[1, 1],
                  [1, 1]]),  # o shape
        
        np.array([[2],
                  [2],
                  [2],
                  [2]]),  # i shape

        np.array([[0, 3, 3],
                  [3, 3, 0]]),  # s shape

        np.array([[4, 4, 0],
                  [0, 4, 4]]),  # z shape

        np.array([[5, 0],
                  [5, 0],
                  [5, 5]]),  # l shape
        
        np.array([[0, 6],
                  [0, 6],
                  [6, 6]]),  # j shape

        np.array([[7, 7, 7],
                  [0, 7, 0]])  # t shape
]


def choose_random_shape():
    return random.choice(shapez)