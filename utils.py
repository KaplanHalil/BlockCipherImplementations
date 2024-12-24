def str_to_int_array(hex_str):
    # Remove the '0x' prefix if it exists
    hex_str = hex_str[2:] if hex_str.startswith("0x") else hex_str
    
    # Ensure the length of the string is even for grouping into bytes
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str  # Add leading zero if necessary
    
    # Convert each pair of characters into a byte (integer)
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]


def int_array_to_hex_array(int_array):
    # Convert each integer in the array to a hexadecimal string
    return [hex(x) for x in int_array]

if __name__ == "__main__":

    #key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0xcf, 0x9b, 0x6d, 0x8f, 0x6c, 0x7e]
    print(str_to_int_array("0x0001c2"))