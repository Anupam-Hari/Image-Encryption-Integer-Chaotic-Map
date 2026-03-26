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

    for (i, j) in scan_indices:
        P = int(encrypted[i, j])
        K = int(keystream[idx])
        r = int(rotation_vals[idx])

        # Stateless keyed diffusion
        C = rotl8(P ^ K, r)

        encrypted[i, j] = C
        idx += 1

    return encrypted


def decrypt_stateless_diffusion_block(
    block,
    keystream,
    rotation_vals,
    scan_indices
):
    decrypted = block.copy()
    idx = 0

    for (i, j) in scan_indices:
        C = int(decrypted[i, j])
        K = int(keystream[idx])
        r = int(rotation_vals[idx])

        # Exact inverse
        P = rotr8(C, r) ^ K

        decrypted[i, j] = P
        idx += 1

    return decrypted