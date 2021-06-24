import random
from set2.q10 import fixed_xor
from set2.q13 import encrypt_profile
from Crypto.Cipher import AES
from set2.q9 import pad_pkcs7
from set2.q11 import detect
import base64

encrypted_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
key = b""
randomBytes = b""


def gen_aes_key():
    return random.randbytes(16)


def aes_encrypt(data):
    global key
    global randomBytes
    data = randomBytes + data
    data += base64.b64decode(encrypted_string)
    data = pad_pkcs7(data, 16)
    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(data)


def discover_block_size(encryptor):
    input = b""
    # on blank input the encryptor returns original_length output
    original_length = len(encryptor(input))
    i = 1
    while True:
        input += b"A"
        new_length = len(encryptor(input))
        # if there is a jump then the jump difference must be block size
        if new_length != original_length:
            return new_length - original_length
        i += 1


def find_bytes(encryptor, blocksize, known, padding):
    input = padding + b"A" * (blocksize - (len(known) % blocksize) - 1)
    one_byte_short_output = encryptor(input)
    dictionary = {}

    block_to_remember = (len(known) + len(padding)) // blocksize
    address = block_to_remember * blocksize

    for i in range(256):
        output = encryptor(input + known + bytes([i]))
        dictionary[output[address : address + blocksize]] = i
    if one_byte_short_output[address : address + blocksize] in dictionary:
        return dictionary[one_byte_short_output[address : address + blocksize]]
    else:
        return None


def find_pre_padding(encryptor):
    # return second increase in block size
    input = b""
    original = len(encryptor(input)) // 16
    while True:
        if len(encryptor(input)) // 16 == original + 2:
            return input[:-1]
        input += b"A"


def find_block_address(encryptor, padding):
    input = b"A" * padding
    input2 = b"B" * padding
    output = encryptor(input)
    output2 = encryptor(input2)
    xor_res = fixed_xor(output, output2)
    for i, e in enumerate(xor_res):
        if e != 0:
            return i // 16


if __name__ == "__main__":
    key = gen_aes_key()
    randomBytes = random.randbytes(random.randint(5, 10))
    blocksize = discover_block_size(aes_encrypt)
    # print(blocksize)
    assert detect(aes_encrypt) == "ECB"
    padding = find_pre_padding(aes_encrypt)
    # print(find_block_address(aes_encrypt, len(padding)))
    result = b""
    while True:
        new_byte = find_bytes(aes_encrypt, blocksize, result, padding)
        if new_byte == None:
            break
        result += bytes([new_byte])
    print(result)
