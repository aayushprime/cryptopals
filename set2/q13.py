from Crypto.Cipher import AES
from set2.q9 import pad_pkcs7
from set2.q11 import gen_aes_key


def kv_parser(string: bytes):
    s = string.split(b"&")
    dictionary = {}
    for i in s:
        j = i.split(b"=")
        dictionary[j[0]] = j[1]
    return dictionary


def prune(string: bytes):
    return string.replace(b"&", b"").replace(b"=", b"")


def profile_for(email: bytes, id: bytes, role: bytes):
    data = {b"email": prune(email), b"uid": prune(id), b"role": prune(role)}
    return data


def encode(data):
    s = []
    for i in data:
        s.append(i + b"=" + data[i])
    return b"&".join(s)


def encrypt_aes(data: bytes, key: bytes) -> bytes:
    data = pad_pkcs7(data, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def decrypt_aes(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)


key = gen_aes_key()


def encrypt_profile(email, id, role):
    return encrypt_aes(encode(profile_for(email, id, role)), key)


def unpad_pkcs7(data: bytes):
    return data[: -data[-1]]


def decrypt_profile(data: bytes):
    return kv_parser(unpad_pkcs7(decrypt_aes(data, key)))


if __name__ == "__main__":
    # assume we can only control the email parameter
    # "email=" is 6 characters so to have "admin" on new block padding required is 10
    # we want admin to be a whole block so padding is 16 - len("admin") = 11
    email = b"XXXX@XXXXXadmin" + b"\x0b" * 11
    payload = encrypt_profile(email, b"33", b"testuser")

    # we control padding so that the block ends with "role=" so that we can inject admin block
    # "email=&uid=33&role=" is 19 bytes so to make 32 bytes we enter 32-19 bytes long email
    encrypted = encrypt_profile(b"XXXX@XXXXXXXX", b"33", b"testuser")
    # put the admin block in right place
    x = encrypted[:-16] + payload[16:32]
    decrypted = decrypt_profile(x)

    if b"role" in decrypted and decrypted[b"role"] == b"admin":
        print("passed")
    else:
        print("failed")
    print(decrypted)
