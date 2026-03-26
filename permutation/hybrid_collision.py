import numpy as np

def encrypt_hybrid_collision(block, collision_bits):

    B = block.shape[0]
    half = B // 2

    top = block[:half, :].copy()
    bottom = block[half:, :].copy()

    idx = 0

    for i in range(half):
        for j in range(B):

            decision = collision_bits[idx]

            if decision == 1:
                top[i, j], bottom[i, j] = bottom[i, j], top[i, j]

            idx += 1

    block[:half, :] = top
    block[half:, :] = bottom

    return block


def decrypt_hybrid_collision(block, collision_bits):

    return encrypt_hybrid_collision(block, collision_bits)