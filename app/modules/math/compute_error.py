import math

from scipy.spatial import distance
import numpy as np


def euclidean_distance(p1: np.ndarray, p2: np.ndarray) -> float:
    return distance.euclidean(p1, p2)


def compute_average_error(m1: np.ndarray, m2: np.ndarray) -> float:
    assert m1.shape == m2.shape
    s = 0
    num_coords = m1.shape[0]
    for i in range(num_coords):
        try:
            s += euclidean_distance(m1[i], m2[i])
        except ValueError:
            return math.nan
    return s/num_coords
