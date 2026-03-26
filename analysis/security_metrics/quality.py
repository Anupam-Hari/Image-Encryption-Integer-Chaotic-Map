import numpy as np
from skimage.metrics import structural_similarity as ssim


def compute_psnr(original: np.ndarray, encrypted: np.ndarray) -> float:
    mse = np.mean((original.astype(np.float64) -
                   encrypted.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10((255 ** 2) / mse)


def compute_ssim(original: np.ndarray, encrypted: np.ndarray) -> float:
    return ssim(original, encrypted, data_range=255)