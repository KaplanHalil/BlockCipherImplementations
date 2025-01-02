import utils

# PRESENT S-Box
SBOX = [
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
]

# PRESENT P-layer permutation
PBOX = [
    0, 16, 32, 48, 1, 17, 33, 49,
    2, 18, 34, 50, 3, 19, 35, 51,
    4, 20, 36, 52, 5, 21, 37, 53,
    6, 22, 38, 54, 7, 23, 39, 55,
    8, 24, 40, 56, 9, 25, 41, 57,
    10, 26, 42, 58, 11, 27, 43, 59,
    12, 28, 44, 60, 13, 29, 45, 61,
    14, 30, 46, 62, 15, 31, 47, 63
]

# Key schedule for 80-bit key
def key_schedule(key):
    round_keys = []
    current_key = key[:]
    for round in range(32):
        round_keys.append(current_key[:8])  # Extract the first 64 bits
        # Rotate key: left shift by 61 bits
        full_key = int.from_bytes(current_key, 'big')
        rotated_key = ((full_key << 61) | (full_key >> 19)) & ((1 << 80) - 1)
        current_key = list(rotated_key.to_bytes(10, 'big'))
        # Apply S-box to the leftmost nibble
        current_key[0] = (SBOX[current_key[0] >> 4] << 4) | (current_key[0] & 0xF)
        # XOR the round counter into the key
        current_key[9] ^= round + 1
    return round_keys

# Substitute nibbles using the S-box
def sub_nibbles(state):
    return [(SBOX[(byte >> 4) & 0xF] << 4) | SBOX[byte & 0xF] for byte in state]

# Permutation layer using the P-box
def permute(state):
    bitstring = "".join(f"{byte:08b}" for byte in state)
    print(bitstring)
    permuted_bits = ['0'] * 64
    for i in range(64):
        permuted_bits[PBOX[i]] = bitstring[i]
    permuted_bytes = [
        int("".join(permuted_bits[i:i + 8]), 2) for i in range(0, 64, 8)
    ]
    return permuted_bytes


if __name__ == "__main__":
    # Test vector from the PRESENT specification
    p = [0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x0f]
    k = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    print(key_schedule(k))