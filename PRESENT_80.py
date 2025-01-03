# Not working correctly

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

# Substitute nibbles using the S-box
def sub_nibbles(state):
    return [(SBOX[(byte >> 4) & 0xF] << 4) | SBOX[byte & 0xF] for byte in state]

# Permutation layer using the P-box
def permute(state):
    bitstring = "".join(f"{byte:08b}" for byte in state)
    permuted_bits = ['0'] * 64
    for i in range(64):
        permuted_bits[PBOX[i]] = bitstring[i]
    permuted_bytes = [
        int("".join(permuted_bits[i:i + 8]), 2) for i in range(0, 64, 8)
    ]
    return permuted_bytes

# Add round key
def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

# Key schedule for 80-bit key
def key_schedule(key):
    round_keys = []
    current_key = key[:]
    for round in range(32):
        round_keys.append(current_key[:8])  # Extract the first 64 bits
        print(f"Round key {round + 1}: {''.join(f'{byte:02x}' for byte in current_key[:8])}")
        
        # Rotate key: left shift by 61 bits
        full_key = int.from_bytes(current_key, 'big')
        rotated_key = ((full_key << 61) | (full_key >> 19)) & ((1 << 80) - 1)
        current_key = list(rotated_key.to_bytes(10, 'big'))
        
        # Apply S-box to the leftmost nibble
        current_key[0] = (SBOX[current_key[0] >> 4] << 4) | (current_key[0] & 0xF)
        
        # XOR the round counter into bits 15-19
        round_counter = round + 1
        current_key[1] ^= (round_counter >> 2) & 0xF
        current_key[2] ^= ((round_counter & 0x3) << 6)
    return round_keys

# PRESENT encryption
def encrypt(block, key):
    state = block[:]
    round_keys = key_schedule(key)
    for i, round_key in enumerate(round_keys[:-1]):
        state = add_round_key(state, round_key)
        state = sub_nibbles(state)
        state = permute(state)
        print(f"Round Output {i + 1}: {''.join(f'{byte:02x}' for byte in state)}")
    state = add_round_key(state, round_keys[-1])
    return state

if __name__ == "__main__":
    # Test vector from the PRESENT specification
    plaintext = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    key = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", "".join(f"{byte:02X}" for byte in ciphertext))  # Should be 5579C1387B228445
