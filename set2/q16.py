from set2.q10 import encrypt_block, decrypt_block
from set2.q9 import pad_pkcs7
from Crypto.Cipher import AES
import random

IV = b""


def encrypt(data):
    global IV
    global key
    data = data.replace(b";", b'";"').replace(b"=", b'"="')
    data = b"comment1=cooking%20MCs;userdata=" + data
    data += b";comment2=%20like%20a%20pound%20of%20bacon"
    cipher = AES.new(key, AES.MODE_ECB)
    return encrypt_block(pad_pkcs7(data, 16), 16, IV, cipher)


def decrypt(data):
    global IV
    global key
    cipher = AES.new(key, AES.MODE_ECB)
    return decrypt_block(data, 16, IV, cipher)


if __name__ == "__main__":
    IV = random.randbytes(16)
    key = random.randbytes(16)
    # enter extra block because the bit flipped block is scrambled
    encrypted = encrypt(b"AAAAAAAAAAAAAAAA:admin<true:AAAA")
    print(encrypted)

    l = list(encrypted)
    # flip
    l[32] ^= 1
    l[38] ^= 1
    l[43] ^= 1
    decrypted = decrypt(bytes(l))
    print(decrypted)
    if b";admin=true;" in decrypted:
        print("passed")
    else:
        print("failed")
