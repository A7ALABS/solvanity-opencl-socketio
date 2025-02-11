import base58

priv_key_array = [27, 160, 93, 155, 1, 62, 12, 0, 194, 41, 119, 244, 189, 179, 195, 250, 65, 102, 247, 65, 165, 182, 214, 85, 53, 0, 199, 231, 204, 0, 134, 151, 2, 116, 143, 200, 72, 200, 205, 13, 3, 28, 81, 152, 142, 164, 71, 70, 115, 190, 144, 43, 222, 141, 248, 232, 7, 190, 102, 103, 25, 151, 164, 73]
hex_string = ''.join(format(x, '02x') for x in priv_key_array)
privatekey_base58 = base58.b58encode(bytes.fromhex(hex_string))
print(privatekey_base58.decode())
