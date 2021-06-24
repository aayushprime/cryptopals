from Crypto.Cipher import AES
import base64

# fixed xor function
def fixed_xor(x, y):
    if len(x) != len(y):
        print("length not equal")
        return
    l = []
    for i, a in enumerate(x):
        l.append(a ^ y[i])
    return bytes(l)


def decrypt_block(data, k, IV, cipher):
    # split into blocks
    blocks = [data[i : i + k] for i in range(0, len(data), k)]
    result = b""
    # initially the previous block is IV
    previous = IV
    for block in blocks:
        result += fixed_xor(cipher.decrypt(block), previous)
        previous = block
    return result


def encrypt_block(data, k, IV, cipher):
    # split into blocks
    blocks = [data[i : i + k] for i in range(0, len(data), k)]
    result = b""
    previous = IV
    for block in blocks:
        cipher_text = cipher.encrypt(fixed_xor(block, previous))
        result += cipher_text
        previous = cipher_text
    return result


if __name__ == "__main__":
    # read the base64 encoded data into r
    r = base64.b64decode(open("q10.data").read())

    blocksize = 16
    # key for ecb mode
    key = b"YELLOW SUBMARINE"
    # setup cipher variable
    cipher = AES.new(key, AES.MODE_ECB)

    res = decrypt_block(r, blocksize, b"\x00" * blocksize, cipher)
    reencrypted = encrypt_block(res, blocksize, b"\x00" * blocksize, cipher)

    assert reencrypted == r

    print(res)
