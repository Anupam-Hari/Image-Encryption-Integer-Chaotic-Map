import numpy as np


def compute_entropy(image: np.ndarray) -> float:
    histogram = np.histogram(
        image.flatten(),
        bins=256,
        range=(0, 256)
    )[0]

    prob = histogram / np.sum(histogram)
    prob = prob[prob > 0]

    return -np.sum(prob * np.log2(prob))