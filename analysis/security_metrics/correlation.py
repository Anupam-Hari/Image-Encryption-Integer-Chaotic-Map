import numpy as np


def horizontal_correlation(image: np.ndarray) -> float:
    x = image[:, :-1].flatten()
    y = image[:, 1:].flatten()
    return np.corrcoef(x, y)[0, 1]


def vertical_correlation(image: np.ndarray) -> float:
    x = image[:-1, :].flatten()
    y = image[1:, :].flatten()
    return np.corrcoef(x, y)[0, 1]


def diagonal_correlation(image: np.ndarray) -> float:
    x = image[:-1, :-1].flatten()
    y = image[1:, 1:].flatten()
    return np.corrcoef(x, y)[0, 1]