""" The original content was encrypted then encoded with base64
    
"""
from Crypto.Cipher import AES
import base64

key = b"YELLOW SUBMARINE"
r = base64.b64decode(open("q7.data").read())


def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def decrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)


if __name__ == "__main__":
    print(decrypt_aes(r, key))
