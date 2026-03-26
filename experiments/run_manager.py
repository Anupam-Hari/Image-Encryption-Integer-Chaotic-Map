# IMAGE_ENCRYPTION/experiments/run_manager.py

import os
import json
from datetime import datetime


def create_run(algorithm_name: str, config: dict):

    # Generate timestamp-based run ID
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")

    base_path = os.path.join("experiments", algorithm_name, run_id)

    encrypted_path = os.path.join(base_path, "encrypted")
    decrypted_path = os.path.join(base_path, "decrypted")

    os.makedirs(encrypted_path, exist_ok=True)
    os.makedirs(decrypted_path, exist_ok=True)

    # Save metadata
    metadata_path = os.path.join(base_path, "metadata.json")

    with open(metadata_path, "w") as f:
        json.dump(config, f, indent=4)

    return {
        "run_id": run_id,
        "base_path": base_path,
        "encrypted_path": encrypted_path,
        "decrypted_path": decrypted_path,
        "metadata_path": metadata_path
    }