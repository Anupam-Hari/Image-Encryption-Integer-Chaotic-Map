import numpy as np

from keygen.seed_derivation import derive_seed_sha512, split_seed
from chaotic_maps.coupled_3d_uint64 import initialize_state
from encryption.block_processor import encrypt_block, decrypt_block


# Utility: Split Image into Blocks
def split_into_blocks(image, block_size):
    h, w = image.shape
    blocks = []

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            blocks.append(image[i:i+block_size, j:j+block_size])

    return blocks


def reconstruct_from_blocks(blocks, image_shape, block_size):
    h, w = image_shape
    reconstructed = np.zeros((h, w), dtype=np.uint8)

    idx = 0
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            reconstructed[i:i+block_size, j:j+block_size] = blocks[idx]
            idx += 1

    return reconstructed

# Encryption
def encrypt_image(image, key_bytes, iv_bytes, config, return_keystream=False):

    image = image.astype(np.uint8)

    block_size = config["lightweight_3d_uint64"]["block_size"]

    # 1. Seed derivation
    seed = derive_seed_sha512(key_bytes, iv_bytes)
    seed_params = split_seed(seed)

    # 2. Initialize chaotic state
    state = initialize_state(seed_params, config)

    # 3. Initialize C_prev from IV (last byte)
    c_prev = iv_bytes[-1]

    # 4. Process blocks
    blocks = split_into_blocks(image, block_size)
    encrypted_blocks = []
    all_keystream = []

    for block in blocks:
        block = block.copy()
        encrypted_block, state, ks = encrypt_block(
            block,
            state,
            config
        )
        encrypted_blocks.append(encrypted_block)
        ks_array = np.frombuffer(ks, dtype=np.uint8)
        all_keystream.append(ks_array)

    # 5. Reconstruct image
    cipher_image = reconstruct_from_blocks(
        encrypted_blocks,
        image.shape,
        block_size
    )

    if return_keystream:
        ks_full = np.concatenate(all_keystream).astype(np.uint8)
        return cipher_image, ks_full

    return cipher_image

    return cipher_image

# Decryption
def decrypt_image(cipher_image, key_bytes, iv_bytes, config):

    cipher_image = cipher_image.astype(np.uint8)

    block_size = config["lightweight_3d_uint64"]["block_size"]

    # 1. Seed derivation
    seed = derive_seed_sha512(key_bytes, iv_bytes)
    seed_params = split_seed(seed)

    # 2. Initialize chaotic state
    state = initialize_state(seed_params, config)

    # 3. Initialize C_prev from IV
    c_prev = iv_bytes[-1]

    # 4. Process blocks
    blocks = split_into_blocks(cipher_image, block_size)
    decrypted_blocks = []

    for block in blocks:
        block = block.copy()
        decrypted_block, state = decrypt_block(
            block,
            state,
            config
        )
        decrypted_blocks.append(decrypted_block)

    # 5. Reconstruct image
    plain_image = reconstruct_from_blocks(
        decrypted_blocks,
        cipher_image.shape,
        block_size
    )

    return plain_image