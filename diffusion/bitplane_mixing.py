import numpy as np

def rotl_n(value, r, width):
    r = r % width
    return ((value << r) | (value >> (width - r))) & ((1 << width) - 1)


def rotr_n(value, r, width):
    r = r % width
    return ((value >> r) | (value << (width - r))) & ((1 << width) - 1)

def encrypt_bitplane_mix(block, rotation_vals, bitplane_masks, config):

    msb_mask = config["lightweight_3d_uint64"]["msb_mask"]
    lsb_mask = config["lightweight_3d_uint64"]["lsb_mask"]
    rotation_max = config["lightweight_3d_uint64"]["bitplane_rotation_max"]

    B = block.shape[0]
    mixed = block.copy()

    idx = 0

    for i in range(B):
        for j in range(B):

            pixel = int(mixed[i, j])

            msb = (pixel & msb_mask) >> 4
            lsb = pixel & lsb_mask

            r = (rotation_vals[idx] % rotation_max) + 1
            mask = bitplane_masks[idx] & lsb_mask

            # Rotate MSB (4-bit width assumed)
            msb = rotl_n(msb, r, 4)

            # XOR LSB
            lsb = lsb ^ mask

            mixed[i, j] = ((msb << 4) | lsb) & 0xFF

            idx += 1

    return mixed

def decrypt_bitplane_mix(block, rotation_vals, bitplane_masks, config):

    msb_mask = config["lightweight_3d_uint64"]["msb_mask"]
    lsb_mask = config["lightweight_3d_uint64"]["lsb_mask"]
    rotation_max = config["lightweight_3d_uint64"]["bitplane_rotation_max"]

    B = block.shape[0]
    unmixed = block.copy()

    idx = 0

    for i in range(B):
        for j in range(B):

            pixel = int(unmixed[i, j])

            msb = (pixel & msb_mask) >> 4
            lsb = pixel & lsb_mask

            r = (rotation_vals[idx] % rotation_max) + 1
            mask = bitplane_masks[idx] & lsb_mask

            # Reverse LSB XOR
            lsb = lsb ^ mask

            # Reverse MSB rotation
            msb = rotr_n(msb, r, 4)

            unmixed[i, j] = ((msb << 4) | lsb) & 0xFF

            idx += 1

    return unmixed