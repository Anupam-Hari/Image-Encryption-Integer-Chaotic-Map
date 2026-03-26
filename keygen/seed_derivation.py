# IMAGE_ENCRYPTION/keygen/seed_derivation.py

import hashlib

MASK = (1 << 64) - 1


def derive_seed_sha512(key_bytes: bytes, iv_bytes: bytes) -> bytes:
    """
    Derive 512-bit seed using SHA512(key || iv).
    """

    if not isinstance(key_bytes, (bytes, bytearray)):
        raise TypeError("key_bytes must be bytes")

    if not isinstance(iv_bytes, (bytes, bytearray)):
        raise TypeError("iv_bytes must be bytes")

    hasher = hashlib.sha512()
    hasher.update(key_bytes)
    hasher.update(iv_bytes)

    return hasher.digest()  # 64 bytes


def split_seed(seed: bytes) -> dict:
    """
    Split SHA512 seed into:
        x0, y0, z0  (state variables)
        r1, r2, r3  (multipliers)

    Layout (big-endian):

        0–7    → x0
        8–15   → y0
        16–23  → z0
        24–31  → r1
        32–39  → r2
        40–47  → r3

    Remaining 16 bytes reserved.
    """

    if len(seed) != 64:
        raise ValueError("Seed must be 64 bytes (SHA512 output)")

    def bytes_to_uint64(b: bytes) -> int:
        return int.from_bytes(b, byteorder="big", signed=False) & MASK

    x0 = bytes_to_uint64(seed[0:8])
    y0 = bytes_to_uint64(seed[8:16])
    z0 = bytes_to_uint64(seed[16:24])

    r1 = bytes_to_uint64(seed[24:32])
    r2 = bytes_to_uint64(seed[32:40])
    r3 = bytes_to_uint64(seed[40:48])

    # Prevent zero-state collapse
    if x0 == 0:
        x0 = 1
    if y0 == 0:
        y0 = 1
    if z0 == 0:
        z0 = 1

    # Ensure multipliers are odd (important for mod 2^64 mixing)
    r1 = (r1 | 1) & MASK
    r2 = (r2 | 1) & MASK
    r3 = (r3 | 1) & MASK

    return {
        "x0": x0,
        "y0": y0,
        "z0": z0,
        "r1": r1,
        "r2": r2,
        "r3": r3
    }