MASK = (1 << 64) - 1


def chaotic_map_step(x, y, z, r1, r2, r3):

    x = int(x) & MASK
    y = int(y) & MASK
    z = int(z) & MASK

    r1 = int(r1) | 1  # force odd
    r2 = int(r2) | 1
    r3 = int(r3) | 1

    # Linear coupling
    x_new = (x * r1 + y) & MASK
    y_new = (y * r2 + z) & MASK
    z_new = (z * r3 + x_new) & MASK

    # Bit diffusion
    x_new = (x_new ^ (x_new >> 17)) & MASK
    y_new = (y_new ^ (y_new >> 23)) & MASK
    z_new = (z_new ^ (z_new >> 29)) & MASK

    return x_new, y_new, z_new

def initialize_state(seed_params: dict, config: dict):

    x = seed_params["x0"] & MASK
    y = seed_params["y0"] & MASK
    z = seed_params["z0"] & MASK

    r1 = seed_params["r1"] & MASK
    r2 = seed_params["r2"] & MASK
    r3 = seed_params["r3"] & MASK

    discard = config["lightweight_3d_uint64"]["discard_transient"]

    # Transient discard
    for _ in range(discard):
        x, y, z = chaotic_map_step(x, y, z, r1, r2, r3)

    return {
        "x": x,
        "y": y,
        "z": z,
        "r1": r1,
        "r2": r2,
        "r3": r3
    }


def iterate(state: dict):

    x, y, z = chaotic_map_step(
        state["x"],
        state["y"],
        state["z"],
        state["r1"],
        state["r2"],
        state["r3"]
    )

    state["x"] = x
    state["y"] = y
    state["z"] = z

    return state


def iterate_n(state: dict, n: int):

    for _ in range(n):
        state = iterate(state)

    return state