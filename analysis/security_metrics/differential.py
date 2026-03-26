import numpy as np


def compute_npcr(cipher1: np.ndarray, cipher2: np.ndarray) -> float:
    diff = cipher1 != cipher2
    return np.sum(diff) * 100.0 / cipher1.size


def compute_uaci(cipher1: np.ndarray, cipher2: np.ndarray) -> float:
    return np.mean(
        np.abs(cipher1.astype(np.int32) -
               cipher2.astype(np.int32)) / 255.0
    ) * 100.0