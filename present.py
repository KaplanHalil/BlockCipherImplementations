# PRESENT block cipher implementation in Python

# S-box for PRESENT
SBOX = [
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
]

# Inverse S-box for decryption
INV_SBOX = [
    0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD,
    0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA
]

# Permutation table
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

# Number of rounds
ROUNDS = 31

# Rotate left
def rotate_left(value, shift, size=80):
    return ((value << shift) | (value >> (size - shift))) & ((1 << size) - 1)

# Substitute using S-box
def substitute(value, sbox):
    result = 0
    for i in range(16):
        nibble = (value >> (4 * i)) & 0xF
        result |= sbox[nibble] << (4 * i)
    return result

# Permute bits using P-box
def permute(value):
    result = 0
    for i, p in enumerate(PBOX):
        if value & (1 << i):
            result |= 1 << p
    return result

# Key schedule
def generate_round_keys(key):
    round_keys = []
    for round_number in range(1, ROUNDS + 2):
        round_keys.append(key >> 16)
        key = rotate_left(key, 61, 80)
        key = (key & 0xFFFFFFFFFFF0) | SBOX[(key >> 76) & 0xF]
        key ^= round_number << 15
    return round_keys

# Encrypt block
def encrypt_block(block, round_keys):
    state = block
    for round_number in range(ROUNDS):
        state ^= round_keys[round_number]
        state = substitute(state, SBOX)
        state = permute(state)
    state ^= round_keys[ROUNDS]  # Final round key addition
    return state

# Decrypt block
def decrypt_block(block, round_keys):
    state = block
    state ^= round_keys[ROUNDS]
    for round_number in range(ROUNDS - 1, -1, -1):
        state = permute(state)  # Reverse permutation
        state = substitute(state, INV_SBOX)
        state ^= round_keys[round_number]
    return state

# Main function to encrypt plaintext
def present_encrypt(plaintext, key):
    round_keys = generate_round_keys(key)
    return encrypt_block(plaintext, round_keys)

# Main function to decrypt ciphertext
def present_decrypt(ciphertext, key):
    round_keys = generate_round_keys(key)
    return decrypt_block(ciphertext, round_keys)

# Example usage
if __name__ == "__main__":
    # Example 64-bit block and 80-bit key
    plaintext = 0x0123456789ABCDEF
    key = 0x0123456789ABCDEF0123

    print(f"Plaintext: {plaintext:016X}")
    ciphertext = present_encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext:016X}")
    decrypted = present_decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted:016X}")
