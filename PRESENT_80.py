import sys
import os
# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import utils

block_size = 8  # bytes (64 bits)
key_size_80 = 10  # bytes (80 bits)
key_size_128 = 16  # bytes (128 bits)
num_rounds = 31

# PRESENT S-Box
SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# PRESENT P-Layer permutation
PBOX = [
    0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
    4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
    8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
    12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63
]

# Key update function for 80-bit key
def key_update_80(key, round_counter):
    # Rotate key 61 bits to the left
    key = ((key << 61) | (key >> 19)) & 0xFFFFFFFFFFFFFFFFFFFF  # 80-bit mask
    
    # Apply S-box to the most significant 4 bits
    sbox_out = SBOX[key >> 76]
    key = (key & 0x0FFFFFFFFFFFFFFFFFFFF) | (sbox_out << 76)
    
    # XOR round counter into bits 15-19
    key ^= (round_counter << 15)
    
    return key

# Key update function for 128-bit key
def key_update_128(key, round_counter):
    # Rotate key 61 bits to the left
    key = ((key << 61) | (key >> 67)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  # 128-bit mask
    
    # Apply S-box to the most significant 4 bits
    sbox_out = SBOX[key >> 124]
    key = (key & 0x0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) | (sbox_out << 124)
    
    # XOR round counter into bits 62-66
    key ^= (round_counter << 62)
    
    return key

# Substitution layer
def sbox_layer(state):
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        new_state |= SBOX[nibble] << (i * 4)
    return new_state

# Permutation layer
def pbox_layer(state):
    new_state = 0
    for i in range(64):
        bit = (state >> i) & 0x1
        new_state |= bit << PBOX[i]
    return new_state

# PRESENT encryption
def encrypt(block, key, key_size=80):
    if key_size == 80:
        key = int.from_bytes(key, byteorder='big')
        for round in range(num_rounds):
            # Add round key
            round_key = (key >> 16) & 0xFFFF  # Extract 64-bit round key
            block ^= round_key
            
            # S-box layer
            block = sbox_layer(block)
            
            # P-box layer
            block = pbox_layer(block)
            
            # Update key
            key = key_update_80(key, round + 1)
        
        # Final round key addition
        round_key = (key >> 16) & 0xFFFF
        block ^= round_key
    
    elif key_size == 128:
        key = int.from_bytes(key, byteorder='big')
        for round in range(num_rounds):
            # Add round key
            round_key = (key >> 64) & 0xFFFFFFFFFFFFFFFF  # Extract 64-bit round key
            block ^= round_key
            
            # S-box layer
            block = sbox_layer(block)
            
            # P-box layer
            block = pbox_layer(block)
            
            # Update key
            key = key_update_128(key, round + 1)
        
        # Final round key addition
        round_key = (key >> 64) & 0xFFFFFFFFFFFFFFFF
        block ^= round_key
    
    return block

if __name__ == "__main__":
    # Test vectors for PRESENT-80
    plaintext = utils.str_to_int_array("0x0000000000000000")
    key_80 = utils.str_to_int_array("0x00000000000000000000")
    
    plaintext_int = int.from_bytes(plaintext, byteorder='big')
    key_80_int = int.from_bytes(key_80, byteorder='big')
    
    ciphertext = encrypt(plaintext_int, key_80_int, key_size=80)
    print("Ciphertext (PRESENT-80):", hex(ciphertext))
    
    # Test vectors for PRESENT-128
    key_128 = utils.str_to_int_array("0x00000000000000000000000000000000")
    
    key_128_int = int.from_bytes(key_128, byteorder='big')
    
    ciphertext = encrypt(plaintext_int, key_128_int, key_size=128)
    print("Ciphertext (PRESENT-128):", hex(ciphertext))