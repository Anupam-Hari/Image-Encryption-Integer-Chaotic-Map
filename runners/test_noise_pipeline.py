import cv2
import numpy as np
import secrets

from config.default_config import CONFIG
from encryption.lightweight_image_encryptor import encrypt_image, decrypt_image


# ------------------------------------------------------------
# Load Image
# ------------------------------------------------------------
image_path = "cameraman.png"
img = cv2.imread(image_path, 0)

if img is None:
    raise ValueError("Image not found.")


# ------------------------------------------------------------
# Bit-Flip Noise on Ciphertext
# ------------------------------------------------------------
def add_bitflip_noise(image, bit_error_rate=0.001):
    noisy = image.copy()
    rows, cols = noisy.shape

    total_bits = rows * cols * 8
    num_flips = int(total_bits * bit_error_rate)

    for _ in range(num_flips):
        i = np.random.randint(0, rows)
        j = np.random.randint(0, cols)
        bit = 1 << np.random.randint(0, 8)
        noisy[i, j] ^= bit

    return noisy


# ------------------------------------------------------------
# Key / IV Generation
# ------------------------------------------------------------
key_size_bytes = CONFIG["lightweight_3d_uint64"]["key_size_bits"] // 8
iv_size_bytes = CONFIG["lightweight_3d_uint64"]["iv_size_bits"] // 8

key = secrets.token_bytes(key_size_bytes)
iv = secrets.token_bytes(iv_size_bytes)


# ------------------------------------------------------------
# Encrypt
# ------------------------------------------------------------
cipher = encrypt_image(img, key, iv, CONFIG)


# ------------------------------------------------------------
# Simulate Transmission Bit Errors
# ------------------------------------------------------------
cipher_noisy = add_bitflip_noise(cipher, bit_error_rate=0.001)


# ------------------------------------------------------------
# Decrypt Corrupted Ciphertext
# ------------------------------------------------------------
decrypted = decrypt_image(cipher_noisy, key, iv, CONFIG)


# ------------------------------------------------------------
# Display Results
# ------------------------------------------------------------
cv2.imshow("Original", img)
cv2.imshow("Encrypted", cipher)
cv2.imshow("Decrypted from Corrupted Cipher", decrypted)

cv2.waitKey(0)
cv2.destroyAllWindows()