import numpy as np
from scipy.stats import chisquare


def compute_chi_square(image: np.ndarray):
    histogram = np.histogram(
        image.flatten(),
        bins=256,
        range=(0, 256)
    )[0]

    expected = np.ones(256) * (image.size / 256)

    chi_value, p_value = chisquare(histogram, expected)

    return chi_value, p_value