import random
from Crypto.Cipher import AES
from set2.q9 import pad_pkcs7
from set2.q10 import encrypt_block


def gen_aes_key():
    return random.randbytes(16)


def aes_encrypt_random(data):
    data = (
        random.randbytes(random.randint(5, 10))
        + data
        + random.randbytes(random.randint(5, 10))
    )
    data = pad_pkcs7(data, 16)
    cipher = AES.new(gen_aes_key(), AES.MODE_ECB)

    if random.randint(0, 1) == 0:
        # do ecb
        print("ECB")
        return cipher.encrypt(data)
    else:
        # do cbc
        print("CBC")
        return encrypt_block(data, 16, random.randbytes(16), cipher)


def detect(encryptor):
    # enter random number(22) of long enough bytes(50) into the encryptor
    output = encryptor(bytes([22] * 50))
    # if output slices towards the middle (to skip randomness in beginning and end)
    # are same then the mode must be ECB since same bytes should evaluate to same output
    # if they are not same then it is probably CBC
    if output[16 : 16 + 16] == output[32 : 32 + 16]:
        return "ECB"
    else:
        return "CBC"


if __name__ == "__main__":
    print(detect(aes_encrypt_random))
    print(aes_encrypt_random(b"hello who this"))
