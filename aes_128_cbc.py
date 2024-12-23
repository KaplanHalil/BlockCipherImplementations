import AES_128 as cipher

block_size = 16  #bytes

# XOR operation
def xor_blocks(block1, block2):
    return [b1 ^ b2 for b1, b2 in zip(block1, block2)]

# CBC mode encryption
def cbc_encrypt(plaintext, key, iv):
    ciphertext = []
    previous_block = iv

    # Process each block
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        if len(block) < block_size:
            # Padding if block is smaller than block size
            block += [0] * (block_size - len(block))
        # XOR with previous block or IV
        xor_result = xor_blocks(block, previous_block)
        # Encrypt the XOR result
        encrypted_block = cipher.encrypt(xor_result, key)
        # Append to ciphertext
        ciphertext.extend(encrypted_block)
        # Update the previous block for the next iteration
        previous_block = encrypted_block

    return ciphertext

if __name__ == "__main__":
    #key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0xcf, 0x9b, 0x6d, 0x8f, 0x6c, 0x7e]
    key = [0x00] * 16
    iv = [0x00] * 16  # Example IV with 16 zero bytes
    #plaintext = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34,]
    plaintext = [0x00]* 16
    ciphertext = cbc_encrypt(plaintext, key, iv)
    print("Ciphertext:", ciphertext)