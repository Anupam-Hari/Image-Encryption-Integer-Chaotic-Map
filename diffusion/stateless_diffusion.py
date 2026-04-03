import numpy as np

def rotl8(value, r):
    r = r % 8
    return ((value << r) | (value >> (8 - r))) & 0xFF

def rotr8(value, r):
    r = r % 8
    return ((value >> r) | (value << (8 - r))) & 0xFF


def encrypt_stateless_diffusion_block(
    block,
    keystream,
    rotation_vals,
    scan_indices
):
    encrypted = block.copy()
    idx = 0
    prev_c = 0

    for (i, j) in scan_indices:
        P = int(encrypted[i, j])
        K = int(keystream[idx])
        r = int(rotation_vals[idx])

        # Intra-block chained diffusion
        mixed = ((P ^ K) + prev_c) % 256
        C = rotl8(mixed, r)

        encrypted[i, j] = C
        prev_c = C
        idx += 1

    return encrypted


def decrypt_stateless_diffusion_block(
    block,
    keystream,
    rotation_vals,
    scan_indices
):
    decrypted = block.copy()
    prev_c = 0
    idx = 0

    for (i, j) in scan_indices:
        C = int(decrypted[i, j])
        K = int(keystream[idx])
        r = int(rotation_vals[idx])

        # Exact inverse
        mixed = rotr8(C, r)
        P = ((mixed - prev_c) % 256) ^ K

        decrypted[i, j] = P
        prev_c = C
        idx += 1

    return decrypted