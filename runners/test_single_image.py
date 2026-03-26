import os
import cv2
import numpy as np
import secrets

from config.default_config import CONFIG
from encryption.lightweight_image_encryptor import encrypt_image, decrypt_image
from analysis.evaluator import evaluate
from experiments.run_manager import create_run
# from results.result_writer import save_results


algorithm = CONFIG["algorithm"]

if algorithm != "lightweight_3d_uint64":
    raise ValueError("CONFIG['algorithm'] must be 'lightweight_3d_uint64'.")

run_info = create_run(algorithm, CONFIG)

encrypted_path = run_info["encrypted_path"]
decrypted_path = run_info["decrypted_path"]
run_id = run_info["run_id"]

image_path = "test_images/256x256/cameraman.png"

img = cv2.imread(image_path, 0)
if img is None:
    raise ValueError("Image not found.")

key_size_bytes = CONFIG["lightweight_3d_uint64"]["key_size_bits"] // 8
iv_size_bytes = CONFIG["lightweight_3d_uint64"]["iv_size_bits"] // 8

key = secrets.token_bytes(key_size_bytes)
iv = secrets.token_bytes(iv_size_bytes)

cipher = encrypt_image(img, key, iv, CONFIG)

recovered = decrypt_image(cipher, key, iv, CONFIG)

cv2.imwrite(os.path.join(encrypted_path, "encrypted.png"), cipher)
cv2.imwrite(os.path.join(decrypted_path, "decrypted.png"), recovered)

img_modified = img.copy()
img_modified[0, 0] ^= 1

cipher2 = encrypt_image(img_modified, key, iv, CONFIG)
results = evaluate(
    original=img,
    encrypted=cipher,
    encrypt_function=lambda x: encrypt_image(x, key, iv, CONFIG),
    encrypted_modified=cipher2,
    num_runs=10,
    plot = True
)
results["decryption_correct"] = bool(np.array_equal(img, recovered))

# save_results(results, algorithm, run_id)

print("Single image lightweight test complete.")

cv2.imshow("Original", img)
cv2.imshow("Encrypted", cipher)
cv2.imshow("Decrypted", recovered)

cv2.waitKey(0)
cv2.destroyAllWindows()