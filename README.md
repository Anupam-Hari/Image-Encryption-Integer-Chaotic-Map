# Integer Chaotic Map Image Encryption

Core implementation of chaotic image encryption using integer chaotic maps.

## Structure
- chaotic_maps/ → integer based map logic
- permutation/ → block permutation
- diffusion/ → bit plane mixing and stateless diffusion for blocks
- encryption/ → main encryption logic and block encryption
- keygen/ → key generation and seed derivation
- config/ → parameters
- runners/ → execution scripts

## Setup
```bash
pip install -r requirements.txt