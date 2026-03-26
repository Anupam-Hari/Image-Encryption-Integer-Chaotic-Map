import cv2
import numpy as np
import secrets

from config.default_config import CONFIG
from encryption.lightweight_image_encryptor import encrypt_image, decrypt_image
from analysis.evaluator import evaluate


# ------------------------------------------------------------------
# Load Image
# ------------------------------------------------------------------
image_path = "test_images/256x256/cameraman.png"
img = cv2.imread(image_path, 0)

if img is None:
    raise ValueError("Image not found.")


# ------------------------------------------------------------------
# Key / IV Generation
# ------------------------------------------------------------------
key_size_bytes = CONFIG["lightweight_3d_uint64"]["key_size_bits"] // 8
iv_size_bytes = CONFIG["lightweight_3d_uint64"]["iv_size_bits"] // 8

key = secrets.token_bytes(key_size_bytes)
iv = secrets.token_bytes(iv_size_bytes)


# ------------------------------------------------------------------
# Encryption
# ------------------------------------------------------------------
cipher = encrypt_image(img, key, iv, CONFIG)


# ------------------------------------------------------------------
# Differential Attack Setup (NPCR / UACI)
# ------------------------------------------------------------------
img_modified = img.copy()
img_modified[0, 0] ^= 1

cipher2 = encrypt_image(img_modified, key, iv, CONFIG)


# ------------------------------------------------------------------
# Metric Evaluation
# ------------------------------------------------------------------
results = evaluate(
    original=img,
    encrypted=cipher,
    encrypted_modified=cipher2,
    encrypt_function=lambda x: encrypt_image(x, key, iv, CONFIG)
)

for k, v in results.items():
    print(f"{k}: {v}")