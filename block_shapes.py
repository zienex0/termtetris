import random
import numpy as np

shapez = [np.array([[1, 1],
                   [0, 1],
                   [0, 1]]),
        np.array([[2, 2],
                  [2, 2]]),
        np.array([[0, 3],
                  [3, 3],
                  [3, 0]]),
        np.array([[4],
                  [4],
                  [4],
                  [4]])]


def choose_random_shape():
    return random.choice(shapez)