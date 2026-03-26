from chaotic_maps.coupled_3d_uint64 import iterate

MASK_8 = 0xFF

# Keystream Generation (for XOR diffusion)
def generate_keystream(state: dict, n_bytes: int):

    keystream = bytearray()

    while len(keystream) < n_bytes:
        state = iterate(state)

        x = state["x"]
        y = state["y"]
        z = state["z"]

        # Extract 1 byte from each variable (LSB)
        keystream.append(x & MASK_8)
        if len(keystream) < n_bytes:
            keystream.append(y & MASK_8)
        if len(keystream) < n_bytes:
            keystream.append(z & MASK_8)

    return bytes(keystream[:n_bytes]), state


# Control Stream Generation
def generate_control_stream(state: dict, n_elements: int, config: dict):

    rotation_vals = []
    collision_bits = []
    bitplane_masks = []

    rotation_width = config["lightweight_3d_uint64"]["rotation_bit_width"]
    bitplane_mask_bits = config["lightweight_3d_uint64"]["bitplane_mask_bits"]

    for _ in range(n_elements):
        state = iterate(state)

        x = state["x"]
        y = state["y"]
        z = state["z"]

        # Rotation amount (bounded)
        rotation_vals.append(x % rotation_width)

        # Single-bit collision decision
        collision_bits.append(y & 1)

        # Bitplane mask (lower bits only)
        mask = z & ((1 << bitplane_mask_bits) - 1)
        bitplane_masks.append(mask)

    control = {
        "rotation_vals": rotation_vals,
        "collision_bits": collision_bits,
        "bitplane_masks": bitplane_masks
    }

    return control, state