import utils
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

    key = utils.str_to_int_array("0x2b7e151628aed2a6abf7158809cf4f3c")
    iv  = utils.str_to_int_array("0x000102030405060708090A0B0C0D0E0F")
    plaintext = utils.str_to_int_array("0x6bc1bee22e409f96e93d7e117393172a")
    print("Plaintext:",plaintext)
    print("key:",key)
    print("iv:",iv)

    ciphertext = cbc_encrypt(plaintext, key, iv)
    print(utils.int_to_hex(ciphertext))

    