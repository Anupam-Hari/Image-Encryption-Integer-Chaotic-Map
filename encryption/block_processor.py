# IMAGE_ENCRYPTION/encryption/block_processor.py

import numpy as np

from keygen.keystream_generator import generate_keystream, generate_control_stream
from permutation.hybrid_collision import (
    encrypt_hybrid_collision,
    decrypt_hybrid_collision
)
from permutation.dynamic_scan import select_scan_mode, scan_indices
from diffusion.stateless_diffusion import (
    encrypt_stateless_diffusion_block,
    decrypt_stateless_diffusion_block
)
from diffusion.bitplane_mixing import (
    encrypt_bitplane_mix,
    decrypt_bitplane_mix
)

# ============================================================
# Encryption
# ============================================================

def encrypt_block(block, state, config):

    B = block.shape[0]
    num_pixels = B * B

    # 1. Generate control entropy
    control, state = generate_control_stream(state, num_pixels, config)

    rotation_vals = control["rotation_vals"]
    collision_bits = control["collision_bits"]
    bitplane_masks = control["bitplane_masks"]

    # 2. Select scan mode
    scan_selector = rotation_vals[0]
    mode = select_scan_mode(scan_selector, config)
    indices = scan_indices(block.shape, mode)

    # 3. Hybrid collision (spatial)
    block = encrypt_hybrid_collision(block, collision_bits)

    # 4. Generate keystream
    keystream, state = generate_keystream(state, num_pixels)
    raw_keystream = keystream

    # 5. Stateless keyed diffusion
    block = encrypt_stateless_diffusion_block(
        block,
        keystream,
        rotation_vals,
        indices
    )

    # 6. Bitplane adaptive mixing
    block = encrypt_bitplane_mix(
        block,
        rotation_vals,
        bitplane_masks,
        config
    )

    block_sum = int(np.sum(block)) & ((1 << 64) - 1)

    # state["r1"] ^= block_sum
    # state["r2"] ^= (block_sum << 1) & ((1 << 64) - 1)
    # state["r3"] ^= (block_sum << 2) & ((1 << 64) - 1)

    return block, state, raw_keystream


# ============================================================
# Decryption
# ============================================================

def decrypt_block(block, state, config):

    B = block.shape[0]
    num_pixels = B * B

    # Preserve original ciphertext for feedback
    original_cipher_block = block.copy()

    # 1. Regenerate control entropy
    control, state = generate_control_stream(state, num_pixels, config)

    rotation_vals = control["rotation_vals"]
    collision_bits = control["collision_bits"]
    bitplane_masks = control["bitplane_masks"]

    # 2. Select scan mode
    scan_selector = rotation_vals[0]
    mode = select_scan_mode(scan_selector, config)
    indices = scan_indices(block.shape, mode)

    # 3. Reverse bitplane mixing
    block = decrypt_bitplane_mix(
        block,
        rotation_vals,
        bitplane_masks,
        config
    )

    # 4. Generate keystream
    keystream, state = generate_keystream(state, num_pixels)

    # 5. Reverse Stateless keyed diffusion
    block = decrypt_stateless_diffusion_block(
        block,
        keystream,
        rotation_vals,
        indices
    )

    # 6. Reverse hybrid collision
    block = decrypt_hybrid_collision(block, collision_bits)

    block_sum = int(np.sum(original_cipher_block)) & ((1 << 64) - 1)

    # state["r1"] ^= block_sum
    # state["r2"] ^= (block_sum << 1) & ((1 << 64) - 1)
    # state["r3"] ^= (block_sum << 2) & ((1 << 64) - 1)

    return block, state