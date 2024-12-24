import utils
import AES_128 as cipher
#import AES_256 as cipher

block_size = 16  # bytes

# XOR operation
def xor_blocks(block1, block2):
    return [b1 ^ b2 for b1, b2 in zip(block1, block2)]

# Construct counter block as per RFC 3686
def construct_counter_block(nonce, iv, block_counter):
    # Nonce (4 bytes) || IV (8 bytes) || Block Counter (4 bytes)
    nonce_iv = nonce + iv
    counter = list(block_counter.to_bytes(4, byteorder='big'))
    return nonce_iv + counter

# CTR mode encryption (RFC 3686 compliant)
def ctr_encrypt(plaintext, key, nonce, iv):
    ciphertext = []
    block_counter = 0

    # Process each block
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        if len(block) < block_size:
            # Padding if block is smaller than block size
            block += [0] * (block_size - len(block))
        # Construct the counter block
        counter_block = construct_counter_block(nonce, iv, block_counter)
        # Encrypt the counter block
        encrypted_counter = cipher.encrypt(list(counter_block), key)
        # XOR plaintext block with encrypted counter
        xor_result = xor_blocks(block, encrypted_counter)
        # Append to ciphertext
        ciphertext.extend(xor_result)
        # Increment block counter
        block_counter += 1

    return ciphertext

if __name__ == "__main__":
    key = utils.str_to_int_array("0xAE6852F8121067CC4BF7A5765577F39E")
    nonce = utils.str_to_int_array("0x00000030")  # 4 bytes
    iv = utils.str_to_int_array("0x0000000000000000")  # 8 bytes
    plaintext = utils.str_to_int_array("0x53696E676C6520626C6F636B206D7367")
    print("Plaintext:", plaintext)
    print("Key:", key)
    print("Nonce:", nonce)
    print("IV:", iv)

    ciphertext = ctr_encrypt(plaintext, key, nonce, iv)
    print("Ciphertext:", utils.int_to_hex(ciphertext))
