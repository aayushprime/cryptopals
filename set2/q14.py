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
blocksize = 16


def gen_aes_key():
    return random.randbytes(16)


def aes_encrypt(data):
    global blocksize
    global key
    global randomBytes
    data = randomBytes + data
    data += base64.b64decode(encrypted_string)
    data = pad_pkcs7(data, blocksize)
    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(data)


# function used while debugging
def aes_decrypt(data):
    global key
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)


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


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def find_blockindex(l1, l2):
    global blocksize
    for i, e in enumerate(byte_xor(l1, l2)):
        if e != 0:
            return i // blocksize


def find_bytes(encryptor, blocksize, known, padding):
    # we just add padding to answer of question number 12
    input = padding + b"A" * (blocksize - (len(known) % blocksize) - 1)
    one_byte_short_output = encryptor(input)

    # the block to remember is the one having 1st non zero while xoring one byte short input and perfect block matching input
    blockindex = find_blockindex(one_byte_short_output, encryptor(input + b"0"))
    # the known bytes shift the index of block to remember
    block_to_remember = blockindex + len(known) // blocksize
    address = block_to_remember * blocksize

    dictionary = {}
    for i in range(256):
        output = encryptor(input + known + bytes([i]))
        dictionary[output[address : address + blocksize]] = i
    if one_byte_short_output[address : address + blocksize] in dictionary:
        return dictionary[one_byte_short_output[address : address + blocksize]]
    else:
        return None


def find_pre_padding(encryptor, blocksize):
    input = b""

    """
    keep on adding to input until we find that 2 consecutive blocks of output are identical
    the first time we arrive at such condition should be when (our padding + random bytes at beginning) % blocksize = 0
    however the random bytes and our input may coincide and thus 2 consecutive blocks are identical 
    (very unlikely that random keys are longer than a block comprising of all same letters and the same letter as our input, but still)
    so we test with another input of same length and see if the blocks match
    """
    while True:
        output = encryptor(input)
        blocks = [output[i : i + blocksize] for i in range(0, len(output), blocksize)]
        for i in range(len(blocks) - 1):
            if blocks[i] == blocks[i + 1]:
                # if blocks match we have found the required padding unless
                # the match is just a coincidence (the random bytes and our input matched)
                alternative = b"B" * len(input)
                new_blocks = [
                    encryptor(alternative)[k : k + blocksize]
                    for k in range(0, len(output), blocksize)
                ]
                if new_blocks[i] == new_blocks[i + 1]:
                    return input

        input += b"A"


if __name__ == "__main__":
    key = gen_aes_key()
    randomBytes = random.randbytes(random.randint(5, 10))
    blocksize = discover_block_size(aes_encrypt)

    assert detect(aes_encrypt) == "ECB"
    padding = find_pre_padding(aes_encrypt, blocksize)

    result = b""
    while True:
        new_byte = find_bytes(aes_encrypt, blocksize, result, padding)
        if new_byte == None:
            break
        result += bytes([new_byte])
    print(result)
