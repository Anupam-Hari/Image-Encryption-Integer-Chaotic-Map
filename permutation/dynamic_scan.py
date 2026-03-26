
def select_scan_mode(scan_selector_value, config):

    modes = config["lightweight_3d_uint64"]["scan_modes"]
    index = scan_selector_value % len(modes)

    return modes[index]

def scan_indices(block_shape, mode):

    B = block_shape[0]
    indices = []

    if mode == "row":
        for i in range(B):
            for j in range(B):
                indices.append((i, j))

    elif mode == "column":
        for j in range(B):
            for i in range(B):
                indices.append((i, j))

    elif mode == "reverse":
        for i in reversed(range(B)):
            for j in reversed(range(B)):
                indices.append((i, j))

    elif mode == "zigzag":
        for s in range(2 * B - 1):
            if s % 2 == 0:
                for i in range(B):
                    j = s - i
                    if 0 <= j < B:
                        indices.append((i, j))
            else:
                for i in reversed(range(B)):
                    j = s - i
                    if 0 <= j < B:
                        indices.append((i, j))

    else:
        raise ValueError(f"Unsupported scan mode: {mode}")

    return indices