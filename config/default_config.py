# IMAGE_ENCRYPTION/config/default_config.py

CONFIG = {

    # Algorithm selection
    "algorithm": "lightweight_3d_uint64",

    # LIGHTWEIGHT 3D UINT64 CHAOTIC ENCRYPTION
    "lightweight_3d_uint64": {

        # Key / IV settings (runtime use)
        "key_size_bits": 128,
        "iv_size_bits": 128,
        "hash_function": "sha512",


        # Chaotic map configuration
        "state_bits": 64,              # uint64 fixed-point
        "state_variables": 3,          # x, y, z
        "parameter_variables": 3,      # r1, r2, r3

        "discard_transient": 2000,     # initial iterations to discard

        "fixed_point_modulus": 2**64,  # implicit uint64 wrap


        # Block processing
        "block_size": 32,               # B x B block size
        "block_parameter_feedback": True,


        # Scan mode control
        "scan_modes": [
            "row",
            "column",
            "zigzag",
            "reverse"
        ],


        # Diffusion control
        "rotation_bit_width": 8,       # pixel assumed uint8
        "enable_cipher_feedback": True,


        # Bit-plane adaptive mixing
        "msb_mask": 0xF0,
        "lsb_mask": 0x0F,

        "bitplane_rotation_max": 4,    # MSB rotation range
        "bitplane_mask_bits": 4,       # mask width for LSB


        # Control stream sizing
        "separate_control_stream": True,


        # Image format control
        "pixel_dtype": "uint8",
        "grayscale_only": True
    },

    # Batch processing settings
    "batch": {
        "enabled": True,
        "num_images": 10,
        "shuffle": True,
        "compute_std": True
    },

    # Dataset settings
    "dataset": {
        "input_folder": "test_images",
        "num_images": 10,
        "grayscale": True
    },

    # Experiment control
    "experiment": {
        "save_decrypted": True,
        "compute_differential": True
    }
}